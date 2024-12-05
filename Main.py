from Model import Model
from Stream import Stream
from Slot import Slot

def main():
    model = Model(name="CustomModel", model_path="keras.tflite")
    stream = Stream(name="CustomStream", stream_url="http://example.stream")

    slot = Slot(name="CustomSlot", model=model, stream=stream)

    slot.process()

if __name__ == "__main__":
    main()
