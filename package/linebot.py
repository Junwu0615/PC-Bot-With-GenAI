# -*- coding: utf-8 -*-
"""
@author: PC
Update Time: 2025-01-09
"""
import copy, json
from datetime import datetime
from flask import request, Flask, abort
from linebot import LineBotApi, WebhookHandler
from linebot.models import MessageEvent, TextSendMessage, TextMessage, FileMessage, ImageMessage

from package.gemini import GeminiFormat
from developer.package.norm_function import DATE_YMD_ONE
from developer.package.interface import Interface
from developer.definition.state import State
from developer.model.TLineGenAI import TLineGenAIField, TLineGenAIFormat

class LineBotHandler(Interface):
    def __init__(self):
        super().__init__([])
        self.app = Flask(__name__)
        self.linebot_api, self.handler, gemini_token = LineBotHandler.token_settings()
        self.gemini = GeminiFormat(self, gemini_token)
        self.register_event()
        self.register_routes()

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
    def parsing_body(body) -> tuple:
        loader = json.loads(body)
        loader = loader['events'][0]
        reply_token = loader['replyToken']
        user_id = loader['source']['userId']
        event_type = loader['message']['type'].lower()

        match event_type:
            case 'text':
                msg = loader['message']['text']
                return reply_token, user_id, event_type, msg
            case 'image':
                return reply_token, user_id, event_type, 'None'

    def register_event(self):
        self.handler.add(MessageEvent, message=TextMessage)(self.process)
        self.handler.add(MessageEvent, message=FileMessage)(self.process)
        self.handler.add(MessageEvent, message=ImageMessage)(self.process)

    def process(self, event):
        self.log_info(f"Event received: {event}")
        if isinstance(event.message, TextMessage):
            self.log_info(f"Text message: {event.message.text}")
        elif isinstance(event.message, FileMessage):
            self.log_info(f"File message: {event.message.file_name}")
        elif isinstance(event.message, ImageMessage):
            self.log_info("Image message received.")

        file_id = event.message.id
        file_name = event.message.file_name
        file_size = event.message.file_size
        message_content = line_bot_api.get_message_content(file_id)
        self.log_warning(f'file_id: {file_id}, file_name: {file_name}, file_size: {file_size}')

        ret = None
        event_dict = {}
        reply_token, user_id, event_type, msg = LineBotHandler.parsing_body(body)

        if user_id not in event_dict:
            event_dict[user_id] = LineBotHandler.initial_user_stat()

        match event_type:
            case 'text':
                event_dict[user_id]['text_count'] += 1
            case 'media' | 'image':
                event_dict[user_id]['media_count'] += 1
            case _:
                print(f'[ERROR] event_type: {event_type}')

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
                ret =  "<ERROR> The format doesn't match type."

        # finally
        self.log_warning(f"user id: {user_id}, content type: {event_type}, msg: {msg}")
        self.linebot_api.reply_message(reply_token, TextSendMessage(ret))

        # save record
        # json.dump(event_dict, open('sample/record.json', 'w'))
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

    def register_routes(self):
        self.app.add_url_rule('/callback', methods=['POST'], view_func=self.callback)

    def callback(self):
        body = request.get_data(as_text=True)
        signature = request.headers['X-Line-Signature']
        try:
            self.log_info(f'Received body: {body}')
            self.log_info(f'Received signature: {signature}')
            self.handler.handle(body, signature)

        except:
            self.log_error(exc_info=True)
            abort(400)
        finally:
            return '', 200

    def run(self, host='0.0.0.0', port=5000):
        self.app.run(port=port)
        # self.app.run(host=host, port=port)