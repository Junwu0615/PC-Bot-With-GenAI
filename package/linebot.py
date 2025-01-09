# -*- coding: utf-8 -*-
"""
@author: PC
Update Time: 2025-01-09
"""
import os, copy, json
from decimal import Decimal, ROUND_HALF_UP
from linebot import LineBotApi, WebhookHandler
from linebot.models import TextSendMessage

from package.gemini import GeminiFormat
from developer.package.norm_function import DATE_YMD_ONE
from developer.package.interface import Interface
from developer.definition.state import State
from developer.model.TLineGenAI import TLineGenAIField, TLineGenAIFormat

class LineBotHandler(Interface):
    def __init__(self, gemini_token):
        super().__init__([])
        self.gemini = GeminiFormat(self, gemini_token)
        self.event = {'msg': None, 'file': None}

    @staticmethod
    def make_decimal(target, decimal_num: str) -> Decimal:
        return Decimal(target).quantize(Decimal(decimal_num), rounding=ROUND_HALF_UP)

    @staticmethod
    def make_folder(path: str):
        folder = os.path.exists(path)
        if not folder:
            os.makedirs(path)

    @staticmethod
    def token_settings() -> tuple:
        linebot_api = handler = gemini_token = None
        for _ in [i for i in open('package/token.txt', 'r')]:
            idx = _.split(',')
            match idx[0]:
                case 'Line_Access':
                    linebot_api = LineBotApi(idx[1].replace('\n', ''))
                case 'Line_Secret':
                    handler = WebhookHandler(idx[1].replace('\n', ''))
                case 'Gemini_Token':
                    gemini_token = idx[1].replace('\n', '')
                case _:
                    self.log_warning('*** [token_settings] other error ***')
        return linebot_api, handler, gemini_token

    @staticmethod
    def initial_user_stat() -> dict:
        initial_settings = {
            'text_count': 0,
            'media_count': 0,
            'identify food and feedback': 0,
            'gif meme name search': 0,
            'human companion robot': 0,
            'generate self-introduction': 0,
        }
        return initial_settings

    @staticmethod
    def parsing_event(event) -> tuple[str, str, str, str]:
        user_id = event.source.user_id
        event_type = event.message.type
        msg = event.message.text
        reply_token = event.reply_token
        return user_id, event_type, msg, reply_token

    def process(self, event=None, file=None):
        ret = ''
        event_dict = {}
        user_id, event_type, msg, reply_token = LineBotHandler.parsing_event(event)

        if user_id not in event_dict:
            event_dict[user_id] = LineBotHandler.initial_user_stat()

        match event_type:
            case 'text':
                event_dict[user_id]['text_count'] += 1
            case 'image':
                event_dict[user_id]['media_count'] += 1
            case _:
                self.log_warning(f'[ERROR] event_type: {event_type}')

        match msg.lower():
            case 'identify food and feedback':
                event_dict[user_id]['identify food and feedback'] += 1
                ret = 'Coming Soon ...'

            case 'gif meme name search':
                event_dict[user_id]['gif meme name search'] += 1
                ret = 'Coming Soon ...'

            case 'human companion robot':
                event_dict[user_id]['human companion robot'] += 1
                ret = 'Coming Soon ...'

            case 'generate self-introduction':
                event_dict[user_id]['generate self-introduction'] += 1
                ret = 'Coming Soon ...'

            case event_type if event_type[:5] == 'admin':
                ret = self.gemini.chat(msg[5:])

            case _:
                ret = "<ERROR> The format doesn't match type."

        # finally
        self.log_warning(f"user id: {user_id}, content type: {event_type}, msg: {msg}")
        self.linebot_api.reply_message(reply_token, TextSendMessage(ret))

        # save record
        check_datum = self.get_datum(db_name=TLineGenAIField.DB_NAME.value,
                                     table_format=TLineGenAIFormat,
                                     **{'SQL_WHERE': f"USER_ID = '{user_id}'"})
        datum = {
            user_id: {
                TLineGenAIField.USER_ID.value: user_id,
                TLineGenAIField.TEXT_COUNT.value: event_dict[user_id]['text_count'],
                TLineGenAIField.MEDIA_COUNT.value: event_dict[user_id]['media_count'],
                TLineGenAIField.A_SERVE.value: event_dict[user_id]['identify food and feedback'],
                TLineGenAIField.B_SERVE.value: event_dict[user_id]['gif meme name search'],
                TLineGenAIField.C_SERVE.value: event_dict[user_id]['human companion robot'],
                TLineGenAIField.D_SERVE.value: event_dict[user_id]['generate self-introduction'],
            }
        }
        if check_datum != {}:
            datum[user_id][TLineGenAIField.TEXT_COUNT.value] += check_datum[user_id]['TEXT_COUNT']
            datum[user_id][TLineGenAIField.MEDIA_COUNT.value] += check_datum[user_id]['MEDIA_COUNT']
            datum[user_id][TLineGenAIField.A_SERVE.value] += check_datum[user_id]['A_SERVE']
            datum[user_id][TLineGenAIField.B_SERVE.value] += check_datum[user_id]['B_SERVE']
            datum[user_id][TLineGenAIField.C_SERVE.value] += check_datum[user_id]['C_SERVE']
            datum[user_id][TLineGenAIField.D_SERVE.value] += check_datum[user_id]['D_SERVE']

        self.save_datum(db_name=TLineGenAIField.DB_NAME.value,
                        table_format=TLineGenAIFormat,
                        save_data=datum)