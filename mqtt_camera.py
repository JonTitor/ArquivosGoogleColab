#!/usr/bin/env python
"""
Capture frames from a camera using OpenCV and publish on an MQTT topic.
"""
import os
import time

from helpers import get_config, get_now_string, pil_image_to_byte_array
from imutils import opencv2matplotlib
from imutils.video import VideoStream
from mqtt import get_mqtt_client
from PIL import Image

MQTT_BROKER = '142.93.58.237'
MQTT_PORT = 3000
MQTT_QOS = 1

MQTT_TOPIC_CAMERA = "/usb_cam/image_raw_mqtt"
VIDEO_SOURCE = 0
FPS =  30


def main():
    client = get_mqtt_client()
    client.connect(MQTT_BROKER, port=MQTT_PORT)
    time.sleep(4)  # Wait for connection setup to complete
    client.loop_start()

    # Open camera
    camera = VideoStream(src=VIDEO_SOURCE, framerate=FPS).start()
    time.sleep(2)  # Webcam light should come on if using one

    while True:
        frame = camera.read()
        np_array_RGB = opencv2matplotlib(frame)  # Convert to RGB

        image = Image.fromarray(np_array_RGB)  #  PIL image
        byte_array = pil_image_to_byte_array(image)
        client.publish(MQTT_TOPIC_CAMERA, byte_array, qos=MQTT_QOS)
        now = get_now_string()
        
        time.sleep(1 / FPS)


if __name__ == "__main__":
    main()