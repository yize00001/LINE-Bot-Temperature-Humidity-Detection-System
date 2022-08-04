# coding=UTF-8
import rclpy
import time
from pygame import mixer
from rclpy.node import Node
from std_msgs.msg import String

class Sound_sub(Node):
    def __init__(self):
        super().__init__('light')
        self.subscription = self.create_subscription(String,"chatter",self.listener_callback,10)
        self.subscription
        self.STATE = 0
    def listener_callback(self, msg):
        mixer.init()
        mixer.music.load('Warning.mp3')
        SoundControl = 0
        TempHum = msg.data.split(':')                   # 溫濕度資料切割
#        print (float(TempHum[0]),float(TempHum[1]))     # 轉成float
        if float(TempHum[0]) >= 70.00 and  time.time() - self.STATE > 3:
            try:
                mixer.music.play()
                # time.sleep(5)
                # mixer.music.stop()
                while mixer.music.get_busy() == True:continue
                mixer.music.stop()
            except:pass
            self.STATE = time.time()
        else:
            mixer.music.stop()

if __name__ == '__main__':
    rclpy.init()
    Sound = Sound_sub()
    rclpy.spin(Sound)
    Sound.destroy_node()
    rclpy.shutdown()

