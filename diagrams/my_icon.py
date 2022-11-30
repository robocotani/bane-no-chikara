from diagrams.custom import Custom
import os

class my_icon(Custom):

    def __init__(self, name, relative_pass):
        dir = os.path.dirname(os.path.abspath(__file__))
        print(dir+relative_pass)
        super().__init__(name, dir+"/"+relative_pass)