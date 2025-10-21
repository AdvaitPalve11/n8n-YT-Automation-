# STEM Automation – AI Video Generator

[![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?logo=python&logoColor=white)](#)
[![Manim](https://img.shields.io/badge/Manim-Community-1f7a8c?logo=python&logoColor=white)](#)
[![FastAPI](https://img.shields.io/badge/FastAPI-API%20Server-009688?logo=fastapi&logoColor=white)](#)

Create short, engaging math videos automatically using Wikipedia + AI scripts + dynamic Manim animations. This project turns a topic into a ~60‑second narrated video with smart keyframes, on‑screen text, and math formulas—no cloud APIs required. Supports batch generation and REST automation.



## Quick Start---



```bash## 🚀 Quick Start (60 seconds)

# Start server

python server.py```powershell

# Start the server

# Generate AI prompts and videospython server.py

python scripts/auto_generate_pipeline.py --count 5

# In another terminal, generate a video

# Generate just promptsInvoke-RestMethod -Uri http://127.0.0.1:8000/run-animation -Method POST

python scripts/generate_prompts_hf.py --count 10

```# Done! Video is in: output/final_[topic].mp4

```

## Features

---

- 🤖 **AI Prompt Generation** - Qwen3-4B generates creative video ideas

- 🎬 **Automated Video Creation** - Manim renders mathematical animations## 📋 What This Does

- 📊 **Batch Processing** - Generate multiple videos at once

- 🎨 **YouTube Shorts Format** - Vertical 1080x1920, 60fpsAutomatically creates **YouTube Shorts** (vertical 9:16, 60fps) by:



## Project Structure1. ✅ Picking a **popular math topic** (Pythagoras, Fibonacci, Pi, etc.)

2. ✅ Generating an **engaging script** with hooks and CTAs  

```3. ✅ Creating **audio narration** from the script

├── scripts/           # Core automation scripts4. ✅ Rendering **vertical animated video** (1080x1920)

├── output/           # Generated content5. ✅ Combining into **ready-to-upload YouTube Short**

├── media/            # Manim cache

├── workflows/        # n8n automation workflows**Time per video**: ~60 seconds

└── docs/             # Documentation

```---



## Requirements## 🛠️ Installation



- Python 3.13+```powershell

- PyTorch, Transformers (for AI)# Install dependencies

- Manim Community (for videos)pip install manim pyttsx3 moviepy fastapi uvicorn wikipedia-api

- n8n (optional, for automation)

# Verify Manim

## Documentationmanim --version

```

See `docs/` folder for detailed guides.

---

## 📁 Project Structure

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
    └── final_[topic].mp4          # Final video ✅
```

---

## 🎯 Usage

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

### Mode 2: Bulk Videos (NEW! 🎬)

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

## 📊 Example Output

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
- **Ready to upload!** ✅

---

## 🎨 Features

### ✨ Smart & DYNAMIC Content
- **45+ curated math topics** (Pythagoras, Fibonacci, Pi, etc.)
- **Topic-specific animations**: 
  - Pascal's Triangle: Builds row by row with number highlighting
  - Fibonacci: Shows sequence building + golden spiral
  - Pythagorean theorem: Visual proof with squares
  - Pi: Circle with circumference unwrapping
  - Euler's identity: Highlighted equation parts
  - And more custom animations for each topic!
- **Engaging narration** with hooks & CTAs
- **NOT just static symbols** - Real educational animations!

### 📱 YouTube Shorts Optimized
- Vertical format (1080x1920)
- 60fps smooth animations
- Topic displayed prominently
- 30-45 second duration

### 🤖 Fully Automated
- One command → complete video
- No API costs (offline TTS)
- Scalable to 100s of videos

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

## 📤 Upload to YouTube

1. Go to YouTube Studio
2. Upload `output/final_[topic].mp4`
3. Title: "[Topic] Explained! 🔢 #Shorts"
4. Add hashtags: #Shorts #Math #STEM
5. Publish!

**Best Practice**: Upload 4 shorts/day at consistent times

---

## 🎬 Customization

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

## 🐛 Troubleshooting

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

## 🏆 Success Metrics

Track in YouTube Analytics:
- **Views**: 1K+ per short
- **Retention**: 70%+
- **Likes**: 5%+ rate
- **Subscribers**: 10+ per 1K views

---

## 📞 API Endpoints

### Status Check
```powershell
Invoke-RestMethod -Uri http://127.0.0.1:8000/status
```

### Generate Single Video
```powershell
Invoke-RestMethod -Uri http://127.0.0.1:8000/run-animation -Method POST
```

### Generate Bulk Videos (NEW!)
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

### Original Generate Video Endpoint
```powershell
Invoke-RestMethod -Uri http://127.0.0.1:8000/run-animation -Method POST
```

---

## 💡 Pro Tips

1. **Batch generate** 50 videos, schedule uploads
2. **Track analytics** - focus on best-performing topics
3. **Engage** - reply to all comments
4. **Consistency** - upload daily at same times
5. **Hashtags** - always use #Shorts
6. **Series** - create themed weeks

---

## 🚀 Start Creating!

```powershell
python server.py
```

**Your first YouTube Short will be ready in 60 seconds!** 🎉

---

**Made with ❤️ for Math Education & Content Automation**
