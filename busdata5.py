from pykafka import KafkaClient
from datetime import datetime
import json
import uuid
import time


#For bus data get coardinates from GEOJSON
input_file = open('./Kafka_BusData/bus5.json')
json_array = json.load(input_file)
cooordinates = json_array["features"][0]["geometry"]["coordinates"]

#UUID Function
def generate_uuid():
    return uuid.uuid4()


#KAFKA PRODUCER
client = KafkaClient(hosts="localhost:9092")
topic = client.topics['geodata']
producer = topic.get_sync_producer()



#Construct message for kafka send
data = {}
data["busline"] = "00005"

def generate_checkpoint(cooordinates):
    i = 0
    while i < len(cooordinates):
        data["key"] = data["busline"] + '_' + str(generate_uuid())
        data["timestamp"] = str(datetime.utcnow())
        data["latitude"] = cooordinates[i][1]
        data["longitude"] = cooordinates[i][0]
        message = json.dumps(data)
        print(message)
        producer.produce(message.encode('ascii'))
        time.sleep(0.5)

        if i == len(cooordinates)-1:
            i = 0
        else:    
            i += 1
    
generate_checkpoint(cooordinates)    


#testBusData