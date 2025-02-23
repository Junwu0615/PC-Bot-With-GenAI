# -*- coding: utf-8 -*-
"""
@author: PC
"""
import os, time, copy, json
import requests, subprocess
from subprocess import PIPE, STDOUT
from decimal import Decimal, ROUND_HALF_UP
from linebot import LineBotApi, WebhookHandler
from linebot.models import TextSendMessage

from package.gemini import GeminiFormat
from developer.package.interface import Interface
from developer.model.TLineGenAI import TLineGenAIField, TLineGenAIFormat

SAVE_PATH = './preprocess'
TEXT_SERVE = ["creator’s github", "creator’s dashboard", 'human companion robot']
NORM_SERVE = ['identify food and feedback', 'gif meme name search', 'generate self-introduction']
SPECIAL_MISSION = ['admin', 'upload to gist']
GIST_API_URL = "https://api.github.com/gists"

class LineBotHandler(Interface):
    def __init__(self, linebot_token, gemini_token, github_token):
        super().__init__([])
        self.use_count = 0
        self.gemini = GeminiFormat(self, gemini_token)
        self.linebot_token = linebot_token
        self.github_token = github_token
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
        linebot_token = LineBotApi(os.environ.get('LINE_ACCESS_TOKEN'))
        handler = WebhookHandler(os.environ.get('LINE_SECRET_TOKEN'))
        gemini_token = os.environ.get('GEMINI_TOKEN')
        github_token = os.environ.get('GITHUB_PERSONAL_TOKEN')
        return linebot_token, handler, gemini_token, github_token

    @staticmethod
    def initial_stat() -> tuple[dict, dict, str]:
        stat = {
            'text_count': 0,
            'media_count': 0,
            "creator’s github": 0, # A
            'identify food and feedback': 0, # B
            'gif meme name search': 0, # C
            "creator’s dashboard": 0, # D
            'human companion robot': 0, # E
            'generate self-introduction': 0, # F
        }
        event = {'msg': 'None', 'file1': None, 'file2': None}
        return event, stat, ''

    def update_webhook(self):
        try:
            self.log_warning('Wait for NGROK to start (10s) ...')
            time.sleep(15)
            self.log_warning('Update Linebot Webhook...')
            linebot_token = os.environ.get('LINE_ACCESS_TOKEN')
            args = 'curl -s http://localhost:4040/api/tunnels' if os.environ.get('DOCKER_BOOL') is None \
                else 'curl -s http://172.17.0.1:4040/api/tunnels' # 172.17.0.1 代表 Docker Host (即 VM 本身)
            pop = subprocess.Popen(args,
                                   stdout=PIPE,
                                   stderr=STDOUT,
                                   shell=True,
                                   )
            while pop.poll() is None:
                line = pop.stdout.readline()
                try:
                    line = line.decode('utf8')
                    if line != '':
                        # self.log_info(line)
                        loader = json.loads(line)
                        headers = {
                            "Content-Type": "application/json",
                            "Authorization": f"Bearer {linebot_token}"
                        }
                        url = f"{loader['tunnels'][0]['public_url']}/callback"
                        payload = {
                            "endpoint": url
                        }
                        res = requests.put("https://api.line.me/v2/bot/channel/webhook/endpoint",
                                           headers=headers,
                                           data=json.dumps(payload))
                        self.log_warning(f"[Change Webhook URL] callback | code: {res.status_code} | url: {url}")

                        headers = {
                            "Authorization": f"Bearer {linebot_token}"
                        }
                        res = requests.post("https://api.line.me/v2/bot/channel/webhook/test",
                                            headers=headers)
                        self.log_warning(f"[Verify Webhook URL] callback | code: {res.status_code} | content: {res.text}")

                except UnicodeDecodeError as e:
                    pass
                except:
                    self.log_error(exc_info=True)

        except:
            self.log_error(exc_info=True)

    def switch_gist(self):
        file = './package/git_gist.txt'
        if os.path.exists(file):
            gist_id = [i for i in open(file, 'r')][0]
            self.ret = self.patch_upload_to_gist(gist_id)
        else:
            self.ret = self.once_upload_to_gist()

    def once_upload_to_gist(self) -> str:
        # 單純上傳數據
        get_data = self.get_datum(db_name=TLineGenAIField.DB_NAME.value, table_format=TLineGenAIFormat, **{'SQL_WHERE': "1=1'"})
        stat = {'user': 0, 'text count': 0, 'media count': 0,
                'a. service': 0, 'b. service': 0, 'c. service': 0,
                'd. service': 0, 'e. service': 0, 'f. service': 0}
        for k,v in get_data.items():
            stat['user'] += 1
            stat['text count'] += v['TEXT_COUNT']
            stat['media count'] += v['MEDIA_COUNT']
            stat['a. service'] += v['A_SERVE']
            stat['b. service'] += v['B_SERVE']
            stat['c. service'] += v['C_SERVE']
            stat['d. service'] += v['D_SERVE']
            stat['e. service'] += v['E_SERVE']
            stat['f. service'] += v['F_SERVE']

        payload = {
            'description': 'For streamlit dashboard using.',
            'public': True,
            'files': {
                'PC-Bot-With-GenAI.json': {
                    'content': json.dumps(stat, ensure_ascii=False, indent=4)
                }
            }
        }
        headers = {"Authorization": f"token {self.github_token}"}
        res = requests.post(GIST_API_URL, json=payload, headers=headers)
        if res.status_code in [200, 201]:
            gist_url = res.json()["html_url"]
            ret = f'Gist created successfully! URL: {gist_url}'
            self.log_warning(ret)
            # 第一次上傳保留位置紀錄，下次直接基於紀錄延續做更新
            with open('./package/git_gist.txt', 'w') as f:
                f.write(gist_url.split('/')[-1])
            return ret
        else:
            ret = f'Failed to create Gist: {res.status_code}'
            self.log_error(f'{ret}')
            return ret

    def patch_upload_to_gist(self, gist_id: str) -> str:
        # 更新既有數據
        get_data = self.get_datum(db_name=TLineGenAIField.DB_NAME.value, table_format=TLineGenAIFormat, **{'SQL_WHERE': "1=1'"})
        stat = {'user': 0, 'text count': 0, 'media count': 0,
                'a. service': 0, 'b. service': 0, 'c. service': 0,
                'd. service': 0, 'e. service': 0, 'f. service': 0}
        for k,v in get_data.items():
            stat['user'] += 1
            stat['text count'] += v['TEXT_COUNT']
            stat['media count'] += v['MEDIA_COUNT']
            stat['a. service'] += v['A_SERVE']
            stat['b. service'] += v['B_SERVE']
            stat['c. service'] += v['C_SERVE']
            stat['d. service'] += v['D_SERVE']
            stat['e. service'] += v['E_SERVE']
            stat['f. service'] += v['F_SERVE']

        payload = {
            'description': 'For streamlit dashboard using.',
            'public': True,
            'files': {
                'PC-Bot-With-GenAI.json': {
                    'content': json.dumps(stat, ensure_ascii=False, indent=4)
                }
            }
        }
        headers = {"Authorization": f"token {self.github_token}"}
        res = requests.post(GIST_API_URL + '/' + gist_id, json=payload, headers=headers)
        if res.status_code in [200, 201]:
            gist_url = res.json()["html_url"]
            ret = f'Gist update data successfully! URL: {gist_url}'
            self.log_warning(ret)
            return ret
        else:
            ret = f'Failed to update data: {res.status_code}'
            self.log_error(f'{ret}')
            return ret

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
                TLineGenAIField.A_SERVE.value: stat["creator’s github"],
                TLineGenAIField.B_SERVE.value: stat['identify food and feedback'],
                TLineGenAIField.C_SERVE.value: stat['gif meme name search'],
                TLineGenAIField.D_SERVE.value: stat["creator’s dashboard"],
                TLineGenAIField.E_SERVE.value: stat['human companion robot'],
                TLineGenAIField.F_SERVE.value: stat['generate self-introduction'],
            }
        }
        if check_datum != {} and user_id in check_datum:
            datum[user_id][TLineGenAIField.TEXT_COUNT.value] += check_datum[user_id]['TEXT_COUNT']
            datum[user_id][TLineGenAIField.MEDIA_COUNT.value] += check_datum[user_id]['MEDIA_COUNT']
            datum[user_id][TLineGenAIField.A_SERVE.value] += check_datum[user_id]['A_SERVE']
            datum[user_id][TLineGenAIField.B_SERVE.value] += check_datum[user_id]['B_SERVE']
            datum[user_id][TLineGenAIField.C_SERVE.value] += check_datum[user_id]['C_SERVE']
            datum[user_id][TLineGenAIField.D_SERVE.value] += check_datum[user_id]['D_SERVE']
            datum[user_id][TLineGenAIField.E_SERVE.value] += check_datum[user_id]['E_SERVE']
            datum[user_id][TLineGenAIField.F_SERVE.value] += check_datum[user_id]['F_SERVE']

        self.save_datum(db_name=TLineGenAIField.DB_NAME.value,
                        table_format=TLineGenAIFormat,
                        save_data=datum)

    def process(self, event=None, file=None):
        try:
            self.use_count += 1
            user_id, event_type, msg, reply_token = self.parsing_event(event)

            # 應處理接收字串的判斷式
            if ((self.event['msg'].lower() in NORM_SERVE or self.event['msg'].lower() in TEXT_SERVE)
                    and (msg.lower() in NORM_SERVE or msg.lower() in TEXT_SERVE)):
                self.event, self.stat, self.ret = LineBotHandler.initial_stat()
                self.event['msg'] = msg
            elif msg.lower() in NORM_SERVE or msg.lower() in TEXT_SERVE:
                self.event['msg'] = msg
            elif msg.lower()[:5] in SPECIAL_MISSION:
                self.event['msg'] = msg
            elif msg.lower()[:14] in SPECIAL_MISSION:
                self.event['msg'] = msg

            # [其他服務] 接受檔案的判斷式
            if file is not None:
                self.event['file1'] = file

            # [生成自介] 接受檔案的判斷式
            if (self.event['msg'] == 'Generate Self-Introduction' and
                    self.event['file1'] is None and msg != 'Generate Self-Introduction' and 'http' in msg):
                self.event['file1'] = msg

            elif (self.event['msg'] == 'Generate Self-Introduction' and
                    self.event['file1'] is not None and msg != 'Generate Self-Introduction' and 'http' in msg):
                self.event['file2'] = msg

            elif (self.event['msg'] == 'Generate Self-Introduction' and
                    self.event['file1'] is not None and msg != 'Generate Self-Introduction' and SAVE_PATH in file):
                self.event['file2'] = file

            elif (self.event['msg'] == 'Generate Self-Introduction' and
                    self.event['file1'] is None and msg != 'Generate Self-Introduction' and 'http' not in msg):
                self.event['msg'] = 'None'

            elif (self.event['msg'] == 'Generate Self-Introduction' and
                    self.event['file1'] is not None and msg != 'Generate Self-Introduction' and 'http' not in msg):
                self.event['msg'] = 'None'

            self.log_info(f'{self.event}')

            if self.event['msg'] == 'None' and self.event['file1'] is not None:
                self.event, self.stat, self.ret = LineBotHandler.initial_stat()
                self.ret = '<ERROR: 0> wrong order of operations.'
                self.linebot_token.reply_message(reply_token, TextSendMessage(self.ret))

            elif self.event['msg'] != 'None' and self.event['file1'] is None:
                match self.event['msg'].lower():
                    case "creator’s github":
                        self.ret = 'https://github.com/Junwu0615'
                        self.stat["creator’s github"] += 1
                        self.stat['text_count'] += 1

                    case "creator’s dashboard":
                        self.ret = 'https://pc-dashboard.streamlit.app/'
                        self.stat["creator’s dashboard"] += 1
                        self.stat['text_count'] += 1

                    case 'identify food and feedback':
                        self.ret = '請上傳食物照片'

                    case 'gif meme name search':
                        self.ret = '請上傳迷因圖檔 (jpg/png/gif/...)'

                    case 'human companion robot':
                        self.ret = 'Coming Soon ...'
                        self.stat['human companion robot'] += 1
                        self.stat['text_count'] += 1

                    case 'generate self-introduction':
                        self.ret = '請貼上欲應徵職缺連結'

                    case msg if msg[:14] == 'upload to gist':
                        # self.switch_gist()
                        self.stat['text_count'] += 1

                    case msg if msg[:5] == 'admin':
                        self.ret = self.gemini.career_consultant_chat(msg[5:])
                        self.stat['text_count'] += 1

                    case _:
                        self.ret = "<ERROR: 1> The format doesn't match type."

                self.linebot_token.reply_message(reply_token, TextSendMessage(self.ret))
                if self.event['msg'].lower() not in NORM_SERVE:
                    # self.save_state_db(user_id, self.stat)
                    self.event, self.stat, self.ret = LineBotHandler.initial_stat()

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
                        self.ret = "<ERROR: 2> The format doesn't match type."

                self.linebot_token.reply_message(reply_token, TextSendMessage(self.ret))
                if self.stat['media_count'] == 0 and self.event['msg'].lower() in NORM_SERVE:
                    pass

                elif self.stat['media_count'] == 0 and msg.lower() not in NORM_SERVE:
                    self.event, self.stat, self.ret = LineBotHandler.initial_stat()

                else:
                    self.log_warning(f"user id: {user_id}, content type: {event_type}, msg: {msg}")
                    # self.save_state_db(user_id, self.stat)
                    self.event, self.stat, self.ret = LineBotHandler.initial_stat()

            else:
                self.event, self.stat, self.ret = LineBotHandler.initial_stat()
                self.ret = '<ERROR: 3> UNKNOWN'
                self.linebot_token.reply_message(reply_token, TextSendMessage(self.ret))

            if self.use_count % 10 == 0:
                # self.switch_gist()
                pass

        except:
            self.log_error(exc_info=True)
            self.event, self.stat, self.ret = LineBotHandler.initial_stat()