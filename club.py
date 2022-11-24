import time
import HC_SR04
import L298N
import MG996R


class club():

    # ホールド位置
    hold_dis = 28

    # 許容誤差
    pull_dis_target_range = 1   # [mm]

    # HC_SR04
    TRIG_PIN = 15
    ECHO_PIN = 14

    # L298N
    IN3_PIN = 10
    IN4_PIN = 9
    FREQ = 50
    duty = 60

    # MG996R
    SIG_PIN = 24
    hold_angle = 0
    release_angle = -25
    sleep_for_servo = 0.5   # [s]

    hold = False
    DC_motor = None
    servo = None

    # 初期化
    def __init__(self, duty=60):

        self.duty = duty

        self.DC_motor = L298N.DC_motor(self.IN3_PIN, self.IN4_PIN, self.FREQ)
        
        self.servo = MG996R.MG996R(self.SIG_PIN)
        self.servo.update_angle(0)

    def shot(self, target_shot_dis):
        target_pull_dis = target_shot_dis / 20
        self.shot_from_pull_dis(target_pull_dis)

    def shot_from_pull_dis(self, target_pull_dis):
        if self.hold == False:
            self.sheer_hold()
        self.sheer_move(target_pull_dis, self.duty)
        self.sheer_release()

    # ホールド (最下端へ移動+ホールド)
    def sheer_hold(self):
        if self.hold == False:
            self.sheer_move(100, self.duty)
            self.sheer_move(80, self.duty)
            self.servo.update_angle(self.release_angle)
            self.sheer_move(self.hold_dis, self.duty)
            self.servo.update_angle(self.hold_angle)
            self.hold = True
            time.sleep(self.sleep_for_servo)

    # リリース
    def sheer_release(self):
        self.servo.update_angle(self.release_angle)
        self.hold = False

    # シアー移動
    def sheer_move(self, target_pull_dis, duty):

        while True:

            self.now_pull_dis = HC_SR04.get_distance(self.TRIG_PIN, self.ECHO_PIN, num=5, temp=20)
            print("\rsheer distance = " + str(self.now_pull_dis) + " [mm]  ", end="")

            if self.now_pull_dis == -1:
                self.DC_motor.stop()

            if self.now_pull_dis <= target_pull_dis-self.pull_dis_target_range:
                self.sheer_up(duty)
            elif target_pull_dis+self.pull_dis_target_range <= self.now_pull_dis:
                self.sheer_down(duty)
            else:
                self.DC_motor.stop()
                break

        print("")
        return self.now_pull_dis

    def sheer_up(self, duty):
        self.DC_motor.rotate("CW", duty)

    def sheer_down(self, duty):
        self.DC_motor.rotate("CCW", duty)

    def sheer_stop(self):
        self.DC_motor.stop()

    def end(self):
        self.servo.update_angle(self.hold_angle)
        time.sleep(self.sleep_for_servo)
        self.DC_motor.end()
        self.servo.end()

if __name__ == "__main__":

    print("=== club.py ===")
    print("[command]")
    print(" ・move x (x is distance[mm])")
    print(" ・hold")
    print(" ・release")
    print("end with Ctrl+C")
    print("---------------")
    
    club_ = club()

    club_.now_pull_dis = HC_SR04.get_distance(club_.TRIG_PIN, club_.ECHO_PIN, num=5, temp=20)

    try:
        while True:

            command = input('command : ')
            try:
                oder, option = command.split()
            except:
                oder = command
                option = None

            if oder=="move":
                if option is None:
                    option = input("distance:")
                dis = club_.sheer_move(int(option), club_.duty)
            if oder=="hold":
                club_.sheer_hold()
            if oder=="release":
                club_.sheer_release()

    except KeyboardInterrupt:
        club_.end()
        print("")