#!/usr/bin/env python3
"""
Run the full STEM video pipeline end-to-end:
1) Generate topic
2) Generate script (Ollama if available, otherwise local)
3) Analyze script entities
4) Download Wikipedia images
5) Generate TTS audio
6) Render Manim animation (vertical 1080x1920)
7) Combine audio + video into final file

Usage (Windows PowerShell):
  python run_pipeline.py

Options:
  --script-generator [auto|ollama|local]
  --quality [qk|ql|qm|qh]
  --fps 60
  --resolution 1080,1920
  --render-script scripts/render_manim_dynamic.py
  --scene STEMScene

Outputs go to the output/ directory. Final video will be named final_*.mp4
"""
from __future__ import annotations

import argparse
import json
import logging
import os
import sys
import subprocess
from datetime import datetime
from pathlib import Path
from shutil import which
from typing import List, Optional


def setup_logging() -> None:
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s",
        handlers=[
            logging.FileHandler("automation.log"),
            logging.StreamHandler()
        ]
    )


def run(cmd: List[str], name: Optional[str] = None, cwd: Optional[str] = None) -> subprocess.CompletedProcess:
    disp = " ".join(cmd)
    logging.info(f"$ {disp}")
    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            cwd=cwd,
            check=False
        )
    except FileNotFoundError as e:
        raise RuntimeError(f"Command not found: {cmd[0]}") from e

    if result.returncode != 0:
        logging.error(result.stdout)
        logging.error(result.stderr)
        raise RuntimeError(f"Step failed ({name or cmd[0]}): {result.stderr.strip() or result.stdout.strip()}")

    if result.stdout:
        logging.debug(result.stdout)
    if result.stderr:
        logging.debug(result.stderr)
    return result


def find_script_generator(prefer: str = "auto") -> List[str]:
    ollama_path = Path("scripts/generate_script_ollama.py")
    local_path = Path("scripts/generate_script.py")

    if prefer == "ollama":
        if ollama_path.exists():
            return [sys.executable, str(ollama_path)]
        raise FileNotFoundError("scripts/generate_script_ollama.py not found; use --script-generator local or auto")
    if prefer == "local":
        return [sys.executable, str(local_path)]

    # auto
    if ollama_path.exists():
        return [sys.executable, str(ollama_path)]
    return [sys.executable, str(local_path)]


def manim_cmd(quality: str, fps: int, resolution: str, render_script: str, scene: str) -> List[str]:
    # Use manim CLI if available, otherwise fallback to python -m manim
    base = ["manim"] if which("manim") else [sys.executable, "-m", "manim"]
    return base + [f"-{quality}", "--format=mp4", "--fps", str(fps), "--resolution", resolution, render_script, scene]


def find_latest_final_video(output_dir: Path) -> Optional[Path]:
    vids = list(output_dir.glob("final_*.mp4"))
    if not vids:
        return None
    return max(vids, key=lambda p: p.stat().st_mtime)


def main() -> int:
    parser = argparse.ArgumentParser(description="Run full STEM video pipeline")
    parser.add_argument("--script-generator", choices=["auto", "ollama", "local"], default="auto",
                        help="Choose script generator (default: auto)")
    parser.add_argument("--quality", default="qh", choices=["qk", "ql", "qm", "qh"],
                        help="Manim quality preset (qh=high)")
    parser.add_argument("--fps", type=int, default=60, help="Frames per second for render")
    parser.add_argument("--resolution", default="1080,1920", help="Render resolution WxH (e.g., 1080,1920)")
    parser.add_argument("--render-script", default="scripts/render_manim_dynamic.py", help="Path to Manim script")
    parser.add_argument("--scene", default="STEMScene", help="Manim Scene class name")
    args = parser.parse_args()

    setup_logging()

    start_time = datetime.now()
    out_dir = Path("output")
    out_dir.mkdir(exist_ok=True, parents=True)

    logging.info("=" * 80)
    logging.info("🚀 Starting STEM video generation pipeline (script)")
    logging.info("=" * 80)

    # Step 1: Generate topic
    logging.info("Step 1/7: Generating topic…")
    run([sys.executable, "scripts/generate_prompt.py"], name="generate_prompt")

    # Step 2: Generate script
    logging.info("Step 2/7: Generating script…")
    gen_cmd = find_script_generator(args.__dict__["script_generator"])  # access hyphenated arg
    run(gen_cmd, name="generate_script")

    # Step 3: Analyze script entities
    logging.info("Step 3/7: Analyzing script…")
    run([sys.executable, "scripts/analyze_script.py"], name="analyze_script")

    # Step 4: Download images
    logging.info("Step 4/7: Downloading images…")
    run([sys.executable, "scripts/download_images.py"], name="download_images")

    # Step 5: Generate TTS audio
    logging.info("Step 5/7: Generating audio…")
    run([sys.executable, "scripts/generate_audio.py"], name="generate_audio")

    # Step 6: Render Manim animation
    logging.info("Step 6/7: Rendering Manim…")
    cmd = manim_cmd(args.quality, args.fps, args.resolution, args.render_script, args.scene)
    run(cmd, name="manim_render", cwd=os.getcwd())

    # Step 7: Combine audio + video
    logging.info("Step 7/7: Combining audio + video…")
    run([sys.executable, "scripts/combine_video.py"], name="combine_video")

    latest = find_latest_final_video(out_dir)
    size_mb = round(latest.stat().st_size / (1024 * 1024), 2) if latest and latest.exists() else 0.0
    end_time = datetime.now()
    duration = (end_time - start_time).total_seconds()

    summary = {
        "status": "success",
        "video_path": str(latest.absolute()) if latest else "not found",
        "file_size_mb": size_mb,
        "duration_seconds": round(duration, 1),
        "timestamp": end_time.strftime("%Y-%m-%d %H:%M:%S"),
        "render": {
            "quality": args.quality,
            "fps": args.fps,
            "resolution": args.resolution,
            "scene": args.scene,
            "script": args.render_script,
        },
        "script_generator": args.__dict__["script_generator"],
    }

    logging.info("=" * 80)
    logging.info(f"📹 Final video: {summary['video_path']}")
    logging.info(f"📊 Size: {summary['file_size_mb']} MB | ⏱️  {summary['duration_seconds']}s")
    logging.info("=" * 80)

    # Also print JSON summary to stdout for automation
    print(json.dumps(summary, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as e:
        logging.exception("Pipeline failed")
        # Emit a machine-readable error as well
        err = {"status": "error", "message": str(e)}
        print(json.dumps(err, ensure_ascii=False))
        raise SystemExit(1)
