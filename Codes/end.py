from subprocess import call
import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)

GPIO.setup(3, GPIO.IN, pull_up_down=GPIO.PUD_UP)

try:
 while True:
   GPIO.wait_for_edge(3, GPIO.FALLING)
   call(['sudo killall -9 timidity'], shell=True)
   call(['sudo killall -9 python3'], shell=True)
   time.sleep(3)
   call(['sudo poweroff -f'], shell=True)

except:
 GPIO.cleanup()


