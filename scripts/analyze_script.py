"""
Script: analyze_script.py
Purpose: Analyzes the script to extract entities (people, countries, formulas, concepts)
Input: Reads output/script.json
Output: Creates output/entities.json with extracted information
"""

import json
import re
import logging
from pathlib import Path
import requests

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Common country names and their Wikipedia image searches
COUNTRY_PATTERNS = [
    'India', 'China', 'France', 'Germany', 'Italy', 'Spain', 'Greece', 'Egypt',
    'Persia', 'Japan', 'England', 'Scotland', 'Ireland', 'Rome', 'Athens',
    'United States', 'America', 'Britain', 'Russia', 'Arabia'
]

# Common mathematician patterns
MATHEMATICIAN_PATTERNS = [
    r'([A-Z][a-z]+ )?[A-Z][a-z]+(?:\'s)?(?= theorem| formula| principle| law| paradox| conjecture| sequence| triangle| constant| number)',
    r'(?:named after |by |from )([A-Z][a-z]+ )?[A-Z][a-z]+',
]

def extract_countries(text):
    """Extract country names from text"""
    countries = []
    for country in COUNTRY_PATTERNS:
        if country.lower() in text.lower():
            countries.append(country)
    return list(set(countries))

def extract_mathematicians(text):
    """Extract mathematician names from text"""
    mathematicians = []
    
    # Look for common patterns
    for pattern in MATHEMATICIAN_PATTERNS:
        matches = re.findall(pattern, text)
        for match in matches:
            if isinstance(match, tuple):
                name = ' '.join([m.strip() for m in match if m]).strip()
            else:
                name = match.strip()
            
            if name and len(name) > 2:
                mathematicians.append(name)
    
    # Look for specific famous mathematicians
    famous_names = [
        'Pythagoras', 'Euclid', 'Archimedes', 'Euler', 'Gauss', 'Newton', 
        'Leibniz', 'Fermat', 'Pascal', 'Fibonacci', 'Descartes', 'Riemann',
        'Cantor', 'Hilbert', 'Poincaré', 'Ramanujan', 'Turing', 'Gödel',
        'Blaise Pascal', 'Isaac Newton', 'Carl Friedrich Gauss', 'Leonhard Euler',
        'Pierre de Fermat', 'René Descartes', 'Leonardo Fibonacci'
    ]
    
    for name in famous_names:
        if name in text:
            mathematicians.append(name)
    
    return list(set(mathematicians))

def extract_formulas(text):
    """Extract mathematical formulas and concepts"""
    formulas = []
    
    # Look for common formula patterns
    formula_patterns = [
        r'([a-z])\s*[²³⁴]\s*\+\s*([a-z])\s*[²³⁴]\s*=\s*([a-z])\s*[²³⁴]',  # a² + b² = c²
        r'e\s*\^\s*\(?\s*i\s*π\s*\)?\s*\+\s*1\s*=\s*0',  # e^(iπ) + 1 = 0
        r'F_n\s*=\s*F_\{n-1\}\s*\+\s*F_\{n-2\}',  # Fibonacci
        r'\d+\s*\/\s*\d+',  # Fractions
    ]
    
    for pattern in formula_patterns:
        matches = re.findall(pattern, text, re.IGNORECASE)
        if matches:
            formulas.extend(matches)
    
    # Look for specific formula mentions
    formula_keywords = {
        'pythagorean theorem': 'a² + b² = c²',
        'euler\'s identity': 'e^(iπ) + 1 = 0',
        'quadratic formula': 'x = (-b ± √(b²-4ac)) / 2a',
        'golden ratio': 'φ = (1 + √5) / 2',
        'fibonacci': 'F(n) = F(n-1) + F(n-2)',
    }
    
    text_lower = text.lower()
    for keyword, formula in formula_keywords.items():
        if keyword in text_lower:
            formulas.append(formula)
    
    return list(set(formulas))

def extract_concepts(topic, text):
    """Extract mathematical concepts to visualize"""
    concepts = []
    
    concept_keywords = {
        'triangle': ['triangle', 'triangular', 'pythagorean'],
        'circle': ['circle', 'circular', 'radius', 'circumference'],
        'spiral': ['spiral', 'fibonacci', 'golden ratio'],
        'graph': ['graph', 'distribution', 'curve', 'function'],
        'sequence': ['sequence', 'series', 'progression'],
        'geometry': ['geometric', 'shape', 'polygon'],
        'number_line': ['number', 'integer', 'prime'],
        'infinity': ['infinity', 'infinite', 'endless'],
    }
    
    text_lower = text.lower()
    topic_lower = topic.lower()
    
    for concept, keywords in concept_keywords.items():
        if any(kw in text_lower or kw in topic_lower for kw in keywords):
            concepts.append(concept)
    
    return concepts

def search_wikipedia_image(search_term):
    """Search Wikipedia for an image URL"""
    try:
        # Use Wikipedia API to get page images
        api_url = "https://en.wikipedia.org/w/api.php"
        params = {
            "action": "query",
            "format": "json",
            "titles": search_term,
            "prop": "pageimages",
            "pithumbsize": 500
        }
        
        response = requests.get(api_url, params=params, timeout=5)
        data = response.json()
        
        pages = data.get("query", {}).get("pages", {})
        for page_id, page_data in pages.items():
            if "thumbnail" in page_data:
                return page_data["thumbnail"]["source"]
        
        return None
        
    except Exception as e:
        logger.warning(f"Failed to search Wikipedia image for '{search_term}': {e}")
        return None

def analyze_script():
    """Main function to analyze script and extract entities"""
    try:
        # Read script data
        script_file = Path("output/script.json")
        
        if not script_file.exists():
            logger.error(f"Script file not found: {script_file}")
            return
        
        logger.info(f"Analyzing script: {script_file}")
        
        with open(script_file, "r", encoding="utf-8") as f:
            script_data = json.load(f)
        
        topic = script_data.get("topic", "")
        full_text = script_data.get("script", {}).get("full_text", "")
        
        logger.info("Extracting entities from script text")
        
        # Extract entities
        countries = extract_countries(full_text)
        mathematicians = extract_mathematicians(full_text)
        formulas = extract_formulas(full_text)
        concepts = extract_concepts(topic, full_text)
        
        logger.info(f"Found {len(countries)} countries")
        logger.info(f"Found {len(mathematicians)} mathematicians")
        logger.info(f"Found {len(formulas)} formulas")
        logger.info(f"Found {len(concepts)} concepts")
        
        # Search for images
        entity_images = {}
        
        # Country flags
        for country in countries:
            logger.info(f"Searching Wikipedia for {country} flag...")
            image_url = search_wikipedia_image(f"Flag of {country}")
            if image_url:
                entity_images[country] = {
                    "type": "country_flag",
                    "url": image_url,
                    "name": country
                }
                logger.info(f"Found flag: {country}")
        
        # Mathematician portraits
        for mathematician in mathematicians:
            logger.info(f"Searching Wikipedia for {mathematician} portrait...")
            image_url = search_wikipedia_image(mathematician)
            if image_url:
                entity_images[mathematician] = {
                    "type": "person",
                    "url": image_url,
                    "name": mathematician
                }
                logger.info(f"Found portrait: {mathematician}")
        
        # Create entities data
        entities = {
            "topic": topic,
            "countries": countries,
            "mathematicians": mathematicians,
            "formulas": formulas,
            "concepts": concepts,
            "images": entity_images,
            "has_rich_content": len(entity_images) > 0
        }
        
        # Save entities
        entities_file = Path("output/entities.json")
        with open(entities_file, "w", encoding="utf-8") as f:
            json.dump(entities, f, indent=2, ensure_ascii=False)
        
        logger.info(f"Entities saved: {entities_file}")
        logger.info(f"Total images found: {len(entity_images)}")
        
        return entities
        
    except Exception as e:
        logger.error(f"Error analyzing script: {e}")
        raise

if __name__ == "__main__":
    try:
        result = analyze_script()
        # ASCII-only minimal console output to avoid encoding issues
        print("\nEntity analysis complete")
        print("Entities saved to: output/entities.json")
        print(f"Images found: {len(result['images'])}")
        print(f"Rich content available: {'Yes' if result['has_rich_content'] else 'No'}")
    except Exception as e:
        logger.error(f"Failed to analyze script: {e}")
        exit(1)
