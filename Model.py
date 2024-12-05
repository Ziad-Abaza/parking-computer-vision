from Main import Main

class Model(Main):
    def __init__(self, name="ModelClass", model_path="keras.tflite"):
        super().__init__(name)
        self.model_path = model_path

    def load_model(self):
        print(f"Loading model from {self.model_path}.")

    def predict(self, data):
        print(f"Predicting on data: {data}.")
        return "Prediction result"
