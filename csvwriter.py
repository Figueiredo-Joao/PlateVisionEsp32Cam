import machine
import os

FNAME = "authorized.csv"
FNAME2 = "detectHistory.csv"
SDFNAME = "/sd/authorized.csv"
SDFNAME2 ="/sd/detectHistory.csv"

PLATES = []

isSDMounted = False

def addAuthPlate(plate):
    PLATES.append(plate)
    authPlates(PLATES)

def removePlate(plate):
    PLATES.remove(plate)
    authPlates(PLATES)

    
def detectionHistory(time, plate, state):
    file = open (FNAME2, "a")
    file.write("%s, %s, %s"%(time,plate,state+"\n"))
    file.close()
    
def authPlates(authList):
    file = open (FNAME, "w")
    for value in authList:
        file.write(value + "\n")
    file.close()
    
def SD():
    global isSDMounted
    try:
        sd = machine.SDCard(slot=1)
        os.mount(sd, "/sd")
        isSDMounted = True
        print(isSDMounted)
    except:
        isSDMounted = False
        print(isSDMounted)
  
    
def readPlatesFromFile():
    global PLATES
    with open(FNAME, "r") as f:
        lines = f.read().splitlines()
        PLATES = []
        for allowed in lines:
            PLATES.append(allowed)
        return PLATES

def getPlatesFromMemory():
    return PLATES
        
def readPlatesFromDetection():
    with open(FNAME2, "r") as f:
        lines = f.read().splitlines()
        finalDetected = []
        for detected in lines:
            finalDetected.append(detected.split(','))
        return finalDetected
           
def SDdetectionHistory(time, plate, state):
    file = open (SDFNAME2, "a")
    file.write("%s, %s, %s"%(time,plate,state+"\n"))
    file.close()
            



#Lista de plates autorizads: Input de matriculas manuais neste caso se for para uma empresa com um parque de estacionamento por exemplo
#Quando um empregado é contratado dá a informação da sua matricula e esta é posta manualmente na lista de autorizados
#Se for autorizado a cancela abre se nao fecha

def authPlate(plate):
    if plate in PLATES:
        return True
    else:
        return False


SD()