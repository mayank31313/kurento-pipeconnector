FROM ubuntu:bionic

RUN apt-get update && apt install python3 python3-pip python3-opencv -y

WORKDIR /zmq

COPY requirements.txt ./
RUN pip3 install --no-cache-dir  -r requirements.txt

COPY . .


CMD ["python3", "server/start.py"]