#!/usr/bin/env python3
"""
Generate a script using local Ollama model and save to output/script.json
- Reads topic from output/topic.json
- Prefers Qwen models (qwen3:4b, qwen2.5:4b, qwen2.5:7b), falls back to llama3.1
- Optionally pass --model to force a specific model name
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

import requests

try:
    import wikipedia
except Exception:
    wikipedia = None


def pick_ollama_model(preferred: str | None = None) -> str:
    try:
        r = requests.get("http://127.0.0.1:11434/api/tags", timeout=1)
        models = r.json().get("models", []) if r.status_code == 200 else []
        names = {m.get("name", "").lower() for m in models}
    except Exception:
        names = set()

    if preferred and preferred.lower() in names:
        return preferred

    for cand in ("qwen3:4b", "qwen2.5:4b", "qwen2.5:7b", "qwen:4b"):
        if cand in names:
            return cand

    return "llama3.1"


def fetch_wiki_summary(topic: str) -> str:
    if wikipedia is None:
        return topic
    try:
        wikipedia.set_lang("en")
        return wikipedia.summary(topic, sentences=5)
    except Exception:
        return topic


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--model", help="Ollama model name to use (e.g., qwen3:4b)")
    parser.add_argument("--max_words", type=int, default=150)
    args = parser.parse_args()

    topic_file = Path("output/topic.json")
    if not topic_file.exists():
        print("topic.json not found. Run the topic generation step first.")
        return 1

    with topic_file.open("r", encoding="utf-8") as f:
        data = json.load(f)
    topic = data.get("topic") or "Mathematics"

    model = pick_ollama_model(args.model)
    context = fetch_wiki_summary(topic)

    prompt = (
        f"Write an engaging ~{args.max_words}-word educational script about {topic}.\n\n"
        f"Context: {context[:800]}\n\n"
        "Rules:\n- Hook first\n- Simple language\n- Clear flow\n- No markdown, plain text\n"
    )

    payload = {
        "model": model,
        "prompt": prompt,
        "stream": False,
        "options": {"temperature": 0.7}
    }

    try:
        r = requests.post("http://127.0.0.1:11434/api/generate", json=payload, timeout=60)
        r.raise_for_status()
        text = (r.json().get("response") or "").strip()
        if not text:
            print("Ollama returned empty response")
            return 2
    except Exception as e:
        print(f"Ollama request failed: {e}")
        return 2

    # Build structured output compatible with generate_audio.py expectations
    # Try to carry category forward if present
    category = "Mathematics"
    topic_meta = Path("output/topic.json")
    if topic_meta.exists():
        try:
            with topic_meta.open("r", encoding="utf-8") as tf:
                tdata = json.load(tf)
                category = tdata.get("category", category)
        except Exception:
            pass

    script_struct = {
        "hook": f"Let's talk about {topic}.",
        "main_point_1": "",
        "main_point_2": "",
        "closing": "",
        "full_text": text,
        "estimated_duration": max(30, int(len(text.split()) * 0.5)),
    }

    script_data = {
        "topic": topic,
        "category": category,
        "script": script_struct,
        "metadata": {
            "word_count": len(text.split()),
            "estimated_duration_seconds": script_struct["estimated_duration"],
            "source": "ollama",
            "model": model,
        },
    }

    out = Path("output")
    out.mkdir(exist_ok=True)
    with (out / "script.json").open("w", encoding="utf-8") as f:
        json.dump(script_data, f, ensure_ascii=False, indent=2)

    print(f"Script generated with {model} ({len(text.split())} words)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
