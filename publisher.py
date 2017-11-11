from kafka import KafkaConsumer
import json
import datetime
import sys
import requests
import time

t=time.time()
# To consume latest messages and auto-commit offsets
print("**Starting publisher")
consumer = KafkaConsumer('normal.'+'rango1',
                         group_id='my-group',
                         bootstrap_servers=['172.24.42.46:8090'])

i=0
print("*started looking for topics to eat*")
class AgregadorThread(threading.Thread):
	def __init__(self,payload):
		threading.Thread.__init__(self)
		self.payload=payload
	def run(self):
		global promedio
		global i
    url = "http://172.24.42.40:8000/mediciones/"
		response = requests.post(url, data=json.dumps(payload), headers={'Content-type': 'application/json'})
		sem.acquire()
		promedio= (self.time-time.time()+promedio*i)/(i+1)
		sem.release()


for message in consumer:
   # print(message)
    try:
        jsonVal=json.loads(message.value)
        if (jsonVal!= None and jsonVal['data']!=None):
            valor=int(jsonVal['data'])
           
            payload={
        
                "idMicro": jsonVal['idMicro'],
                "temperatura":jsonVal['temperatura'],
                "sonido":jsonVal['sonido'],
                "gas":jsonVal['gas'],
                "luz":jsonVal['luz'],
                "time": str(datetime.datetime.now()).split(" ")[1]    
          }

            #print(json.dumps(payload))
           
            print(message.topic)
            i+=1
            print("Msj:"+ str(i)+" Response Status Code: " + str(response.status_code))
        ## caso en el que el valor recibido esta mal formado
        else:
            print("null value received")

    except:
        print("Error (in)esperado: ",sys.exc_info())
