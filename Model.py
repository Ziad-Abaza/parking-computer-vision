import mediapipe as mp
import cv2
import numpy as np

class Model:
    def __init__(self, name="ModelClass", model_path="./ssd_mobilenet_v2.tflite", confidence_threshold=0.5):
        self.name = name
        self.confidence_threshold = confidence_threshold

        # Initialize MediaPipe object detection
        BaseOptions = mp.tasks.BaseOptions
        ObjectDetector = mp.tasks.vision.ObjectDetector
        ObjectDetectorOptions = mp.tasks.vision.ObjectDetectorOptions
        VisionRunningMode = mp.tasks.vision.RunningMode

        options = ObjectDetectorOptions(
            base_options=BaseOptions(model_asset_path=model_path),
            max_results=5,
            running_mode=VisionRunningMode.IMAGE
        )
        self.detector = ObjectDetector.create_from_options(options)

    def detect(self, frame):
        """Run object detection on the provided frame."""
        # Convert BGR (OpenCV) to RGB for MediaPipe
        image_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        image_rgb = np.clip(image_rgb, 0, 255).astype(np.uint8)

        # Create MediaPipe image
        mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=image_rgb)
        results = self.detector.detect(mp_image)

        # Parse detections
        detections = []
        if results.detections:
            for detection in results.detections:
                score = detection.categories[0].score
                if score >= self.confidence_threshold:
                    bbox = detection.bounding_box
                    category = detection.categories[0].category_name
                    detections.append({
                        "category": category,
                        "score": score,
                        "bbox": {
                            "x": bbox.origin_x,
                            "y": bbox.origin_y,
                            "width": bbox.width,
                            "height": bbox.height
                        }
                    })
        return detections

    def annotate(self, frame, detections):
        """Annotate the frame with detection results."""
        for detection in detections:
            bbox = detection["bbox"]
            category = detection["category"]
            score = detection["score"]

            start_point = (int(bbox["x"]), int(bbox["y"]))
            end_point = (int(bbox["x"] + bbox["width"]), int(bbox["y"] + bbox["height"]))

            cv2.rectangle(frame, start_point, end_point, (0, 255, 0), 2)
            cv2.putText(frame, f"{category}: {score:.2f}", start_point,
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 2)
        return frame