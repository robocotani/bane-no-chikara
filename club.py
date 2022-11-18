import HC_SR04
import L298N
import MG996R
import time
import RPi.GPIO as GPIO

class club():

    hold = False

    hold_dis = 25

    # HC_SR04
    TRIG_PIN = 15
    ECHO_PIN = 14

    # L298N
    IN3_PIN = 10
    IN4_PIN = 9
    FREQ = 50
    duty = 30

    # MG996R
    SIG_PIN = 24
    hold_angle = 0
    release_angle = -25

    pull_dis_target_range = 1   # [mm]

    DC_motor = None
    servo = None

    def __init__(self, duty=60):

        # GPIO.cleanup()

        self.duty = duty

        self.DC_motor = L298N.DC_motor(self.IN3_PIN, self.IN4_PIN, self.FREQ)
        
        self.servo = MG996R.MG996R(self.SIG_PIN)
        self.servo.update_angle(0)

        # self.DC_motor.rotate("CW", 30)
        # time.sleep(1)
        # self.DC_motor.stop()

    def shot(self, target_shot_dis):
        target_pull_dis = target_shot_dis / 20
        self.shot_from_pull_dis(target_pull_dis)

    def shot_from_pull_dis(self, target_pull_dis):
        if self.hold == False:
            self.sheer_hold()
        self.sheer_move(target_pull_dis, self.duty)
        self.sheer_release()

    def sheer_hold(self):
        if self.hold == False:
            self.sheer_move(100, self.duty)
            self.sheer_move(80, self.duty)
            self.servo.update_angle(self.release_angle)
            self.sheer_move(self.hold_dis, self.duty)
            self.servo.update_angle(self.hold_angle)
            self.hold = True
            time.sleep(1)

    def sheer_release(self):
        self.servo.update_angle(self.release_angle)
        self.hold = False

    def sheer_move(self, target_pull_dis, duty):

        while True:

            self.now_pull_dis = HC_SR04.get_distance(self.TRIG_PIN, self.ECHO_PIN, num=5, temp=20)
            if self.now_pull_dis == -1:
                DC_motor.stop()

            # print(self.now_pull_dis)

            if self.now_pull_dis <= target_pull_dis-self.pull_dis_target_range:
                # print("if1")
                self.sheer_up(duty)
            elif target_pull_dis+self.pull_dis_target_range <= self.now_pull_dis:
                self.sheer_down(duty)
                # print("if2")
            else:
                # print("if3")
                self.DC_motor.stop()
                break
            
            # time.sleep(1)                

        return self.now_pull_dis

    def sheer_up(self, duty):
        # print("up")
        self.DC_motor.rotate("CW", duty)

    def sheer_down(self, duty):
        # print("down")
        self.DC_motor.rotate("CCW", duty)

    def sheer_stop(self):
        self.DC_motor.stop()

    def end(self):
        self.servo.update_angle(self.hold_angle)
        self.DC_motor.end()
        self.servo.end()

if __name__ == "__main__":
    
    club_ = club()

    # club_.DC_motor.rotate("CW", 30)
    # time.sleep(1)
    # club_.DC_motor.
    # stop()
    club_.now_pull_dis = HC_SR04.get_distance(club_.TRIG_PIN, club_.ECHO_PIN, num=5, temp=20)

    # club_.sheer_down(30)
    # time.sleep(1)
    # club_.DC_motor.stop()


    try:
        while True:
            oder = input('"move" or "hold" or "release" : ')
            if oder=="move":
                distance = float(input("pull distance"))
                dis = club_.sheer_move(distance, club_.duty)
                print(dis)
            if oder=="hold":
                club_.sheer_hold()
            if oder=="release":
                club_.sheer_release()

    except:
        club_.end()