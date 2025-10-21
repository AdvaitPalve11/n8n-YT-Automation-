"""
Script: generate_audio.py
Purpose: Converts the STEM explanation text to TTS audio using pyttsx3
Input: Reads output/topic.json
Output: Creates output/audio.wav (offline TTS audio)
"""

import pyttsx3
import json
import logging
from pathlib import Path

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def generate_tts_audio():
    """
    Generates TTS audio from the educational script or topic explanation.
    Prioritizes structured script, falls back to raw explanation.
    Returns: Path to the generated audio file
    """
    try:
        # Define file paths
        script_file = Path("output/script.json")
        topic_file = Path("output/topic.json")
        output_file = Path("output/audio.wav")
        
        # Try to load structured script first
        text_to_speak = None
        topic = "Unknown"
        
        if script_file.exists():
            logger.info(f"Loading educational script from {script_file}")
            with open(script_file, "r", encoding="utf-8") as f:
                script_data = json.load(f)
            text_to_speak = script_data["script"]["full_text"]
            topic = script_data.get("topic", "Unknown")
            logger.info(f"Using structured script for: {topic}")
        elif topic_file.exists():
            logger.info(f"Loading topic data from {topic_file}")
            with open(topic_file, "r", encoding="utf-8") as f:
                data = json.load(f)
            text_to_speak = data.get("explanation", "")
            topic = data.get("topic", "Unknown")
            logger.info(f"Using raw explanation for: {topic}")
        else:
            raise FileNotFoundError("Neither script.json nor topic.json found")
        
        if not text_to_speak:
            raise ValueError("No text content found to generate audio")
        
        logger.info(f"Generating TTS audio for topic: {topic}")
        logger.info(f"Text length: {len(text_to_speak)} characters")
        
        # Initialize TTS engine
        engine = pyttsx3.init()
        
        # Optional: Configure voice properties
        voices = engine.getProperty('voices')
        rate = engine.getProperty('rate')
        
        # Set voice properties for YouTube Shorts (engaging pace)
        engine.setProperty('rate', rate - 10)  # Slightly faster for shorts
        # engine.setProperty('voice', voices[0].id)  # Use first voice (usually male)
        # engine.setProperty('voice', voices[1].id)  # Use second voice (usually female)
        
        logger.info(f"TTS settings for YouTube Shorts - Rate: {rate - 10}")
        
        # Save audio to file
        logger.info(f"Saving audio to {output_file}")
        engine.save_to_file(text_to_speak, str(output_file))
        engine.runAndWait()
        
        # Verify file was created
        if not output_file.exists():
            raise FileNotFoundError(f"Failed to create audio file: {output_file}")
        
        file_size = output_file.stat().st_size
        logger.info(f"✅ Audio generated successfully: {output_file} ({file_size} bytes)")
        
        return str(output_file)
        
    except Exception as e:
        logger.error(f"Error generating TTS audio: {str(e)}")
        raise

if __name__ == "__main__":
    try:
        audio_path = generate_tts_audio()
        print(f"\n✅ Successfully generated TTS audio:")
        print(f"Audio file: {audio_path}")
    except Exception as e:
        print(f"\n❌ Error: {str(e)}")
        exit(1)
