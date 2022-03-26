import microlite
import urequests as requests
import camera
import time
import machine
import csvwriter
import uasyncio as asyncio
import os


rtc = machine.RTC()    


class PlateDetector():
    def __init__(self,modelpath):
        # load file
        with open (modelpath, 'rb') as plate_detection_model_file:
            plate_detection_model = plate_detection_model_file.read()
        # setup interpreter
        def dummycallback(x):
            pass
        self.microlite_interpreter = microlite.interpreter(plate_detection_model,136*1024, dummycallback, dummycallback)

    def process_image(self,image):
        # prepare input
        inputTensor = self.microlite_interpreter.getInputTensor(0)
        for i in range (0, len(image)): 
            inputTensor.setValue(i, image[i])

        self.microlite_interpreter.invoke()

        # prepare ouput
        outputTensor = self.microlite_interpreter.getOutputTensor(0)
        not_a_plate = outputTensor.getValue(0)
        plate = outputTensor.getValue(1)

        #We return true if the trust of plate > not_a_plate
        return plate>not_a_plate

class PlateVisionApi():
    def __init__(self, apikey,url):
        self.header = { 'accept': 'application/json','Content-Type': 'image/jpg','X-API-Key': apikey }
        self.url = url

    def call(self,imagebytes):
        response = requests.post(self.url,
                             headers = self.header,
                             data = imagebytes)
        return response.json()


async def main():
    plate_detector = PlateDetector('plate_model_quant.tflite')
    plate_api = PlateVisionApi('rkPk9W990e7B8UHpbGEKw2TLa1715MyA0APY9Rhe','http://192.168.0.112:8080/recognize/body?profile=eu_ir')
    led_frontal = machine.Pin(4, machine.Pin.OUT)
    back_led = machine.Pin(33, machine.Pin.OUT)
    print ("Starting camera...")

    #Loop principal
    while True:
        #Inicializar camara em grayscale mode
        camera.deinit()
        camera.init(0, format=camera.GRAYSCALE, framesize=camera.FRAME_96X96,xclk_freq=camera.XCLK_10MHz);
        #Loop de captura de imagens em grayscale:
        while True:
            await asyncio.sleep(0.01)
            print(".", end="")
            #Capturar a imagem da camara
            gray_image = camera.capture()
            #Se nao foi devolvido imagem continuar
            if not gray_image:
                continue
            #Processar a imagem da camara
            result = plate_detector.process_image(gray_image)
            #if True sair do loop
            if result:
                break
        #Ligar LED Frontal 
        led_frontal.value(1)
        #Inicializar camara em JPEG, frame VGA
        camera.deinit()
        
        camera.init(0, format=camera.JPEG, framesize=camera.FRAME_VGA, xclk_freq=camera.XCLK_10MHz) 
        #Capturar a imagem da camara
        with open("/sd/photo.jpg", "w") as imgfile:
            imgfile.write(camera.capture())
            imgfile.close()
        jpeg = camera.capture()        
        #Desligar LED Frontal
        led_frontal.value(0)
        #Invocar platevisionapi.call com a imagem capturada pela camara
        finalResult = plate_api.call(jpeg)
        if len(finalResult['plates'])>0 and len(finalResult['plates'][0]['results'])>0:
            plateText = (finalResult['plates'][0]['results'][0]['rawText'])
            try:
                if csvwriter.authPlate(plateText):
                    authorizedLed = machine.Pin(0, machine.Pin.OUT)
                    print(plateText)
                    print("Authorized.\nOpening the barrier")
                    authorizedLed.value(1)
                    time.sleep(0.5)
                    authorizedLed.value(0)
                    time.sleep(0.5)
                    authorizedLed.value(1)
                    time.sleep(0.5)
                    authorizedLed.value(0)
                    t = rtc.datetime()
                    hour1 = '{:02d}/{:02d}/{:02d}T{:02d}:{:02d}:{:02d}'.format(t[2], t[1], t[0], t[4], t[5], t[3])
                    csvwriter.SDdetectionHistory(plateText, hour1, state = "Authorized")
                    print("License plate detected and saved to SD Card CSV File.")
                else:
                    t = rtc.datetime()
                    hour2 = '{:02d}/{:02d}/{:02d}T{:02d}:{:02d}:{:02d}'.format(t[2], t[1], t[0], t[4], t[5], t[3])
                    print(plateText)
                    print("Plate is not authorized, please speak to the managers")
                    csvwriter.SDdetectionHistory(plateText, hour2, state = "Not authorized")
                    print("License plate detected and saved to SD Card CSV File.")
            except:
                print("No SD Card found! Saving in memory...")
                if csvwriter.authPlate(plateText):
                    print("Authorized.\nOpening the barrier")
                    authorizedLed.value(1)
                    time.sleep(2)
                    authorizedLed.value(0)
                    t = rtc.datetime()
                    hour1 = '{:02d}/{:02d}/{:02d}T{:02d}:{:02d}:{:02d}'.format(t[2], t[1], t[0], t[4], t[5], t[3])
                    csvwriter.detectionHistory(plateText, hour1, state = "Authorized")
                    print("License plate detected and saved to CSV File.")
                else:
                    t = rtc.datetime()
                    hour2 = '{:02d}/{:02d}/{:02d}T{:02d}:{:02d}:{:02d}'.format(t[2], t[1], t[0], t[4], t[5], t[3])
                    print(plateText)
                    print("Plate is not authorized, please speak to the managers")
                    csvwriter.detectionHistory(plateText, hour2, state = "Not authorized")
                    print("License plate detected and saved to CSV File.")
        else:
            print("No licenses were found")
    


       