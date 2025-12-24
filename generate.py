import json
from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv
import os 
from typing import List
from pydantic import BaseModel,Field
from typing import List
from vectordb import collection
load_dotenv()

llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    api_key=os.getenv("GOOGLE_API_KEY"),
    temperature=0.3
)

class Item(BaseModel):
    label: str = Field(..., example="onion")

class GenerateRequest(BaseModel):
    items: List[Item]
    servings: int = Field(default=2, ge=1, le=10)
    style: str = Field(default="Indian")


def retrive_recipe(ingredients:str,k=3):
    query = ingredients

    results = collection.query(
        query_texts=[query],
        n_results=k,
    )
    return results["documents"][0], results["metadatas"][0]



def extract_json(text: str) -> dict:
    try:
        start = text.index("{")
        end = text.rindex("}") + 1
        return json.loads(text[start:end])
    except Exception:
        raise ValueError("Invalid JSON from LLM")
    
def run_recipe_generation(items: List[Item], servings: int =2, style: str ="any") -> dict:
    
    from prompts import build_prompt

    prompt = build_prompt(items, servings, style)
    response = llm.invoke(prompt)

    return extract_json(response.content)
