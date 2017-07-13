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
    time.sleep(0.08)
    elapsed = stop - start
    distance = (elapsed * 34300)/2
    return int(distance)

def get_vol(dist):
    minDist = 6
    maxDist = 40
    minVol = 80
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

def append_list (vliste, single_dist):
    vliste.pop(0)
    vliste.append(single_dist)
    return vliste

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

GPIO_TRIGGER = 25
GPIO_ECHO = 8

prepare(GPIO_TRIGGER, GPIO_ECHO)

vol = 50

vliste = [0]*5

try:
    while True:
        time.sleep(0.1)
        b4vol = vol
        single_dist = get_distance(GPIO_TRIGGER, GPIO_ECHO)
        vliste = append_list (vliste, single_dist)
        median_dist = statistics.median(vliste)
        vol = get_vol(median_dist)
        subprocess.call("amixer sset PCM,0 {}%".format(vol), shell=True)
     
except KeyboardInterrupt:
    GPIO.cleanup()
GPIO.cleanup()
