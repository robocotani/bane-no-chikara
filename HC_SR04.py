
import RPi.GPIO as GPIO
import time

TIMEOUT = 0.1

# HIGH or LOWの時計測
def pulseIn(PIN, start=1, end=0):
    
    timeout = False
    if start==0: end = 1
    t_start = 0
    t_end = 0

    timeout_start = time.time()
    # ECHO_PINがHIGHである時間を計測
    while GPIO.input(PIN) == end:
        timeout_end = time.time()
        if TIMEOUT < timeout_end-timeout_start:
            return -1
    t_start = time.time()
        
    timeout_start = time.time()
    while GPIO.input(PIN) == start:
        timeout_end = time.time()
        if TIMEOUT < timeout_end-timeout_start:
            return -1
    t_end = time.time()

    return t_end - t_start

# 距離計測
def get_distance(TRIG_PIN, ECHO_PIN, num=1, temp=24):

    # 気温24[℃]の場合の音速[cm/s]
    v = 33150 + 60*temp

    GPIO.setmode(GPIO.BCM)
    GPIO.setup(TRIG_PIN,GPIO.OUT)
    GPIO.setup(ECHO_PIN,GPIO.IN)
    # GPIO.setwarnings(False)
    
    distances = []

    i = 0

    while i < num:

        # TRIGピンを0.001[s]だけLOW
        GPIO.output(TRIG_PIN, GPIO.LOW)
        time.sleep(0.001)

        # TRIGピンを0.00001[s]だけ出力(超音波発射)        
        GPIO.output(TRIG_PIN, True)
        time.sleep(0.00001)
        GPIO.output(TRIG_PIN, False)
        
        t = pulseIn(ECHO_PIN)   # HIGHの時間計測

        if t == -1:
            continue
            # return -1

        distance = v * t/2      # 距離[cm] = 音速[cm/s] * 時間[s]/2
        distance = distance*10  # [cm] → [mm]

        # print(distance, "mm")
        distances.append(distance)
        i += 1

    # 平均
    average = sum(distances)/len(distances)
            
    GPIO.cleanup(TRIG_PIN)
    GPIO.cleanup(ECHO_PIN)

    return average


if __name__ == "__main__":

    TRIG_PIN = 15
    ECHO_PIN = 14

    try:
        while True:
            distance_mm = get_distance(TRIG_PIN, ECHO_PIN, num=10, temp=20)
            print(str(distance_mm) + " [mm]")
            time.sleep(0.01)

    except KeyboardInterrupt:
        GPIO.cleanup()