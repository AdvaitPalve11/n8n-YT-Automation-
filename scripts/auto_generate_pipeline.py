"""
AUTONOMOUS VIDEO GENERATION PIPELINE
Uses AI to generate prompts, scripts, AND videos automatically

Steps:
1. AI generates creative video prompts (Qwen3-4B)
2. AI writes engaging scripts
3. Manim generates videos
4. Everything saved and ready

Usage:
    python scripts/auto_generate_pipeline.py --count 10
"""

import subprocess
import sys
import time
from pathlib import Path

def run_command(cmd: list, description: str):
    """Run a command and handle errors"""
    print(f"\n{'='*60}")
    print(f"🔄 {description}")
    print(f"{'='*60}")
    print(f"Command: {' '.join(cmd)}\n")
    
    try:
        result = subprocess.run(
            cmd,
            check=True,
            capture_output=True,
            text=True
        )
        print(result.stdout)
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Error: {e}")
        print(f"Output: {e.stdout}")
        print(f"Error: {e.stderr}")
        return False


def autonomous_generation(
    video_count: int = 10,
    topic: str = "mathematics",
    backend: str = "manim",
    enhance_scripts: bool = True
):
    """
    Fully autonomous video generation pipeline
    """
    
    print("\n" + "="*70)
    print("🤖 AUTONOMOUS VIDEO GENERATION PIPELINE")
    print("="*70)
    print(f"📊 Videos to generate: {video_count}")
    print(f"📚 Topic: {topic}")
    print(f"🎨 Backend: {backend}")
    print(f"✨ Enhanced scripts: {enhance_scripts}")
    print("="*70 + "\n")
    
    start_time = time.time()
    
    # Step 1: Generate prompts with AI (Qwen3-4B)
    print("\n🎯 STEP 1: AI PROMPT GENERATION")
    print("-" * 70)
    
    cmd = [
        sys.executable,
        "scripts/generate_prompts_hf.py",
        "--count", str(video_count),
        "--topic", topic,
        "--output", "prompts.csv"
    ]
    
    if enhance_scripts:
        cmd.append("--enhance")
    
    if not run_command(cmd, "Generating prompts with AI (Qwen3-4B)"):
        print("❌ AI prompt generation failed. Aborting.")
        return False
    
    print("\n✅ Prompts generated successfully!")
    
    # Small delay
    time.sleep(2)
    
    # Step 2: Generate videos from prompts
    print("\n🎬 STEP 2: VIDEO GENERATION")
    print("-" * 70)
    
    cmd = [
        sys.executable,
        "scripts/generate_bulk_videos.py",
        "--csv", "prompts.csv",
        "--backend", backend,
        "--output", "output/bulk_videos",
        "--duration", "5"
    ]
    
    if not run_command(cmd, f"Generating {video_count} videos with {backend}"):
        print("⚠️  Video generation encountered errors, but may have partial results.")
    
    # Step 3: Summary
    total_time = time.time() - start_time
    
    print("\n" + "="*70)
    print("🎉 PIPELINE COMPLETE!")
    print("="*70)
    print(f"⏱️  Total Time: {total_time/60:.1f} minutes")
    print(f"📁 Videos: output/bulk_videos/")
    print(f"📋 Prompts: prompts.csv")
    print("="*70)
    
    # Check results
    results_file = Path("output/bulk_videos/generation_results.json")
    if results_file.exists():
        import json
        with open(results_file) as f:
            results = json.load(f)
        
        print(f"\n📈 SUCCESS RATE: {results['success']}/{results['total']} videos")
        
        if results['success'] > 0:
            print(f"\n🎬 Sample videos:")
            for video in results['videos'][:5]:
                print(f"  ✅ {video['name']}_v{video['variation']}.mp4")
            
            if len(results['videos']) > 5:
                print(f"  ... and {len(results['videos']) - 5} more")
    
    print("\n🚀 Ready for upload to YouTube/social media!")
    print("="*70 + "\n")
    
    return True


def main():
    import argparse
    
    parser = argparse.ArgumentParser(
        description="Fully autonomous video generation with Ollama AI"
    )
    parser.add_argument(
        '--count',
        type=int,
        default=10,
        help='Number of videos to generate (default: 10)'
    )
    parser.add_argument(
        '--topic',
        default='mathematics',
        help='Topic area (default: mathematics)'
    )
    parser.add_argument(
        '--backend',
        choices=['manim', 'svd', 'text2video'],
        default='manim',
        help='Video generation backend (default: manim)'
    )
    parser.add_argument(
        '--model',
        default='gemma2:2b',
        help='Ollama model to use (default: gemma2:2b - Google DeepMind)'
    )
    parser.add_argument(
        '--no-enhance',
        action='store_true',
        help='Skip enhanced script generation (faster)'
    )
    
    args = parser.parse_args()
    
    autonomous_generation(
        video_count=args.count,
        topic=args.topic,
        backend=args.backend,
        enhance_scripts=not args.no_enhance
    )


if __name__ == "__main__":
    main()
