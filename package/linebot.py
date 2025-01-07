# -*- coding: utf-8 -*-
"""
@author: PC
Update Time: 2025-01-08
"""
import json
from flask import request
from datetime import datetime
from linebot import LineBotApi, WebhookHandler

from package.gemini import GeminiFormat
from package.base import BaseLogic

class LineBotProcess:
    def __init__(self):
        self.gemini = GeminiFormat(self)

    @staticmethod
    def initial_body() -> tuple:
        body = request.get_data(as_text=True)
        loader = json.loads(body)
        reply_token = loader['events'][0]['replyToken']
        event_type = loader['events'][0]['message']['type']
        return body, loader, reply_token, event_type

    @staticmethod
    def token_settings() -> tuple:
        linebot_api = handler = gemini_token = None
        for _ in [i for i in open('package/token.txt', 'r')]:
            idx = _.split(',')
            match idx[0]:
                case 'Line_Access_Token':
                    linebot_api = LineBotApi(idx[1].replace('\n', ''))
                case 'Line_Secret':
                    handler = WebhookHandler(idx[1].replace('\n', ''))
                case 'Gemini_Token':
                    gemini_token = idx[1].replace('\n', '')
                case _:
                    print('*** [token_settings] other error ***')

        return linebot_api, handler, gemini_token

    def switch(self, msg: str, gemini_token: str) -> str:
        msg = msg.split(',')
        event_type = msg[0].lower()
        match event_type:
            case 'identify food and feedback':
                return 'Coming Soon ...'

            case 'gif meme name search':
                return 'Coming Soon ...'

            case 'human companion robot':
                return 'Coming Soon ...'

            case 'generate self-introduction':
                return 'Coming Soon ...'

            case _:
                return self.gemini.chat(msg, gemini_token)
                # return "<ERROR> The format doesn't match type."