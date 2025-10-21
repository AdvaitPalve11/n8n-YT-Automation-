# 🚀 Complete Automation Setup Guide
## Math Video → YouTube Pipeline with n8n

This guide will help you set up **fully automated** YouTube Shorts generation and upload using n8n and Python.

---

## 📋 Prerequisites

### Required Software:
1. **Python 3.13+** ✅ (Already installed)
2. **Docker Desktop** - [Download](https://www.docker.com/products/docker-desktop/)
3. **Ollama** (Optional, for AI scripts) - [Download](https://ollama.ai/)

### Required Accounts:
1. **Google Cloud Console** account (for YouTube API)
2. **YouTube channel** where videos will be uploaded

---

## 🐳 Part 1: Setup n8n in Docker

### Step 1: Start n8n Container

```powershell
# From STEM_Automation folder
docker-compose up -d
```

**What this does:**
- Starts n8n on `http://localhost:5678`
- Creates persistent data storage
- Mounts `output/` folder for video access
- Enables communication with Python server

### Step 2: Access n8n Interface

1. Open browser: `http://localhost:5678`
2. Login with:
   - Username: `admin`
   - Password: `admin123`

**⚠️ Change credentials in `docker-compose.yml` for production!**

---

## 🔑 Part 2: Setup YouTube API Access

### Step 1: Create Google Cloud Project

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Click **"New Project"**
3. Name it: `Math-Automation`
4. Click **"Create"**

### Step 2: Enable YouTube Data API

1. In your project, go to **"APIs & Services" → "Library"**
2. Search for: `YouTube Data API v3`
3. Click **"Enable"**

### Step 3: Create OAuth 2.0 Credentials

1. Go to **"APIs & Services" → "Credentials"**
2. Click **"Create Credentials" → "OAuth client ID"**
3. Configure consent screen first if prompted:
   - User Type: **External**
   - App name: `Math Video Automation`
   - Support email: Your email
   - Scopes: Add `../auth/youtube.upload`
   - Test users: Add your email
4. Create OAuth client ID:
   - Application type: **Web application**
   - Name: `n8n YouTube Upload`
   - Authorized redirect URIs:
     ```
     http://localhost:5678/rest/oauth2-credential/callback
     ```
5. Click **"Create"**
6. **SAVE** the Client ID and Client Secret!

### Step 4: Configure OAuth Consent Screen

1. Go to **"OAuth consent screen"**
2. Add your YouTube channel email to **Test users**
3. Status should be: **Testing** (100 users max, no review needed)

---

## 🔧 Part 3: Configure n8n Workflow

### Step 1: Import Workflow

1. In n8n interface, click **"+" → "Import from File"**
2. Select: `n8n_workflow.json`
3. Click **"Import"**

### Step 2: Setup YouTube Credentials

1. Click on **"Upload to YouTube"** node
2. Click **"Create New Credential"**
3. Enter:
   - **Client ID**: (from Google Cloud Console)
   - **Client Secret**: (from Google Cloud Console)
4. Click **"Connect my account"**
5. Authorize with your YouTube account
6. Select your channel

### Step 3: Configure Cron Schedule

Click on **"Every 6 Hours"** node to adjust:

**Options:**
- Every 6 hours (default)
- Every 4 hours
- Twice daily (8am, 8pm)
- Custom schedule

**Example custom schedules:**
```
Every 4 hours: hoursInterval = 4
Every 8 hours: hoursInterval = 8
Daily at 9am: specificTime = 09:00
```

### Step 4: Test the Workflow

1. Click **"Execute Workflow"** (play button)
2. Watch the execution:
   - ✅ Cron triggers
   - ✅ Calls Python server
   - ✅ Generates video
   - ✅ Reads video file
   - ✅ Uploads to YouTube

---

## 🐍 Part 4: Start Python Server

### Step 1: Ensure Dependencies Installed

```powershell
pip install fastapi uvicorn wikipedia-api pyttsx3 manim moviepy requests Pillow
```

### Step 2: Start the Server

```powershell
python server.py
```

**Expected output:**
```
INFO:     Started server process
INFO:     Uvicorn running on http://0.0.0.0:8000
INFO:     Application startup complete
```

**Keep this terminal running!**

### Step 3: Test the Endpoint

In another terminal:
```powershell
Invoke-RestMethod -Uri http://127.0.0.1:8000/run-animation -Method POST
```

**Expected response:**
```json
{
  "status": "success",
  "topic": "Fibonacci sequence",
  "video_path": "C:\\Users\\...\\output\\final_Fibonacci_sequence.mp4",
  "youtube_title": "Fibonacci sequence Explained! 🔢 #Shorts",
  "youtube_description": "Learn about...",
  "youtube_tags": "math,fibonacci,shorts..."
}
```

---

## 🎬 Part 5: Complete System Workflow

### Automatic Pipeline:

```
┌──────────────┐
│  n8n Cron    │ ← Every 6 hours
│  Triggers    │
└──────┬───────┘
       │
       ▼
┌──────────────┐
│   HTTP POST  │ → http://host.docker.internal:8000/run-animation
│   Request    │
└──────┬───────┘
       │
       ▼
┌──────────────┐
│ Python       │ → 7-Step Pipeline:
│ FastAPI      │   1. Pick math topic
│ Server       │   2. Generate AI script (Ollama)
│              │   3. Analyze entities
│              │   4. Download images
│              │   5. Generate TTS audio
│              │   6. Render dynamic animation
│              │   7. Combine video + audio
└──────┬───────┘
       │
       ▼
┌──────────────┐
│  Returns     │ → video_path, youtube_title, etc.
│  JSON        │
└──────┬───────┘
       │
       ▼
┌──────────────┐
│  Read Video  │ → Load video file as binary
│  File        │
└──────┬───────┘
       │
       ▼
┌──────────────┐
│  Upload to   │ → YouTube Data API v3
│  YouTube     │
└──────┬───────┘
       │
       ▼
┌──────────────┐
│  ✅ Video    │ → Public/Unlisted/Private
│  Published!  │
└──────────────┘
```

---

## 📊 Part 6: Monitoring & Management

### Check n8n Executions

1. Go to **"Executions"** tab in n8n
2. View:
   - ✅ Success count
   - ❌ Failed executions
   - ⏱️ Execution times
   - 📊 Data flow

### Check Python Logs

Watch the Python terminal for:
```
INFO - Starting YouTube Shorts generation pipeline...
INFO - Step 1/7: Generating popular math topic...
INFO - Step 2/7: Generating AI-powered script...
...
INFO - ✅ PIPELINE COMPLETED in 75.3 seconds
INFO - 📹 Final video: output\final_[topic].mp4
```

### Check YouTube Studio

1. Go to [YouTube Studio](https://studio.youtube.com/)
2. Navigate to **"Content"**
3. Your videos appear as **Shorts** automatically!

---

## ⚙️ Configuration Options

### Change Upload Frequency

Edit `n8n_workflow.json` → **"Every 6 Hours"** node:
```json
"hoursInterval": 4  // Every 4 hours
```

### Change Video Privacy

Edit `n8n_workflow.json` → **"Upload to YouTube"** node:
```json
"privacyStatus": "unlisted"  // Options: public, unlisted, private
```

### Change Video Category

Edit `n8n_workflow.json` → **"Upload to YouTube"** node:
```json
"categoryId": "27"  // 27 = Education
```

**Other categories:**
- 28 = Science & Technology
- 24 = Entertainment
- 10 = Music

### Customize YouTube Metadata

Edit `server.py` around line 203:
```python
youtube_title = f"{topic} Explained! 🔢 #Shorts"
youtube_description = f"Your custom description..."
youtube_tags = "your,custom,tags"
```

---

## 🐛 Troubleshooting

### Issue: n8n can't reach Python server

**Solution:**
```powershell
# In workflow, use:
http://host.docker.internal:8000/run-animation

# NOT localhost:8000 (won't work from container)
```

### Issue: YouTube upload fails - 403 error

**Solution:**
1. Check OAuth consent screen has your email in **Test users**
2. Verify YouTube Data API v3 is **enabled**
3. Reconnect YouTube credentials in n8n

### Issue: Video file not found

**Solution:**
```powershell
# Check docker-compose.yml has:
volumes:
  - ./output:/output

# Verify video path is absolute in server response
```

### Issue: Quota exceeded

**YouTube API limits:**
- Daily quota: 10,000 units
- Each upload: ~1,600 units
- Max uploads per day: ~6 videos

**Solution:** Reduce upload frequency or request quota increase.

### Issue: Docker container can't start

**Solution:**
```powershell
# Stop and remove
docker-compose down

# Clean restart
docker-compose up -d

# Check logs
docker logs n8n_math_automation
```

---

## 📈 Scaling & Optimization

### Increase Production Capacity

1. **Multiple topics per run:**
   ```python
   # server.py - add batch endpoint
   @app.post("/run-batch")
   async def run_batch(count: int = 5):
       # Generate 5 videos in sequence
   ```

2. **Parallel processing:**
   - Run multiple Python servers on different ports
   - Create multiple n8n workflows

3. **Cloud deployment:**
   - Deploy n8n to cloud (Railway, Render, DigitalOcean)
   - Deploy Python to cloud (AWS EC2, GCP)
   - Use cloud storage for videos

### Optimize Video Quality

Edit Manim render command in `server.py`:
```python
# Higher quality (slower):
["manim", "-qk", "--format=mp4", "--fps=60", ...]  # 4K quality

# Faster (lower quality):
["manim", "-ql", "--format=mp4", "--fps=30", ...]  # Low quality
```

---

## 🎯 Production Checklist

Before going live:

- [ ] Changed n8n admin password in `docker-compose.yml`
- [ ] YouTube API quota sufficient for upload frequency
- [ ] OAuth consent screen approved (optional, for >100 users)
- [ ] Python server set to auto-restart on crash
- [ ] Docker set to restart on system boot
- [ ] Backup `output/` folder regularly
- [ ] Monitor YouTube community guidelines compliance
- [ ] Test full pipeline end-to-end at least 3 times
- [ ] Set up error notifications (email/Slack/Discord)

---

## 🚀 Quick Start Commands

### Start Everything:
```powershell
# Terminal 1: Start n8n
docker-compose up -d

# Terminal 2: Start Python server
python server.py

# Browser: Access n8n
# http://localhost:5678
```

### Stop Everything:
```powershell
# Stop Python server: Ctrl+C in terminal

# Stop n8n
docker-compose down
```

### Restart After Changes:
```powershell
# Restart n8n
docker-compose restart

# Restart Python server: Ctrl+C then python server.py
```

---

## 📚 Additional Resources

### Documentation:
- [n8n Documentation](https://docs.n8n.io/)
- [YouTube Data API](https://developers.google.com/youtube/v3)
- [FastAPI Docs](https://fastapi.tiangolo.com/)
- [Manim Documentation](https://docs.manim.community/)

### Your System:
- Python server: `http://localhost:8000`
- n8n interface: `http://localhost:5678`
- API docs: `http://localhost:8000/docs`

---

## 🎉 Success!

Your automated system is now:
✅ Generating math videos every 6 hours  
✅ Uploading directly to YouTube  
✅ Running 24/7 without intervention  
✅ Creating engaging AI-powered content  

**Sit back and watch your channel grow!** 📈

---

## 💡 Pro Tips

1. **Content strategy:** Focus on trending math topics for better engagement
2. **Timing:** Schedule uploads for peak hours (check YouTube Analytics)
3. **Thumbnails:** Auto-generated, but custom thumbnails perform 3x better
4. **Engagement:** Respond to comments to boost algorithm ranking
5. **Series:** Create themed weeks (Fibonacci Week, Geometry Week, etc.)
6. **Analytics:** Monitor which topics perform best, adjust accordingly

**Happy automating!** 🚀
