# STEM Automation – AI Video Generator

[![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?logo=python&logoColor=white)](#)
[![Manim](https://img.shields.io/badge/Manim-Community-1f7a8c?logo=python&logoColor=white)](#)
[![FastAPI](https://img.shields.io/badge/FastAPI-API%20Server-009688?logo=fastapi&logoColor=white)](#)

Create short, engaging math videos automatically using Wikipedia + AI scripts + dynamic Manim animations. This project turns a topic into a ~60‑second narrated video with smart keyframes, on‑screen text, and math formulas—no cloud APIs required. Supports batch generation and REST automation.

## Quick Start (Windows)

```powershell
# 1) Install dependencies
pip install -r requirements.txt

# 2) Start the API server (opens on http://127.0.0.1:8000)
python server.py

# 3) In another PowerShell window, trigger a render
Invoke-RestMethod -Uri http://127.0.0.1:8000/run-animation -Method POST

# Optional: discover topics (free)
Invoke-RestMethod -Uri "http://127.0.0.1:8000/topics/suggest?source=wikipedia&query=graph%20theory&limit=5"

# Optional: generate a script (free fallbacks)
Invoke-RestMethod -Uri http://127.0.0.1:8000/scripts/generate -Method POST -Body (@{
  topic = "Four color theorem"; provider = "auto"; max_words = 120
} | ConvertTo-Json) -ContentType "application/json"
```

Videos are saved to `output/videos/` (audio and videos are ignored by git).

---

## Features

- AI topic + script generation (Qwen3-4B via Transformers; Wikipedia fallback)
- Professional TTS with Edge TTS (gTTS fallback)
- Dynamic Manim scenes (intro, key points, formulas, outro)
- Smart text wrapping and audio‑synced timings
- No cloud APIs required; optional GPU acceleration
- REST API + n8n workflows for automation

---

## Installation

Requirements:
- Python 3.10+
- Manim Community
- FFmpeg available in PATH
- Optional: CUDA GPU for faster model inference

```powershell
pip install -r requirements.txt
manim --version  # verify Manim install
```

See `docs/` for detailed guides.

---

## Project Structure

```
STEM_Automation/
├── server.py                      # Main orchestrator
├── scripts/
│   ├── generate_prompt.py         # Pick topic
│   ├── generate_script.py         # Create script
│   ├── generate_audio.py          # Generate TTS
│   ├── render_manim_shorts.py     # Render video
│   └── combine_video.py           # Combine all
└── output/
    ├── topic.json                 # Topic data
    ├── script.json                # Script
    ├── audio.wav                  # Audio
  └── final_[topic].mp4          # Final video
```

---

## Usage

### Mode 1: Single Video (YouTube Shorts) ⚡

**Automated:**
```powershell
python server.py
Invoke-RestMethod -Uri http://127.0.0.1:8000/run-animation -Method POST
```

**Manual (Step by Step):**
```powershell
python scripts/generate_prompt.py
python scripts/generate_script.py
python scripts/generate_audio.py
manim -qh --format=mp4 --fps=60 --resolution 1080,1920 scripts/render_manim_shorts.py STEMScene
python scripts/combine_video.py
```

### Mode 2: Bulk Videos (NEW)

**Local AI - No Cloud APIs!**

```powershell
# Edit prompts with your ideas
notepad prompts.csv

# Generate all videos (Manim - fastest)
python scripts/generate_bulk_videos.py

# Or use AI backends (requires GPU)
python scripts/generate_bulk_videos.py --backend svd
python scripts/generate_bulk_videos.py --backend text2video

# Via API endpoint
Invoke-RestMethod -Uri http://127.0.0.1:8000/generate-bulk-videos -Method POST

# Via n8n (automated every 12 hours)
# Import n8n_bulk_video_workflow.json
```

**See `LOCAL_VIDEO_SETUP.md` for complete bulk video guide!**

---

## Example Output

**Topic**: "Fibonacci Sequence"

**Files Generated**:
- `topic.json` - Topic metadata
- `script.json` - Script with hook, points, CTA
- `audio.wav` - Narration (~30 sec)
- `final_Fibonacci_sequence.mp4` - YouTube Short (1080x1920, 60fps)

**Video Specs**:
- Resolution: 1080x1920 (9:16)
- Frame rate: 60fps
- Duration: 30-45 seconds
- Size: 2-4MB
- Ready to upload.

---

## 📈 Batch Generation

```powershell
# Generate 10 videos
1..10 | ForEach-Object {
    Invoke-RestMethod -Uri http://127.0.0.1:8000/run-animation -Method POST
    Start-Sleep -Seconds 65
}
```

---

## Upload to YouTube

1. Go to YouTube Studio
2. Upload `output/final_[topic].mp4`
3. Title: "[Topic] Explained! #Shorts"
4. Add hashtags: #Shorts #Math #STEM
5. Publish!

**Best Practice**: Upload 4 shorts/day at consistent times

---

## Customization

### Change Topics
Edit `scripts/generate_prompt.py`:
```python
popular_math_topics = [
    "Your topic",
    "Another topic",
]
```

### Change CTAs
Edit `scripts/generate_script.py`:
```python
ctas = [
    "Like and subscribe! 👍",
    "Follow for more math! 🔔",
]
```

---

## Troubleshooting

**Video not generating?**
```powershell
manim --version  # Check installation
```

**Audio issues?**
```powershell
python -c "import pyttsx3; print('OK')"
```

**Vertical format not working?**
```powershell
manim -qh --resolution 1080,1920 scripts/render_manim_shorts.py STEMScene
```

---

## Success Metrics

Track in YouTube Analytics:
- **Views**: 1K+ per short
- **Retention**: 70%+
- **Likes**: 5%+ rate
- **Subscribers**: 10+ per 1K views

---

## API Endpoints

### Status Check
```powershell
Invoke-RestMethod -Uri http://127.0.0.1:8000/status
```

### Generate Single Video
```powershell
Invoke-RestMethod -Uri http://127.0.0.1:8000/run-animation -Method POST
```

### Suggest Topics (free)
- Wikipedia
```powershell
Invoke-RestMethod -Uri "http://127.0.0.1:8000/topics/suggest?source=wikipedia&query=linear%20algebra&limit=5"
```
- arXiv (recent submissions by category)
```powershell
Invoke-RestMethod -Uri "http://127.0.0.1:8000/topics/suggest?source=arxiv&arxiv_category=math.CO&limit=5"
```

### Generate Script (free fallbacks)
Provider priority: requested provider → Ollama (if running) → Transformers (if installed) → Wikipedia-only fallback.
```powershell
Invoke-RestMethod -Uri http://127.0.0.1:8000/scripts/generate -Method POST -Body (@{
  topic = "Euler's identity"; provider = "auto"; max_words = 140
} | ConvertTo-Json) -ContentType "application/json"
```

Using your local Ollama with Qwen (preferred if installed):
```powershell
Invoke-RestMethod -Uri http://127.0.0.1:8000/scripts/generate -Method POST -Body (@{
  topic = "Four color theorem"; provider = "ollama"; model = "qwen3:4b"; max_words = 140
} | ConvertTo-Json) -ContentType "application/json"
```

### Generate Bulk Videos (NEW)
```powershell
Invoke-RestMethod -Uri http://127.0.0.1:8000/generate-bulk-videos -Method POST -Body (@{
    csv_path = "prompts.csv"
    backend = "manim"
    duration = 5
} | ConvertTo-Json) -ContentType "application/json"
```

**Response:**
```json
{
  "status": "success",
  "total_videos": 18,
  "successful": 18,
  "videos": [
    {"name": "fibonacci", "variation": 1, "path": "C:\\...\\video_fibonacci_v1.mp4"}
  ]
}
```

### Autonomous Generation (experimental)
```powershell
Invoke-RestMethod -Uri http://127.0.0.1:8000/auto-generate-videos -Method POST -Body (@{
  count = 5; topic = "mathematics"; backend = "manim"; enhance_scripts = $true
} | ConvertTo-Json) -ContentType "application/json"
```

---

## Pro Tips

1. **Batch generate** 50 videos, schedule uploads
2. **Track analytics** - focus on best-performing topics
3. **Engage** - reply to all comments
4. **Consistency** - upload daily at same times
5. **Hashtags** - always use #Shorts
6. **Series** - create themed weeks

---

## Start Creating

```powershell
python server.py
```

**Your first YouTube Short will be ready in 60 seconds!** 🎉

---
