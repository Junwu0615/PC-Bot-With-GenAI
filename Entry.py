# -*- coding: utf-8 -*-
"""
@author: PC
Update Time: 2025-01-09
"""
from flask import request, Flask, abort
from linebot.models import MessageEvent, TextMessage, FileMessage, ImageMessage
from package.linebot import LineBotHandler

app = Flask(__name__)
linebot_api, handler, gemini_token = LineBotHandler.token_settings()
lbh = LineBotHandler(gemini_token)

SAVE_PATH = './preprocess'

@app.route('/callback', methods=['POST'])
def callback():
    body = request.get_data(as_text=True)
    signature = request.headers['X-Line-Signature']
    try:
        handler.handle(body, signature)
    except Exception as e:
        print(e)
        abort(400)
    finally:
        return '', 200

@handler.add(MessageEvent, message=TextMessage)
def text_message(event: MessageEvent):
    if isinstance(event.message, TextMessage):
        lbh.process(event)

@handler.add(MessageEvent, message=FileMessage)
def file_message(event: MessageEvent):
    LineBotHandler.make_folder(SAVE_PATH)
    if isinstance(event.message, FileMessage):
        msg_id = event.message.id
        msg_name = event.message.file_name
        msg_size = LineBotHandler.make_decimal(event.message.file_size/1024/1024, '0.01')
        msg_content = linebot_api.get_message_content(msg_id)
        print(f'msg_id: {msg_id}, msg_name: {msg_name}, msg_size: {msg_size} MB')
        with open(f'{SAVE_PATH}/{msg_id}_{msg_name}', 'wb') as f:
            for chunk in msg_content.iter_content():
                f.write(chunk)

@handler.add(MessageEvent, message=ImageMessage)
def img_message(event: MessageEvent):
    LineBotHandler.make_folder(SAVE_PATH)
    if isinstance(event.message, ImageMessage):
        msg_id = event.message.id
        msg_content = linebot_api.get_message_content(msg_id)
        with open(f'{SAVE_PATH}/{msg_id}.jpg', 'wb') as f:
            for chunk in msg_content.iter_content():
                f.write(chunk)

if __name__ == '__main__':
    app.run(port=5000)