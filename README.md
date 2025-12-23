# 📸 Recipe Detection & Generation System

An end-to-end AI-powered system that detects food ingredients from images and generates real, structured recipes using retrieval-augmented generation (RAG).

---

## 🧠 What This System Does

- Detects ingredients from a food image using **YOLOv8**
- Allows users to **confirm, edit, or add ingredients**
- Retrieves similar recipes using **ChromaDB**
- Generates **exactly 3 real recipes** using **Gemini LLM**
- Displays everything in a clean **Streamlit UI**

No fake dishes. No hallucinated garbage. Real food only.

---

## 📂 Project Structure
```
RESCIPE_DETECTION/
│
├── app.py # FastAPI backend entry point
├── frontend.py # Streamlit UI
├── detect.py # YOLO ingredient detection logic
├── yolo.py # YOLO model loader & inference wrapper
├── generate.py # Recipe generation pipeline
├── prompts.py # System + user prompts for LLM
├── vectordb.py # ChromaDB creation & retrieval
├── recipes.csv # Real recipe dataset (used for RAG)
├── configs.py # Central configuration
├── best.pt # Trained YOLOv8 model
```
---

## 🧠 System Architecture
```
Image (Upload / Camera)
↓
YOLOv8 Ingredient Detection
↓
User Confirmation + Edits
↓
ChromaDB Recipe Retrieval (RAG)
↓
Gemini LLM (Strict Prompt)
↓
3 Structured Recipes (JSON → UI)
```

---

## 🚀 How to Run the Project

### 1️⃣ Create Virtual Environment

```bash
python -m venv venv
source venv/bin/activate      # Linux / macOS
# venv\Scripts\activate       # Windows
```
2️⃣ Install Dependencies
```bash
pip install -r requirements.txt
```

3️⃣ Set Environment Variables
Create a .env file:
```bash
GOOGLE_API_KEY=your_gemini_api_key
```

4️⃣ Start Backend (FastAPI)
```bash
uvicorn app:app --reload
```

Backend runs at:
```
http://127.0.0.1:8000
```
5️⃣ Start Frontend (Streamlit)
```bash
streamlit run frontend.py
```
Frontend runs at:
```
http://localhost:8501
```
🔌 API Endpoints
🔍 POST /detect

Detects ingredients from an uploaded image.

Input: Image

Response:
```bash
{
  "items": [
    { "label": "onion", "score": 0.82 },
    { "label": "tomato", "score": 0.76 }
  ],
  "meta": {
    "model": "yolov8-food",
    "threshold": 0.4
  }
}
```
🍳 POST /generate

Generates recipes using RAG + Gemini LLM.

Input:
```bash
{
  "items": [
    { "label": "onion", "score": 0.9 },
    { "label": "tomato", "score": 0.8 }
  ],
  "servings": 2,
  "style": "Indian"
}
```
Response:
```bash
{
  "recipe_text": "Markdown with 3 dishes",
  "ingredients_list": [
    { "name": "onion", "quantity": "1 cup" }
  ],
  "metadata": {
    "cook_time": "30 minutes",
    "difficulty": "Easy",
    "dietary": ["Vegetarian"]
  }
}
```
🎯 Key Design Decisions

- YOLO only detects ingredients — it never decides recipes

- User confirmation is mandatory for low-confidence detections

- ChromaDB is used as a vector database for retrieval (no hype, just RAG)

- Gemini is strictly controlled via system prompts

- Exactly 3 recipes are generated — no more, no less

- Only real dishes, no vague or imaginary food names

⚠️ Known Limitations

-> Camera images may vary in exposure → detection accuracy can drop

-> YOLO performance depends heavily on training data quality

-> LLM output improves as recipe dataset quality improves

📌 Future Improvements

-> Ingredient icons

-> Step-by-step cooking mode

-> Voice-based instructions

-> Calorie estimation
