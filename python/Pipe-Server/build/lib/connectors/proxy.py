from connectors import AbstractConnector
import zmq
from connectors.consts import INCREMENT_VAR
from connectors.image_encoding import decode, encode

class ProxyConnector(AbstractConnector):
    def name(self):
        self.context = zmq.Context.instance()
        self.zmq_socket = self.context.socket(zmq.REQ)
        self.zmq_socket.connect("tcp://localhost:34263")
        return "proxy_connector"

    def doEncoding(self):
        return True

    def receiveImage(self):
        data = self.zmq_socket.recv_multipart()
        imageStr = b''.join(data)
        return decode(imageStr)

    def process(self, **kwargs):
        message = kwargs["encoded"]
        output_message = []
        start_index = 0
        endIndex = len(kwargs) - INCREMENT_VAR

        while start_index < endIndex:
            output_message.append(message[start_index:start_index + INCREMENT_VAR])
            start_index += INCREMENT_VAR
        output_message.append(message[start_index:])
        self.zmq_socket.send_multipart(output_message)
        kwargs['frame'] = self.receiveImage()
        return kwargs