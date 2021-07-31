import multiprocessing
from server.server_zmq import start as zmq_start
from server.server_flask import start as flask_start
from yaml import load, Loader
import importlib, os, sys

def run(config):
    executor = {}
    with open(config, "r") as stream:
        config = load(stream, Loader=Loader)
    connectors = config['connectors']
    paths = connectors['path']
    skipList = ['AbstractConnector', 'ElfieConfig', '__builtins__', '__cached__', '__doc__', '__file__',
                '__loader__', '__name__', '__package__', '__spec__']


    for path in paths:
        files = filter(lambda x: x.endswith(".py") and x != "__init__.py", os.listdir(path))
        files = list(map(lambda x: x.replace(".py", ""), files))
        print(files)

        for file in files:
            if "/" in path:
                sys.path.append(path)
                path = path.split("/")
                sys.path.append("/".join(path[:-1]))
                path = path[-1]
            try:
                module = importlib.import_module('.' + file, path)
            except ModuleNotFoundError as e:
                print(e.path)
                continue;
            connectorsList = filter(lambda x: x not in skipList, dir(module))
            for connector in connectorsList:
                classInstance = getattr(module, connector)
                base = getattr(classInstance, "__base__", None)
                if base is None:
                    continue
                baseClass = '.'.join([base.__module__, base.__name__])

                if baseClass.endswith("connectors.AbstractConnector"):
                    objInstance = classInstance()
                    if objInstance.name() is "proxy_connector":
                        continue
                    print("Registering ", objInstance.name())
                    executor[objInstance.name()] = objInstance

    server = config["server"]
    queue = multiprocessing.JoinableQueue()
    zmq_process = multiprocessing.Process(target=zmq_start, kwargs={'queue': queue, 'executor': executor, **server["zmq"]})
    flask_process = multiprocessing.Process(target=flask_start, kwargs={'queue': queue, 'executor': executor,  **server["http"], 'zmq': server['zmq']})

    zmq_process.start()
    flask_process.start()

    queue.join()
    zmq_process.join()
    flask_process.join()

if __name__ == "__main__":
    run("./config.yml")