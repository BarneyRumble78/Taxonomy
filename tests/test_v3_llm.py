"""Local model client: timeout, retry, and JSON salvage. No network."""
import json, sys, urllib.error
from email.message import Message
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "engine" / "v3"))
import llm


class _Body:
    def __init__(self, payload):
        self.payload = payload

    def read(self):
        return self.payload

    def __enter__(self):
        return self

    def __exit__(self, *args):
        return False


def _http(code):
    return urllib.error.HTTPError("http://127.0.0.1/api/generate", code, "err", Message(), None)


def test_parse_accepts_cutoff_and_a_second_object():
    assert llm.parse_json('{"problem": "hel') == {"problem": "hel"}
    assert llm.parse_json('{"a": 1, "b": [1, 2') == {"a": 1, "b": [1, 2]}
    assert llm.parse_json('{"a": 1}{"b": 2}') == {"a": 1}
    assert llm.parse_json('note\n{"a": 1}\n{"b": 2}') == {"a": 1}
    fenced = "```json\n{\"a\": 1}\n```"
    assert llm.parse_json(fenced) == {"a": 1}


def test_ollama_timeout_follows_the_environment(monkeypatch):
    seen = {}

    def fake_urlopen(req, timeout=None):
        seen["timeout"] = timeout
        raise urllib.error.URLError("down")

    monkeypatch.setattr(llm.urllib.request, "urlopen", fake_urlopen)
    monkeypatch.setattr(llm.time, "sleep", lambda _s: None)
    monkeypatch.delenv("TAXONOMY_OLLAMA_TIMEOUT", raising=False)
    try:
        llm.Ollama()("hi")
    except llm.LLMError:
        pass
    else:
        raise AssertionError("a dead host returned JSON")
    assert seen["timeout"] == 120

    monkeypatch.setenv("TAXONOMY_OLLAMA_TIMEOUT", "45")
    try:
        llm.Ollama()("hi")
    except llm.LLMError:
        pass
    assert seen["timeout"] == 45
    monkeypatch.setenv("TAXONOMY_OLLAMA_TIMEOUT", "nope")
    assert llm.Ollama().timeout == 120


def test_connection_errors_retry_three_times(monkeypatch):
    calls = {"n": 0}
    slept = []

    def fake_urlopen(req, timeout=None):
        calls["n"] += 1
        if calls["n"] < 3:
            raise urllib.error.URLError("down")
        body = json.dumps({"response": '{"a": 1}'}).encode()
        return _Body(body)

    monkeypatch.setattr(llm.urllib.request, "urlopen", fake_urlopen)
    monkeypatch.setattr(llm.time, "sleep", lambda s: slept.append(s))
    monkeypatch.delenv("TAXONOMY_OLLAMA_TIMEOUT", raising=False)
    assert llm.Ollama()("prompt") == {"a": 1}
    assert calls["n"] == 3
    assert slept == [1, 2]


def test_server_errors_retry_and_client_errors_do_not(monkeypatch):
    calls = {"n": 0}
    slept = []

    def fake_urlopen(req, timeout=None):
        calls["n"] += 1
        if calls["n"] < 3:
            raise _http(503)
        return _Body(json.dumps({"response": '{"a": 1}'}).encode())

    monkeypatch.setattr(llm.urllib.request, "urlopen", fake_urlopen)
    monkeypatch.setattr(llm.time, "sleep", lambda s: slept.append(s))
    assert llm.Ollama()("prompt") == {"a": 1}
    assert calls["n"] == 3 and slept == [1, 2]

    calls["n"] = 0
    slept.clear()

    def denied(req, timeout=None):
        calls["n"] += 1
        raise _http(401)

    monkeypatch.setattr(llm.urllib.request, "urlopen", denied)
    monkeypatch.setenv("ANTHROPIC_API_KEY", "test-key")
    monkeypatch.setenv("TAXONOMY_ADJUDICATE_PAID", "1")
    try:
        llm.Anthropic()("prompt")
    except llm.LLMError as exc:
        assert "401" in str(exc)
    else:
        raise AssertionError("a 401 was retried into success")
    assert calls["n"] == 1 and slept == []


def test_bad_json_is_asked_once_more(monkeypatch):
    prompts = []

    def fake_urlopen(req, timeout=None):
        sent = json.loads(req.data.decode())["prompt"]
        prompts.append(sent)
        if len(prompts) == 1:
            body = json.dumps({"response": "not json at all"})
        else:
            body = json.dumps({"response": '{"a": 1}'})
        return _Body(body.encode())

    monkeypatch.setattr(llm.urllib.request, "urlopen", fake_urlopen)
    monkeypatch.setattr(llm.time, "sleep", lambda _s: None)
    assert llm.Ollama()("classify this") == {"a": 1}
    assert len(prompts) == 2
    assert prompts[1].endswith("Return valid JSON only")
    assert prompts[1].startswith("classify this")


def test_qwen_is_the_default_and_gemma_is_the_fallback(monkeypatch):
    monkeypatch.delenv("TAXONOMY_MODEL", raising=False)
    assert llm.Ollama().model == "qwen3:30b-a3b"
    assert llm.Ollama().fallback == "gemma3:12b"
    monkeypatch.setenv("TAXONOMY_MODEL", "gemma3:12b")
    assert llm.Ollama().model == "gemma3:12b"
    assert llm.Ollama().fallback is None
    monkeypatch.delenv("TAXONOMY_MODEL", raising=False)
    models = []

    def fake_urlopen(req, timeout=None):
        body = json.loads(req.data.decode())
        models.append(body["model"])
        assert body["think"] is False
        if body["model"] == "qwen3:30b-a3b":
            raise urllib.error.URLError("down")
        return _Body(json.dumps({"response": '{"a": 1}'}).encode())

    monkeypatch.setattr(llm.urllib.request, "urlopen", fake_urlopen)
    monkeypatch.setattr(llm.time, "sleep", lambda _s: None)
    assert llm.Ollama()("prompt") == {"a": 1}
    assert models[:3] == ["qwen3:30b-a3b"] * 3
    assert models[3] == "gemma3:12b"


def test_empty_response_uses_thinking_text(monkeypatch):
    def fake_urlopen(req, timeout=None):
        body = json.loads(req.data.decode())
        assert body["think"] is False
        return _Body(json.dumps({"response": "  ", "thinking": '{"a": 2}'}).encode())

    monkeypatch.setattr(llm.urllib.request, "urlopen", fake_urlopen)
    monkeypatch.delenv("TAXONOMY_MODEL", raising=False)
    assert llm.Ollama()("prompt") == {"a": 2}


def test_cutoff_json_does_not_reask(monkeypatch):
    calls = {"n": 0}

    def fake_urlopen(req, timeout=None):
        calls["n"] += 1
        return _Body(json.dumps({"response": '{"problem": "hel'}).encode())

    monkeypatch.setattr(llm.urllib.request, "urlopen", fake_urlopen)
    assert llm.Ollama()("prompt") == {"problem": "hel"}
    assert calls["n"] == 1
