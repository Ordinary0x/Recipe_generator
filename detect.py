import json
from yolo import capture_image, process_image

def run_detection(image_path=None):
    if image_path:
        items = process_image(image_path)
        print("Detected Ingredients:")
        # print(json.dumps(items, indent=4))
        return items
    else:
        print("No image captured.")
        return None
