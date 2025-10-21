"""
Script: server.py
Purpose: FastAPI server that orchestrates the entire STEM video generation pipeline
Endpoint: POST /run-animation - Triggers the full automation workflow
Server: Runs on http://127.0.0.1:8000
"""

from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
import subprocess
import uvicorn
import os
import logging
import json
from pathlib import Path
from datetime import datetime

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('automation.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="STEM Video Automation API",
    description="Automated STEM video generation system with TTS and Manim animations",
    version="1.0.0"
)

@app.get("/")
def read_root():
    """
    Health check endpoint
    """
    return {
        "status": "online",
        "service": "STEM Video Automation",
        "version": "1.0.0",
        "endpoints": {
            "health": "/",
            "run_animation": "/run-animation (POST)",
            "status": "/status"
        }
    }

@app.get("/status")
def get_status():
    """
    Returns the status of the output directory and last generated video
    """
    try:
        output_dir = Path("output")
        if not output_dir.exists():
            return {"status": "No videos generated yet"}
        
        # Get all final videos
        videos = list(output_dir.glob("final_*.mp4"))
        
        if not videos:
            return {"status": "No final videos found", "files_in_output": len(list(output_dir.iterdir()))}
        
        # Get most recent video
        latest_video = max(videos, key=lambda p: p.stat().st_mtime)
        file_size = latest_video.stat().st_size / (1024 * 1024)  # MB
        modified_time = datetime.fromtimestamp(latest_video.stat().st_mtime)
        
        return {
            "status": "operational",
            "total_videos": len(videos),
            "latest_video": latest_video.name,
            "size_mb": round(file_size, 2),
            "last_generated": modified_time.strftime("%Y-%m-%d %H:%M:%S")
        }
    except Exception as e:
        logger.error(f"Error getting status: {str(e)}")
        return {"status": "error", "detail": str(e)}

@app.post("/run-animation")
def run_animation():
    """
    Main endpoint that triggers the INTELLIGENT YouTube Shorts generation pipeline:
    1. Generate popular math topic
    2. Generate educational script with hooks & CTAs
    3. Analyze script for entities (countries, people, formulas)
    4. Download Wikipedia images (flags, portraits, etc.)
    5. Convert script to TTS audio
    6. Render DYNAMIC vertical Manim animation (1080x1920) with content-aware visuals
    7. Combine video and audio into final YouTube Short
    
    Returns: JSON with status, topic, and final video path
    """
    start_time = datetime.now()
    logger.info("=" * 80)
    logger.info("🚀 Starting STEM video generation pipeline...")
    logger.info("=" * 80)
    
    try:
        # Ensure output directory exists
        output_dir = Path("output")
        output_dir.mkdir(exist_ok=True)
        
        # Step 1: Generate math topic
        logger.info("Step 1/5: Generating popular math topic...")
        result = subprocess.run(
            ["python", "scripts/generate_prompt.py"],
            check=True,
            capture_output=True,
            text=True
        )
        logger.info("✅ Topic generated successfully")
        
        # Load topic info
        with open("output/topic.json", "r", encoding="utf-8") as f:
            topic_data = json.load(f)
        topic = topic_data.get("topic", "Unknown")
        category = topic_data.get("category", "Unknown")
        logger.info(f"Topic: {topic} (Category: {category})")

        # Step 2: Generate AI-powered script using Ollama
        logger.info("Step 2/7: Generating AI script with Ollama...")
        result = subprocess.run(
            ["python", "scripts/generate_script_ollama.py"],
            check=True,
            capture_output=True,
            text=True
        )
        logger.info("✅ AI script generated successfully")

        # Step 3: Analyze script for entities (countries, people, formulas)
        logger.info("Step 3/7: Analyzing script for entities (countries, people, formulas)...")
        result = subprocess.run(
            ["python", "scripts/analyze_script.py"],
            check=True,
            capture_output=True,
            text=True
        )
        logger.info("✅ Script analysis completed")

        # Step 4: Download Wikipedia images
        logger.info("Step 4/7: Downloading Wikipedia images...")
        result = subprocess.run(
            ["python", "scripts/download_images.py"],
            check=True,
            capture_output=True,
            text=True
        )
        logger.info("✅ Images downloaded")

        # Step 5: Generate TTS audio from script
        logger.info("Step 5/7: Generating TTS audio from structured script...")
        result = subprocess.run(
            ["python", "scripts/generate_audio.py"],
            check=True,
            capture_output=True,
            text=True
        )
        logger.info("✅ Audio generated successfully")

        # Step 6: Render DYNAMIC YouTube Shorts animation (vertical 1080x1920, 60fps)
        logger.info("Step 6/7: Rendering DYNAMIC YouTube Shorts animation (vertical 1080x1920, 60fps)...")
        logger.info("This will create intelligent, content-aware animations...")
        result = subprocess.run(
            ["manim", "-qh", "--format=mp4", "--fps=60", "--resolution", "1080,1920", "scripts\\render_manim_dynamic.py", "STEMScene"],
            check=True,
            capture_output=True,
            text=True,
            cwd=os.getcwd()
        )
        logger.info("✅ YouTube Shorts animation rendered successfully")

        # Step 7: Combine video + audio
        logger.info("Step 7/7: Combining video and audio...")
        result = subprocess.run(
            ["python", "scripts/combine_video.py"],
            check=True,
            capture_output=True,
            text=True
        )
        logger.info("✅ Final video created successfully")
        
        # Get final video path
        final_videos = list(output_dir.glob("final_*.mp4"))
        if final_videos:
            latest_video = max(final_videos, key=lambda p: p.stat().st_mtime)
            video_path = str(latest_video.absolute())  # Absolute path for n8n
            file_size = latest_video.stat().st_size / (1024 * 1024)  # MB
        else:
            video_path = "Not found"
            file_size = 0
        
        # Calculate total time
        end_time = datetime.now()
        duration = (end_time - start_time).total_seconds()
        
        logger.info("=" * 80)
        logger.info(f"✅ PIPELINE COMPLETED SUCCESSFULLY in {duration:.1f} seconds")
        logger.info(f"📹 Final video: {video_path}")
        logger.info(f"📊 File size: {file_size:.2f} MB")
        logger.info("=" * 80)
        
        # Prepare YouTube metadata
        youtube_title = f"{topic} Explained! 🔢 #Shorts"
        youtube_description = f"""Learn about {topic} in 30 seconds!

📚 {category}
🎓 Perfect for quick math learning
💡 Subscribe for daily math shorts!

#Shorts #Mathematics #Math #STEM #Education #{topic.replace(' ', '')}"""
        
        youtube_tags = f"math,mathematics,{topic.lower()},education,shorts,stem,quick learning,{category.lower()}"
        
        return JSONResponse(
            status_code=200,
            content={
                "status": "success",
                "message": "Video created successfully",
                "topic": topic,
                "category": category,
                "video_path": video_path,
                "file_size_mb": round(file_size, 2),
                "duration_seconds": round(duration, 1),
                # YouTube metadata for n8n
                "youtube_title": youtube_title,
                "youtube_description": youtube_description,
                "youtube_tags": youtube_tags,
                "timestamp": end_time.strftime("%Y-%m-%d %H:%M:%S")
            }
        )
        
    except subprocess.CalledProcessError as e:
        logger.error(f"❌ Pipeline failed at subprocess: {str(e)}")
        logger.error(f"Command output: {e.output if hasattr(e, 'output') else 'N/A'}")
        logger.error(f"Command stderr: {e.stderr if hasattr(e, 'stderr') else 'N/A'}")
        
        raise HTTPException(
            status_code=500,
            detail={
                "status": "error",
                "message": "Pipeline execution failed",
                "error": str(e),
                "step": "See logs for details"
            }
        )
    
    except Exception as e:
        logger.error(f"❌ Unexpected error: {str(e)}")
        
        raise HTTPException(
            status_code=500,
            detail={
                "status": "error",
                "message": "Unexpected error occurred",
                "error": str(e)
            }
        )

@app.post("/auto-generate-videos")
async def auto_generate_videos_endpoint(
    count: int = 10,
    topic: str = "mathematics",
    backend: str = "manim",
    enhance_scripts: bool = True
):
    """
    FULLY AUTONOMOUS video generation endpoint
    Uses Ollama to generate prompts AND scripts, then creates videos
    
    Args:
        count: Number of videos to generate
        topic: Topic area (e.g., "mathematics", "geometry")
        backend: Video backend (svd, text2video, manim)
        enhance_scripts: Generate detailed scripts with Ollama
    
    Returns:
        JSON with generation results
    """
    import subprocess
    from pathlib import Path
    
    logger.info("\n" + "="*60)
    logger.info("🤖 AUTONOMOUS VIDEO GENERATION STARTED")
    logger.info("="*60)
    logger.info(f"📊 Count: {count} videos")
    logger.info(f"📚 Topic: {topic}")
    logger.info(f"🎨 Backend: {backend}")
    logger.info(f"✨ Enhanced scripts: {enhance_scripts}")
    logger.info("="*60 + "\n")
    
    try:
        # Run autonomous pipeline script
        cmd = [
            sys.executable,
            "scripts/auto_generate_pipeline.py",
            "--count", str(count),
            "--topic", topic,
            "--backend", backend
        ]
        
        if not enhance_scripts:
            cmd.append("--no-enhance")
        
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=3600  # 1 hour timeout
        )
        
        # Read results
        results_file = Path("output/bulk_videos/generation_results.json")
        if results_file.exists():
            import json
            with open(results_file) as f:
                results = json.load(f)
            
            return JSONResponse(
                status_code=200,
                content={
                    "status": "success",
                    "message": "Autonomous generation completed",
                    "mode": "autonomous_ai",
                    "total_videos": results['total'],
                    "successful": results['success'],
                    "failed": results['failed'],
                    "videos": results['videos'],
                    "output_directory": str(Path("output/bulk_videos").absolute()),
                    "prompts_file": str(Path("prompts.csv").absolute()),
                    "results_file": str(results_file.absolute()),
                    "ollama_used": True
                }
            )
        else:
            return JSONResponse(
                status_code=500,
                content={
                    "status": "error",
                    "message": "Generation completed but no results file found",
                    "output": result.stdout,
                    "error": result.stderr
                }
            )
    
    except subprocess.TimeoutExpired:
        return JSONResponse(
            status_code=408,
            content={
                "status": "timeout",
                "message": "Generation timed out (>1 hour)"
            }
        )
    except Exception as e:
        logger.error(f"❌ Error in autonomous generation: {e}")
        import traceback
        traceback.print_exc()
        
        return JSONResponse(
            status_code=500,
            content={
                "status": "error",
                "message": str(e),
                "traceback": traceback.format_exc()
            }
        )


@app.post("/generate-bulk-videos")
async def generate_bulk_videos_endpoint(
    csv_path: str = "prompts.csv",
    backend: str = "manim",
    duration: int = 5
):
    """
    Bulk video generation endpoint for n8n workflow
    Uses existing CSV file with prompts
    
    Args:
        csv_path: Path to CSV with prompts (default: prompts.csv)
        backend: Video backend (svd, text2video, manim)
        duration: Video duration in seconds
    
    Returns:
        JSON with generation results and video paths
    """
    import sys
    from pathlib import Path
    
    logger.info("\n" + "="*60)
    logger.info("🎬 BULK VIDEO GENERATION STARTED")
    logger.info("="*60)
    logger.info(f"📋 CSV: {csv_path}")
    logger.info(f"🎨 Backend: {backend}")
    logger.info(f"⏱️  Duration: {duration}s")
    logger.info("="*60 + "\n")
    
    try:
        # Import the bulk generation function
        sys.path.append(str(Path(__file__).parent / "scripts"))
        from generate_bulk_videos import generate_bulk_videos
        
        # Run bulk generation
        results = generate_bulk_videos(
            csv_path=csv_path,
            backend=backend,
            output_dir="output/bulk_videos",
            duration=duration
        )
        
        if results:
            # Prepare response for n8n
            return JSONResponse(
                status_code=200,
                content={
                    "status": "success",
                    "message": "Bulk video generation completed",
                    "backend": backend,
                    "total_videos": results['total'],
                    "successful": results['success'],
                    "failed": results['failed'],
                    "videos": results['videos'],
                    "output_directory": str(Path("output/bulk_videos").absolute()),
                    "results_file": str(Path("output/bulk_videos/generation_results.json").absolute())
                }
            )
        else:
            return JSONResponse(
                status_code=500,
                content={
                    "status": "error",
                    "message": "No videos generated",
                    "error": "Check CSV file and prompts"
                }
            )
        
    except Exception as e:
        logger.error(f"❌ Error in bulk generation: {e}")
        import traceback
        traceback.print_exc()
        
        return JSONResponse(
            status_code=500,
            content={
                "status": "error",
                "message": str(e),
                "traceback": traceback.format_exc()
            }
        )


if __name__ == "__main__":
    # Create output directory on startup
    os.makedirs("output", exist_ok=True)
    os.makedirs("output/bulk_videos", exist_ok=True)
    
    logger.info("=" * 80)
    logger.info("🎬 STEM Video Automation Server Starting...")
    logger.info("=" * 80)
    logger.info("Server: http://127.0.0.1:8000")
    logger.info("Docs: http://127.0.0.1:8000/docs")
    logger.info("Health Check: http://127.0.0.1:8000/")
    logger.info("Run Animation: POST http://127.0.0.1:8000/run-animation")
    logger.info("Bulk Videos: POST http://127.0.0.1:8000/generate-bulk-videos")
    logger.info("🤖 AUTONOMOUS: POST http://127.0.0.1:8000/auto-generate-videos")
    logger.info("=" * 80)
    
    # Run the server
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8000,
        log_level="info"
    )
