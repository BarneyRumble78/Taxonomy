"""Model backends for v3 (Survey, Consult, Connect, Frame).

Choose with TAXONOMY_LLM. The default is ollama, a local model. A key in the
environment does not by itself call a paid API.
  ollama     local model (TAXONOMY_MODEL, default gemma3:12b; host OLLAMA_HOST)
  manual     no model: writes each prompt to runs/prompts/ and reads the answer you paste
             back from a .answer.json file. Useful inside Claude chat or for auditing.
  anthropic  Claude via the Messages API. Refused unless TAXONOMY_ADJUDICATE_PAID is on.
             Needs ANTHROPIC_API_KEY. Model TAXONOMY_MODEL, default claude-sonnet-5-5.
Every backend returns parsed JSON. No other dependencies.
"""
import json, os, re, socket, time, urllib.error, urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
_REASK = "Return valid JSON only"


class LLMError(Exception):
    pass


def ollama_timeout(default=120):
    """Seconds for one local generate call. TAXONOMY_OLLAMA_TIMEOUT overrides the default."""
    raw = os.environ.get("TAXONOMY_OLLAMA_TIMEOUT", "").strip()
    if not raw:
        return default
    try:
        n = int(raw)
    except ValueError:
        return default
    return n if n > 0 else default


def _salvage(text):
    """Close a cut-off JSON value. Returns an object, or None when it cannot."""
    out = []
    stack = []
    in_str = False
    esc = False
    for ch in text:
        out.append(ch)
        if in_str:
            if esc:
                esc = False
            elif ch == "\\":
                esc = True
            elif ch == '"':
                in_str = False
            continue
        if ch == '"':
            in_str = True
        elif ch == "{":
            stack.append("}")
        elif ch == "[":
            stack.append("]")
        elif ch in "}]" and stack and stack[-1] == ch:
            stack.pop()
    if not stack and not in_str:
        return None
    if in_str:
        if esc:
            out.append("\\")
        out.append('"')
    body = "".join(out).rstrip()
    body = re.sub(r":\s*$", ": null", body)
    body = re.sub(r",\s*$", "", body)
    body = re.sub(r',\s*"[^"]*"\s*$', "", body)
    body = re.sub(r'\{\s*"[^"]*"\s*$', "{", body)
    body = re.sub(r",\s*$", "", body)
    closed = body + "".join(reversed(stack))
    try:
        return json.loads(closed)
    except json.JSONDecodeError:
        return None


def parse_json(text):
    """First JSON value in the reply. A later object is ignored. A cut-off value is closed."""
    text = (text or "").strip()
    fenced = re.search(r"```(?:json)?\s*(.*?)```", text, re.S)
    if fenced:
        text = fenced.group(1).strip()
    decoder = json.JSONDecoder()
    for i, ch in enumerate(text):
        if ch not in "{[":
            continue
        try:
            obj, _end = decoder.raw_decode(text[i:])
        except json.JSONDecodeError:
            obj = _salvage(text[i:])
        if obj is not None:
            return obj
    raise LLMError("model reply was not JSON: " + text[:200])


def _post(url, body, headers, timeout=180):
    req = urllib.request.Request(url, data=json.dumps(body).encode(), headers=headers, method="POST")
    with urllib.request.urlopen(req, timeout=timeout) as r:
        raw = r.read()
    try:
        return json.loads(raw)
    except json.JSONDecodeError as exc:
        raise LLMError("model transport was not JSON") from exc


def _read_retry(do, attempts=3):
    """Up to three tries. Backoff on connection errors, timeouts and HTTP 5xx. A 4xx is not retried."""
    last = None
    for attempt in range(attempts):
        try:
            return do()
        except urllib.error.HTTPError as exc:
            last = exc
            if exc.code < 500 or attempt == attempts - 1:
                raise LLMError(str(exc)) from exc
            time.sleep(2 ** attempt)
        except (urllib.error.URLError, TimeoutError, socket.timeout, ConnectionError, OSError) as exc:
            last = exc
            if attempt == attempts - 1:
                raise LLMError(str(exc)) from exc
            time.sleep(2 ** attempt)
    raise LLMError(str(last))


def _complete_text(fetch_text, prompt):
    text = _read_retry(lambda: fetch_text(prompt))
    try:
        return parse_json(text)
    except LLMError:
        text = _read_retry(lambda: fetch_text(prompt + "\n" + _REASK))
        return parse_json(text)


class Anthropic:
    def __init__(self, model=None):
        self.key = os.environ.get("ANTHROPIC_API_KEY")
        if not self.key:
            raise LLMError("ANTHROPIC_API_KEY is not set")
        self.model = model or os.environ.get("TAXONOMY_MODEL", "claude-sonnet-5-5")

    def __call__(self, prompt, max_tokens=4000):
        def fetch(p):
            data = _post("https://api.anthropic.com/v1/messages",
                         {"model": self.model, "max_tokens": max_tokens,
                          "messages": [{"role": "user", "content": p}]},
                         {"x-api-key": self.key, "anthropic-version": "2023-06-01", "content-type": "application/json"})
            return "".join(b.get("text", "") for b in data.get("content", []) if b.get("type") == "text")

        return _complete_text(fetch, prompt)


class Ollama:
    def __init__(self, model=None):
        self.model = model or os.environ.get("TAXONOMY_MODEL", "gemma3:12b")
        self.host = os.environ.get("OLLAMA_HOST", "http://127.0.0.1:11434")
        self.timeout = ollama_timeout()

    def __call__(self, prompt, max_tokens=4000):
        def fetch(p):
            data = _post(f"{self.host}/api/generate",
                         {"model": self.model, "prompt": p, "stream": False,
                          "format": "json", "options": {"num_predict": max_tokens}},
                         {"content-type": "application/json"}, timeout=self.timeout)
            return data.get("response", "")

        return _complete_text(fetch, prompt)


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


_ON = {"1", "true", "on", "yes"}


def get_llm(name=None):
    """Local Ollama unless TAXONOMY_LLM names another backend.

    Anthropic is built only when TAXONOMY_ADJUDICATE_PAID is on, the same switch
    the claim adjudicator uses. Naming anthropic without that switch raises.
    """
    name = (name or os.environ.get("TAXONOMY_LLM") or "ollama").strip().lower()
    if name == "anthropic" and os.environ.get("TAXONOMY_ADJUDICATE_PAID", "").strip().lower() not in _ON:
        raise LLMError(
            "Anthropic is a paid API and is off. Set TAXONOMY_ADJUDICATE_PAID=1 to allow it. "
            "The default backend is local Ollama."
        )
    try:
        cls = {"anthropic": Anthropic, "ollama": Ollama, "manual": Manual}[name]
    except KeyError:
        raise LLMError("TAXONOMY_LLM must be ollama, manual, or anthropic") from None
    return cls()
