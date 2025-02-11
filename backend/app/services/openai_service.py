from openai import OpenAI
from app.config.settings import settings
import json
import logging

logger = logging.getLogger(__name__)

SYSTEM_PROMPT = """
You are a professional chef and recipe generator. Analyze the provided ingredients and create SIX different recipes that exclusively use these ingredients. Follow these rules:

1. Recipe Requirements:
- Title: Clear and appetizing (40 characters max)
- Description: Brief overview (15-20 words)
- Use ONLY the detected ingredients - no substitutions
- Quantities: Estimate using common measurements (cups, tbsp, grams)
- Time Format: Combine units as needed (e.g., "25 Min", "1 Hr 10 Min")
- Nutritional Estimates: Per serving, round to nearest 5
- Instructions: 4-6 clear, numbered steps

2. Strict JSON Format:
{
    "recipes": [
        {
            "title": "Recipe Name 1",
            "description": "Brief description",
            "imageURL": "",
            "calories": 350,
            "carbs": 45,
            "fats": 12,
            "proteins": 20,
            "time_to_cook": "30 Min",
            "ingredients": [
                {"name": "flour", "quantity": "1.5 cups"},
                {"name": "yeast", "quantity": "1 tsp"}
            ],
            "instructions": [
                {"step": "Mix dry ingredients"},
                {"step": "Knead dough for 5 minutes"}
            ]
        },
        {
            "title": "Recipe Name 2",
            "description": "Brief description",
            "imageURL": "",
            "calories": 400,
            "carbs": 50,
            "fats": 15,
            "proteins": 25,
            "time_to_cook": "45 Min",
            "ingredients": [
                {"name": "flour", "quantity": "2 cups"},
                {"name": "yeast", "quantity": "1 tsp"}
            ],
            "instructions": [
                {"step": "Mix dry ingredients"},
                {"step": "Knead dough for 5 minutes"}
            ]
        }
        // Add 4 more recipes here...
    ]
}

3. Mandatory Rules:
- Provide EXACTLY 6 recipes
- Keep "imageURL" as empty string
- Never use markdown formatting
- Only include ingredients visible in the image
- If exact quantities aren't visible, make reasonable estimates
- Respond ONLY with valid JSON (no extra text)
- Numbers as values (no units in nutrition fields)
- Time format: Combine Hr/Min when >60 minutes
"""

def generate_recipes(image_b64: str) -> dict:
    client = OpenAI(api_key=settings.openai_api_key)
    
    try:
        logger.info("Sending request to OpenAI API")
        response = client.chat.completions.create(
            model="gpt-4-turbo",  # Verified working model name
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {
                    "role": "user", 
                    "content": [
                        {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{image_b64}"}},
                        {"type": "text", "text": "Generate recipes based on these ingredients."}
                    ]
                }
            ],
            response_format={"type": "json_object"},
            timeout=30  # Add timeout
        )
        
        logger.info("Received OpenAI response")
        response_content = response.choices[0].message.content
        logger.debug(f"Raw response: {response_content}")
        
        recipes_data = json.loads(response_content)
        
        # Validate response structure
        if not isinstance(recipes_data.get("recipes", None), list) or len(recipes_data["recipes"]) != 6:
            raise ValueError("Invalid recipe format from OpenAI")
            
        return recipes_data
    
    except json.JSONDecodeError as e:
        logger.error(f"JSON parse error: {str(e)}")
        raise ValueError("Failed to parse OpenAI response")
    except Exception as e:
        logger.error(f"OpenAI API error: {str(e)}")
        raise