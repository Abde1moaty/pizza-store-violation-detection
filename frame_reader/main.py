import cv2
from producer import FrameProducer

def main():
    video_path = "video1.mp4"  # 🔁 Use full path if needed
    cap = cv2.VideoCapture(video_path)

    if not cap.isOpened():
        print(" Couldn't open video file.")
        return

    # Initialize RabbitMQ producer
    producer = FrameProducer()

    while True:
        ret, frame = cap.read()
        if not ret:
            print(" Video ended")
            break

        # Send frame to RabbitMQ
        producer.publish_frame(frame)

        # Optional: Display while sending
        cv2.imshow("Sending Frames", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()
    producer.close()

if __name__ == "__main__":
    main()
