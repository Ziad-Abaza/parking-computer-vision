import cv2

class Stream:
    def __init__(self, name="Stream", stream_url="http://default.stream", res=None):
        self.name = name
        self.stream_url = stream_url
        self.cap = None
        self.res = res

    def start_stream(self):
        self.cap = cv2.VideoCapture(self.stream_url)
        if not self.cap.isOpened():
            print(f"[{self.name}] Failed to open stream.")
        else:
            print(f"[{self.name}] Stream started.")

    def read_frame(self):
        if self.cap and self.cap.isOpened():
            ret, frame = self.cap.read()
            if ret:
                if self.res:
                    frame = self.resize_frame(frame)
                return frame
        return None

    def resize_frame(self, frame):
        if isinstance(self.res, tuple):
            return cv2.resize(frame, self.res)
        elif isinstance(self.res, (float, int)):
            width = int(frame.shape[1] * self.res)
            height = int(frame.shape[0] * self.res)
            return cv2.resize(frame, (width, height))
        return frame

    def stop_stream(self):
        if self.cap:
            self.cap.release()
            print(f"[{self.name}] Stream stopped.")