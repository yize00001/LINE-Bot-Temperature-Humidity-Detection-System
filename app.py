from __future__ import unicode_literals
import os
import re
from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage

import configparser
import random

import rclpy
import time
from rclpy.node import Node
from std_msgs.msg import String




app = Flask(__name__)

# LINE 聊天機器人的基本資料
config = configparser.ConfigParser()
config.read('config.ini')

line_bot_api = LineBotApi(config.get('line-bot', 'channel_access_token'))
handler = WebhookHandler(config.get('line-bot', 'channel_secret'))


# 接收 LINE 的資訊
@app.route("/callback", methods=['POST'])
def callback():
    signature = request.headers['X-Line-Signature']

    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)
    
    try:
        print(body, signature)
        handler.handle(body, signature)
        
    except InvalidSignatureError:
        abort(400)

    return 'OK'

# 學你說話
@handler.add(MessageEvent, message=TextMessage)
def pretty_echo(event):
        j=[]
        class Sound_sub(Node):
            def __init__(self):        
                super().__init__('light')
                self.subscription = self.create_subscription(String,"chatter",self.listener_callback,10)
                self.subscription
            def listener_callback(self, msg):

                j = msg.data.split(':')
                str = "現在相對濕度:"+j[0]+"%\n現在溫度:"+j[1]+"度"
                line_bot_api.reply_message(
                    event.reply_token,
                    TextSendMessage(text=str)
                )


                print (float(j[0]))
                print (float(j[1]))

                print (event.source)
        if event.message.text in "查看":
            print (event.message.text)
            rclpy.init()
            Sound = Sound_sub()
            rclpy.spin_once(Sound)
            Sound.destroy_node()
            rclpy.shutdown()

        if event.message.text in "設定提醒": 
            userID = event.source.user_id
           
            print (userID)
            f = open('userId.txt','w+')
            f.write(userID)
            line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(text="設定成功\n濕度>70")
            )
        if event.message.text in "取消提醒": 
            userID = event.source.user_id
            #data = event.source
            #re.sub('{','',data)
            #re.sub('}','',data) 
            #re.sub('"','',data) 
            #data1 = data.split(',')
            #userID = data1.split(':')
            print (userID)
            f = open('userId.txt','w+')
            f.write("")
            line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(text="設定成功\n將不會提醒給你")
            )
if __name__ == "__main__":
    app.run()
