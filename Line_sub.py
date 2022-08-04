# coding=UTF-8
import rclpy
import time
import configparser

from rclpy.node import Node
from std_msgs.msg import String
from linebot import LineBotApi
from linebot.models import TextSendMessage
import time

# 必須放上自己的Channel Access Token
config = configparser.ConfigParser()
config.read('config.ini')

line_bot_api = LineBotApi(config.get('line-bot', 'channel_access_token'))

class Line_sub(Node):
    def __init__(self):
        super().__init__('light')
        self.subscription = self.create_subscription(String,"chatter",self.listener_callback,10)
        self.subscription
        self.STATE = 0
    def listener_callback(self, msg):
       
        j = msg.data.split(':')
        tmp = float(j[1])
        hum = float(j[0])
        str ="警告！！\n"
        if hum > 70.00:
           str = str+"濕度過高："+j[0]+"%\n"
        if tmp > 40.00:
           str = str+"溫度過高："+j[1]+"C\n"
        if (hum > 70.00 or tmp > 40.00) and  time.time() - self.STATE > 60:
           print (str)
           #讀取user_id 在userId.txt中
           f = open('userId.txt','r')
           yourID=f.readline()
           if (yourID!=""):
               line_bot_api.push_message(yourID,TextSendMessage(text=str))
               self.STATE = time.time()

if __name__ == '__main__':
    rclpy.init()
    Line = Line_sub()
    rclpy.spin(Line)
    Sound.destroy_node()
    rclpy.shutdown()

