# **Smart Parking System**

This is a Python-based Smart Parking System designed to detect vehicles in a parking lot and determine the occupancy status of predefined parking slots. The system uses object detection to identify vehicles and maps them to polygon-shaped parking slots using geometric calculations.

---

## **Features**
- Real-time parking slot occupancy detection.
- Scalable to different resolutions and parking layouts.
- Flexible input options (video stream, webcam, or video file).
- Modular design with components for streaming, detection, and slot management.

---

## **Project Structure**
```
.
├── Main.py          # Main script to run the application
├── Stream.py        # Handles video streaming
├── Slot.py          # Manages parking slot definitions and occupancy checks
├── Model.py         # Performs vehicle detection using a TensorFlow Lite model
├── slots.json       # JSON file defining parking slots and the original resolution
├── Video_test/      # Directory for test video streams
├── efficientdet_lite0.tflite  # Pretrained object detection model
└── README.md        # Project documentation
```

---

## **Setup and Installation**
1. **Clone the repository**:
   ```bash
   git clone https://github.com/your-username/smart-parking-system.git
   cd smart-parking-system
   ```

2. **Install dependencies**:
   - Python 3.8 or higher is required.
   - Install required packages:
     ```bash
     pip install -r requirements.txt
     ```
     Example `requirements.txt`:
     ```
     opencv-python
     mediapipe
     numpy
     ```

3. **Prepare the environment**:
   - Ensure you have a `slots.json` file defining parking slots (see the example below).
   - Place your test video streams or stream URLs in the appropriate location.

---

## **Usage**
1. **Run the application**:
   ```bash
   python Main.py
   ```

2. **Control**:
   - Press **`q`** to exit the application.

---

## **Configuration**
- **`slots.json`**:
   The `slots.json` file defines the parking slots and the original resolution of the layout. Example format:
   ```json
   {
       "original_resolution": [960, 540],
       "slots": {
           "1": [[432, 405], [401, 366], [467, 363], [514, 401]],
           "2": [[530, 410], [490, 370], [560, 370], [600, 410]]
       }
   }
   ```
- **Adjust resolution**:
   Update the `res` parameter in `Stream` to change the video resolution:
   ```python
   self.stream = Stream(name="ESP-CAM Stream", stream_url="./Video_test/stream.mp4", res=1)
   ```

---

## **How It Works**
1. **Streaming**:
   The `Stream` class opens the video source (e.g., file, webcam, or IP camera) and processes frames.
   
2. **Object Detection**:
   The `Model` class uses TensorFlow Lite to detect vehicles in each frame and returns bounding boxes for detected objects.

3. **Slot Management**:
   The `Slot` class:
   - Scales the defined parking slots to the current frame resolution.
   - Checks if detected objects overlap with any slots.
   - Returns the IDs of occupied slots.

4. **Visualization**:
   The application draws bounding boxes around detected vehicles and highlights parking slots in real-time:
   - **Red**: Occupied slots.
   - **Green**: Available slots.

---

## **Demo**
![Smart Parking System Demo](https://via.placeholder.com/960x540?text=Demo+Image+Placeholder)

---

## **Contributing**
1. Fork the repository.
2. Create your feature branch:
   ```bash
   git checkout -b feature/your-feature
   ```
3. Commit your changes:
   ```bash
   git commit -m "Add your feature"
   ```
4. Push to the branch:
   ```bash
   git push origin feature/your-feature
   ```
5. Open a pull request.

---

## **License**
This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

---

## **Acknowledgments**
- TensorFlow Lite for the object detection model.
- OpenCV and MediaPipe for processing and visualization.
- Inspiration from smart parking systems and IoT solutions.

Let me know if you need further customizations!