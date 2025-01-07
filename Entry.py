# -*- coding: utf-8 -*-
"""
@author: PC
Update Time: 2025-01-08
"""
from flask import Flask
from linebot.models import TextSendMessage
from package.linebot import LineBotProcess

lbp = LineBotProcess()
app = Flask(__name__)
linebot_api, handler, gemini_token = LineBotProcess.token_settings()

@app.route('/', methods=['POST'])
def main():
    body, loader, reply_token, event_type = LineBotProcess.initial_body()
    match event_type:
        case 'text':
            msg = loader['events'][0]['message']['text']
            reply = lbp.switch(msg, gemini_token)
        case _:
            reply = f"<ERROR> The format doesn't comply with the regulations -> {event_type}"

    linebot_api.reply_message(reply_token, TextSendMessage(reply))
    return '', 200

if __name__ == '__main__':
    app.run()