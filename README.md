#  AI-Powered Video Violation Detection System

A real-time video processing system that uses YOLOv12 object detection to monitor and detect violations in video streams. The system is designed to detect specific scenarios like hand interactions with food items without proper utensils.

## 🎯 Features

- **Real-time Video Processing**: Stream video frames through RabbitMQ for scalable processing
- **AI-Powered Detection**: Uses YOLOv12 model for accurate object detection
- **Violation Monitoring**: Detects specific violation scenarios (e.g., hands touching food without scooper)
- **ROI Selection**: Interactive region-of-interest selection for focused monitoring
- **Violation Recording**: Automatically saves violation frames with timestamps
- **Live Visualization**: Real-time display of detection results and violation alerts

## 🏗️ Architecture

The system consists of two main components:

### 1. Frame Reader (Producer)
- Reads video files and streams frames
- Converts frames to base64 format
- Publishes frames to RabbitMQ queue

### 2. Detection Service (Consumer)
- Consumes frames from RabbitMQ
- Runs YOLOv12 object detection
- Monitors for violations based on detection results
- Saves violation images and displays live results

## 📋 Prerequisites

- Python 3.8+
- RabbitMQ Server
- OpenCV
- YOLOv12 model file (`est.pt`)

## 🚀 Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/eagle-vision.git
   cd eagle-vision
   ```

2. **Install RabbitMQ**
   - [Download and install RabbitMQ](https://www.rabbitmq.com/download.html)
   - Start the RabbitMQ server

3. **Install Python dependencies**

   For Frame Reader:
   ```bash
   cd frame_reader
   pip install -r requirements.txt
   ```

   For Detection Service:
   ```bash
   cd detection_service
   pip install -r requirements.txt
   ```

4. **Prepare your model**
   - Place your YOLOv12 model file (`est.pt`) in the `detection_service/` directory
   - Update the model path in `yolov12_detector.py` if needed

## 🎮 Usage

### 1. Start the Detection Service
```bash
cd detection_service
python main.py
```

The detection service will:
- Connect to RabbitMQ
- Wait for video frames
- Open a window for ROI selection on the first frame
- Begin monitoring for violations

### 2. Start the Frame Reader
```bash
cd frame_reader
python main.py
```

The frame reader will:
- Load the specified video file (`video1.mp4`)
- Stream frames to RabbitMQ
- Display the video being processed

### 3. Monitor Violations
- The system will automatically detect violations based on the configured rules
- Violation frames are saved in the `violations/` directory
- Live detection results are displayed in real-time
- Press 'Q' to quit the detection service

## 🔧 Configuration

### Video Source
Edit `frame_reader/main.py` to change the video source:
```python
video_path = "your_video.mp4"  # Change to your video file
```

### Detection Rules
The current violation detection logic in `detection_service/consumer.py`:
- Detects when a hand is inside the ROI
- Pizza is detected in the frame
- No scooper is present
- This combination triggers a violation

### Model Configuration
Update detection confidence and model path in `yolov12_detector.py`:
```python
model = YOLO("path/to/your/model.pt")
results = model.predict(source=frame, conf=0.75, verbose=False)
```

## 📁 Project Structure

```
pizza store violation/
├── detection_service/
│   ├── main.py              # Detection service entry point
│   ├── consumer.py          # RabbitMQ consumer and violation logic
│   ├── yolov12_detector.py  # YOLOv12 detection wrapper
│   ├── est.pt              # YOLOv12 model file
│   └── requirements.txt     # Python dependencies
├── frame_reader/
│   ├── main.py              # Frame reader entry point
│   ├── producer.py          # RabbitMQ producer
│   ├── requirements.txt     # Python dependencies
│   └── video1.mp4          # Sample video file
├── violations/              # Saved violation images
└── README.md               # This file
```

## 🎯 Detection Classes

The system is trained to detect:
- **Hand**: Human hands in the video
- **Pizza**: Pizza or food items
- **Scooper**: Utensils or scoops for handling food

## 📊 Output

### Violation Images
- Automatically saved in `violations/` directory
- Filename format: `violation_YYYYMMDD_HHMMSS_microseconds.jpg`
- Contains annotated frame with detection boxes and violation alert

### Live Display
- Real-time video feed with detection overlays
- ROI boundary visualization
- Violation counter and alerts
- Detection confidence scores

## 🔧 Customization

### Adding New Detection Classes
1. Retrain your YOLOv12 model with new classes
2. Update the model file in `detection_service/`
3. Modify violation logic in `consumer.py`

### Changing Violation Rules
Edit the violation detection logic in `consumer.py`:
```python
# Example: Different violation condition
if hand_in_roi and not scooper_detected:
    # Trigger violation
```

### ROI Configuration
- The system prompts for ROI selection on the first frame
- Click and drag to select the region of interest
- The ROI defines the area where hand detection is monitored

## 🐛 Troubleshooting

### Common Issues

1. **RabbitMQ Connection Error**
   - Ensure RabbitMQ server is running
   - Check connection parameters in producer/consumer

2. **Model Loading Error**
   - Verify the model file path in `yolov12_detector.py`
   - Ensure the model file is compatible with YOLOv12

3. **Video File Not Found**
   - Check the video path in `frame_reader/main.py`
   - Use absolute paths if needed

4. **Dependencies Issues**
   - Install all requirements: `pip install -r requirements.txt`
   - Ensure OpenCV and other libraries are properly installed

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature-name`
3. Commit your changes: `git commit -am 'Add feature'`
4. Push to the branch: `git push origin feature-name`
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- [Ultralytics YOLOv12](https://github.com/ultralytics/ultralytics) for object detection
- [OpenCV](https://opencv.org/) for computer vision capabilities
- [RabbitMQ](https://www.rabbitmq.com/) for message queuing

## 📞 Support

For questions and support, please open an issue on GitHub or contact the development team.

---

**Note**: This system is designed for educational and research purposes. Ensure compliance with local regulations when deploying in production environments. 
