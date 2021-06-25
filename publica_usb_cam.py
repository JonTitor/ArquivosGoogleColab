#!/usr/bin/env python
import os
import cv2
import numpy
from simple_pid import PID
from cv_bridge import CvBridge
import paho.mqtt.client as mqtt
import os, rospkg
from imutils.video import VideoStream
import time
from imutils import opencv2matplotlib
from PIL import Image
import io
mqttc = mqtt.Client()
diminuir_imagem = False
Porcentagem = 50
Qualidade = 100
start = 0

def on_message(mqttc, obj, msg):
    print(msg.topic + " " + str(msg.qos) + " " + str(msg.payload))

def on_message_msgs(mosq, obj, msg):
    global time

    time = 0
    data = numpy.fromstring(msg.payload, dtype='uint8')
    encode_param=[int(cv2.IMWRITE_JPEG_QUALITY),Qualidade]
    imageBGR=cv2.imdecode(data,cv2.IMREAD_COLOR)
    imageRGB = cv2.cvtColor(imageBGR , cv2.COLOR_BGR2RGB)
    cv2.imshow('Robot Cam',imageRGB)
    cv2.waitKey(1)
    print("passou")
   

def conecta():
	global mqttc
	mqttc = mqtt.Client()
	mqttc.message_callback_add("/usb_cam/image_raw_mqtt2", on_message_msgs) 
	#mqttc.connect("10.181.2.30", 1883)
	mqttc.connect("142.93.58.237", 3000)
	#mqttc.connect("mqtt.googleapis.com", 8883)
	mqttc.loop_start()	
	print("Conectado!")

def pil_image_to_byte_array(image):
    imgByteArr = io.BytesIO()
    image.save(imgByteArr, "PNG")
    return imgByteArr.getvalue()	




if __name__ == '__main__':
	conecta()
	mqttc.subscribe("/usb_cam/image_raw_mqtt2", 1)
    
	#camera = VideoStream(src=4, framerate=60 ).start()
	#cam = cv2.VideoCapture(0)
	mqttc.loop_start()
	while True:
		timev = 1
		#ret_val, frame = cam.read()
	
		
		
		#frame = camera.read()		
                #frame = bridge.imgmsg_to_cv2(camera.read(), desired_encoding='passthrough')
             #   try:
             #           if diminuir_imagem == True:
				        #modifica o tamnho da figura
			#				scale_percent = Porcentagem # percent of original size
			#				width = int(frame.shape[1] * scale_percent / 100)
			#				height = int(frame.shape[0] * scale_percent / 100)
			#				dim = (width, height)
			#				# resize image
			#				resized = cv2.resize(frame, dim, interpolation = cv2.INTER_AREA)
			#				frame = resized
				        
		#except:
		#	print "Erro ao obter o video, verifique se esta na fonte certa"

		#np_array_RGB = opencv2matplotlib(frame)  # Convert to RGB

		#image = Image.fromarray(np_array_RGB)  #  PIL image
		#byte_array = pil_image_to_byte_array(image)
		#mqttc.publish("/usb_cam/image_raw_mqtt", byte_array,  qos=0)
		
		
			
		#try:
			#encode_param=[int(cv2.IMWRITE_JPEG_QUALITY)]
			#result, imgencode = cv2.imencode('.png', frame, encode_param)
			#data = numpy.array(imgencode)
			#stringData = data.tostring()
			#print len(stringData)
			#mqttc.publish("/usb_cam/image_raw_mqtt", stringData,  qos=1)                                              
		       
		#except:
			#sock.close()
			#time.sleep(2)
			#conecta()

