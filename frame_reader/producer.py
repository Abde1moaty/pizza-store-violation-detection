import pika
import cv2
import base64
import json

class FrameProducer:
    def __init__(self, host='localhost', queue='video_frames'):
        # Connect to RabbitMQ
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(host=host))
        self.channel = self.connection.channel()
        self.queue = queue
        self.channel.queue_declare(queue=self.queue)

    def publish_frame(self, frame):
        # Encode frame to base64 JPEG
        _, buffer = cv2.imencode('.jpg', frame)
        jpg_as_text = base64.b64encode(buffer).decode('utf-8')

        message = json.dumps({'frame': jpg_as_text})
        self.channel.basic_publish(
            exchange='',
            routing_key=self.queue,
            body=message
        )
        print(" Frame sent to RabbitMQ")

    def close(self):
        self.connection.close()
