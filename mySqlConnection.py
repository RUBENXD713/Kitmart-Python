import mysql.connector

class mySql():
    sensoresList = []
    def __init__(self):
        self.mydb = mysql.connector.connect(
        host="localhost",
        user="admin",
        password="123456789",
        database="Raspberry2" 
        )
        
    def getSensoresList(self):
        mycursor = self.mydb.cursor()
        sql = "SELECT * FROM sensores" 
        mycursor.execute(sql)
        self.sensoresList = mycursor.fetchall()
        print(self.sensoresList)
        return self.sensoresList

    def createDataBase(self):
        mycursor = self.mydb.cursor()
        mycursor.execute("CREATE DATABASE IF NOT EXISTS Raspberry2")
        
    def InsertarRegistro(self, Sensor, Valor):
        mycursor = self.mydb.cursor()
        #sql = "SELECT idSensor as id FROM sensores where Nombre = %s"
        #value = (Sensor, )
        #mycursor.execute(sql, value)
        sql = "INSERT INTO registros (Sensor, Valor, Fecha) VALUES (%s, %s, NOW())"
        value = 0
        for lista in self.sensoresList:
            if lista[1] == Sensor:
                value = lista[0]
                #print(value)
        #e = str(mycursor.fetchone()[0]) 
        val = (value, Valor)
        mycursor.execute(sql,val)
        self.mydb.commit()

    def CreateTableReg(self):
        mycursor = self.mydb.cursor()
        mycursor.execute("CREATE TABLE IF NOT EXISTS registros (idR INT AUTO_INCREMENT PRIMARY KEY, Sensor INT, Valor VARCHAR(255), Fecha DATETIME)")

    def CreateTableSensor(self):
        mycursor = self.mydb.cursor()
        mycursor.execute("CREATE TABLE IF NOT EXISTS sensores (idR INT AUTO_INCREMENT PRIMARY KEY, Nombre varchar(100), Descripcion varchar(200),Tipo CHAR, pinIn INT, pinOut INT,tema varchar(200))")
#--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
