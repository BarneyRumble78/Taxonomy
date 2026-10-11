"""Model backends for v3 (Survey, Consult, Connect, Frame).

Choose with TAXONOMY_LLM:
  anthropic  Claude via the Messages API (needs ANTHROPIC_API_KEY; model TAXONOMY_MODEL,
             default claude-sonnet-5-5)
  ollama     a local model (TAXONOMY_MODEL, default gemma3:12b; host OLLAMA_HOST)
  manual     no model: writes each prompt to runs/prompts/ and reads the answer you paste
             back from a .answer.json file. Useful inside Claude chat or for auditing.
Every backend returns parsed JSON. No other dependencies.
"""
import json, os, re, time, urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]


class LLMError(Exception):
    pass


def parse_json(text):
    text = text.strip()
    m = re.search(r"```(?:json)?\s*(.*?)```", text, re.S)
    if m:
        text = m.group(1)
    for opener, closer in (("{", "}"), ("[", "]")):
        i, j = text.find(opener), text.rfind(closer)
        if i != -1 and j > i:
            try:
                return json.loads(text[i:j + 1])
            except json.JSONDecodeError:
                continue
    raise LLMError("model reply was not JSON: " + text[:200])


def _post(url, body, headers, timeout=180):
    req = urllib.request.Request(url, data=json.dumps(body).encode(), headers=headers, method="POST")
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return json.loads(r.read())


class Anthropic:
    def __init__(self, model=None):
        self.key = os.environ.get("ANTHROPIC_API_KEY")
        if not self.key:
            raise LLMError("ANTHROPIC_API_KEY is not set")
        self.model = model or os.environ.get("TAXONOMY_MODEL", "claude-sonnet-5-5")

    def __call__(self, prompt, max_tokens=4000):
        for attempt in range(3):
            try:
                data = _post("https://api.anthropic.com/v1/messages",
                             {"model": self.model, "max_tokens": max_tokens,
                              "messages": [{"role": "user", "content": prompt}]},
                             {"x-api-key": self.key, "anthropic-version": "2023-06-01", "content-type": "application/json"})
                text = "".join(b.get("text", "") for b in data.get("content", []) if b.get("type") == "text")
                return parse_json(text)
            except (urllib.error.HTTPError, urllib.error.URLError) as e:
                if attempt == 2:
                    raise LLMError(str(e))
                time.sleep(2 ** attempt)


class Ollama:
    def __init__(self, model=None):
        self.model = model or os.environ.get("TAXONOMY_MODEL", "gemma3:12b")
        self.host = os.environ.get("OLLAMA_HOST", "http://127.0.0.1:11434")

    def __call__(self, prompt, max_tokens=4000):
        data = _post(f"{self.host}/api/generate", {"model": self.model, "prompt": prompt, "stream": False,
                                                    "format": "json", "options": {"num_predict": max_tokens}}, {"content-type": "application/json"}, timeout=600)
        return parse_json(data.get("response", ""))


class Manual:
    """Writes prompts to disk; reads a pasted answer. Raises until the answer exists."""
    def __init__(self, folder=None):
        self.folder = Path(folder or ROOT / "runs" / "prompts")
        self.folder.mkdir(parents=True, exist_ok=True)

    def __call__(self, prompt, max_tokens=4000):
        import hashlib
        h = hashlib.sha1(prompt.encode()).hexdigest()[:12]
        p, a = self.folder / f"{h}.prompt.txt", self.folder / f"{h}.answer.json"
        p.write_text(prompt, encoding="utf-8")
        if not a.exists():
            raise LLMError(f"manual mode: paste the model's JSON answer into {a} and run again")
        return parse_json(a.read_text(encoding="utf-8"))


def get_llm(name=None):
    name = name or os.environ.get("TAXONOMY_LLM", "anthropic")
    return {"anthropic": Anthropic, "ollama": Ollama, "manual": Manual}[name]()
