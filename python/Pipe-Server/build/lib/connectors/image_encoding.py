import base64
import numpy as np
import cv2

def decode(encodedImage):
    encodedImage = base64.b64decode(encodedImage)
    im_arr = np.frombuffer(encodedImage, dtype=np.uint8)  # im_arr is one-dim Numpy array
    img = cv2.imdecode(im_arr, flags=cv2.IMREAD_COLOR)
    return img

def encode(image):
    b, image = cv2.imencode('.jpg', image)  # im_arr: image in Numpy one-dim array format.
    im_bytes = image.tobytes()
    im_b64 = base64.b64encode(im_bytes)
    return im_b64