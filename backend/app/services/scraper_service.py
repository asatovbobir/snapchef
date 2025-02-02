import subprocess
import os
from pathlib import Path
from app.config.settings import settings
import logging

logger = logging.getLogger(__name__)

def get_recipe_image(title: str) -> str:
    try:
        scraper_path = Path(__file__).parent / 'scrapers' / 'image_scraper.js'

        logger.info(f"Running scraper for: {title}")
        
        result = subprocess.run(
            ['node', str(scraper_path), title],
            capture_output=True,
            text=True,
            check=True,
            env={
                **os.environ,
                "PEXELS_API_KEY": settings.pexels_api_key,  # Use settings value
                "DEFAULT_IMAGE_URL": settings.default_image_url
            }
        )
        
        url = result.stdout.strip().split('\n')[-1]
        
        # Validate URL format
        if not url.startswith("http"):
            logger.warning(f"Invalid URL format: {url}")
            return settings.default_image_url
            
        return url
        
    except subprocess.CalledProcessError as e:
        logger.error(f"Scraper failed: {e.stderr}")
        return settings.default_image_url
    except Exception as e:
        logger.error(f"Scraper error: {str(e)}")
        return settings.default_image_url