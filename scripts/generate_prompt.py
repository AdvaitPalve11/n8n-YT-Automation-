"""
Script: generate_prompt.py
Purpose: Randomly selects a STEM topic from Wikipedia and generates a short explanation
Output: Creates output/topic.json with topic name and explanation
"""

import wikipedia
import random
import json
import os
import logging
from pathlib import Path

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def generate_stem_prompt():
    """
    Selects a POPULAR mathematics topic/equation for YouTube Shorts.
    Returns: dict with 'topic' and 'explanation' keys
    """
    try:
        # Popular math topics and famous equations for YouTube Shorts
        popular_math_topics = [
            # Famous Equations
            "Pythagorean theorem",
            "Quadratic equation", 
            "Euler's identity",
            "Fibonacci sequence",
            "Golden ratio",
            
            # Important Concepts
            "Prime number",
            "Factorial",
            "Derivative",
            "Integral",
            "Probability",
            
            # Fascinating Topics
            "Pi",
            "Infinity",
            "Fractal",
            "Chaos theory",
            "Game theory",
            
            # Number Theory
            "Perfect number",
            "Mersenne prime",
            "Twin prime",
            "Fermat's Last Theorem",
            "Riemann hypothesis",
            
            # Geometry
            "Circle",
            "Triangle",
            "Sphere",
            "Tesseract",
            "Platonic solid",
            
            # Algebra & Calculus
            "Polynomial",
            "Exponential function",
            "Logarithm",
            "Complex number",
            "Matrix (mathematics)",
            
            # Statistics
            "Normal distribution",
            "Standard deviation",
            "Correlation",
            "Regression analysis",
            
            # Fun Math
            "Monty Hall problem",
            "Birthday paradox",
            "Benford's law",
            "Collatz conjecture",
            "Pascal's triangle",
        ]
        
        category = "Mathematics"
        logger.info(f"Selected category: {category}")
        
        # Pick a random popular math topic
        topic = random.choice(popular_math_topics)
        logger.info(f"Selected popular topic: {topic}")
        
        # Get 3 sentences for YouTube Shorts (30-45 seconds)
        max_retries = 3
        for attempt in range(max_retries):
            try:
                summary = wikipedia.summary(topic, sentences=3, auto_suggest=False)
                break
            except wikipedia.exceptions.DisambiguationError as e:
                # Handle disambiguation by picking the first option
                topic = e.options[0]
                logger.warning(f"Disambiguation occurred. Using: {topic}")
                try:
                    summary = wikipedia.summary(topic, sentences=6)
                    break
                except:
                    if attempt < max_retries - 1:
                        topic = random.choice(popular_math_topics)
                        logger.warning(f"Retrying with: {topic}")
                        continue
                    else:
                        raise
            except wikipedia.exceptions.PageError:
                # If page not found, try another topic
                if attempt < max_retries - 1:
                    topic = random.choice(popular_math_topics)
                    logger.warning(f"Page not found. Trying: {topic}")
                    continue
                else:
                    raise
        
        # Create output directory if it doesn't exist
        output_dir = Path("output")
        output_dir.mkdir(exist_ok=True)
        
        # Prepare data
        data = {
            "topic": topic,
            "explanation": summary,
            "category": category
        }
        
        # Save to JSON file
        output_file = output_dir / "topic.json"
        with open(output_file, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        
        logger.info(f"Topic and explanation saved to {output_file}")
        logger.info(f"Explanation preview: {summary[:100]}...")
        
        return data
        
    except Exception as e:
        logger.error(f"Error generating STEM prompt: {str(e)}")
        raise

if __name__ == "__main__":
    try:
        result = generate_stem_prompt()
        print("\nSuccessfully generated YouTube Shorts topic:")
        print(f"Topic: {result['topic']}")
        print(f"Category: {result['category']}")
        print("Explanation saved to output/topic.json")
    except Exception as e:
        print(f"\nError: {str(e)}")
        exit(1)
