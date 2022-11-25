import os
os.environ["OPENCV_VIDEOIO_MSMF_ENABLE_HW_TRANSFORMS"] = "0"
import cv2
import M_ball
import M_bunker

class picamera():

    size_w = 1280
    size_h = 720

    #バンカー避け設定
    bunker_lim = 300
    bunker_down = 400
    bunker_percent = 0.65
    bunker_rotation = 100

    bunker_x = None
    bunker_y = None
    bunker_w = None
    bunker_h = None
    bunker_frame = None
    ball_left = None
    ball_top = None
    ball_center_x = None
    ball_center_y = None

    frame = None
    cap = None

    def __init__(self):
        self.cap = cv2.VideoCapture(6)
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, self.size_w)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, self.size_h)

    def get_frame(self):
        ret, self.frame = self.cap.read()
        return self.frame
    
    def detect_ball_banker(self):

        ball_frame = self.frame

        x1 = 400
        x2 = 560
        x3 = 590
        x4 = 880

        y1 = 360
        y2 = 470
        y3 = 490
        y4 = 510

        self.bunker_x, self.bunker_y, self.bunker_w, self.bunker_h, self.bunker_frame = M_bunker.bunker_detect(ball_frame)
        self.ball_left, self.ball_top, self.ball_center_x, self.ball_center_y, ball_frame = M_ball.ball_detect(ball_frame)

        if self.bunker_x != None:
            cv2.rectangle(ball_frame, (self.bunker_x, self.bunker_y), (self.bunker_x + self.bunker_w, self.bunker_y + self.bunker_h), (0, 255, 0), 2)
        cv2.line(ball_frame, (0, self.bunker_lim), (self.size_w, self.bunker_lim), (0, 255, 0), thickness=2, lineType=cv2.LINE_4)
        cv2.line(ball_frame, (int(self.size_w * self.bunker_percent), 0), (int(self.size_w * self.bunker_percent), self.size_h), (0, 255, 0), thickness=2, lineType=cv2.LINE_4)
        #ボール検出範囲描画
        cv2.rectangle(ball_frame, (x2, 0), (x3, self.size_h), (0, 255, 0), 2)
        cv2.rectangle(ball_frame, (x1, 0), (x4, self.size_h), (0, 255, 0), 2)
        cv2.rectangle(ball_frame, (0, y2), (self.size_w, y4), (0, 255, 0), 2)
        
        return ball_frame
    
    def end(self):
        self.cap.release()