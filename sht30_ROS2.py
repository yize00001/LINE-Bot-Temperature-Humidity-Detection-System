# coding=UTF-8 
import rclpy 
import serial
import time
from rclpy.node import Node 
from std_msgs.msg import String 

def readlight(port):
    rv = ""
    while True:
        ch = port.read().decode()
        if ch=='\r' or ch=='':
            return rv
        if ch != '\n':rv += ch

class light_pub(Node): 
    def __init__(self): 
        super().__init__('light')
        self.publisher_ = self.create_publisher(String, 'chatter', 10)
        self.port = serial.Serial("/dev/ttyACM0", baudrate=9600, timeout=3.0)

    def run(self): 
        msg = String()
        while 1:
            msg.data = readlight(self.port)
            self.publisher_.publish(msg) 

if __name__ == '__main__': 
    rclpy.init() 
    light = light_pub() 
    light.run()
    light.destroy_node() 
    rclpy.shutdown()
