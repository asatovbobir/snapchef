"use client";

import { useState } from "react";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { Alert, AlertDescription, AlertTitle } from "@/components/ui/alert";

interface Ingredient {
  name: string;
  quantity: string;
}

interface Instruction {
  step: string;
}

interface Recipe {
  title: string;
  description: string;
  imageURL: string;
  calories: number;
  carbs: number;
  fats: number;
  proteins: number;
  time_to_cook: string;
  ingredients: Ingredient[];
  instructions: Instruction[];
}

interface RecipesResponse {
  recipes: Recipe[];
}

export default function Home() {
  const [file, setFile] = useState<File | null>(null);
  const [recipes, setRecipes] = useState<RecipesResponse | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files) {
      setFile(e.target.files[0]);
      setError(null);
    }
  };

  const handleSubmit = async (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    if (!file) {
      setError("Please select an image file.");
      return;
    }

    setLoading(true);
    setError(null);
    const formData = new FormData();
    formData.append("file", file);

    try {
      const response = await fetch(
        "http://127.0.0.1:8000/api/generate-recipes",
        {
          method: "POST",
          body: formData,
        }
      );

      if (!response.ok) {
        const errorBody = await response.text();
        throw new Error(
          `HTTP error! status: ${response.status}, body: ${errorBody}`
        );
      }

      const data: RecipesResponse = await response.json();
      setRecipes(data);
    } catch (error) {
      console.error("Error:", error);
      setError(
        `Failed to generate recipes. Error: ${
          error instanceof Error ? error.message : String(error)
        }`
      );
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="container mx-auto p-4">
      <h1 className="text-2xl font-bold mb-4">Recipe Generator</h1>
      <form onSubmit={handleSubmit} className="mb-4 space-y-4">
        <Input
          type="file"
          onChange={handleFileChange}
          accept="image/*"
          className="mb-2"
        />
        <Button type="submit" disabled={!file || loading}>
          {loading ? "Generating..." : "Generate Recipes"}
        </Button>
      </form>

      {error && (
        <Alert variant="destructive" className="mb-4">
          <AlertTitle>Error</AlertTitle>
          <AlertDescription>{error}</AlertDescription>
        </Alert>
      )}

      {recipes &&
        recipes.recipes.map((recipe, index) => (
          <Card key={index} className="mb-4">
            <CardHeader>
              <CardTitle>{recipe.title}</CardTitle>
            </CardHeader>
            <CardContent>
              <p className="mb-2">{recipe.description}</p>
              <p className="mb-2">Cooking Time: {recipe.time_to_cook}</p>
              <p className="mb-2">
                Calories: {recipe.calories}, Carbs: {recipe.carbs}g, Fats:{" "}
                {recipe.fats}g, Proteins: {recipe.proteins}g
              </p>
              <h3 className="font-bold mt-4 mb-2">Ingredients:</h3>
              <ul className="list-disc pl-5 mb-2">
                {recipe.ingredients.map((ingredient, idx) => (
                  <li key={idx}>
                    {ingredient.quantity} {ingredient.name}
                  </li>
                ))}
              </ul>
              <h3 className="font-bold mt-4 mb-2">Instructions:</h3>
              <ol className="list-decimal pl-5">
                {recipe.instructions.map((instruction, idx) => (
                  <li key={idx}>{instruction.step}</li>
                ))}
              </ol>
            </CardContent>
          </Card>
        ))}
    </div>
  );
}
