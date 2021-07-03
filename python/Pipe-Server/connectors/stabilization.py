from vidstab import VidStab

from connectors import AbstractConnector
import cv2

class VideoStabilization(AbstractConnector):
    def __init__(self):
        self.stabilizer = VidStab()
    def name(self):
        return "video_stabilization"

    def process(self, **kwargs):
        kwargs['frame'] = self.stabilizer.stabilize_frame(input_frame=kwargs['frame'],
                                                      smoothing_window=30)
        return kwargs


class CannyEdgeDectector(AbstractConnector):
    def name(self):
        return "canny_edges"

    def process(self, **kwargs):
        image = cv2.cvtColor(kwargs['frame'], cv2.COLOR_BGRA2GRAY)
        image = cv2.Canny(image, 100, 200)
        kwargs['frame'] = cv2.cvtColor(image, cv2.COLOR_GRAY2BGR)
        return kwargs