import importlib
import threading
import multiprocessing
import cv2, base64
import numpy as np
import zmq
import time
import os, sys

sys.path.append("D:/monodepth2")
from test_pipe import DepthConnector
from yaml import load, Loader

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

users_info = dict()
INCREMENT_VAR = 10240
# executor = dict()


def worker_routine(worker_url):
    context = zmq.Context.instance()
    socket = context.socket(zmq.REP)
    socket.connect(worker_url)
    connector = DepthConnector()
    print("Listening for connections")
    while True:
        message = socket.recv_multipart()
        message = b"".join(message)

        image = decode(message)
        image = connector.process(frame = image)['frame']
        message = encode(image)

        output_message = []
        start_index = 0
        endIndex = len(message) - INCREMENT_VAR

        while start_index < endIndex:
            output_message.append(message[start_index:start_index + INCREMENT_VAR])
            start_index += INCREMENT_VAR

        output_message.append(message[start_index:])
        socket.send_multipart(output_message)

def start():
    server_url = "tcp://*:34263"
    worker_url = "inproc://worker"

    try:
        context = zmq.Context.instance()
        server_socket = context.socket(zmq.ROUTER)
        server_socket.bind(server_url)

        worker_socket = context.socket(zmq.DEALER)
        worker_socket.bind(worker_url)

        for i in range(1):
            thread = threading.Thread(target=worker_routine, args=(worker_url,))
            thread.daemon = True
            thread.start()

        zmq.proxy(server_socket, worker_socket)

    finally:
        context.term()

if __name__ == "__main__":
    start()