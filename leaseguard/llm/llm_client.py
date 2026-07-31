"""
Unified LLM client — switches between Groq, Ollama, and Gemini
via a single LLM_PROVIDER environment variable.

All free:
  • Groq       — 14,400 req/day,  Llama 3.1 70B (fastest free cloud LLM)
  • Ollama     — unlimited,       local Mistral / Llama (fully private)
  • Gemini     — 1M tokens/day,   Gemini 1.5 Flash (backup)
"""
from __future__ import annotations
import json
import time
from typing import Any

from loguru import logger
from tenacity import retry, stop_after_attempt, wait_exponential

import leaseguard.config as cfg


class LLMClient:
    """Drop-in LLM client supporting Groq, Ollama, and Google Gemini."""

    def __init__(self, provider: str | None = None) -> None:
        self.provider = (provider or cfg.LLM_PROVIDER).lower()
        self._client: Any = None
        logger.info(f"LLMClient initialised — provider={self.provider}")

    # ── Public interface ───────────────────────────────────────────────────

    @retry(stop=stop_after_attempt(cfg.LLM_MAX_RETRIES),
           wait=wait_exponential(multiplier=1, min=2, max=30),
           reraise=True)
    def chat(self, system: str, user: str) -> str:
        """Send a system + user prompt and return the text response."""
        t0 = time.perf_counter()
        text = self._dispatch(system, user)
        elapsed = time.perf_counter() - t0
        logger.debug(f"LLM call  provider={self.provider}  tokens≈{len(text)//4}  {elapsed:.1f}s")
        return text

    def extract_json(self, system: str, user: str) -> dict:
        """Call LLM and parse its response as JSON. Returns {} on failure."""
        raw = self.chat(system, user).strip()
        # Strip markdown code fences if the model added them
        raw = raw.lstrip("```json").lstrip("```").rstrip("```").strip()
        # Some models wrap with a single-key object — try to unwrap
        try:
            return json.loads(raw)
        except json.JSONDecodeError:
            # Try to find the first { … } block
            start = raw.find("{")
            end   = raw.rfind("}") + 1
            if 0 <= start < end:
                try:
                    return json.loads(raw[start:end])
                except json.JSONDecodeError:
                    pass
            logger.warning(f"JSON parse failed — raw response: {raw[:300]}")
            return {}

    # ── Provider dispatch ──────────────────────────────────────────────────

    def _dispatch(self, system: str, user: str) -> str:
        if self.provider == "groq":
            return self._groq(system, user)
        if self.provider == "ollama":
            return self._ollama(system, user)
        if self.provider == "gemini":
            return self._gemini(system, user)
        if self.provider == "openai":
            return self._openai(system, user)
        raise ValueError(
            f"Unknown LLM_PROVIDER='{self.provider}'. "
            "Set to one of: groq | ollama | gemini | openai"
        )

    # ── OpenAI (GPT-4o-mini etc.) ────────────────────────────────────────────

    def _openai(self, system: str, user: str) -> str:
        if self._client is None:
            from openai import OpenAI  # type: ignore
            kwargs: dict[str, Any] = {"api_key": cfg.OPENAI_API_KEY}
            if cfg.OPENAI_BASE_URL:
                kwargs["base_url"] = cfg.OPENAI_BASE_URL
            self._client = OpenAI(**kwargs)
        resp = self._client.chat.completions.create(
            model=cfg.OPENAI_MODEL,
            temperature=cfg.LLM_TEMPERATURE,
            max_tokens=cfg.LLM_MAX_TOKENS,
            messages=[
                {"role": "system", "content": system},
                {"role": "user",   "content": user},
            ],
        )
        return resp.choices[0].message.content or ""

    # ── Groq ────────────────────────────────────────────────────────────────

    def _groq(self, system: str, user: str) -> str:
        if self._client is None:
            from groq import Groq  # type: ignore
            self._client = Groq(api_key=cfg.GROQ_API_KEY)
        resp = self._client.chat.completions.create(
            model=cfg.GROQ_MODEL,
            temperature=cfg.LLM_TEMPERATURE,
            max_tokens=cfg.LLM_MAX_TOKENS,
            messages=[
                {"role": "system", "content": system},
                {"role": "user",   "content": user},
            ],
        )
        return resp.choices[0].message.content or ""

    # ── Ollama (local) ──────────────────────────────────────────────────────

    def _ollama(self, system: str, user: str) -> str:
        import requests  # type: ignore
        resp = requests.post(
            f"{cfg.OLLAMA_BASE_URL}/api/chat",
            json={
                "model":  cfg.OLLAMA_MODEL,
                "stream": False,
                "options": {"temperature": cfg.LLM_TEMPERATURE, "num_predict": cfg.LLM_MAX_TOKENS},
                "messages": [
                    {"role": "system", "content": system},
                    {"role": "user",   "content": user},
                ],
            },
            timeout=180,
        )
        resp.raise_for_status()
        return resp.json()["message"]["content"]

    # ── Google Gemini Flash ─────────────────────────────────────────────────

    def _gemini(self, system: str, user: str) -> str:
        import google.generativeai as genai  # type: ignore
        if self._client is None:
            genai.configure(api_key=cfg.GEMINI_API_KEY)
            self._client = genai.GenerativeModel(
                cfg.GEMINI_MODEL,
                system_instruction=system,
            )
        resp = self._client.generate_content(
            user,
            generation_config={"temperature": cfg.LLM_TEMPERATURE,
                               "max_output_tokens": cfg.LLM_MAX_TOKENS},
        )
        return resp.text
