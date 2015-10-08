import cv2
from sauron.recording import Recording
import time

class MotionDetector(object):

    def __init__(self, frames):
        self.frames = frames
        self.background = None
        self.recording = None
        self.state = 'waiting'

    def detect(self):
        self.background = self.frames.next()
        for frame in self.frames:
            self.process_frame(frame)

    def frames(self):
        return read_frames(self.source)

    def process_frame(self, frame):
        diffs = self.background.diffs(frame)
        if len(diffs):
            if self.state == 'waiting':
                self.state = 'capturing'
                self.new_recording()
            self.recording.write(frame, diffs)
        else:
            if self.state == 'capturing':
                self.finalise_recording()
                self.state = 'waiting'

    def new_recording(self):
        self.recording = Recording.setup()
        self.recording.write_image(self.background.raw)

    def finalise_recording(self):
        path = self.recording.finalise()
        # upload
