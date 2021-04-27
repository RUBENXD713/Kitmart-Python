import pymongo
import json
import requests
from datetime import datetime
#hola 
class Mongo:
    mydb = ""
    lista = []
    url = ''
    def __init__(self):
        self.url = 'http://192.168.1.86:3333/sensor'


    def getSensores(self):
        #mycol = self.mydb["Sensores"]
        response = requests.get(self.url)
        respuesta = response.json()
        #print(respuesta)
        for x in respuesta:
            self.lista.append((str(x["_id"]),x["nombre"],x["descripcion"],x["tipo"],x["pinIn"],x["pinOut"],x["estado"]))
            
        return self.lista
#------------------------------------------------------------------------------------------------------------------------------------------------------
