# https://tech.gunosy.io/entry/diagram_as_code

from diagrams import Cluster, Diagram
from my_icon import my_icon

graph_attr = {
    "pad": "0.5",
    "splines": "ortho",
    "nodesep": "0.4",
    "ranksep": "0.75",
    "fontname": "Arial",
    "fontsize": "20",
    "fontcolor": "#2D3436",
}

node_attr = {
    "fontname": "Arial",
    'fontsize': '20'
}

edge_attr = {
    'arrowsize': '1.0',
    'penwidth': '3.0'
}

with Diagram('System', direction="TB", graph_attr=graph_attr, edge_attr=edge_attr, node_attr=node_attr):

    with Cluster("BANE-NO-CHIKARA", graph_attr=graph_attr):

        # インスタンス化によってノードを作成
        # ノードにラベルを付与でき、\nを入れることでラベルの改行も可能
        ras_pi = my_icon("raspberry pi", "icon/raspberry_pi.png")

        with Cluster("camera", graph_attr=graph_attr):
            picamera = my_icon("pi camera", "icon/picamera.png")
            realsense = my_icon("realsense", "icon/D435i.png")

        with Cluster("move", graph_attr=graph_attr):
            driver_1 = my_icon("L298N", "icon/L298N.png")
            DC_motor_1 = my_icon("DC Motor", "icon/JGY-370.png")
            DC_motor_2 = my_icon("DC Motor", "icon/JGY-370.png")

        with Cluster("club", graph_attr=graph_attr):
            Echo = my_icon("HC-SR04", "icon/HC-SR04.png")
            servo = my_icon("MG996R", "icon/MG996R.png")
            driver_2 = my_icon("L298N", "icon/L298N.png")
            DC_motor_3 = my_icon("DC Motor", "icon/JGY-370.png")
        
    ras_pi >> realsense
    ras_pi >> picamera
    ras_pi >> driver_1 >> DC_motor_1
    driver_1 >> DC_motor_2
    ras_pi >> driver_2 >> DC_motor_3
    ras_pi >> Echo
    ras_pi >> servo