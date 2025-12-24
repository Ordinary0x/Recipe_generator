from fastapi import FastAPI,HTTPException,UploadFile, File
from detect import run_detection
from generate import run_recipe_generation,GenerateRequest
import uuid,os
app = FastAPI() 

@app.post("/detect")
async def detect(file: UploadFile = File(...)):
    img_path = f"/tmp/{uuid.uuid4()}.jpg"
    
    with open(img_path, "wb") as f:
        f.write(await file.read())
    items = run_detection(img_path)
    os.remove(img_path)
    return {
        "items": items,
        "meta": {
            "model": "yolov8-food",
            "threshold": 0.4,
            "item_count": len(items)
        }
    }

@app.post("/generate")
async def generate_recipe(payload: GenerateRequest):
    try:
        recipe = run_recipe_generation(
            items=payload.items,
            servings=payload.servings,
            style=payload.style
            )
        return recipe
    except Exception as e:
        print(f"Error during recipe generation: {e}")
        raise HTTPException(status_code=500, detail=str(e))
    
    

