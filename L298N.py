import RPi.GPIO as GPIO

IN1 = 10
IN2 = 9
FREQ = 50

class DC_motor():

    in1 = None
    in2 = None
    p1 = None
    p2 = None

    def __init__(self, in1, in2, f, reverse=False):

        self.in1 = in1
        self.in2 = in2
        self.revase = reverse

        # GPIO設定
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(in1, GPIO.OUT)
        GPIO.setup(in2, GPIO.OUT)

        # PWM設定
        self.p1 = GPIO.PWM(in1, f) #50Hz
        self.p2 = GPIO.PWM(in2, f) #50Hz

        # PWM出力開始
        self.p1.start(0)
        self.p2.start(0)

    # 回転
    def rotate(self, dir, duty):

        if dir=="CW":
            # print("CW")
            if self.revase==False:
                self.rotate_CW(duty)
            elif self.revase==True:
                self.rotate_CCW(duty)
        elif dir=="CCW":
            # print("CCW")
            if self.revase==False:
                self.rotate_CCW(duty)
            elif self.revase==True:
                self.rotate_CW(duty)

    # 停止
    def stop(self):
        self.p1.ChangeDutyCycle(0)
        self.p2.ChangeDutyCycle(0)

    # 時計回り
    def rotate_CW(self, duty):
        self.p1.ChangeDutyCycle(0)
        self.p2.ChangeDutyCycle(duty)
    
    # 反時計周り
    def rotate_CCW(self, duty):
        self.p1.ChangeDutyCycle(duty)
        self.p2.ChangeDutyCycle(0) 

    # 終了
    def end(self):
        GPIO.cleanup(self.in1)
        GPIO.cleanup(self.in2)

if __name__ == "__main__":

    import time

    motor1 = DC_motor(IN1, IN2, FREQ)

    print('direction chenge : "CW" or "CCW')
    print('rotate : "" (Enter)')
    print('end : "end"')
    
    dir = "CW"

    try:

        while True:

            oder = input("")

            if oder=="":
                motor1.rotate(dir, 30)
                time.sleep(0.05)
                motor1.stop()

            elif oder=="CW":
                dir = oder

            elif oder=="CCW":
                dir = oder

            elif oder=="end":
                break

    except:

        motor1.end()


        