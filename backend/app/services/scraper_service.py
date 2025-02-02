import subprocess
import os
from pathlib import Path

def get_recipe_image(title: str) -> str:
    try:
        scraper_path = Path(__file__).parent.parent / 'scrapers' / 'image_scraper.js'
        
        result = subprocess.run(
            ['node', str(scraper_path), title],
            capture_output=True,
            text=True,
            check=True,
            env={
                **os.environ,
                "PEXELS_API_KEY": os.getenv("PEXELS_API_KEY"),
                "DEFAULT_IMAGE_URL": os.getenv("DEFAULT_IMAGE_URL")
            }
        )
        
        # Clean any extra output from node
        return result.stdout.strip().split('\n')[-1]
        
    except subprocess.CalledProcessError as e:
        print(f"Scraper error: {e.stderr}")
        return os.getenv("DEFAULT_IMAGE_URL")