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

dir_path = os.path.dirname(os.path.realpath(__file__))
sys.path.append('/usr/local/python');
try:
    from openpose import pyopenpose as op
except ImportError as e:
    print(
        'Error: OpenPose library could not be found. Did you enable `BUILD_PYTHON` in CMake and have this Python script in the right folder?')
    raise e
def set_params():

        params = dict()
        params["model_folder"] = "/content/openpose/models/"
        #params["hand"] = True

        return params

params = set_params()
#openpose = OpenPose(params)
opWrapper = op.WrapperPython()
opWrapper.configure(params)
opWrapper.start()
datum = op.Datum()
mqttc = mqtt.Client()

def on_message(mqttc, obj, msg):
    print(msg.topic + " " + str(msg.qos) + " " + str(msg.payload))

def on_message_msgs(mosq, obj, msg):
    global time

    time = 0
    data = numpy.fromstring(msg.payload, dtype='uint8')
    imageBGR=cv2.imdecode(data,cv2.IMREAD_COLOR)
    imageRGB = cv2.cvtColor(imageBGR , cv2.COLOR_BGR2RGB)




    
    imageToProcess = imageRGB
    datum.cvInputData = imageToProcess
    opWrapper.emplaceAndPop(op.VectorDatum([datum])) 
    #encode_param=[int(cv2.IMWRITE_JPEG_QUALITY),100]
    result, imgencode = cv2.imencode('.jpg', datum.cvOutputData)
    data = numpy.array(imgencode)
    stringData = data.tostring()
		#print len(stringData)
    mqttc.publish("/usb_cam/image_raw_mqtt2", stringData,  qos=1)                                              
      

def conecta():
	global mqttc
	mqttc = mqtt.Client()
	mqttc.on_message = on_message
	mqttc.message_callback_add("/usb_cam/image_raw_mqtt", on_message_msgs)    
	mqttc.connect("142.93.58.237", 3000)
	print("Conectado!")
	

if __name__ == '__main__':

	conecta()
	mqttc.subscribe("/usb_cam/image_raw_mqtt", 1)
	mqttc.loop_start()
	while True:
		print("")	

