import cv2
from ultralytics import YOLO
from configs import YOLO_MODEL_PATH,CLASS_NAMES

yolo_model = YOLO(YOLO_MODEL_PATH)

def capture_image():
    cap = cv2.VideoCapture(0)
    print("Press SPACE to capture, ESC to exit")
    captured_file = None
    while True:
        ret, frame = cap.read()
        cv2.imshow("Camera - Ingredients Detection", frame)
        key = cv2.waitKey(1)

        if key == 27:  # ESC key
            break
        if key == 32:  # SPACE key
            captured_file = "captured.jpg"
            cv2.imwrite(captured_file, frame)
            print(f"Image captured and saved as {captured_file}")
            break
    cap.release()
    cv2.destroyAllWindows()
    return captured_file

def process_image(image_path):
    results = yolo_model.predict(image_path)
    items = []
    print("Processing image for ingredient detection...")
    print(results)
    for result in results:
        if len(result.boxes) ==0 or result.boxes is None:
            continue

        boxes = result.boxes.xyxy.cpu().numpy()
        confidences = result.boxes.conf.cpu().numpy()
        class_ids = result.boxes.cls.cpu().numpy()

        for box, conf, cls_id in zip(boxes, confidences, class_ids):
             items.append({
            "label": CLASS_NAMES[int(cls_id)],
            "score": float(conf),
            "x1": float(box[0]),
            "y1": float(box[1]),
            "x2": float(box[2]),
            "y2": float(box[3]),
        })
    return items
            
                
                