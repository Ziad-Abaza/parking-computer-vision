from Main import Main
from Stream import Stream
from Model import Model

class Slot(Main):
    def __init__(self, name="SlotClass", model=None, stream=None):
        super().__init__(name)
        self.model = model if model else Model(name="DefaultModel")
        self.stream = stream if stream else Stream(name="DefaultStream")

    def process(self):
        print(f"{self.name} is processing using:")
        self.model.load_model()
        self.stream.start_stream()

        # Simulate some processing
        data = "frame_from_stream"
        result = self.model.predict(data)
        print(f"Processing result: {result}")

        self.stream.stop_stream()
