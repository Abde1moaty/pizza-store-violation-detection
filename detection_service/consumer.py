import pika
import base64
import cv2
import numpy as np
import json
import os
from datetime import datetime
from yolov12_detector import yolov12_detect


def is_inside_roi(box, roi):
    x1, y1, x2, y2 = box
    rx1, ry1, rx2, ry2 = roi
    return x1 >= rx1 and y1 >= ry1 and x2 <= rx2 and y2 <= ry2


class FrameConsumer:
    def __init__(self, host='localhost', queue='video_frames'):
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(host=host))
        self.channel = self.connection.channel()
        self.channel.queue_declare(queue=queue)
        self.queue = queue
        self.violation_count = 0
        self.violation_active = False
        self.roi_selected = False
        self.roi = None  # (x1, y1, x2, y2)
        os.makedirs("violations", exist_ok=True)

    def select_roi_once(self, frame):
        roi = cv2.selectROI("Select Protein ROI", frame, fromCenter=False, showCrosshair=True)
        cv2.destroyWindow("Select Protein ROI")

        x, y, w, h = roi
        x2, y2 = x + w, y + h
        self.roi = (x, y, x2, y2)
        self.roi_selected = True
        print(f"✅ ROI Selected: {self.roi}")

    def callback(self, ch, method, properties, body):
        message = json.loads(body)
        frame_b64 = message['frame']

        # Decode base64 to image
        jpg_original = base64.b64decode(frame_b64)
        jpg_array = np.frombuffer(jpg_original, dtype=np.uint8)
        frame = cv2.imdecode(jpg_array, cv2.IMREAD_COLOR)

        # Select ROI on first frame only
        if not self.roi_selected:
            self.select_roi_once(frame)

        # Run detection
        results = yolov12_detect(frame)

        # Draw the ROI
        x1, y1, x2, y2 = self.roi
        cv2.rectangle(frame, (x1, y1), (x2, y2), (255, 0, 0), 2)
        cv2.putText(frame, "Protein ROI", (x1, y1 - 10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 1)

        # Detection Flags
        hand_in_roi = False
        pizza_detected = False
        scooper_detected = False

        for det in results:
            label = det['label']
            conf = det['confidence']
            x1b, y1b, x2b, y2b = det['box']
            box = (x1b, y1b, x2b, y2b)

            # Color based on label
            if label == "hand":
                color = (0, 0, 255)
                if is_inside_roi(box, self.roi):
                    hand_in_roi = True
            elif label == "scooper":
                color = (255, 165, 0)
                scooper_detected = True
            elif label == "pizza":
                color = (0, 255, 0)
                pizza_detected = True
            else:
                color = (200, 200, 200)

            # Draw box
            cv2.rectangle(frame, (x1b, y1b), (x2b, y2b), color, 2)
            cv2.putText(frame, f"{label} {conf:.2f}", (x1b, y1b - 8),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)

        # Violation logic
        if hand_in_roi and pizza_detected and not scooper_detected:
            if not self.violation_active:
             self.violation_count += 1
             self.violation_active = True
             
            print(f"🚨 Violation #{self.violation_count} Detected!")

            cv2.putText(frame, f"🚨 VIOLATION #{self.violation_count}", (30, 50),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 3)

            # Save violation frame
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
            cv2.imwrite(f"violations/violation_{timestamp}.jpg", frame)
        else:
            self.violation_active = False

        # Show final frame
        cv2.imshow("YOLOv12 Live Detection", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            print("🛑 Exiting cleanly.")
            cv2.destroyAllWindows()
            self.connection.close()
            exit()

    def start_consuming(self):
        self.channel.basic_consume(queue=self.queue, on_message_callback=self.callback, auto_ack=True)
        print("🔁 Waiting for frames. Press Q to quit.")
        self.channel.start_consuming()
