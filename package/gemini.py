# -*- coding: utf-8 -*-
"""
@author: PC
Update Time: 2025-01-10
"""
import base64
from PIL import Image
import google.generativeai as genai

MODEL_TYPE = 'gemini-1.5-flash'

class GeminiFormat:
    def __init__(self, obj, token):
        self.obj = obj
        self.token = token

    def meme_search(self, file1: str) -> str:
        # 迷因圖片搜尋
        genai.configure(api_key=self.token)
        model = genai.GenerativeModel(MODEL_TYPE)
        organ = Image.open(file1)
        prompt = f"""
        你是一位迷因大師，閱覽無數個迷因內容，同時記住迷因的名稱
        這張迷因圖是何名稱?
        * 遵守下列條件:
        - 名稱用[英文表達]
        - 只顯示結果，無贅詞等
        - 請勿幻覺答覆
        """
        res = model.generate_content([prompt, organ])
        return res.text

    def food_feedback(self, file1: str) -> str:
        # 食物營養識別反饋
        genai.configure(api_key=self.token)
        model = genai.GenerativeModel(MODEL_TYPE)
        organ = Image.open(file1)
        prompt = f"""
        你是一位嚐遍各國美食的美食家，同時也是營養學大師，擁有豐富的增肌減脂的經驗，
        這張食物圖，你看到哪些食物，並且這些食物是否有改善空間(營養成分, 熱量推估)
        * 遵守下列條件:
        - 答覆結果，無贅詞等
        - 無法識別也明確答覆
        - 請勿幻覺答覆
        """
        res = model.generate_content([prompt, organ])
        return res.text

    def resume_chat_http(self, file1: str, file2: str) -> str:
        # 履歷健檢 # 網頁資源
        genai.configure(api_key=self.token)
        model = genai.GenerativeModel(MODEL_TYPE)
        prompt = f"""
        你是一位專業的繁體中文職涯顧問，基於求職者欲投職缺，並基於給予的履歷生成簡潔的自我介紹。
        * 求職者欲投職缺: {file1}
        * 求職者履歷資源: {file2}
        * 遵守下列條件:
        - 須上網了解求職者履歷
        - 須上網了解求職者欲投職缺
        - 答覆結果，無贅詞等
        - 請勿幻覺答覆
        """
        res = model.generate_content(prompt)
        return res.text

    def resume_chat_file(self, file1: str, file2: str) -> str:
        # 履歷健檢 # 線下資源
        genai.configure(api_key=self.token)
        model = genai.GenerativeModel(MODEL_TYPE)

        with open(file2, "rb") as doc_file:
            doc_data = base64.standard_b64encode(doc_file.read()).decode("utf-8")

        prompt = f"""
        你是一位專業的繁體中文職涯顧問，基於求職者欲投職缺，並基於給予的履歷生成簡潔的自我介紹
        * 求職者欲投職缺: {file1}
        * 遵守下列條件:
        - 答覆結果，無贅詞等
        - 請勿幻覺答覆
        """
        res = model.generate_content([{'mime_type': 'application/pdf', 'data': doc_data}, prompt])
        return res.text

    def casual_chat(self, msg: str) -> str:
        # create the prompt.
        prompt = f"""
        你是一位專業的繁體中文職涯顧問
        問題內容: {msg}
        遵守下列條件:
        -答覆結果，無贅詞等
        -請勿幻覺答覆
        """
        genai.configure(api_key=self.token)
        model = genai.GenerativeModel(MODEL_TYPE)
        res = model.generate_content(prompt)
        return res.text