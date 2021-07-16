import requests,json
import zmq, cv2
from server_zmq import encode, decode
import time

class PipeClient:
    def __init__(self, token):
        self._context = zmq.Context()
        self.socket = zmq.Socket(self._context, zmq.REQ)
        self.socket.connect("tcp://localhost:5555")
        self.token = token
        print(self.token)

    def sendImage(self, img):
        start = time.time()
        imgString = encode(img)
        self.socket.send_multipart([self.token.encode(), imgString])

    def receiveImage(self):
        data = self.socket.recv_multipart()
        imageStr = b''.join(data)
        start = time.time()
        decoded = decode(imageStr)
        return decoded

def makeRequestToServer(data):
    response = requests.post("http://localhost:26534/setPipeline", data=json.dumps(data))
    return response.json()

if __name__ == "__main__":
    data = makeRequestToServer({
        "pipeline": [{
            "name": "proxy_connector"
        }]
    })
    client = PipeClient(data['token'])

    capture = cv2.VideoCapture("D:\monodepth2\Driving Downtown - New York City 4K - USA.mp4")
    time.sleep(0.5)
    capture.set(cv2.CAP_PROP_POS_FRAMES, 1006)
    while True:
        start = time.time()
        _, frame = capture.read()
        frame = cv2.resize(frame, (640,480))
        cv2.imshow('Original', frame)
        if not _:
            break;
        client.sendImage(frame)
        processedImage = client.receiveImage()
        cv2.putText(processedImage, "FPS: %.2f"%(1/(time.time() - start)), (40 , 50),
                    cv2.FONT_HERSHEY_COMPLEX, .5, (255, 255, 255), 2, cv2.LINE_AA)
        cv2.imshow('Depth', processedImage)
        if cv2.waitKey(1) == ord('q'):
            break

    cv2.destroyAllWindows()