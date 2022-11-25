import cv2
import time
import D435i
import picamera
import move
# import club
# import HC_SR04

move_ = move.move()
realsense = D435i.D435i()
pi_camera = picamera.picamera()

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

# club
# club_ = club.club()
# club_.now_pull_dis = HC_SR04.get_distance(club_.TRIG_PIN, club_.ECHO_PIN, num=5, temp=20)
# club_.sheer_down(30)
# time.sleep(1)
# club_.DC_motor.stop()

# club_.sheer_hold()
# club_.sheer_move(100, club_.duty)

try:
    while True:
        
        k=cv2.waitKey(1)
        
        if k==ord('q'):#qで終了
            cv2.destroyAllWindows()
            # club_.sheer_release()
            # club_.end()
            move_.end()
            realsense.end()
            break

#ボール検出、追尾------------------------------------

        if ball == True:

            ball_frame = pi_camera.get_frame()
            ball_frame = pi_camera.detect_ball_banker()
            
            cv2.imshow('ball_bunker', ball_frame)

            if pi_camera.bunker_x != None:
                #バンカー回避
                if pi_camera.bunker_y + pi_camera.bunker_h > pi_camera.bunker_lim and pi_camera.ball_center_y != None:

                    print("=== bunker move ===")

                    if pi_camera.ball_center_y==None or pi_camera.ball_top + ((pi_camera.ball_center_y - pi_camera.ball_top)*2) < pi_camera.bunker_y+pi_camera.bunker_h:

                        bunker_MAX = pi_camera.bunker_x + pi_camera.bunker_w
                        bunker_min = pi_camera.bunker_x
                        # print(bunker_min)

                        if bunker_min < 30 and bunker_MAX >= int(size_w * pi_camera.bunker_percent):#画面の65％
                            #画面いっぱい
                            if pi_camera.bunker_y + pi_camera.bunker_h > pi_camera.bunker_down:
                                move_.back(duty_bunker)#duty=40
                                time.sleep(1)
                                move_.stop()
                            #フラッグが右なら左回転　2
                            #フラッグが左なら右回転　1
                            move_.right_rotation(duty_bunker)
                            time.sleep(3.5)
                            move_.forward(duty_bunker)
                            time.sleep(3)
                            bunker_rotation = 1

                            print('bunker center')



                        if bunker_min < 30 and bunker_MAX < int(size_w * pi_camera.bunker_percent):
                            if pi_camera.bunker_y + pi_camera.bunker_h > pi_camera.bunker_down:
                                move_.back(duty_bunker)
                                time.sleep(1)
                                move_.stop()
                            #画面の左側
                            move_.right_rotation(duty_bunker)
                            time.sleep(3)
                            move_.forward(duty_bunker)
                            time.sleep(3)
                            print('bunker right')
                            ritation = 1


                        if 0 != bunker_min and int(size_w * pi_camera.bunker_percent) < bunker_MAX:
                            if pi_camera.bunker_y + pi_camera.bunker_h > pi_camera.bunker_down:
                                move_.back(duty_bunker)
                                time.sleep(1)
                                move_.stop()
                            #画面の右側
                            print('bunker left')
                            move_.left_rotation(duty_bunker)
                            time.sleep(3)
                            move_.forward(duty_bunker)
                            time.sleep(3)
                            bunker_rotation = 2

            print("=== ball move ===")

            if pi_camera.ball_left == None:
                #right_rotation(duty_ball_flag_None)
                depth = True
                ball = False
                print("未検出")
            else:
                if pi_camera.ball_center_x < x1 and pi_camera.ball_top < y1:
                    move_.left_rotation_back(duty_middle)
                    print('left')

                if x1 <= pi_camera.ball_center_x and pi_camera.ball_center_x < x2:
                    if y3 <= pi_camera.ball_top:
                        move_.back(duty_fast)
                        print('down')
                    else:
                        move_.left_rotation_back(duty_middle)
                        print('left')

                if x3 < pi_camera.ball_center_x and pi_camera.ball_center_x <= x4:
                    if y3 <= pi_camera.ball_top:
                        move_.back(duty_fast)
                        print('down')
                    else:
                        move_.right_rotation_back(duty_middle)
                        print('right')

                if x4 < pi_camera.ball_center_x and pi_camera.ball_top < y1:
                    move_.right_rotation_back(duty_middle)
                    print('right')
                

                if x2 <= pi_camera.ball_center_x and pi_camera.ball_center_x <= x3:
                    if pi_camera.ball_top < y1:
                        move_.forward(duty_fast)
                        print('move fast')
                    else:
                        move_.forward(duty_slow)
                        print('move')

                if x4 < pi_camera.ball_center_x and y1 <= pi_camera.ball_top:
                    move_.back(duty_fast)
                    print('down')

                if pi_camera.ball_center_x < x1 and y1 <= pi_camera.ball_top:
                    move_.back(duty_fast)  
                    print('down')

                if x2 <= pi_camera.ball_center_x and pi_camera.ball_center_x <= x3:
                    if y2 <= pi_camera.ball_top and pi_camera.ball_top <= y4:
                        move_.stop()
                        print('stop')
                        ball = False
                        flag = True
                        cv2.destroyWindow('ball_bunker')
                        time.sleep(0.1)

            #カメラ処理遅れ対策
            for i in range(5):
                pi_camera.get_frame()
#------------------------------------------------

#デプスカメラ
        if depth == True:

            move_.forward(duty_fast)
            time.sleep(2)
            move_.stop()
            depth = False
            ball = True
#------------------------------------------------------


                
 
            
#フラッグ検出-------------------------------------------------------
        if flag == True:

            print("=== flag move ===")

            # リアルセンス処理
            realsense.get_image()
            RGB_image = realsense.RGB_image
            realsense.detect_flag()

            # 表示
            if realsense.flag_x != None:
                cv2.rectangle(RGB_image, (x2_f, 0), (x3_f, size_w), (0, 255, 0), 2)
                cv2.imshow('RealSense', RGB_image)
            
            print(realsense.flag_x)

            if realsense.flag_x == None:
                #フラッグ未検出
                move_.right_rotation(duty_ball_flag_None)
                print("未検出")
            else:
                if realsense.flag_x < x2_f:
                    move_.left_rotation(duty_slow)
                    print('left flag slow')
                if x3_f < realsense.flag_x:
                    move_.right_rotation(duty_slow) 
                    print('right slow')
                if x2_f <= realsense.flag_x and realsense.flag_x <= x3_f:
                #停止
                    print('stop flag')
                    move_.stop()

                    dist_depth = realsense.distance(realsense.center_flag_x, realsense.center_flag_y)
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
                move_.back(duty_fast)
                time.sleep(0.5)
                move_.stop()

            print("打球")
            # club_.sheer_move(power, club_.duty)
            # time.sleep(0.5)
            # club_.sheer_release()

            move_.stop()

            time.sleep(3)

            # club_.sheer_hold()
            # club_.sheer_move(80, club_.duty)

            hole = False
            flag = False
            ball = True
#-------------------------------------------------------------

            
              
except KeyboardInterrupt:
    realsense.end()
    cv2.destroyAllWindows()
    # club_.sheer_release()
    # club_.end()
    move_.end()
    pi_camera.end()
