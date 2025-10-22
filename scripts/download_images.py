"""
Script: download_images.py
Purpose: Downloads Wikipedia images for the entities found in the script
Input: Reads output/entities.json
Output: Downloads images to output/images/ folder
"""

import json
import logging
from pathlib import Path
import requests
from urllib.parse import urlparse

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def sanitize_filename(filename):
    """Sanitize filename for Windows/Unix compatibility"""
    invalid_chars = '<>:"/\\|?*'
    for char in invalid_chars:
        filename = filename.replace(char, '_')
    return filename

def download_image(url, save_path):
    """Download an image from URL"""
    try:
        logger.info(f"Downloading: {url}")
        
        response = requests.get(url, timeout=10, stream=True)
        response.raise_for_status()
        
        # Write to file
        with open(save_path, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
        
        file_size = save_path.stat().st_size / 1024  # KB
        logger.info(f"Downloaded: {save_path.name} ({file_size:.1f} KB)")
        return True
        
    except Exception as e:
        logger.error(f"Failed to download {url}: {e}")
        return False

def download_all_images():
    """Download all images from entities.json"""
    try:
        # Read entities data
        entities_file = Path("output/entities.json")
        
        if not entities_file.exists():
            logger.error(f"Entities file not found: {entities_file}")
            logger.error("Run analyze_script.py first")
            return
        
        with open(entities_file, "r", encoding="utf-8") as f:
            entities = json.load(f)
        
        images = entities.get("images", {})
        
        if not images:
            logger.warning("No images to download")
            return
        
        # Create images directory
        images_dir = Path("output/images")
        images_dir.mkdir(exist_ok=True, parents=True)
        
        logger.info(f"Images directory: {images_dir}")
        logger.info(f"Images to download: {len(images)}")
        
        # Download each image
        downloaded = {}
        
        for entity_name, image_data in images.items():
            image_type = image_data["type"]
            image_url = image_data["url"]
            
            # Generate filename
            extension = Path(urlparse(image_url).path).suffix or ".jpg"
            safe_name = sanitize_filename(entity_name)
            filename = f"{image_type}_{safe_name}{extension}"
            save_path = images_dir / filename
            
            # Download
            if download_image(image_url, save_path):
                downloaded[entity_name] = str(save_path)
        
        # Update entities.json with local paths
        entities["downloaded_images"] = downloaded
        
        with open(entities_file, "w", encoding="utf-8") as f:
            json.dump(entities, f, indent=2, ensure_ascii=False)
        
        logger.info(f"Downloaded {len(downloaded)}/{len(images)} images")
        logger.info(f"Updated: {entities_file}")
        
        return downloaded
        
    except Exception as e:
        logger.error(f"Error downloading images: {e}")
        raise

if __name__ == "__main__":
    try:
        result = download_all_images()
        # ASCII-only minimal console output
        if result:
            print("\nImage download complete")
            print(f"Downloaded {len(result)} images")
        else:
            print("\nNo images downloaded")
    except Exception as e:
        logger.error(f"Failed to download images: {e}")
        exit(1)
