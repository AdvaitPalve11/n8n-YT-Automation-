"""
Script: combine_video.py
Purpose: Combines the Manim animation with TTS audio to create the final video
Input: 
    - media/videos/render_manim/720p30/STEMScene.mp4 (Manim video)
    - output/audio.wav (TTS audio)
    - output/topic.json (for filename)
Output: Creates output/final_[topic_name].mp4
"""

import json
import logging
from pathlib import Path
from moviepy import VideoFileClip, AudioFileClip, concatenate_videoclips
import re

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def sanitize_filename(filename):
    """
    Sanitize filename by removing/replacing invalid characters.
    """
    # Remove invalid characters for Windows filenames
    filename = re.sub(r'[<>:"/\\|?*]', '', filename)
    # Replace spaces with underscores
    filename = filename.replace(' ', '_')
    # Limit length
    filename = filename[:100]
    return filename

def combine_video_audio():
    """
    Combines Manim video with TTS audio and saves the final video.
    Returns: Path to the final video file
    """
    try:
        # File paths for YouTube Shorts vertical format
        video_folder_shorts = r"media\videos\render_manim_shorts\1080p60"  # New vertical format
        video_folder_1080p60 = r"media\videos\render_manim\1080p60"  # Old horizontal format (fallback)
        possible_video_paths = [
            # Dynamic renderer (this project’s default)
            Path("media/videos/render_manim_dynamic/1280p60/DynamicScene.mp4"),
            Path("media/videos/render_manim_dynamic/1280p30/DynamicScene.mp4"),
            Path("media/videos/render_manim_dynamic/1080p60/DynamicScene.mp4"),
            Path("media/videos/render_manim_dynamic/1080p30/DynamicScene.mp4"),
            Path("media/videos/render_manim_dynamic/720p30/DynamicScene.mp4"),
            Path("media/videos/render_manim_dynamic/480p15/DynamicScene.mp4"),
            # Shorts and legacy renderers
            Path("media/videos/render_manim_shorts/1080p60/STEMScene.mp4"),  # YouTube Shorts (vertical)
            Path("media/videos/render_manim/1080p60/STEMScene.mp4"),  # High quality (1080p 60fps)
            Path("media/videos/render_manim/1080p30/STEMScene.mp4"),  # High quality (1080p 30fps)
            Path("media/videos/render_manim/720p30/STEMScene.mp4"),   # Medium quality
            Path("media/videos/render_manim/480p15/STEMScene.mp4"),   # Low quality
        ]
        
        video_file = None
        for path in possible_video_paths:
            if path.exists():
                video_file = path
                break
        
        if not video_file:
            raise FileNotFoundError(f"Manim video not found in any quality folder")
        
        audio_file = Path("output/audio.wav")
        topic_file = Path("output/topic.json")
        output_dir = Path("output")
        
        # Check if input files exist
        if not video_file.exists():
            raise FileNotFoundError(f"Manim video not found: {video_file}")
        if not audio_file.exists():
            raise FileNotFoundError(f"Audio file not found: {audio_file}")
        if not topic_file.exists():
            raise FileNotFoundError(f"Topic file not found: {topic_file}")
        
        # Load topic data for dynamic filename
        logger.info(f"Loading topic data from {topic_file}")
        with open(topic_file, "r", encoding="utf-8") as f:
            data = json.load(f)
        
        topic = data.get("topic", "STEM_Video")
        safe_topic = sanitize_filename(topic)
        
        # Create output filename
        output_file = output_dir / f"final_{safe_topic}.mp4"
        
        logger.info(f"Combining video and audio...")
        logger.info(f"Video: {video_file}")
        logger.info(f"Audio: {audio_file}")
        logger.info(f"Output: {output_file}")
        
        # Load video clip
        logger.info("Loading video clip...")
        video_clip = VideoFileClip(str(video_file))
        video_duration = video_clip.duration
        logger.info(f"Video duration: {video_duration:.2f} seconds")
        
        # Load audio clip
        logger.info("Loading audio clip...")
        audio_clip = AudioFileClip(str(audio_file))
        audio_duration = audio_clip.duration
        logger.info(f"Audio duration: {audio_duration:.2f} seconds")
        
        # Adjust video length to match audio duration
        if video_duration < audio_duration:
            # If video is shorter, loop it
            logger.info("Video is shorter than audio. Looping video...")
            loops_needed = int(audio_duration / video_duration) + 1
            video_clip = concatenate_videoclips([video_clip] * loops_needed)
            # Trim to exact audio duration
            video_clip = video_clip.subclipped(0, audio_duration)
        elif video_duration > audio_duration:
            # If video is longer, trim it to audio length
            logger.info("Video is longer than audio. Trimming video...")
            video_clip = video_clip.subclipped(0, audio_duration)
        
        # Set the audio to the video
        logger.info("Combining audio with video...")
        final_clip = video_clip.with_audio(audio_clip)
        
        # Write the final video
        logger.info(f"Writing final video to {output_file}...")
        final_clip.write_videofile(
            str(output_file),
            codec='libx264',
            audio_codec='aac',
            temp_audiofile='temp-audio.m4a',
            remove_temp=True,
            fps=30,
            logger=None  # Suppress moviepy's verbose output
        )
        
        # Clean up
        video_clip.close()
        audio_clip.close()
        final_clip.close()
        
        # Verify output file
        if not output_file.exists():
            raise FileNotFoundError(f"Failed to create final video: {output_file}")
        
        file_size = output_file.stat().st_size / (1024 * 1024)  # Convert to MB
        logger.info("Final video created successfully")
        logger.info(f"File: {output_file}")
        logger.info(f"Size: {file_size:.2f} MB")
        logger.info(f"Duration: {audio_duration:.2f} seconds")
        
        return str(output_file)
        
    except Exception as e:
        logger.error(f"Error combining video and audio: {str(e)}")
        raise

if __name__ == "__main__":
    try:
        final_video = combine_video_audio()
        print("\nFinal video created")
        print(f"Video file: {final_video}")
        print("Ready for upload to YouTube")
    except Exception as e:
        print(f"\nError: {str(e)}")
        exit(1)
