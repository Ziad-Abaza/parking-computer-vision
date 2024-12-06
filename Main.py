import cv2
import numpy as np

class Main:
    def __init__(self):
        from Stream import Stream
        from Model import Model
        from Slot import Slot

        self.stream = Stream(name="ESP-CAM Stream", stream_url="./Video_test/stream.mp4", res=0.5)
        self.model = Model(name="CarDetectionModel", model_path="./efficientdet_lite0.tflite", confidence_threshold=0.5)
        self.slot = Slot(name="ParkingSlotManager", slots_file="slots.json")

    def run(self):
        self.stream.start_stream()

        try:
            while True:
                frame = self.stream.read_frame()
                if frame is None:
                    break

                current_resolution = (frame.shape[1], frame.shape[0]) 

                detections = self.model.detect(frame)

                occupied_slots = self.slot.check_occupancy(detections, current_resolution)

                annotated_frame = self.model.annotate(frame, detections)

                for slot_id, polygon_points in self.slot.slots.items():
                    scale_factor_x = current_resolution[0] / self.slot.original_resolution[0]
                    scale_factor_y = current_resolution[1] / self.slot.original_resolution[1]

                    scaled_polygon = [
                        (int(point[0] * scale_factor_x), int(point[1] * scale_factor_y))
                        for point in polygon_points
                    ]
                    color = (0, 0, 255) if slot_id in occupied_slots else (0, 255, 0)
                    cv2.polylines(annotated_frame, [np.array(scaled_polygon)], isClosed=True, color=color, thickness=2)
                    text_position = tuple(scaled_polygon[0])
                    cv2.putText(annotated_frame, f"Slot {slot_id}", text_position,
                                cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)

                cv2.imshow("Smart Parking System", annotated_frame)

                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break

        except Exception as e:
            print(f"Error: {e}")

        finally:
            self.stream.stop_stream()
            cv2.destroyAllWindows()


if __name__ == "__main__":
    app = Main()
    app.run()
