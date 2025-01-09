# -*- coding: utf-8 -*-
"""
@author: PC
Update Time: 2025-01-08
"""
import google.generativeai as genai

MODEL_TYPE = 'gemini-1.5-flash'

class GeminiFormat:
    def __init__(self, obj, token):
        self.obj = obj
        self.token = token

    def media(self, msg: str, file) -> str:
        genai.configure(api_key=self.token)
        model = genai.GenerativeModel(MODEL_TYPE)
        # organ = PIL.Image.open("/path/to/organ.png")
        response = model.generate_content([msg, file])
        print(response.text)
        return res.text

    def chat(self, msg: str) -> str:
        # create the prompt.
        prompt = f"""
        你是一位專業的繁體中文職涯顧問
        問題內容: {msg}
        """

        genai.configure(api_key=self.token)
        model = genai.GenerativeModel(MODEL_TYPE)
        res = model.generate_content(prompt)
        return res.text