import pyrealsense2.pyrealsense2 as rs
import numpy as np
import M_flag

class D435i():

    #画面サイズ設定
    size_w = 1280
    size_h = 720

    flag_x = None
    center_flag_x = None
    center_flag_y = None
    flag_w = None
    flag_result = None
    flag_distance = None
    
    def __init__(self):

        # ストリーム(Color/Depth)の設定----------
        config = rs.config()

        config.enable_stream(rs.stream.color, self.size_w, self.size_h, rs.format.bgr8, 30)
        config.enable_stream(rs.stream.depth, self.size_w, self.size_h, rs.format.z16, 30)

        # ストリーミング開始
        self.pipeline = rs.pipeline()
        profile = self.pipeline.start(config)

        # Alignオブジェクト生成
        align_to = rs.stream.color
        self.align = rs.align(align_to)
        #---------------------------------------

    def get_image(self):
        
        frames_flag = self.pipeline.wait_for_frames()

        #座標の補正
        aligned_frames = self.align.process(frames_flag)
        color_frame = aligned_frames.get_color_frame()
        self.depth_frame = aligned_frames.get_depth_frame()
        if not self.depth_frame or not color_frame:
            return

        self.RGB_image = np.asanyarray(color_frame.get_data())
        self.depth_image = np.asanyarray(self.depth_frame.get_data())

    def detect_flag(self):
        self.flag_x, self.center_flag_x, self.center_flag_y, self.flag_w, self.flag_result = M_flag.flag_detect(self.RGB_image)
        self.flag_distance = None
        if self.flag_x is not None:
            self.distance(self.center_flag_x, self.center_flag_y)

    #距離計測
    def distance(self, center_x,center_y):
        #ボールとの距離は角度を補正
        #周囲の5点を取って平均
        #かけ離れている点は除外
        dist = []

        for i in range(5):
            for j in range(5):
                dist1 = self.depth_frame.get_distance(center_x + i, center_y + j)
                dist.append(float(format(dist1,'.4f')))
        
        #0.1m以下、3.5m以上の点は除外して平均
        dist_new = [i for i in dist if 0.1 < i < 3.5] 

        try:
            #ゼロ除算の対策
            dist_mean = sum(dist_new)/len(dist_new)
        except ZeroDivisionError:
            dist_mean = None

        self.flag_distance = dist_mean
        return dist_mean
    
    # ファイナライズ
    def end(self):
        self.pipeline.stop()