import json
import threading
import time

from kafka import KafkaConsumer, KafkaProducer

import States

totalSensores = 2500
numeroRangos = 1

micros = []

##valores variables
rango = 1

# To consume latest messages and auto-commit offsets
consumer = KafkaConsumer('normal.' + 'rango' + str(rango), group_id='my-group', bootstrap_servers=['172.24.42.23:8090','172.24.42.63:8090','172.24.42.24:8090'])
# evt= threading.event()
promedio = 1
valorPrueba = 1500
i = 0


class AgregadorThread(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.producer = KafkaProducer(bootstrap_servers=['172.24.42.23:8090','172.24.42.63:8090','172.24.42.24:8090'],
                                      value_serializer=lambda m: json.dumps(m).encode('ascii'))
        self.id = 0
        self.temperatura = 0
        self.gas = 0
        self.ruido = 0
        self.luz = 0
        self.time = 0

    def setVals(self, id, temperatura, gas, ruido, luz, time):
        self.id = id
        self.temperatura = temperatura
        self.gas = gas
        self.ruido = ruido
        self.luz = luz
        self.time = time

    def run(self):
        micros[self.id].agregarTemperatura(self.temperatura)
        micros[self.id].agregarGas(self.gas)
        micros[self.id].agregarRuido(self.ruido)
        micros[self.id].agregarLuz(self.luz)
        payload = {
            "id": self.id,
            "temperatura": self.temperatura,
            "gas": self.gas,
            "ruido": self.ruido,
            "luz": self.luz,
            "sensetime": self.time,
            "estadoTemp": micros[self.id].estadoTemperatura,
            "estadoGas": micros[self.id].estadoGas,
            "estadoRuido": micros[self.id].estadoRuido,
            "estadoLuz": micros[self.id].estadoLuz
        }
        a = self.producer.send('bash.rango1', payload)
        print("publicacion para el publisher")


class PoolWrapper(AgregadorThread):
    def __init__(self):
        super(PoolWrapper, self).__init__()
        self.event = threading.Event()

    def run(self):
        while True:
            self.event.clear()
            self.event.wait()
            super(PoolWrapper, self).run()

    def setId(self, id):
        self.id = id

    def setTemperatura(self, temperatura):
        self.temperatura = temperatura

    def setGas(self, gas):
        self.gas = gas

    def setRuido(self, ruido):
        self.ruido = ruido

    def setLuz(self, luz):
        self.luz = luz

    def setTime(self, time):
        self.time = time


def chequearConexion():
    for micro in micros:
        ya = time.time()
        if (ya - micro.tiempoGas >= 300):
            micro.goState(micro.estadoGas, 0, 350, "gas")
        if (ya - micro.tiempoRuido >= 300):
            micro.goState(micro.estadoRuido, 0, 350, "ruido")
        if (ya - micro.tiempoLuz >= 300):
            micro.goState(micro.estadoLuz, 0, 350, "luz")
        if (ya - micro.tiempoTemperatura >= 300):
            micro.goState(micro.estadoTemperatura, 0, 350, "temperatura")

    threading.Timer(300.0, chequearConexion).start()


# init=totalSensores/numeroRangos*(rango-1)
init = 0
print("creando objetos")
t = time.time()
for i in range(totalSensores):
    micros.append(States.Sensor(init + i))

chequearConexion()
poolSize = 40
pool = []
for i in range(poolSize):
    pool.append(PoolWrapper())
    pool[i].start()
print("Objetos creados en: " + str(time.time() - t) + " s")

for message in consumer:
    print(message)
    jsonVal = json.loads(message.value)
    id = int(jsonVal['id'])
    temperatura = int(jsonVal['temperatura'])
    gas = int(jsonVal['gas'])
    ruido = int(jsonVal['ruido'])
    luz = int(jsonVal['luz'])
    tt = int(jsonVal['sensetime'])
    assigned = False
    while not assigned:
        for i in range(poolSize):
            if not pool[i].event.isSet():
                pool[i].setVals(id, temperatura, gas, ruido, luz, tt)
                pool[i].event.set()
                assigned = True
                break







