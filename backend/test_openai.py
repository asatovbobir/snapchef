# test_openai.py
import os
import json
from datetime import datetime
from app.services.openai_service import generate_recipes
from app.utils.image_utils import image_to_base64

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
    result = generate_recipes(base64_image)
    
    # Save output to file
    output_file = save_output_to_file(result)
    
    # Print summary to console
    print("\nResults:")
    print(f"Number of recipes: {len(result['recipes'])}")
    print(f"First recipe structure: {list(result['recipes'][0].keys())}")
    print(f"Sample recipe: {result['recipes'][0]['title']}")
    print(f"\nDetailed output saved to: {output_file}")

if __name__ == "__main__":
    main()