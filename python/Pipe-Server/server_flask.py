import multiprocessing
import uuid, json
from flask import Flask, request, jsonify

from models import UserInfo

app = Flask(__name__)
app.config['SECRET_KEY'] = "secret"
local_queue = None
kwargsArgs = dict()

@app.route("/setPipeline", methods=["POST"])
def setPipeline():
    data = json.loads(request.data.decode())
    user_info = UserInfo(token=uuid.uuid4().__str__(), pipeline=data['pipeline'])
    local_queue.put(user_info.__dict__)
    return jsonify(status="OK", token=user_info.token, zmqHost=kwargsArgs["zmq"]["server"] + ":" + str(kwargsArgs["zmq"]["port"]))

def start(queue, executor,  server, port, **kwargs):
    global local_queue, kwargsArgs
    local_queue = queue
    kwargsArgs = kwargs
    @app.route("/getConnectors")
    def getConnectors():
        return jsonify(list(map(lambda x: {'name': x}, executor)))

    app.run(host="0.0.0.0", port=port)

if __name__ == "__main__":
    start(multiprocessing.JoinableQueue())