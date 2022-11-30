import cv2
import RPi.GPIO as GPIO
import sys
import time


#GPIO初期設定------------
GPIO.setmode(GPIO.BCM)
GPIO.setup(6, GPIO.OUT)
GPIO.setup(13, GPIO.OUT)
GPIO.setup(5, GPIO.OUT)
GPIO.setup(0, GPIO.OUT)

#左
p1 = GPIO.PWM(6, 50) #50Hz
p2 = GPIO.PWM(13, 50) #50Hz
#右
p3 = GPIO.PWM(5, 50) #50Hz
p4 = GPIO.PWM(0, 50) #50Hz
  

duty = 30
            
p1.start(0) 
p2.start(0)  
p3.start(0) 
p4.start(0) 
#------------------------


try:
    while True:
    #モーター制御------------------
        #「e」キーが押されたら後退
        c = sys.stdin.read(1)
        if c == 'e':
            p1.ChangeDutyCycle(0)
            p2.ChangeDutyCycle(duty)
            p3.ChangeDutyCycle(duty)
            p4.ChangeDutyCycle(0)
            time.sleep(1.2)
            p1.ChangeDutyCycle(0)
            p2.ChangeDutyCycle(0)
            p3.ChangeDutyCycle(0)
            p4.ChangeDutyCycle(0)
              
        #「d」キーが押されたら前進
        if c == 'd':
            p1.ChangeDutyCycle(duty)
            p2.ChangeDutyCycle(0)
            p3.ChangeDutyCycle(0)
            p4.ChangeDutyCycle(duty)

        #「q」キーが押されたら止まる
        if c == 'q':
            p1.ChangeDutyCycle(0)
            p2.ChangeDutyCycle(0)
            p3.ChangeDutyCycle(0)
            p4.ChangeDutyCycle(0)
        #-----------------------------


except KeyboardInterrupt:
    GPIO.cleanup()
    pass


