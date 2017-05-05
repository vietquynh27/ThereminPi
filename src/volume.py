# -*- coding: utf-8 -*-

import RPi.GPIO as GPIO
import subprocess
import time
import math
import statistics

def prepare(GPIO_TRIGGER, GPIO_ECHO):
    GPIO.setup(GPIO_TRIGGER, GPIO.OUT)
    GPIO.setup(GPIO_ECHO, GPIO.IN)
    GPIO.output(GPIO_TRIGGER, False)
    time.sleep(0.1)
    
def get_distance(GPIO_TRIGGER, GPIO_ECHO):
    GPIO.output(GPIO_TRIGGER, True)
    time.sleep(0.00001)
    GPIO.output(GPIO_TRIGGER, False)
    try:
        while GPIO.input(GPIO_ECHO)==0:
            start = time.time()
    except Exception:
        pass
    try:
        while GPIO.input(GPIO_ECHO)==1:
            stop = time.time()
    except Exception:
        pass
    elapsed = stop - start
    distance = (elapsed * 34300)/2
    return int(distance)

      

def get_vol(dist):
   minDist = 6
   maxDist = 56
   minVol = 50
   maxVol = 100

   if (dist>maxDist):
        vol=minVol
   elif (dist<minDist):
        vol=maxVol
   else:
    fup = (dist - minDist)*(maxVol-minVol)
    fdown = (maxDist - minDist)
    vol = maxVol - (fup/fdown)

   return int(vol) 


GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

GPIO_TRIGGER = 25
GPIO_ECHO = 8

prepare(GPIO_TRIGGER, GPIO_ECHO)

vol = 50

try:
    while True:
        b4vol = vol
        vliste = []
        print('starte Messung')
        while len(vliste) < 3:
            dist = get_distance(GPIO_TRIGGER, GPIO_ECHO)
            if dist is None:
                dist = dist_alt
            vliste.append(dist)
        time.sleep(0.1)
        median_dist = statistics.median(vliste)
        print("median:", median_dist)
        str(median_dist)
        del vliste [:]
        vol = get_vol(median_dist)
        print(vol)
        str(vol)
        dist_alt = dist
        subprocess.call("amixer sset Master,0 {}%".format(vol), shell=True)
        time.sleep(0.2)
        
except KeyboardInterrupt:
    GPIO.cleanup()
GPIO.cleanup()
