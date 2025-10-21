"""
Script: generate_script.py
Purpose: Generates an educational script/explanation for math topics
Input: Reads output/topic.json
Output: Creates output/script.json with structured educational content
"""

import json
import logging
from pathlib import Path
import re

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def extract_key_points(explanation, max_points=3):
    """
    Extracts key points from the explanation.
    Returns a list of important sentences.
    """
    # Split into sentences
    sentences = re.split(r'(?<=[.!?])\s+', explanation)
    
    # Filter out very short sentences
    sentences = [s.strip() for s in sentences if len(s.strip()) > 20]
    
    # Return first max_points sentences
    return sentences[:max_points]

def generate_hook(topic):
    """
    Generates an attention-grabbing hook for the topic.
    """
    hooks = {
        "default": f"Let's explore {topic}!",
        "theorem": f"One of math's most important results: {topic}!",
        "equation": f"The famous {topic} explained!",
        "number": f"What makes {topic} special?",
        "sequence": f"The fascinating {topic}!",
        "paradox": f"Can you solve {topic}?",
        "problem": f"The mind-bending {topic}!",
        "constant": f"The mysterious number: {topic}!",
        "function": f"Understanding {topic}!",
        "formula": f"The powerful {topic}!",
    }
    
    topic_lower = topic.lower()
    
    # Check for keywords
    for keyword, hook_template in hooks.items():
        if keyword in topic_lower:
            return hook_template
    
    return hooks["default"]

def generate_call_to_action():
    """
    Generates a call-to-action for the end of the video.
    """
    ctas = [
        "Like and subscribe for more math!",
        "Follow for daily math shorts!",
        "Tap the heart if you learned something!",
        "Subscribe for more quick math lessons!",
        "Share this with math lovers!",
    ]
    
    import random
    return random.choice(ctas)

def structure_content(topic, explanation, category="Mathematics"):
    """
    Structures the content into a script format optimized for YouTube Shorts.
    """
    # Generate hook (opening line)
    hook = generate_hook(topic)
    
    # Extract key points
    key_points = extract_key_points(explanation, max_points=2)
    
    # If we have at least 2 key points, use them
    if len(key_points) >= 2:
        main_point_1 = key_points[0]
        main_point_2 = key_points[1]
    else:
        # Fallback: use the explanation directly
        main_point_1 = explanation[:200] + "..." if len(explanation) > 200 else explanation
        main_point_2 = explanation[200:400] + "..." if len(explanation) > 400 else ""
    
    # Generate closing
    closing = generate_call_to_action()
    
    # Create structured script
    script = {
        "hook": hook,
        "main_point_1": main_point_1,
        "main_point_2": main_point_2,
        "closing": closing,
        "full_text": f"{hook} {main_point_1} {main_point_2} {closing}",
        "estimated_duration": len(f"{hook} {main_point_1} {main_point_2} {closing}".split()) * 0.5  # ~0.5 sec per word
    }
    
    return script

def simplify_explanation(explanation, max_words=100):
    """
    Simplifies the explanation to be more digestible for YouTube Shorts.
    Focuses on the core concept.
    """
    # Split into sentences
    sentences = re.split(r'(?<=[.!?])\s+', explanation)
    
    simplified = []
    word_count = 0
    
    for sentence in sentences:
        sentence_words = len(sentence.split())
        if word_count + sentence_words <= max_words:
            simplified.append(sentence)
            word_count += sentence_words
        else:
            break
    
    return " ".join(simplified)

def generate_educational_script():
    """
    Generates a structured educational script from the topic data.
    Creates a clear, engaging explanation suitable for YouTube Shorts.
    """
    try:
        # Load topic data
        topic_file = Path("output/topic.json")
        
        if not topic_file.exists():
            raise FileNotFoundError(f"Topic file not found: {topic_file}")
        
        logger.info(f"Loading topic from {topic_file}")
        with open(topic_file, "r", encoding="utf-8") as f:
            data = json.load(f)
        
        topic = data.get("topic", "Unknown Topic")
        explanation = data.get("explanation", "")
        category = data.get("category", "Mathematics")
        
        logger.info(f"Generating educational script for: {topic}")
        
        # Simplify the explanation (remove overly technical details)
        simplified_explanation = simplify_explanation(explanation, max_words=80)
        
        # Structure the content into a script
        script = structure_content(topic, simplified_explanation, category)
        
        # Add metadata
        script_data = {
            "topic": topic,
            "category": category,
            "script": script,
            "metadata": {
                "word_count": len(script["full_text"].split()),
                "estimated_duration_seconds": script["estimated_duration"],
                "complexity": "beginner",  # Could be enhanced with NLP analysis
                "suitable_for": "YouTube Shorts, TikTok, Instagram Reels"
            }
        }
        
        # Save to JSON file
        output_file = Path("output/script.json")
        with open(output_file, "w", encoding="utf-8") as f:
            json.dump(script_data, f, indent=2, ensure_ascii=False)
        
        logger.info(f"✅ Script generated successfully: {output_file}")
        logger.info(f"Word count: {script_data['metadata']['word_count']}")
        logger.info(f"Estimated duration: {script_data['metadata']['estimated_duration_seconds']:.1f} seconds")
        logger.info(f"Hook: {script['hook']}")
        
        return script_data
        
    except Exception as e:
        logger.error(f"Error generating educational script: {str(e)}")
        raise

if __name__ == "__main__":
    try:
        result = generate_educational_script()
        
        print(f"\n📝 Educational Script Generated:")
        print(f"\n🎯 Topic: {result['topic']}")
        print(f"📚 Category: {result['category']}")
        print(f"\n🎬 SCRIPT:")
        print(f"\n[HOOK] {result['script']['hook']}")
        print(f"\n[POINT 1] {result['script']['main_point_1']}")
        print(f"\n[POINT 2] {result['script']['main_point_2']}")
        print(f"\n[CTA] {result['script']['closing']}")
        print(f"\n📊 Duration: ~{result['metadata']['estimated_duration_seconds']:.0f} seconds")
        print(f"💬 Words: {result['metadata']['word_count']}")
        
    except Exception as e:
        print(f"\n❌ Error: {str(e)}")
        exit(1)
