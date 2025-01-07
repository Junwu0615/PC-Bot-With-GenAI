# -*- coding: utf-8 -*-
"""
@author: PC
Update Time: 2025-01-08
"""
import copy
from flask import request, Flask
from package.linebot import LineBotHandler

lbh = LineBotHandler()
app = Flask(__name__)

@app.route('/', methods=['POST'])
def main():
    body = request.get_data(as_text=True)
    lbh.process(body)
    return '', 200

if __name__ == '__main__':
    app.run()