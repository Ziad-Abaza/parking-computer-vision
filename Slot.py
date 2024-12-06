import json

class Slot:
    def __init__(self, name="SlotClass", slots_file="slots.json"):
        self.name = name
        self.slots_file = slots_file
        self.data = self.load_slots()
        self.original_resolution = self.data.get("original_resolution", [1, 1]) 
        self.slots = self.data.get("slots", {})

    def load_slots(self):
        try:
            with open(self.slots_file, "r") as file:
                return json.load(file)
        except FileNotFoundError:
            print(f"Slots file not found: {self.slots_file}")
            return {"original_resolution": [1, 1], "slots": {}}

    def save_slots(self):
        with open(self.slots_file, "w") as file:
            json.dump(self.data, file, indent=4)
        print("Saved slots to JSON.")

    def check_occupancy(self, detections, current_resolution):
        scale_factor_x = current_resolution[0] / self.original_resolution[0]
        scale_factor_y = current_resolution[1] / self.original_resolution[1]

        occupied_slots = []
        for slot_id, polygon_points in self.slots.items():
            scaled_polygon = [
                (int(point[0] * scale_factor_x), int(point[1] * scale_factor_y))
                for point in polygon_points
            ]
            for detection in detections:
                if self.is_detection_in_slot(detection["bbox"], scaled_polygon):
                    occupied_slots.append(slot_id)
        return occupied_slots


    @staticmethod
    def is_detection_in_slot(bbox, polygon):
        x, y, width, height = bbox["x"], bbox["y"], bbox["width"], bbox["height"]

        center_x = x + width // 2
        center_y = y + height // 2

        return Slot.point_in_polygon((center_x, center_y), polygon)

    @staticmethod
    def point_in_polygon(point, polygon):
        px, py = point
        n = len(polygon)
        inside = False

        for i in range(n):
            x1, y1 = polygon[i]
            x2, y2 = polygon[(i + 1) % n]

            if ((y1 > py) != (y2 > py)) and (
                px < (x2 - x1) * (py - y1) / (y2 - y1 + 1e-9) + x1
            ):
                inside = not inside

        return inside
