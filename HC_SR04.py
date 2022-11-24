# ====================================
# HC_SR04.py
# ------------------------------------
# 超音波測距モジュール用ライブラリ
# ------------------------------------
# 2022/11/24
# T19JM042 長谷季樹
# ====================================

import RPi.GPIO as GPIO
import time

# タイムアウト時間設定
TIMEOUT = 0.1   # [s]

# HIGH or LOWの時計測
# 秒数を返す (タイムアウト時は-1)
def pulseIn(PIN, start=1, end=0):
    
    timeout = False
    if start==0: end = 1
    t_start = 0
    t_end = 0

    # ECHO_PINがHIGHである時間を計測
    timeout_start = time.time()
    while GPIO.input(PIN) == end:
        timeout_end = time.time()
        if TIMEOUT < timeout_end-timeout_start:
            return -1
    t_start = time.time()
        
    # ECHO_PINがLOWである時間を計測
    timeout_start = time.time()
    while GPIO.input(PIN) == start:
        timeout_end = time.time()
        if TIMEOUT < timeout_end-timeout_start:
            return -1
    t_end = time.time()

    return t_end - t_start  # [s]

# 距離計測(平均)
# num   : 計測回数
# temp  : 気温 [℃]
def get_distance(TRIG_PIN, ECHO_PIN, num=1, temp=24):

    # 気温24[℃]の場合の音速[cm/s]
    v = 33150 + 60*temp

    GPIO.setmode(GPIO.BCM)
    GPIO.setup(TRIG_PIN,GPIO.OUT)
    GPIO.setup(ECHO_PIN,GPIO.IN)
    
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

        # タイムアウト時はカウントせずやり直し
        if t == -1:
            continue

        distance = v * t/2      # 距離[cm] = 音速[cm/s] * 時間[s]/2
        distance = distance*10  # [cm] → [mm]

        distances.append(distance)
        i += 1

    # 平均
    average = sum(distances)/len(distances)
            
    GPIO.cleanup(TRIG_PIN)
    GPIO.cleanup(ECHO_PIN)

    return average


if __name__ == "__main__":

    print("=== HC_SR04.py ===")

    TRIG_PIN = 15
    ECHO_PIN = 14

    try:
        while True:
            distance_mm = get_distance(TRIG_PIN, ECHO_PIN, num=10, temp=20)
            print("\r" + str(distance_mm) + " [mm]  ", end="")
            time.sleep(0.01)

    except KeyboardInterrupt:
        GPIO.cleanup()
        print("")