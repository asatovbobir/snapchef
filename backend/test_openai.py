# test_openai.py
import os
import json
from datetime import datetime
from urllib.parse import urlparse
from app.services.openai_service import generate_recipes
from app.utils.image_utils import image_to_base64

def validate_url(url):
    """Validate URL and return status with message"""
    try:
        result = urlparse(url)
        is_valid = all([result.scheme, result.netloc])
        
        if not is_valid:
            return False, "Invalid URL format"
        if not url.startswith('http'):
            return False, "URL must start with http(s)"
        if "default" in url.lower():
            return False, "Using fallback image"
        
        return True, "Valid image URL"
    except:
        return False, "URL parsing failed"

def save_output_to_file(result):
    # Create outputs directory if it doesn't exist
    output_dir = "outputs"
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    # Generate timestamp for unique filename
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{output_dir}/recipe_output_{timestamp}.txt"
    
    with open(filename, 'w', encoding='utf-8') as f:
        # Write basic info
        f.write("=== Recipe Generation Results ===\n\n")
        f.write(f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write(f"Number of recipes: {len(result['recipes'])}\n")
        f.write(f"Recipe structure: {list(result['recipes'][0].keys())}\n\n")
        
        # Write image URL summary
        f.write("=== Image URL Summary ===\n\n")
        for i, recipe in enumerate(result['recipes'], 1):
            url = recipe['imageURL']
            is_valid, message = validate_url(url)
            status = "✅" if is_valid else "⚠️"
            
            f.write(f"Recipe {i}: {recipe['title']}\n")
            f.write(f"URL: {url}\n")
            f.write(f"Status: {status} {message}\n\n")
        
        # Write detailed recipe information
        f.write("=== Detailed Recipes ===\n\n")
        for i, recipe in enumerate(result['recipes'], 1):
            f.write(f"Recipe {i}:\n")
            f.write(f"Title: {recipe['title']}\n")
            f.write(f"Description: {recipe['description']}\n")
            f.write(f"Image URL: {recipe['imageURL']}\n")
            f.write(f"Calories: {recipe['calories']}\n")
            f.write(f"Macros: Carbs: {recipe['carbs']}, Fats: {recipe['fats']}, Proteins: {recipe['proteins']}\n")
            f.write(f"Time to Cook: {recipe['time_to_cook']}\n")
            
            f.write("\nIngredients:\n")
            for ingredient in recipe['ingredients']:
                f.write(f"- {ingredient}\n")
            
            f.write("\nInstructions:\n")
            for j, instruction in enumerate(recipe['instructions'], 1):
                f.write(f"{j}. {instruction}\n")
            
            f.write("\n" + "="*50 + "\n\n")
        
        # Write raw JSON data for reference
        f.write("\n=== Raw JSON Data ===\n")
        f.write(json.dumps(result, indent=2))
    
    return filename

def main():
    # Load test image
    image_path = "ingredients.jpg"
    base64_image = image_to_base64(image_path)
    
    # Generate recipes
    print("Generating recipes...")
    try:
        result = generate_recipes(base64_image)
    except Exception as e:
        print(f"Generation failed: {str(e)}")
        return

    # Validate scraper integration
    print("\nImage URL Validation:")
    url_validation_summary = []
    
    for i, recipe in enumerate(result['recipes'], 1):
        url = recipe['imageURL']
        is_valid, message = validate_url(url)
        status = "✅" if is_valid else "⚠️"
        
        summary = f"Recipe {i}: {recipe['title']}\n"
        summary += f"URL: {url}\n"
        summary += f"Status: {status} {message}\n"
        
        print(summary)
        url_validation_summary.append(summary)

    # Save output to file
    output_file = save_output_to_file(result)
    
    # Print final summary
    print("\nFinal Summary:")
    print(f"✓ Generated {len(result['recipes'])} recipes")
    print(f"✓ Validated {len(url_validation_summary)} image URLs")
    print(f"✓ Output saved to: {output_file}")
    print("\nCheck the output file for full details")

if __name__ == "__main__":
    main()