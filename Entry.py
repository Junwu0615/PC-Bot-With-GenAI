# -*- coding: utf-8 -*-
"""
@author: PC
Update Time: 2025-01-09
"""
from package.linebot import LineBotHandler

if __name__ == '__main__':
    lbh = LineBotHandler()
    lbh.run(port=5000)