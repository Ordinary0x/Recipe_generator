import chromadb
import csv
from chromadb.utils import embedding_functions

client = chromadb.Client()

embedding_fn = embedding_functions.SentenceTransformerEmbeddingFunction(
    model_name="all-MiniLM-L6-v2"
)

collection = client.get_or_create_collection(
    name="recipes",
    embedding_function=embedding_fn
)

def load_recipes_to_db(csv_file_path= "recipes.csv"):
    with open(csv_file_path, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        
        for row in reader:
            doc= f"""
Title: {row['title']}
Cuisine: {row['cuisine']}
Ingredients: {row['ingredients']}
Steps: {row['steps']}
Serving Size: {row['servings']}
Tags: {row['tags']} 
"""
            collection.add(
                ids=[row['id']],
                documents=[doc],
                metadatas=[{
                    "title": row['title'],
                    "cuisine": row['cuisine'],
                    "ingredients": row['ingredients'],
                    "tags": row['tags']
                }],
            )
        print("Recipes loaded into ChromaDB.")


if __name__ == "__main__":
    load_recipes_to_db()