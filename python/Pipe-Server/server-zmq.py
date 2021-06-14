import socket
import threading

import cv2, base64
import numpy as np
import zmq

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

def compute(image):
    image = cv2.cvtColor(image, cv2.COLOR_BGRA2GRAY)
    image = cv2.Canny(image, 100, 200)
    image = cv2.cvtColor(image, cv2.COLOR_GRAY2BGR)
    return image

user_info = dict()

class UserInfo:
    def __init__(self, token, modal, layers):
        self.modal = modal
        self.layers = layers
        self.token = token

def worker_routine(worker_url, thread_count):
    context = zmq.Context.instance()
    socket = context.socket(zmq.REP)
    socket.connect(worker_url)

    print("Listening for connections")
    while True:
        client_data = socket.recv_multipart()
        if client_data[1] == b"1" and client_data[0] == b"":
            token = "default"
            user_info[token] = UserInfo(token=token, modal="testmodel", layers=[compute])
            socket.send_multipart([token.encode()])
            continue;

        client_info, message = user_info[client_data[0].decode()], client_data[1:]
        message = b"".join(message)

        image = decode(message)
        for layer in client_info.layers:
            image = layer(image)
        message = encode(image)

        output_message = []
        start_index = 0
        endIndex = len(message) - INCREMENT_VAR

        while start_index < endIndex:
            output_message.append(message[start_index:start_index + INCREMENT_VAR])
            start_index += INCREMENT_VAR

        output_message.append(message[start_index:])
        socket.send_multipart(output_message)

if __name__ == "__main__":
    server_url = "tcp://*:5555"
    worker_url = "inproc://worker"

    context = zmq.Context.instance()
    server_socket = context.socket(zmq.ROUTER)
    server_socket.bind(server_url)

    worker_socket = context.socket(zmq.DEALER)
    worker_socket.bind(worker_url)

    INCREMENT_VAR = 10240

    # Launch pool of worker threads
    for i in range(5):
        thread = threading.Thread(target=worker_routine, args=(worker_url,i))
        thread.daemon = True
        thread.start()

    zmq.proxy(server_socket, worker_socket)


