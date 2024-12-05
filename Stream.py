from Main import Main

class Stream(Main):
    def __init__(self, name="Stream", stream_url="http://example.stream"):
        super().__init__(name)
        self.stream_url = stream_url

    def start_stream(self):
        print(f"Starting stream from {self.stream_url}.")

    def stop_stream(self):
        print(f"Stopping stream from {self.stream_url}.")
