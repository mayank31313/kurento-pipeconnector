import importlib
import threading
import multiprocessing
import zmq
import time
from connectors.consts import INCREMENT_VAR
from connectors.image_encoding import decode, encode
from connectors.proxy import ProxyConnector

users_info = dict()

def worker_routine(worker_url, thread_count):
    context = zmq.Context.instance()
    socket = context.socket(zmq.REP)
    socket.connect(worker_url)

    print("Listening for connections")
    while True:
        client_data = socket.recv_multipart()
        layers, message = users_info[client_data[0].decode()], client_data[1:]
        message = b"".join(message)

        kwargs = {
            "encoded": message,
            "frame": decode(message),
            "lastEncodedIndex": -1
        }
        for i,layer in enumerate(layers):
            # if layer.doEncoding() and kwargs["lastEncodedIndex"] != i - 1:
            #     kwargs["encoded"] = encode(kwargs["frame"])
            #     kwargs["lastEncodedIndex"] = i
            kwargs = layer.process(**kwargs)
        message = encode(kwargs["frame"])

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
    proxy = ProxyConnector()
    executor[proxy.name()] = proxy
    try:
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

    except Exception as e:
        print(e)
    finally:
        context.term()
if __name__ == "__main__":
    start(multiprocessing.JoinableQueue(), "./config.yml")