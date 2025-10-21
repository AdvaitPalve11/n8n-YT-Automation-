# 🎬 Local AI Bulk Video System - Quick Reference

## 🚀 Quick Commands

### Test the system
```powershell
# Check if script is working
python scripts/generate_bulk_videos.py --help

# Generate videos (default: Manim, fastest)
python scripts/generate_bulk_videos.py

# Specific backend
python scripts/generate_bulk_videos.py --backend manim --duration 5
```

### Edit prompts
```powershell
notepad prompts.csv
```

### Via API
```powershell
# Start server
python server.py

# In another terminal
Invoke-RestMethod -Uri http://127.0.0.1:8000/generate-bulk-videos -Method POST
```

## 📋 Prompt CSV Format

```csv
Prompt,Name,Variations
"Your video description here",identifier,2
"Another video prompt",another-id,3
```

**Example:**
```csv
Prompt,Name,Variations
"Fibonacci spiral growing from center",fibonacci,2
"Mathematical formulas on chalkboard",formulas,3
```

## 🎨 Backend Options

| Backend | Speed | GPU | Quality | Best For |
|---------|-------|-----|---------|----------|
| `manim` | ⚡⚡⚡ | ❌ | Good | Math content |
| `text2video` | ⚡ | ✅ | Great | Animated |
| `svd` | ⚡ | ✅ | Excellent | Photorealistic |

## 📊 Expected Output

```
output/bulk_videos/
├── video_fibonacci_v1.mp4
├── video_fibonacci_v2.mp4
├── video_formulas_v1.mp4
├── video_formulas_v2.mp4
├── video_formulas_v3.mp4
└── generation_results.json
```

## 🔧 Troubleshooting

### Import errors?
```powershell
pip install pandas opencv-python
```

### GPU not detected?
```powershell
python -c "import torch; print(torch.cuda.is_available())"
```

### Manim errors?
```powershell
manim --version
pip install --upgrade manim
```

## 📚 Full Documentation

See **LOCAL_VIDEO_SETUP.md** for:
- Detailed installation
- AI model setup
- Performance tuning
- Advanced features
- Cost comparisons

---

**Start generating:** `python scripts/generate_bulk_videos.py`
