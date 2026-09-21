"""Base Agent — LLM integration via openRouter/free model, isolation, protocol I/O."""
import json, os, time, subprocess, sys
from pathlib import Path
from typing import Dict, Any, Optional

# Try openrouter API; fall back to Nous inference API if available
OPENROUTER_URL = "https://openrouter.ai/api/v1/chat/completions"
NOUS_URL = "https://inference-api.nousresearch.com/v1/chat/completions"


def _get_key(source="openrouter"):
    env_key = f"{source.upper()}_API_KEY"
    key = os.getenv(env_key, "")
    if key:
        return key
    # Try hermes auth.json via python (only if user grants, else empty)
    try:
        auth_path = Path.home() / ".hermes/auth.json"
        if auth_path.exists():
            d = json.load(open(auth_path))
            for cred in d.get("credential_pool", {}).get(source, []):
                k = cred.get("api_key") or cred.get("key")
                if k and len(str(k)) > 10:
                    return str(k)
    except Exception:
        pass
    return ""


def llm_chat(prompt: str, model: str = "openai/gpt-3.5-turbo", max_tokens: int = 2048, temperature: float = 0.3) -> str:
    """Call LLM. Prefers openRouter/free model; falls back to Nous if available."""
    import requests
    headers = {"Content-Type": "application/json"}
    payload = {
        "model": model,
        "messages": [{"role": "user", "content": prompt}],
        "temperature": temperature,
        "max_tokens": max_tokens,
    }
    # Try openRouter first
    open_key = _get_key("openrouter")
    url = OPENROUTER_URL
    if open_key and open_key.startswith("sk-"):
        headers["Authorization"] = f"Bearer {open_key}"
        headers["HTTP-Referer"] = "https://engineering-team.local"
        headers["X-Title"] = "Engineering Team"
    else:
        # Try Nous
        nous_key = _get_key("nous")
        if nous_key and nous_key.startswith("sk-"):
            url = NOUS_URL
            headers["Authorization"] = f"Bearer {nous_key}"
        else:
            # Mock/fallback mode: return a structured instruction so the framework still works
            return f"[LLM UNAVAILABLE — using mock mode for '{model}']\n{prompt}\n---\nGenerate code/protocol based on the prompt above."

    try:
        resp = requests.post(url, headers=headers, json=payload, timeout=120)
        if resp.status_code == 200:
            data = resp.json()
            return data.get("choices", [{}])[0].get("message", {}).get("content", "")
        else:
            # If openrouter fails with 401, try Nous
            if url == OPENROUTER_URL and (resp.status_code in (401, 403, 404)):
                return llm_chat(prompt, model=model, max_tokens=max_tokens, temperature=temperature)
            msg = resp.text[:500]
            return f"[LLM ERROR {resp.status_code}: {msg}] Generate manually based on: {prompt[:200]}"
    except Exception as e:
        return f"[LLM EXCEPTION: {e}] Generate manually based on: {prompt[:200]}"


def write_artifact(path: Path, content: str):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def read_artifact(path: Path) -> str:
    return path.read_text(encoding="utf-8") if path.exists() else ""
