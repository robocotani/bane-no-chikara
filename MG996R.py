import time
import RPi.GPIO as GPIO

SIG_PIN = 24

class MG996R():

    sig_pin = 24

    def __init__(self, sig_pin):

        self.sig_pin = sig_pin

        # GPIO
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(sig_pin, GPIO.OUT)

        # PWM
        self.p = GPIO.PWM(sig_pin, 50)
        self.p.start(0.0)
        self.update_angle(0)
        self.p.start(0.0)

    def update_angle(self, degree):
        dc = 2.5 + (12.0-2.5)/180*(degree+90)
        self.p.ChangeDutyCycle(dc)
        time.sleep(1)
        self.p.start(0.0)

    def end(self):
        GPIO.cleanup(self.sig_pin)


if __name__ == "__main__":

    servo = MG996R(SIG_PIN)

    try:

        while True:

            # servo.update_angle(0)
            # time.sleep(1)
            # servo.update_angle(-25)
            # time.sleep(1)

            angle = int(input("angle:"))
            servo.update_angle(angle)

    except:
        servo.end()
        print("")