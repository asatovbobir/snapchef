from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from app.services import openai_service, scraper_service
from app.utils.image_utils import save_temp_image, image_to_base64
from app.config import settings
from pathlib import Path
import uuid

app = FastAPI()

# CORS Configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/api/generate-recipes")
async def generate_recipes_endpoint(file: UploadFile = File(...)):
    try:
        # Save temporary image
        temp_image = await save_temp_image(file, settings.temp_image_dir)
        
        # Process image
        image_b64 = image_to_base64(temp_image)
        
        # Get recipes from OpenAI
        recipes_data = openai_service.generate_recipes(image_b64)
        
        # Get images from scraper
        for recipe in recipes_data["recipes"]:
            image_url = scraper_service.get_recipe_image(recipe["title"])
            recipe["imageURL"] = image_url
        
        # Cleanup temporary file
        temp_image.unlink()
        
        return recipes_data
        
    except Exception as e:
        raise HTTPException(
            status_code=500, 
            detail=f"Recipe generation failed: {str(e)}"
        )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=settings.API_PORT,
        reload=True
    )