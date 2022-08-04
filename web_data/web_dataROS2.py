# coding=UTF-8 
import rclpy
import threading
from flask import Flask, render_template,jsonify,request
from rclpy.node import Node 
from std_msgs.msg import String

app = Flask(__name__)

class webAPP(Node): 
    def __init__(self): 
        super().__init__('webAPP')
        self.subscription = self.create_subscription(String,"chatter",self.listener_callback,10) 
        self.subscription #prevent unused variable warning
        self.showText = ""
   
    def listener_callback(self,msg):
        TempHum = msg.data.split(':')
        # print (float(TempHum[0]),float(TempHum[1]))
        self.showText = '現在相對濕度: '+ TempHum[0]+ ' %\n'+ '現在相對溫度: '+ TempHum[1]+ ' °c'

if __name__ == '__main__':
    #實例化，先有實體才能依靠flask呼叫
    rclpy.init() 
    node_webAPP = webAPP()

    #初始畫面
    @app.route('/')
    def index():
        return render_template('index_sub.html')

    #將訂閱之ROS頻道訊息傳送至顯示網頁
    @app.route('/showText')
    def show():
        return node_webAPP.showText

    t = threading.Thread(target = rclpy.spin,args=(node_webAPP,))
    t.start()
    app.run(debug=True,host='0.0.0.0',port=5001)
    rclpy.shutdown()