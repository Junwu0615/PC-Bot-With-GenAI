# -*- coding: utf-8 -*-
"""
@author: PC
Update Time: 2025-01-10
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

SAVE_PATH = './preprocess'
NORM_SERVE = ['identify food and feedback', 'gif meme name search',
              'human companion robot', 'generate self-introduction']

class LineBotHandler(Interface):
    def __init__(self, linebot_api, gemini_token):
        super().__init__([])
        self.gemini = GeminiFormat(self, gemini_token)
        self.linebot_api = linebot_api
        self.event, self.stat, self.ret = LineBotHandler.initial_stat()

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
                    self.log_error('*** [token_settings] other error ***')
        return linebot_api, handler, gemini_token

    @staticmethod
    def initial_stat() -> tuple[dict, dict, str]:
        stat = {
            'text_count': 0,
            'media_count': 0,
            'identify food and feedback': 0,
            'gif meme name search': 0,
            'human companion robot': 0,
            'generate self-introduction': 0,
        }
        event = {'msg': 'None', 'file1': None, 'file2': None}
        return event, stat, ''

    def parsing_event(self, event) -> tuple[str, str, str, str]:
        user_id = event.source.user_id
        event_type = event.message.type
        reply_token = event.reply_token
        match event_type:
            case 'text':
                msg = event.message.text
                return user_id, event_type, msg, reply_token
            case 'image':
                return user_id, event_type, '', reply_token
            case 'file':
                return user_id, event_type, '', reply_token
            case _:
                self.log_error('*** [parsing_event] other error ***')

    def save_state_db(self, user_id: str, stat: dict):
        check_datum = self.get_datum(db_name=TLineGenAIField.DB_NAME.value,
                                     table_format=TLineGenAIFormat,
                                     **{'SQL_WHERE': f"USER_ID = '{user_id}'"})
        datum = {
            user_id: {
                TLineGenAIField.USER_ID.value: user_id,
                TLineGenAIField.TEXT_COUNT.value: stat['text_count'],
                TLineGenAIField.MEDIA_COUNT.value: stat['media_count'],
                TLineGenAIField.A_SERVE.value: stat['identify food and feedback'],
                TLineGenAIField.B_SERVE.value: stat['gif meme name search'],
                TLineGenAIField.C_SERVE.value: stat['human companion robot'],
                TLineGenAIField.D_SERVE.value: stat['generate self-introduction'],
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

    def process(self, event=None, file=None):
        try:
            user_id, event_type, msg, reply_token = self.parsing_event(event)
            if msg.lower() in NORM_SERVE:
                self.event['msg'] = msg
            if file is not None:
                self.event['file1'] = file

            if (self.event['msg'] == 'Generate Self-Introduction' and
                    self.event['file1'] is None and msg != 'Generate Self-Introduction' and 'http' in msg):
                self.event['file1'] = msg

            elif (self.event['msg'] == 'Generate Self-Introduction' and
                    self.event['file1'] is not None and msg != 'Generate Self-Introduction' and 'http' in msg):
                self.event['file2'] = msg

            elif (self.event['msg'] == 'Generate Self-Introduction' and
                    self.event['file1'] is not None and msg != 'Generate Self-Introduction' and SAVE_PATH in file):
                self.event['file2'] = file

            self.log_info(f'{self.event}')

            if self.event['msg'] == 'None' and self.event['file1'] is not None:
                self.event, self.stat, self.ret = LineBotHandler.initial_stat()
                self.ret = '<ERROR: 0> wrong order of operations.'
                self.linebot_api.reply_message(reply_token, TextSendMessage(self.ret))

            elif self.event['msg'] != 'None' and self.event['file1'] is None:
                match self.event['msg'].lower():
                    case 'identify food and feedback':
                        self.ret = '請上傳食物照片'

                    case 'gif meme name search':
                        self.ret = '請上傳迷因圖檔 (jpg/png/gif/...)'

                    case 'human companion robot':
                        self.ret = 'Coming Soon ...'

                    case 'generate self-introduction':
                        self.ret = '請貼上欲應徵職缺連結'

                    case event_type if event_type[:5] == 'admin':
                        self.ret = self.gemini.casual_chat(msg[5:])
                        self.stat['text_count'] += 1
                        self.save_state_db(user_id, self.stat)
                        self.event, self.stat, self.ret = LineBotHandler.initial_stat()

                    case _:
                        self.event, self.stat, self.ret = LineBotHandler.initial_stat()
                        self.ret = "<ERROR: 1> The format doesn't match type."

                self.linebot_api.reply_message(reply_token, TextSendMessage(self.ret))

            elif self.event['msg'] != 'None' and self.event['file1'] is not None:
                match self.event['msg'].lower():
                    case 'identify food and feedback':
                        self.ret = self.gemini.food_feedback(self.event['file1'])
                        self.stat['identify food and feedback'] += 1
                        self.stat['media_count'] += 1

                    case 'gif meme name search':
                        self.ret = self.gemini.meme_search(self.event['file1'])
                        self.stat['gif meme name search'] += 1
                        self.stat['media_count'] += 1

                    case 'human companion robot':
                        self.ret = 'Coming Soon ...'
                        self.stat['human companion robot'] += 1
                        self.stat['media_count'] += 1

                    case 'generate self-introduction':
                        if self.event['file2'] is None:
                            self.ret = '請上傳履歷或是個人簡歷連結'
                        else:
                            if 'http' in self.event['file2']:
                                self.ret = self.gemini.resume_chat_http(self.event['file1'], self.event['file2'])
                            else:
                                self.ret = self.gemini.resume_chat_file(self.event['file1'], self.event['file2'])
                            self.stat['generate self-introduction'] += 1
                            self.stat['media_count'] += 1

                    case _:
                        self.event, self.stat, self.ret = LineBotHandler.initial_stat()
                        self.ret = "<ERROR: 2> The format doesn't match type."

                if self.stat['media_count'] == 0:
                    self.linebot_api.reply_message(reply_token, TextSendMessage(self.ret))
                else:
                    self.log_warning(f"user id: {user_id}, content type: {event_type}, msg: {msg}")
                    self.linebot_api.reply_message(reply_token, TextSendMessage(self.ret))
                    self.save_state_db(user_id, self.stat)
                    self.event, self.stat, self.ret = LineBotHandler.initial_stat()

            else:
                self.event, self.stat, self.ret = LineBotHandler.initial_stat()
                self.ret = '<ERROR: 3> UNKNOWN'
                self.linebot_api.reply_message(reply_token, TextSendMessage(self.ret))

        except:
            self.log_error(exc_info=True)
            self.event, self.stat, self.ret = LineBotHandler.initial_stat()