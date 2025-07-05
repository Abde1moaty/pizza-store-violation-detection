from ultralytics import YOLO

# Load YOLOv12 (or YOLOv8) model
model = YOLO("detection_service\est.pt")  # Change to your model filename

def yolov12_detect(frame):
    # Run prediction
    results = model.predict(source=frame, conf=0.75, verbose=False)

    detections = []
    for r in results:
        for box in r.boxes:
            label_id = int(box.cls[0])
            label = r.names[label_id]
            conf = float(box.conf[0])
            x1, y1, x2, y2 = box.xyxy[0].tolist()

            detections.append({
                "label": label,
                "confidence": conf,
                "box": [int(x1), int(y1), int(x2), int(y2)]
            })

    return detections
