import cv2
import json
from Stream import Stream 


class SlotDrawer:
    def __init__(self, output_file="slots.json"):
        self.slots = {}
        self.current_slot_id = 1
        self.current_points = []
        self.output_file = output_file
        self.original_resolution = None

    def draw_slot(self, event, x, y, flags, param):
        if event == cv2.EVENT_LBUTTONDOWN: 
            self.current_points.append((x, y))

        elif event == cv2.EVENT_RBUTTONDOWN: 
            if len(self.current_points) > 2: 
                self.slots[self.current_slot_id] = self.current_points[:]
                print(f"Slot {self.current_slot_id}: {self.slots[self.current_slot_id]}")
                self.current_slot_id += 1
                self.current_points = []
            else:
                print("A slot must have at least 3 points.")

        elif event == cv2.EVENT_MBUTTONDOWN:  
            self.current_points = []

    def save_slots(self):
        with open(self.output_file, "w") as file:
            json.dump(
                {
                    "original_resolution": self.original_resolution,
                    "slots": self.slots
                },
                file,
                indent=4
            )
        print(f"Slots saved to {self.output_file}")

    def run(self, stream: Stream):
        # Start the video stream
        stream.start_stream()
        window_name = "Draw Slots (L-click to add point, R-click to finish slot, M-click to clear, 's' to save, 'q' to quit)"
        cv2.namedWindow(window_name)
        cv2.setMouseCallback(window_name, self.draw_slot)

        while True:
            # Read a frame from the stream
            frame = stream.read_frame()
            if frame is None:
                print("No more frames. Exiting...")
                break

            if self.original_resolution is None:
                self.original_resolution = (frame.shape[1], frame.shape[0])

            # Draw the current slot points
            for i, point in enumerate(self.current_points):
                cv2.circle(frame, point, 5, (0, 255, 255), -1)
                if i > 0:
                    cv2.line(frame, self.current_points[i - 1], point, (0, 255, 255), 2)

            # Draw finalized slots
            for slot_id, points in self.slots.items():
                for i in range(len(points)):
                    cv2.line(frame, points[i], points[(i + 1) % len(points)], (255, 0, 0), 2)
                centroid = tuple(map(lambda x: int(sum(x) / len(x)), zip(*points)))
                cv2.putText(frame, f"Slot {slot_id}", centroid, cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)

            cv2.imshow(window_name, frame)
            key = cv2.waitKey(1) & 0xFF

            if key == ord('s'):  
                self.save_slots()
            elif key == ord('q'):  
                break

        stream.stop_stream()
        cv2.destroyAllWindows()


if __name__ == "__main__":
    stream = Stream(stream_url="./Video_test/stream.mp4", res=0.5)  

    drawer = SlotDrawer(output_file="slots.json")
    drawer.run(stream)
