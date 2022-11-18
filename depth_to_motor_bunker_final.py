import os
os.environ["OPENCV_VIDEOIO_MSMF_ENABLE_HW_TRANSFORMS"] = "0"
import numpy as np
import cv2
import RPi.GPIO as GPIO
import pyrealsense2.pyrealsense2 as rs
import time
import M_ball
import M_flag
import M_bunker
import club
import HC_SR04


#距離計測用関数
def distance(center_x,center_y):
    #ボールとの距離は角度を補正
    #周囲の5点を取って平均
    #かけ離れている点は除外
    dist = []

    for i in range(5):
        for j in range(5):
            dist1 = depth_frame.get_distance(center_x + i, center_y + j)
            dist.append(float(format(dist1,'.4f')))
    
    #0.1m以下、3.5m以上の点は除外して平均
    dist_new = [i for i in dist if 0.1 < i < 3.5] 

    try:
        #ゼロ除算の対策
        dist_mean = sum(dist_new)/len(dist_new)
    except ZeroDivisionError:
        dist_mean = None

    return dist_mean


def move(duty):
    #前進
    p1.ChangeDutyCycle(duty)
    p2.ChangeDutyCycle(0)
    p3.ChangeDutyCycle(0)
    p4.ChangeDutyCycle(duty)
    


def down(duty):
    #後退
    p1.ChangeDutyCycle(0)
    p2.ChangeDutyCycle(duty)
    p3.ChangeDutyCycle(duty)
    p4.ChangeDutyCycle(0)



def right_rotation_back(duty):
    #前進(後ずさり)
    p1.ChangeDutyCycle(0)
    p2.ChangeDutyCycle(duty)
    p3.ChangeDutyCycle(0)
    p4.ChangeDutyCycle(0)


def right_rotation(duty):
    #前進
    p1.ChangeDutyCycle(0)
    p2.ChangeDutyCycle(duty)
    p3.ChangeDutyCycle(0)
    p4.ChangeDutyCycle(duty)
    
    

def left_rotation_back(duty):
    #左(後ずさり)
    p1.ChangeDutyCycle(0)
    p2.ChangeDutyCycle(0)
    p3.ChangeDutyCycle(duty)
    p4.ChangeDutyCycle(0)


def left_rotation(duty):
    #左
    p1.ChangeDutyCycle(duty)
    p2.ChangeDutyCycle(0)
    p3.ChangeDutyCycle(duty)
    p4.ChangeDutyCycle(0)
    

def stop():
    #停止
    p1.ChangeDutyCycle(0)
    p2.ChangeDutyCycle(0)
    p3.ChangeDutyCycle(0)
    p4.ChangeDutyCycle(0)
    
GPIO.cleanup()

#GPIO初期設定------------
GPIO.setmode(GPIO.BCM)

PIN1 = 6
PIN2 = 13
PIN3 = 5
PIN4 = 0
    

GPIO.setup(PIN1, GPIO.OUT)
GPIO.setup(PIN2, GPIO.OUT)
GPIO.setup(PIN3, GPIO.OUT)
GPIO.setup(PIN4, GPIO.OUT)

#左
p1 = GPIO.PWM(PIN1, 50) #50Hz
p2 = GPIO.PWM(PIN2, 50) #50Hz
#右
p3 = GPIO.PWM(PIN3, 50) #50Hz
p4 = GPIO.PWM(PIN4, 50) #50Hz
            
p1.start(0) 
p2.start(0) 
p3.start(0) 
p4.start(0) 

#------------------------

#フラグの設定
ball = True #下カメラ
depth = False
flag = False
hole = False #打球

#画面サイズ設定
size_w = 1280
size_h = 720

#ボール検出範囲設定
x1 = 400
x2 = 560
x3 = 590
x4 = 880

y1 = 360
y2 = 470
y3 = 490
y4 = 510


x1_depth = 400
x2_depth = 610
x3_depth = 670
x4_depth = 880


y1_depth = 320
y2_depth = 400
y4_depth = 460

#フラッグ検出範囲設定
x2_f = 630
x3_f = 650

#duty比設定
duty_slow = 10
duty_middle = 20
duty_fast = 30
duty_bunker = 30
duty_ball_flag_None = 50

#バンカー避け設定
bunker_lim = 300
bunker_down = 400
bunker_percent = 0.65
bunker_rotation = 100


#カメラ設定----------------------------
cap = cv2.VideoCapture(6)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, size_w)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, size_h)
#--------------------------------------



# ストリーム(Color/Depth)の設定----------
config = rs.config()

config.enable_stream(rs.stream.color, size_w, size_h, rs.format.bgr8, 30)
config.enable_stream(rs.stream.depth, size_w, size_h, rs.format.z16, 30)

# ストリーミング開始
pipeline = rs.pipeline()
profile = pipeline.start(config)

# Alignオブジェクト生成
align_to = rs.stream.color
align = rs.align(align_to)
#---------------------------------------

# club
club_ = club.club()
club_.now_pull_dis = HC_SR04.get_distance(club_.TRIG_PIN, club_.ECHO_PIN, num=5, temp=20)
club_.sheer_down(30)
time.sleep(1)
club_.DC_motor.stop()

club_.sheer_hold()
club_.sheer_move(100, club_.duty)

try:
    while True:
        
        k=cv2.waitKey(1)
        
        if k==ord('q'):#qで終了
            cv2.destroyAllWindows()
            club_.sheer_release()
            club_.end()
            GPIO.cleanup()
            pipeline.stop()
            break

#ボール検出、追尾------------------------------------

        if ball == True:

            ret, frame_ball_1 = cap.read()

            bunker_x, bunker_y, bunker_w, bunker_h, bunker_frame = M_bunker.bunker_detect(frame_ball_1)
            

            upper_left_1_x, upper_left_1_y, center_ball_1_x, center_ball_1_y, frame_ball_1 = M_ball.ball_detect(frame_ball_1)


            if bunker_x != None:
                cv2.rectangle(frame_ball_1, (bunker_x, bunker_y), (bunker_x + bunker_w, bunker_y + bunker_h), (0, 255, 0), 2)
            cv2.line(frame_ball_1, (0, bunker_lim), (size_w, bunker_lim), (0, 255, 0), thickness=2, lineType=cv2.LINE_4)
            cv2.line(frame_ball_1, (int(size_w * bunker_percent), 0), (int(size_w * bunker_percent), size_h), (0, 255, 0), thickness=2, lineType=cv2.LINE_4)
            #ボール検出範囲描画
            cv2.rectangle(frame_ball_1, (x2, 0), (x3, size_h), (0, 255, 0), 2)
            cv2.rectangle(frame_ball_1, (x1, 0), (x4, size_h), (0, 255, 0), 2)
            cv2.rectangle(frame_ball_1, (0, y2), (size_w, y4), (0, 255, 0), 2)
            cv2.imshow('ball_bunker', frame_ball_1)

            if bunker_x != None:
                #バンカー回避
                if bunker_y + bunker_h > bunker_lim and center_ball_1_y != None:

                    print("=== bunker move ===")

                    if center_ball_1_y==None or upper_left_1_y + ((center_ball_1_y - upper_left_1_y)*2) < bunker_y+bunker_h:

                        bunker_MAX = bunker_x + bunker_w
                        bunker_min = bunker_x
                        # print(bunker_min)

                        if bunker_min < 30 and bunker_MAX >= int(size_w * bunker_percent):#画面の65％
                            #画面いっぱい
                            if bunker_y + bunker_h > bunker_down:
                                down(duty_bunker)#duty=40
                                time.sleep(1)
                                stop()
                            #フラッグが右なら左回転　2
                            #フラッグが左なら右回転　1
                            right_rotation(duty_bunker)
                            time.sleep(3.5)
                            move(duty_bunker)
                            time.sleep(3)
                            bunker_rotation = 1

                            print('bunker center')



                        if bunker_min < 30 and bunker_MAX < int(size_w * bunker_percent):
                            if bunker_y + bunker_h > bunker_down:
                                down(duty_bunker)
                                time.sleep(1)
                                stop()
                            #画面の左側
                            right_rotation(duty_bunker)
                            time.sleep(3)
                            move(duty_bunker)
                            time.sleep(3)
                            print('bunker right')
                            ritation = 1


                        if 0 != bunker_min and int(size_w * bunker_percent) < bunker_MAX:
                            if bunker_y + bunker_h > bunker_down:
                                down(duty_bunker)
                                time.sleep(1)
                                stop()
                            #画面の右側
                            print('bunker left')
                            left_rotation(duty_bunker)
                            time.sleep(3)
                            move(duty_bunker)
                            time.sleep(3)
                            bunker_rotation = 2

            print("=== ball move ===")

            if upper_left_1_x == None:
                #right_rotation(duty_ball_flag_None)
                depth = True
                ball = False
                print("未検出")
            else:
                if center_ball_1_x < x1 and upper_left_1_y < y1:
                    left_rotation_back(duty_middle)
                    print('left')

                if x1 <= center_ball_1_x and center_ball_1_x < x2:
                    if y3 <= upper_left_1_y:
                        down(duty_fast)
                        print('down')
                    else:
                        left_rotation_back(duty_middle)
                        print('left')

                if x3 < center_ball_1_x and center_ball_1_x <= x4:
                    if y3 <= upper_left_1_y:
                        down(duty_fast)
                        print('down')
                    else:
                        right_rotation_back(duty_middle)
                        print('right')

                if x4 < center_ball_1_x and upper_left_1_y < y1:
                    right_rotation_back(duty_middle)
                    print('right')
                

                if x2 <= center_ball_1_x and center_ball_1_x <= x3:
                    if upper_left_1_y < y1:
                        move(duty_fast)
                        print('move fast')
                    else:
                        move(duty_slow)
                        print('move')

                if x4 < center_ball_1_x and y1 <= upper_left_1_y:
                    down(duty_fast)
                    print('down')

                if center_ball_1_x < x1 and y1 <= upper_left_1_y:
                    down(duty_fast)  
                    print('down')

                if x2 <= center_ball_1_x and center_ball_1_x <= x3:
                    if y2 <= upper_left_1_y and upper_left_1_y <= y4:
                        stop()
                        print('stop')
                        ball = False
                        flag = True
                        cv2.destroyWindow('ball_bunker')
                        time.sleep(0.1)

            #カメラ処理遅れ対策
            for i in range(5):
                cap.read()
#------------------------------------------------

#デプスカメラ
        if depth == True:

            move(duty_fast)
            time.sleep(2)
            stop()
            depth = False
            ball = True
            # frames_depth = pipeline.wait_for_frames()

            # #座標の補正
            # aligned_frames = align.process(frames_depth)
            # color_frame = aligned_frames.get_color_frame()
            # depth_frame = aligned_frames.get_depth_frame()
            # if not depth_frame or not color_frame:
            #     continue

            # RGB_image = np.asanyarray(color_frame.get_data())
            # depth_image = np.asanyarray(depth_frame.get_data())


            # upper_left_depth_x, upper_left_depth_y, center_ball_depth_x, center_ball_depth_y, frame_depth = M_ball.ball_detect(RGB_image)

            # # 表示
            # if center_ball_depth_x != None:
            #     cv2.rectangle(RGB_image, (0, y2_depth), (1280, y4_depth), (0, 255, 0), 2)
            #     cv2.rectangle(RGB_image, (x2_depth, 0), (x3_depth, 720), (0, 255, 0), 2)
            #     cv2.imshow('depth', RGB_image)

            # if upper_left_depth_x == None:
            #     right_rotation(duty_ball_flag_None)
            #     print("未検出")
            # else:
            #     if center_ball_depth_x < x1:
            #         left_rotation_back(duty_middle)
            #         print('left')

            #     if x1 <= center_ball_depth_x and center_ball_depth_x < x2:
            #         left_rotation_back(duty_middle)
            #         print('left')

            #     if x3 < center_ball_depth_x and center_ball_depth_x <= x4:
            #         if y3 <= upper_left_depth_y:
            #             right_rotation_back(duty_middle)
            #             print('right')

            #     if x4 < center_ball_depth_x:
            #         right_rotation_back(duty_middle)
            #         print('right')
                

            #     if x2 <= center_ball_depth_x and center_ball_depth_x <= x3:
            #         if upper_left_depth_y < y1:
            #             move(duty_fast)
            #             print('move fast')
            #         else:
            #             move(duty_slow)
            #             print('move')

            #     if x2 <= center_ball_depth_x and center_ball_depth_x <= x3:
            #         if y2 <= upper_left_depth_y and upper_left_depth_y <= y4:
            #             stop()
            #             print('stop')
            #             depth = False
            #             ball = True
            #             cv2.destroyWindow('depth')
            #             time.sleep(0.1)
#------------------------------------------------------


                
 
            
#フラッグ検出-------------------------------------------------------
        if flag == True:

            print("=== flag move ===")

            frames_flag = pipeline.wait_for_frames()

            #座標の補正
            aligned_frames = align.process(frames_flag)
            color_frame = aligned_frames.get_color_frame()
            depth_frame = aligned_frames.get_depth_frame()
            if not depth_frame or not color_frame:
                continue

            RGB_image = np.asanyarray(color_frame.get_data())
            depth_image = np.asanyarray(depth_frame.get_data())

            flag_x, center_flag_x, center_flag_y, flag_w, RGB_image = M_flag.flag_detect(RGB_image)

            # 表示
            if flag_x != None:
                cv2.rectangle(RGB_image, (x2_f, 0), (x3_f, size_w), (0, 255, 0), 2)
                cv2.imshow('RealSense', RGB_image)
            
            print(flag_x)

            if flag_x == None:
                #フラッグ未検出
                right_rotation(duty_ball_flag_None)
                print("未検出")
            else:
                if flag_x < x2_f:
                    left_rotation(duty_slow)
                    print('left flag slow')
                if x3_f < flag_x:
                    right_rotation(duty_slow) 
                    print('right slow')
                if x2_f <= flag_x and flag_x <= x3_f:
                #停止
                    print('stop flag')
                    stop()

                    dist_depth = distance(center_flag_x, center_flag_y)
                    if dist_depth == None:
                        #ゼロ除算に引っかかったらもう一回
                        continue
                    
                    flag = False
                    hole = True
                    cv2.destroyWindow('RealSense')
                    time.sleep(0.1)
#------------------------------------------------------------------



#打球---------------------------------------------------------
        if hole == True:

            print("=== hole move ===")
	
            print(dist_depth)
            #どのタイミングでフラッグの距離計測するか
           
            power = 90

            if 2.2 < dist_depth:
                power = 90
            if 0.8 < dist_depth and dist_depth <=2.2:
                power = 80
                # power = 80
            if dist_depth <= 0.8:
                power = 65
                down(duty_fast)
                time.sleep(0.5)
                stop()

            print("打球")
            club_.sheer_move(power, club_.duty)
            time.sleep(0.5)
            club_.sheer_release()

            stop()

            time.sleep(3)

            club_.sheer_hold()
            club_.sheer_move(80, club_.duty)

            hole = False
            flag = False
            ball = True
#-------------------------------------------------------------

            
              
except KeyboardInterrupt:
    # ストリーミング停止
    pipeline.stop()
    cv2.destroyAllWindows()
    club_.sheer_release()
    club_.end()
    GPIO.cleanup()
    cap.release()
