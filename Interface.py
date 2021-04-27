import websocket
from threading import Thread
import sys
import json
import codecs
import requests

import RPi.GPIO as GPIO
import Adafruit_DHT
import time

import Sensores as sensor
import MongoDBConnection as mongo

call = sensor.Sensores()

mongo = mongo.Mongo()

hab = 0

sensoresList = mongo.getSensores()


url='http://192.168.1.86:3333/registro'


class Interface:
    
    def __init__(self):
        websocket.enableTrace(True)
        self.host = "ws://192.168.1.86:3333/adonis-ws"    
        self.ws = websocket.WebSocketApp(self.host,
                                on_message=on_message,
                                on_error=on_error,
                                on_close=on_close,
                                keep_running=True)

    def run(self):
        try:
            while True:
                self.ws.on_open = on_open
                self.ws.run_forever()
        except KeyboardInterrupt:
            sys.exit(1)

def GuardarRegistro(nombre, valor):
    if valor != None:
        param={'sensorId':str(nombre),'valor':valor}
        response=requests.post(url, params = param)
        param = {""}
        print(response)
    else:
        print("none date")
        return


def plagas ():
    sensores = mongo.getSensores()
    while True: 
        for lista in sensores:
            if lista[3] == 'C':
                movimiento = call.PIR(int(lista[4]))
                param={'sensorId':str(lista[0]),'valor':str(movimiento)}
                response=requests.post(url, params = param)
                time.sleep(2)
                
        print("........Plagas........")
        time.sleep(10)#180

def estufa ():
    while True:
        sensores1 = mongo.getSensores()
        #print(sensores1)
        for lista in sensores1:
            if lista[3] == 'D':
                if lista[6] == '1':
                    distancia = call.Ultrasonico(int(lista[4]),int(lista[5])) 
                    param={'sensorId':str(lista[0]),'valor':str(distancia)}
                    response=requests.post(url, params = param)
                    time.sleep(2)
                    print("distancia Calculada oK")
                else:
                    print("Estufa apagada")
        print("........Estufa..........")
        time.sleep(15)#30
        sensores1.clear()

def refrigerador ():
    sensores2 = mongo.getSensores()
    while True:
        #dato = "cerrado"
        for lista in sensores2:
            if lista[3] == 'F':
                dato = call.Refrigerador(int(lista[4]))
                if dato == "abierta":
                    param={'sensorId':str(lista[0]),'valor':str(dato)}
                    response=requests.post(url, params = param)
                    time.sleep(2)
                if dato == "cerrada":
                    param={'sensorId':str(lista[0]),'valor':str(dato)}
                    response=requests.post(url, params = param)
                    time.sleep(2)
        print(".........Refrigerador........")
        time.sleep(20)

def temperatura ():
    sensores3 = mongo.getSensores()
    while True:
        for lista in sensores3:
            if lista[3] == 'B':
                temperatura = call.Temperatura(int(lista[4]))
                param={'sensorId':str(lista[0]),'valor':str(temperatura)}
                response=requests.post(url, params = param)
                time.sleep(2)
        print(".........Temperatura...........")
        time.sleep(50)#600

def temperaturaRefrigerador ():
    sensores5 = mongo.getSensores()
    while True:
        for lista in sensores5:
            if lista[3] == 'H':
                temperatura = call.Temperatura(int(lista[4]))
                param={'sensorId':str(lista[0]),'valor':str(temperatura)}
                response=requests.post(url, params = param)
                time.sleep(2)
        print(".........TemperaturaRefrigerador...........")
        time.sleep(50)#600

def humedadPlantas ():
    sensores4 = mongo.getSensores()
    while True:
        for lista in sensores4:
            if lista[3] == 'G':
                humedadTierra = call.HumedadTierra(int(lista[4]))
                param={'sensorId':str(lista[0]),'valor':str(humedadTierra)}
                response=requests.post(url, params = param)
                time.sleep(2)
        print("........HumedadPlantas..........")
        time.sleep(50)#600


def on_message(ws, message):
        sensoresList = mongo.getSensores()
        sensoresList.clear()
        sensoresList = mongo.getSensores()
        #print(sensoresList)        
        dt = json.loads(message)
        #print(dt['d']["event"] + ' ' + dt['d']["data"])
        for lista in sensoresList:
            if dt['d']["event"] == "plantas":
                if lista[3] == 'G':
                    humedadTierra = call.HumedadTierra(int(lista[4]))
                    GuardarRegistro(lista[0], str(humedadTierra))
                    data={"t":7,"d":{"topic":"kitmart","event":"plantas","data":"plantasPython"}}
                    ws.send(json.dumps(data))
                    print("plantasSocketFunciona")
            elif dt['d']["event"] == "temperatura":
                if lista[3] == 'B':
                    temperatura = call.Temperatura(int(lista[4]))
                    GuardarRegistro(lista[0], str(temperatura))
                    data={"t":7,"d":{"topic":"kitmart","event":"temperatura","data":"temperaturaPython"}}
                    ws.send(json.dumps(data))
                    print("temperaturaSocketFunciona")
            elif dt['d']["event"] == "controlEspacios":
                if lista[3] == 'C':
                    dato = call.PIR(int(lista[4]))
                    GuardarRegistro(lista[0], str(dato))
                    print("controlEspaciosPlagasSocketFunciona")
                elif lista[3] == 'D':
                    dato = call.Ultrasonico(int(lista[4]),int(lista[5])) 
                    GuardarRegistro(lista[0], str(dato))
                    print("controlEspaciosEstufaSocketFunciona")
                elif lista[3] == 'F':
                    dato = call.Refrigerador(int(lista[5]))
                    GuardarRegistro(lista[0],str(dato))
                    print("controlEspaciosRefrigeradorSocketFunciona")
                elif lista[3] == 'H':
                    dato = call.Refrigerador(int(lista[4]))
                    GuardarRegistro(lista[0],str(dato))
                    print("controlEspaciosRefrigeradorTemperaturaSocketFunciona")
                data={"t":7,"d":{"topic":"kitmart","event":"controlEspacios","data":"controlEspaciosPython"}}
                ws.send(json.dumps(data))

            elif dt['d']["event"] == "led":
                if lista[3] == 'E':
                    estado = call.setLed(int(lista[5]),int(lista[6]))
                    data={"t":7,"d":{"topic":"kitmart","event":"led","data":"ledsPython"}}
                    ws.send(json.dumps(data))
                    print("ledSocketFunciona")


def on_error(ws, error):
    print(error)
    print("ERRORR!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
    pass


def on_close(ws):
    print("### closed ###")


def on_open(ws):
    ws.send('{"t":1,"d":{"topic":"kitmart"}}')
    data = 'raspconnected'
    if data == True:
        ws.send('{"t":7,"d":{"topic":"kitmart","event":"ventilador","data":""}}')
    

Thread(target = temperatura).start()
time.sleep(2)
Thread(target = temperaturaRefrigerador).start()
time.sleep(2)
Thread(target = refrigerador).start()
time.sleep(2)
Thread(target = plagas).start()
time.sleep(2)
Thread(target = estufa).start()
time.sleep(2)
Thread(target = humedadPlantas).start()
