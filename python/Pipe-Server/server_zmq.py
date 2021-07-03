import importlib
import threading
import multiprocessing
import cv2, base64
import numpy as np
import zmq
import time
import os

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


def worker_routine(worker_url, thread_count):
    context = zmq.Context.instance()
    socket = context.socket(zmq.REP)
    socket.connect(worker_url)

    print("Listening for connections")
    while True:
        client_data = socket.recv_multipart()
        layers, message = users_info[client_data[0].decode()], client_data[1:]
        message = b"".join(message)

        image = decode(message)
        for layer in layers:
            image = layer.process(frame=image)['frame']
        message = encode(image)

        output_message = []
        start_index = 0
        endIndex = len(message) - INCREMENT_VAR

        while start_index < endIndex:
            output_message.append(message[start_index:start_index + INCREMENT_VAR])
            start_index += INCREMENT_VAR

        output_message.append(message[start_index:])
        socket.send_multipart(output_message)

def start(queue, executor, server, port, **kwargs):
    server_url = "tcp://*:" + str(port)
    worker_url = "inproc://worker"

    context = zmq.Context.instance()
    server_socket = context.socket(zmq.ROUTER)
    server_socket.bind(server_url)

    worker_socket = context.socket(zmq.DEALER)
    worker_socket.bind(worker_url)

    def localStoreThread():
        while True:
            if queue.empty():
                time.sleep(0.5)
                continue

            data = queue.get()
            layers = []
            for pipeElement in data['pipeline']:
                layers.append(executor[pipeElement['name']])
            users_info[data['token']] = layers

    threading.Thread(target=localStoreThread).start()
    for i in range(5):
        thread = threading.Thread(target=worker_routine, args=(worker_url, i))
        thread.daemon = True
        thread.start()

    zmq.proxy(server_socket, worker_socket)
if __name__ == "__main__":
    start(multiprocessing.JoinableQueue(), "./config.yml")