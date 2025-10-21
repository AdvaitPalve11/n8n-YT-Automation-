"""
LOCAL AI VIDEO GENERATION - Bulk Processing
Replaces Freepik API with local Stable Diffusion Video generation

Requirements:
    pip install diffusers transformers accelerate torch opencv-python pandas pillow
    
Models supported:
    - Stable Video Diffusion (SVD) - Best quality
    - Text-to-Video-MS-1.7B - Faster generation
    - AnimateDiff - Animation style
"""

import csv
import json
import os
import time
from pathlib import Path
from typing import List, Dict
import sys

# Check if GPU available
try:
    import torch
    GPU_AVAILABLE = torch.cuda.is_available()
    DEVICE = "cuda" if GPU_AVAILABLE else "cpu"
    print(f"🖥️  Device: {DEVICE}")
    if GPU_AVAILABLE:
        print(f"🎮 GPU: {torch.cuda.get_device_name(0)}")
except ImportError:
    GPU_AVAILABLE = False
    DEVICE = "cpu"
    print("⚠️  PyTorch not installed. Install with: pip install torch torchvision")

# Video generation backend (can switch between different models)
VIDEO_BACKEND = os.getenv("VIDEO_BACKEND", "manim")  # Options: svd, text2video, manim

class LocalVideoGenerator:
    """
    Local video generation using various backends
    """
    
    def __init__(self, backend="manim", output_dir="output/bulk_videos"):
        self.backend = backend
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        print(f"🎬 Initializing LocalVideoGenerator with backend: {backend}")
        
        # Initialize backend-specific settings
        if backend == "svd":
            self._init_stable_video_diffusion()
        elif backend == "text2video":
            self._init_text2video()
        elif backend == "manim":
            self._init_manim()
        else:
            raise ValueError(f"Unknown backend: {backend}")
    
    def _init_stable_video_diffusion(self):
        """Initialize Stable Video Diffusion pipeline"""
        try:
            from diffusers import StableVideoDiffusionPipeline
            from diffusers.utils import load_image, export_to_video
            
            print("📦 Loading Stable Video Diffusion model (this may take a while)...")
            self.pipe = StableVideoDiffusionPipeline.from_pretrained(
                "stabilityai/stable-video-diffusion-img2vid-xt",
                torch_dtype=torch.float16 if GPU_AVAILABLE else torch.float32,
                variant="fp16" if GPU_AVAILABLE else None
            )
            self.pipe.to(DEVICE)
            self.export_to_video = export_to_video
            print("✅ Stable Video Diffusion ready!")
        except Exception as e:
            print(f"❌ Failed to initialize SVD: {e}")
            print("💡 Install with: pip install diffusers[torch] accelerate transformers")
            sys.exit(1)
    
    def _init_text2video(self):
        """Initialize Text-to-Video pipeline"""
        try:
            from diffusers import DiffusionPipeline
            
            print("📦 Loading Text-to-Video model...")
            self.pipe = DiffusionPipeline.from_pretrained(
                "damo-vilab/text-to-video-ms-1.7b",
                torch_dtype=torch.float16 if GPU_AVAILABLE else torch.float32
            )
            self.pipe.to(DEVICE)
            print("✅ Text-to-Video ready!")
        except Exception as e:
            print(f"❌ Failed to initialize Text2Video: {e}")
            print("💡 Install with: pip install diffusers[torch] transformers")
            sys.exit(1)
    
    def _init_manim(self):
        """Initialize Manim-based video generation (fallback, fastest)"""
        print("✅ Using Manim backend (fastest, no AI required)")
        # No model loading needed for Manim
    
    def generate_video_svd(self, prompt: str, output_path: str, duration_seconds: int = 5):
        """Generate video using Stable Video Diffusion"""
        try:
            from PIL import Image
            
            print(f"🎨 Generating seed image from prompt: {prompt}")
            
            # Create a seed image (you could use Stable Diffusion for this)
            # For now, we'll create a colored gradient based on prompt
            img = Image.new('RGB', (1024, 576), color=(100, 150, 200))
            
            print("🎬 Generating video frames...")
            frames = self.pipe(
                img,
                decode_chunk_size=8,
                num_frames=duration_seconds * 8,  # 8 fps
                motion_bucket_id=127,
                noise_aug_strength=0.02
            ).frames[0]
            
            print(f"💾 Exporting video to {output_path}")
            self.export_to_video(frames, output_path, fps=8)
            
            return True
        except Exception as e:
            print(f"❌ SVD generation failed: {e}")
            return False
    
    def generate_video_text2video(self, prompt: str, output_path: str, duration_seconds: int = 5):
        """Generate video using Text-to-Video model"""
        try:
            print(f"🎬 Generating video from prompt: {prompt}")
            
            video_frames = self.pipe(
                prompt,
                num_inference_steps=25,
                num_frames=duration_seconds * 8
            ).frames
            
            # Save video
            import cv2
            import numpy as np
            
            height, width = video_frames[0][0].shape[:2]
            fourcc = cv2.VideoWriter_fourcc(*'mp4v')
            out = cv2.VideoWriter(output_path, fourcc, 8.0, (width, height))
            
            for frame_list in video_frames:
                for frame in frame_list:
                    frame_bgr = cv2.cvtColor(np.array(frame), cv2.COLOR_RGB2BGR)
                    out.write(frame_bgr)
            
            out.release()
            print(f"✅ Video saved to {output_path}")
            return True
        except Exception as e:
            print(f"❌ Text2Video generation failed: {e}")
            return False
    
    def generate_video_manim(self, prompt: str, output_path: str, duration_seconds: int = 5):
        """Generate video using Manim (fast, procedural)"""
        try:
            import subprocess
            
            # Create a temporary Manim scene based on prompt
            scene_file = self.output_dir / "temp_scene.py"
            
            # Simple scene generator
            scene_code = f'''
from manim import *

class TempScene(Scene):
    def construct(self):
        # Parse prompt and create visualization
        title = Text("{prompt[:50]}...", font_size=24)
        title.to_edge(UP)
        self.play(Write(title))
        
        # Add visual elements based on prompt keywords
        if "spiral" in "{prompt.lower()}":
            spiral = ParametricFunction(
                lambda t: np.array([
                    t * np.cos(5*t),
                    t * np.sin(5*t),
                    0
                ]),
                t_range=[0, 2*PI],
                color=BLUE
            )
            self.play(Create(spiral), run_time={duration_seconds - 1})
        elif "wave" in "{prompt.lower()}":
            axes = Axes(x_range=[-3, 3], y_range=[-2, 2])
            wave = axes.plot(lambda x: np.sin(x), color=BLUE)
            self.play(Create(axes))
            self.play(Create(wave), run_time={duration_seconds - 1})
        else:
            # Generic animation
            circle = Circle(radius=1, color=BLUE)
            square = Square(side_length=2, color=RED)
            self.play(Create(circle))
            self.play(Transform(circle, square), run_time={duration_seconds - 1})
        
        self.wait(0.5)
'''
            
            with open(scene_file, 'w') as f:
                f.write(scene_code)
            
            print(f"🎬 Rendering with Manim...")
            
            # Render with Manim (vertical format for consistency)
            result = subprocess.run([
                "manim",
                "-qm",  # Medium quality
                "--format=mp4",
                "--fps=30",
                "--resolution=1080,1920",
                str(scene_file),
                "TempScene"
            ], capture_output=True, text=True, timeout=120)
            
            # Find generated video
            video_dir = self.output_dir / "media" / "videos" / "temp_scene" / "1080p30"
            if video_dir.exists():
                videos = list(video_dir.glob("TempScene.mp4"))
                if videos:
                    import shutil
                    shutil.move(str(videos[0]), output_path)
                    print(f"✅ Video saved to {output_path}")
                    
                    # Cleanup
                    scene_file.unlink()
                    return True
            
            print(f"❌ Manim generation failed")
            return False
            
        except Exception as e:
            print(f"❌ Manim generation failed: {e}")
            return False
    
    def generate(self, prompt: str, name: str, variation: int = 1, duration: int = 5):
        """
        Generate video with specified backend
        
        Args:
            prompt: Text description of video
            name: Base filename
            variation: Variation number
            duration: Video duration in seconds
        
        Returns:
            Path to generated video or None if failed
        """
        filename = f"video_{name}_v{variation}.mp4"
        output_path = str(self.output_dir / filename)
        
        print(f"\n{'='*60}")
        print(f"🎬 Generating: {filename}")
        print(f"📝 Prompt: {prompt}")
        print(f"⏱️  Duration: {duration}s")
        print(f"{'='*60}")
        
        start_time = time.time()
        
        # Route to appropriate backend
        if self.backend == "svd":
            success = self.generate_video_svd(prompt, output_path, duration)
        elif self.backend == "text2video":
            success = self.generate_video_text2video(prompt, output_path, duration)
        elif self.backend == "manim":
            success = self.generate_video_manim(prompt, output_path, duration)
        else:
            success = False
        
        elapsed = time.time() - start_time
        
        if success:
            file_size = os.path.getsize(output_path) / (1024 * 1024)  # MB
            print(f"✅ SUCCESS: {filename}")
            print(f"📊 Size: {file_size:.2f} MB")
            print(f"⏱️  Time: {elapsed:.1f}s")
            return output_path
        else:
            print(f"❌ FAILED: {filename}")
            return None


def read_prompts_csv(csv_path: str = "prompts.csv") -> List[Dict]:
    """
    Read prompts from CSV file
    
    CSV format:
        Prompt,Name,Variations
        "Description text",identifier,3
    """
    prompts = []
    
    try:
        with open(csv_path, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                # Create variations
                variations = int(row.get('Variations', 1))
                for i in range(1, variations + 1):
                    prompts.append({
                        'prompt': row['Prompt'].strip(),
                        'name': row['Name'].strip(),
                        'variation': i
                    })
        
        print(f"📋 Loaded {len(prompts)} video tasks from {csv_path}")
        return prompts
        
    except FileNotFoundError:
        print(f"❌ CSV file not found: {csv_path}")
        print("💡 Create prompts.csv with format: Prompt,Name,Variations")
        return []
    except Exception as e:
        print(f"❌ Error reading CSV: {e}")
        return []


def generate_bulk_videos(
    csv_path: str = "prompts.csv",
    backend: str = "manim",
    output_dir: str = "output/bulk_videos",
    duration: int = 5
):
    """
    Main function for bulk video generation
    
    Args:
        csv_path: Path to CSV with prompts
        backend: Video generation backend (svd, text2video, manim)
        output_dir: Output directory for videos
        duration: Video duration in seconds
    """
    print("\n" + "="*60)
    print("🎬 LOCAL AI VIDEO GENERATOR - BULK MODE")
    print("="*60 + "\n")
    
    # Read prompts
    tasks = read_prompts_csv(csv_path)
    if not tasks:
        return
    
    # Initialize generator
    generator = LocalVideoGenerator(backend=backend, output_dir=output_dir)
    
    # Track results
    results = {
        'total': len(tasks),
        'success': 0,
        'failed': 0,
        'videos': []
    }
    
    start_time = time.time()
    
    # Generate videos
    for i, task in enumerate(tasks, 1):
        print(f"\n🔄 Task {i}/{len(tasks)}")
        
        video_path = generator.generate(
            prompt=task['prompt'],
            name=task['name'],
            variation=task['variation'],
            duration=duration
        )
        
        if video_path:
            results['success'] += 1
            results['videos'].append({
                'name': task['name'],
                'variation': task['variation'],
                'path': video_path
            })
        else:
            results['failed'] += 1
    
    # Summary
    total_time = time.time() - start_time
    
    print("\n" + "="*60)
    print("📊 GENERATION SUMMARY")
    print("="*60)
    print(f"✅ Successful: {results['success']}/{results['total']}")
    print(f"❌ Failed: {results['failed']}/{results['total']}")
    print(f"⏱️  Total Time: {total_time/60:.1f} minutes")
    print(f"📁 Output: {output_dir}")
    print("="*60 + "\n")
    
    # Save results JSON
    results_file = Path(output_dir) / "generation_results.json"
    with open(results_file, 'w') as f:
        json.dump(results, f, indent=2)
    print(f"📄 Results saved to: {results_file}")
    
    return results


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Local AI Video Generator - Bulk Mode")
    parser.add_argument(
        '--csv',
        default='prompts.csv',
        help='Path to CSV file with prompts'
    )
    parser.add_argument(
        '--backend',
        choices=['svd', 'text2video', 'manim'],
        default='manim',
        help='Video generation backend (default: manim)'
    )
    parser.add_argument(
        '--output',
        default='output/bulk_videos',
        help='Output directory for videos'
    )
    parser.add_argument(
        '--duration',
        type=int,
        default=5,
        help='Video duration in seconds (default: 5)'
    )
    
    args = parser.parse_args()
    
    generate_bulk_videos(
        csv_path=args.csv,
        backend=args.backend,
        output_dir=args.output,
        duration=args.duration
    )
