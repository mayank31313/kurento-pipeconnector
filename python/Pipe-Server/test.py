from kafka import KafkaProducer
from kafka.errors import KafkaError
import json, time

# # produce json messages
# producer = KafkaProducer(bootstrap_servers=['192.168.46.131:29092'], value_serializer=lambda m: json.dumps(m).encode('ascii'))
#
# # produce asynchronously
# for _ in range(100):
#     producer.send('example-topic', {'name': "Hii"})
#     print("Message sended")
#     time.sleep(1)


from kafka import KafkaConsumer
consumer = KafkaConsumer('mav_index', bootstrap_servers=['192.168.66.5:29092'])
for msg in consumer:
    print (msg)