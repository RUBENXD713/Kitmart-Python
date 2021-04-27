import RPi.GPIO as GPIO
import Adafruit_DHT
import time

GPIO.setwarnings(False)

class Sensores():
    
    current_state=""
    sensor =""
    gpioIn=""
    gpioOut=""
    init_tiempo=""
    gpioMode=""
    
    def __init__(self):
        GPIO.cleanup()
        self.current_state=0
        self.sensor = Adafruit_DHT.DHT11
        self.init_tiempo=time.time()
        GPIO.setmode(GPIO.BCM)

    def HumedadTierra(self,pin):
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(pin,GPIO.IN)
        if GPIO.input(pin) == 1:
            time.sleep(1)
            print("Secas")
            return "Plantas Secas"
        elif GPIO.input(pin) == 0:
            time.sleep(1)
            print("Hidratadas")
            return "Plantas Hidratadas"

    def Humedad(self,pin):
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(pin,GPIO.IN)
        humedad, temperatura = Adafruit_DHT.read_retry(self.sensor, pin)
        print("humedad: "+str(humedad))
        return humedad
     
    def Temperatura(self,pin):
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(pin,GPIO.IN)
        humedad, temperatura = Adafruit_DHT.read_retry(self.sensor, pin)
        print("temperatura: "+str(temperatura))
        return temperatura
        
    def PIR(self,pin):

        GPIO.setmode(GPIO.BCM)
        GPIO.setup(pin,GPIO.IN)
        GPIO.input(pin)
        time.sleep(1)
        if GPIO.input(pin) == 1:
           time.sleep(1)
           print("Pir: Detecto Movimiento")
           #GPIO.cleanup()
           return "Detecto Movimiento"
        elif GPIO.input(pin) == 0:
            time.sleep(1)
            print("Pir: No Detecto Movimiento")
            #GPIO.cleanup()
            return "No Detecto Movimiento"
        return
        
    def Ultrasonico(self,pin1,pin2):

        GPIO.setmode(GPIO.BCM)
        GPIO.setup(pin1,GPIO.IN)
        GPIO.setup(pin2,GPIO.OUT)
        i=1

        while (i==1):
            GPIO.output(pin2, GPIO.LOW)
            time.sleep(1)

            GPIO.output(pin2, GPIO.HIGH)
            time.sleep(0.00001)
            GPIO.output(pin2, GPIO.LOW)
            while True:
                pulso_inicio = time.time()
                if GPIO.input(pin1) == GPIO.HIGH:
                    break
                while True:
                    pulso_fin = time.time()
                    if GPIO.input(pin1) == GPIO.LOW:
                        break

                duracion = pulso_fin - pulso_inicio
             
                distancia = (343200 * duracion)
                
                print ("Distancia: %.4f cm" % distancia)
                i=0

       
                #GPIO.cleanup()
                return distancia

    def setLed(self,pin,estado):
        GPIO.setmode(GPIO.BCM)
        
        GPIO.setup(pin,GPIO.OUT)
    
        if estado == 1:
            GPIO.output(pin, GPIO.HIGH)
            print ("Encendido")
            return "Encendido"
        elif estado == 0:
            GPIO.output(pin, GPIO.LOW)
            print("Apagado")
            return "Apagado"

    def Refrigerador(self,pin):
        GPIO.setmode(GPIO.BCM)
        
        GPIO.setup(pin, GPIO.IN, pull_up_down = GPIO.PUD_UP)

        if GPIO.input(pin) == 1:
            print("puerta abierta")
            return "abierta"
        elif GPIO.input(pin) == 0:
            print("puerta cerrada")
            return "cerrada"

