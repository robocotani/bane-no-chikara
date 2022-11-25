import L298N

class move():

    PIN1 = 6
    PIN2 = 13
    PIN3 = 5
    PIN4 = 0

    freq = 50

    def __init__(self):

        self.tire_R = L298N.DC_motor(self.PIN1, self.PIN2, self.freq, reverse=True)
        self.tire_L = L298N.DC_motor(self.PIN3, self.PIN4, self.freq)

    def forward(self, duty):
        self.tire_L.rotate("CW", duty)
        self.tire_R.rotate("CW", duty)

    def back(self, duty):
        self.tire_L.rotate("CCW", duty)
        self.tire_R.rotate("CCW", duty)

    def right_rotation(self, duty):
        self.tire_L.rotate("CW", duty)
        self.tire_R.rotate("CCW", duty)

    def left_rotation(self, duty):
        self.tire_L.rotate("CCW", duty)
        self.tire_R.rotate("CW", duty)

    def right_rotation_back(self, duty):
        self.tire_L.stop()
        self.tire_R.rotate("CCW", duty)

    def left_rotation_back(self, duty):
        self.tire_L.rotate("CCW", duty)
        self.tire_R.stop()

    def stop(self):
        self.tire_L.stop()
        self.tire_R.stop()

    def end(self):
        self.tire_L.end()
        self.tire_R.end()

if __name__ == "__main__":

    print("=== move.py ===")
    print("-----------------------------")
    print("[command]")
    print("  f : forward")
    print("  b : back")
    print("  r : right rotation")
    print("  l : left rotation")
    print("  rb : right rotation back")
    print("  lb : lfet rotation back")
    print("-----------------------------")
    print("「f 50」 → move forward (duty50%)")
    print("end with Ctrl+C")
    print("-----------------------------")

    move_ = move()

    try:
        while True:

            command = input('command : ')
            try:
                oder, duty = command.split()
                duty = int(duty)
            except:
                oder = command
                duty = 50

            if oder=="f":
                move_.forward(duty)
            if oder=="b":
                move_.back(duty)
            if oder=="r":
                move_.right_rotation(duty)
            if oder=="l":
                move_.left_rotation(duty)
            if oder=="rb":
                move_.right_rotation_back(duty)
            if oder=="lb":
                move_.left_rotation_back(duty)
            if oder=="s":
                move_.stop()

    except KeyboardInterrupt:
        move_.end()
        print("")