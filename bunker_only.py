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


def move(duty):
    #右回転(左が正転、右が後転)
    p1.ChangeDutyCycle(duty)
    p2.ChangeDutyCycle(0)
    p3.ChangeDutyCycle(0)
    p4.ChangeDutyCycle(duty)
    


def down(duty):
    #左回転(左が後転、右が正転)
    p1.ChangeDutyCycle(0)
    p2.ChangeDutyCycle(duty)
    p3.ChangeDutyCycle(duty)
    p4.ChangeDutyCycle(0)



def right_rotation(duty):
    #前進
    p1.ChangeDutyCycle(0)
    p2.ChangeDutyCycle(duty)
    p3.ChangeDutyCycle(0)
    p4.ChangeDutyCycle(0)

def right_rotation_flag(duty):
    #前進
    p1.ChangeDutyCycle(0)
    p2.ChangeDutyCycle(duty)
    p3.ChangeDutyCycle(0)
    p4.ChangeDutyCycle(duty)
    
    

def left_rotation(duty):
    #
    p1.ChangeDutyCycle(0)
    p2.ChangeDutyCycle(0)
    p3.ChangeDutyCycle(duty)
    p4.ChangeDutyCycle(0)

def left_rotation_flag(duty):
    #
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
ball_1 = True #下カメラ
bunker = False
bunker_1 = False
hole = False #打球

#画面サイズ設定
size_w = 1280
size_h = 720

#ボール検出範囲設定
x1 = 400
x2 = 590
x3 = 670
x4 = 880

y1 = 360
y2 = 470
y3 = 490
y4 = 510

duty_slow = 10
duty_fast = 30
duty_rotation = 20

rotation = 0


#カメラ設定----------------------------
cap = cv2.VideoCapture(6)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, size_w)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, size_h)
#--------------------------------------




try:
    while True:

        k=cv2.waitKey(1)
        
        if k==ord('q'):#qで終了
            cv2.destroyAllWindows()
            GPIO.cleanup()
            break

#ボール検出、追尾------------------------------------
        if ball_1 == True:
            ret,ball_1_frame = cap.read()

            bunker_x,bunker_y,bunker_w,bunker_h,bunker_frame = M_bunker.bunker_detect(ball_1_frame)
            #print(bunker_x)
            
            upper_left_1_x,upper_left_1_y,center_ball_1_x,center_ball_1_y,ball_1_frame = M_ball.ball_detect(ball_1_frame)
            
            #バンカー描画
            if bunker_x != None:
                cv2.rectangle(ball_1_frame, (bunker_x, bunker_y), (bunker_x + bunker_w, bunker_y + bunker_h), (0, 255, 0), 2)
            cv2.line(ball_1_frame, (0, 250), (1280, 250), (0, 255, 0), thickness=2, lineType=cv2.LINE_4)
            cv2.line(ball_1_frame, (int(size_w * 0.65), 0), (int(size_w * 0.65), 720), (0, 255, 0), thickness=2, lineType=cv2.LINE_4)
            #ボール検出範囲描画
            cv2.rectangle(ball_1_frame, (int((size_w / 2) - 100), 0), (int((size_w / 2) + 20), size_h), (0, 255, 0), 2)
            cv2.rectangle(ball_1_frame, (0, 470), (size_w, 510), (0, 255, 0), 2)
            cv2.imshow('ball', ball_1_frame)
    

            #if bunker_y != None:
            if bunker_y != None:
                #バンカー回避
                if bunker_y + bunker_h > 250:

                    # bunker_MAX = bunker_x + bunker_w
                    # bunker_min = bunker_x
                    # print(bunker_min)

                    if bunker_min < 50 and bunker_MAX >= int(size_w * 0.65):#画面の65％
                        #画面いっぱい
                        if bunker_y + bunker_h > 400:
                            down(40)
                            time.sleep(1)
                            stop()
                        #フラッグが右なら左回転　2
                        #フラッグが左なら右回転　1
                        left_rotation_flag(40)
                        time.sleep(3.5)
                        move(40)
                        time.sleep(3)
                        rotation = 2

                        print('bunker center')



                    if bunker_min < 30 and bunker_MAX < int(size_w * 0.65):
                        if bunker_y + bunker_h > 400:
                            down(30)
                            time.sleep(1)
                            stop()
                        #画面の左側
                        right_rotation_flag(40)
                        time.sleep(3.5)
                        move(40)
                        time.sleep(3)
                        print('bunker right')
                        ritation = 1


                    if 0 != bunker_min and int(size_w * 0.65) < bunker_MAX:
                        if bunker_y + bunker_h > 400:
                            down(40)
                            time.sleep(1)
                            stop()
                        #画面の右側
                        print('bunker left')
                        left_rotation_flag(40)
                        time.sleep(3.5)
                        move(40)
                        time.sleep(3)
                        rotation = 2
                    
                
                if upper_left_1_x == None:
                    if rotation != None:
                        if rotation == 1:
                            left_rotation_flag(duty_fast)
                            print("未検出 左")
                        if rotation == 2:
                            right_rotation_flag(duty_fast)
                            print("未検出　右")
                    else:
                        right_rotation_flag(duty_rotation)
                        print("未検出")
                else:
                    if center_ball_1_x < x1 and upper_left_1_y < y1:
                        left_rotation(duty_rotation)
                        print('left')

                    if x1 <= center_ball_1_x and center_ball_1_x < x2:
                        if y3 <= upper_left_1_y:
                            down(duty_fast)
                            print('down')
                        else:
                            left_rotation(duty_rotation)
                            print('left')

                    if x3 < center_ball_1_x and center_ball_1_x <= x4:
                        if y3 <= upper_left_1_y:
                            down(duty_fast)
                            print('down')
                        else:
                            right_rotation(duty_rotation)
                            print('right')

                    if x4 < center_ball_1_x and upper_left_1_y < y1:
                        right_rotation(duty_rotation)
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
                            ball_1 = False
                            flag = True
                            cv2.destroyWindow('frame')
                            time.sleep(0.1)

        #カメラ処理遅れ対策
        for i in range(5):
            cap.read()




#---------------------------------------------------------

#フラッグ検出---------------------------------------------
                
                                  

            
                

            

#--------------------------------------------------------





#打球---------------------------------------------------------
        if hole == True:

            #どのタイミングでフラッグの距離計測するか
            #dist_depth = distance(center_flag_x,center_flag_y)
            #if dist_depth == None:
                #ゼロ除算に引っかかったらもう一回
             #   dist_depth = distance(center_flag_x,center_flag_y)

            print("打球")

            time.sleep(5)

            hole = False
            ball_1 = True
#-------------------------------------------------------------

            
              
except KeyboardInterrupt:
    # ストリーミング停止
    cv2.destroyAllWindows()
    GPIO.cleanup()
