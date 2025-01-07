# -*- coding: utf-8 -*-
"""
@author: PC
Update Time: 2025-01-08
"""
import google.generativeai as genai
from package.base import BaseLogic

MODEL_TYPE = 'gemini-1.5-flash'

class GeminiFormat:
    def __init__(self, obj):
        self.obj = obj

    def chat(self, msg, token):
        genai.configure(api_key=token)
        model = genai.GenerativeModel(MODEL_TYPE)
        res = model.generate_content(msg)
        return res.text