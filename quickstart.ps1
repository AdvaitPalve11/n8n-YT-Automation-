# Quick Start Script for STEM Video Automation
# Run this script to test each component

Write-Host "=" -NoNewline -ForegroundColor Cyan
Write-Host ("=" * 79) -ForegroundColor Cyan
Write-Host "🎬 STEM Video Automation - Quick Start" -ForegroundColor Green
Write-Host "=" -NoNewline -ForegroundColor Cyan
Write-Host ("=" * 79) -ForegroundColor Cyan

# Step 1: Check Python
Write-Host "`n📌 Step 1: Checking Python installation..." -ForegroundColor Yellow
python --version

# Step 2: Install dependencies
Write-Host "`n📌 Step 2: Installing dependencies..." -ForegroundColor Yellow
Write-Host "This may take a few minutes..." -ForegroundColor Gray
pip install -r requirements.txt

# Step 3: Test generate_prompt
Write-Host "`n📌 Step 3: Testing topic generation..." -ForegroundColor Yellow
python scripts/generate_prompt.py

# Step 4: Test generate_audio
Write-Host "`n📌 Step 4: Testing audio generation..." -ForegroundColor Yellow
python scripts/generate_audio.py

# Step 5: Test manim
Write-Host "`n📌 Step 5: Testing Manim animation..." -ForegroundColor Yellow
Write-Host "This will take 30-60 seconds..." -ForegroundColor Gray
manim -ql --format=mp4 scripts/render_manim.py STEMScene

# Step 6: Test combine_video
Write-Host "`n📌 Step 6: Testing video combination..." -ForegroundColor Yellow
python scripts/combine_video.py

# Final check
Write-Host "`n" + ("=" * 80) -ForegroundColor Cyan
if (Test-Path "output/final_*.mp4") {
    Write-Host "✅ SUCCESS! Your STEM video has been generated!" -ForegroundColor Green
    Write-Host "`n📹 Check the 'output' folder for your video" -ForegroundColor Green
    
    Get-ChildItem -Path "output" -Filter "final_*.mp4" | ForEach-Object {
        $sizeMB = [math]::Round($_.Length / 1MB, 2)
        Write-Host "   - $($_.Name) ($sizeMB MB)" -ForegroundColor Cyan
    }
    
    Write-Host "`n🚀 Next steps:" -ForegroundColor Yellow
    Write-Host "   1. Start the server: python server.py" -ForegroundColor White
    Write-Host "   2. Test the API: python test_pipeline.py" -ForegroundColor White
    Write-Host "   3. Set up n8n automation (see README.md)" -ForegroundColor White
} else {
    Write-Host "❌ Video generation incomplete" -ForegroundColor Red
    Write-Host "Check the error messages above" -ForegroundColor Red
}
Write-Host ("=" * 80) -ForegroundColor Cyan
