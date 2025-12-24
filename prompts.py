import json
from typing import Dict, Any
from generate import Item,retrive_recipe
class PromptTemplates:

    @staticmethod
    def get_system_prompt():
        return """
You are a recipe generation assistant.

STRICT RULES:
1. You MUST generate exactly 3 dishes.
2. Dish 1 is the PRIMARY dish (mandatory).
3. Dish 2 and Dish 3 are ALTERNATIVES.
4. Each dish MUST have a REAL, COMMONLY KNOWN dish name
   (e.g., Paneer Butter Masala, Vada Pav, Dal Tadka, Vegetable Pulao,chainese noodles).
5. Do NOT invent vague or generic names.
6. Do NOT generate more or fewer than 3 dishes.
7. Follow the output structure EXACTLY.
8. Do NOT add explanations, comments, emojis, or extra text.
9. Ingredients must be realistic and easily available in India.
10. Steps must be short, clear, and numbered.
11. Do NOT generate more or fewer than 3 dishes.
12. Follow the output structure EXACTLY.

markdown formatted recipe (STRICT):

Dish 1 (Primary):
Name:
Estimated Time:
Ingredients:
- item
- item
Steps:
1.
2.
3.

Dish 2 (Alternative):
Name:
Estimated Time:
Ingredients:
- item
- item
Steps:
1.
2.
3.

Dish 3 (Alternative):
Name:
Estimated Time:
Ingredients:
- item
- item
Steps:
1.
2.
3.

Return VALID JSON ONLY in this exact format:

{{
  "recipe_text": "markdown formatted recipe",
  "ingredients_list": [
    {{ "name": "ingredient", "quantity": "amount" }}
  ],
  "metadata": {{
    "cook_time": "time",
    "difficulty": "Easy | Medium | Hard",
    "dietary": ["Vegetarian", "Vegan", "Gluten-Free"]
  }}
}}


"""
    @staticmethod
    def get_user_prompt(ingredients: str, servings: int, style: str,retrieved_text:str) ->str:
        return f"""
You are a professional chef AI.

Detected ingredients:
{ingredients}


Reference recipes (use these as guidance, do NOT copy exactly):
{retrieved_text}

Cuisine style: {style}
Servings: {servings}

Rules:
- Use ONLY the detected ingredients.
- Choose ONE realistic dish.
- Quantities must match servings.

Return VALID JSON ONLY in the specified format.

No explanations. No extra text.
"""


def create_message_pair(system_prompt: str, user_prompt: str) -> list[Dict[str, Any]]:
    """
    Create a standardized message pair for LLM interactions.

    Args:
        system_prompt: The system message content
        user_prompt: The user message content

    Returns:
        List containing system and user message dictionaries
    """
    return [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_prompt},
    ]

def build_prompt(items: list[Item], servings: int, style: str) -> list[Dict[str, Any]]:
    ingredients = ", ".join([item.label for item in items])
    system_prompt = PromptTemplates.get_system_prompt()
    docs,meta = retrive_recipe(ingredients)
    user_prompt = PromptTemplates.get_user_prompt(
        ingredients=ingredients,
        servings=servings,
        style=style,
        retrieved_text=docs  
    )
    return create_message_pair(system_prompt, user_prompt)

