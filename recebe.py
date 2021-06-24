#!/usr/bin/env python
import cv2
import numpy
#from simple_pid import PID
import time
import json
import paho.mqtt.client as mqtt
#from cv_bridge import CvBridge
from timeit import default_timer as timer
import os

import sys

mqttc = mqtt.Client()

Porcentagem = 50
Qualidade = 20

def on_message(mqttc, obj, msg):
    print(msg.topic + " " + str(msg.qos) + " " + str(msg.payload))

def on_message_msgs(mosq, obj, msg):
    global time

    time = 0
    data = numpy.fromstring(msg.payload, dtype='uint8')
    imageBGR=cv2.imdecode(data,cv2.IMREAD_COLOR)
    imageRGB = cv2.cvtColor(imageBGR , cv2.COLOR_BGR2RGB)

    #encode_param=[int(cv2.IMWRITE_JPEG_QUALITY),100]
    result, imgencode = cv2.imencode('.jpg', imageRGB)
    data = numpy.array(imgencode)
    stringData = data.tostring()
    mqttc.publish("/usb_cam/image_raw_mqtt2", stringData,  qos=1)                                              
      

def conecta():
	global mqttc
	mqttc = mqtt.Client()
	mqttc.on_message = on_message
	mqttc.message_callback_add("/usb_cam/image_raw_mqtt", on_message_msgs)    
	#mqttc.connect("10.181.2.30", 1883)
	mqttc.connect("142.93.58.237", 3000)
	#mqttc.connect("mqtt.googleapis.com", 8883)
	print("Conectado!")
	

if __name__ == '__main__':

	conecta()
	mqttc.subscribe("/usb_cam/image_raw_mqtt", 1)
	mqttc.loop_start()
	while True:
		print("")
			

