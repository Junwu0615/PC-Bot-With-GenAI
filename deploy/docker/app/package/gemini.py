# -*- coding: utf-8 -*-
"""
@author: PC
"""
import base64
import google.generativeai as genai
from PIL import Image

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
        我希望你扮演 "閱覽無數個迷因內容的迷因大師" 的角色。
        * 這張迷因圖可能的名稱?
        * 遵守下列條件:
        - 名稱用[英文表達]
        - 只顯示答覆結果，無贅詞，無多餘換行等
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
        我希望你扮演 "美食家兼營養學大師" 的角色。
        * 你收到一張食物圖，描述看到哪些食物。
        * 這些食物是否有改善空間。
        * 評估可能富含的營養成分。
        * 推估可能的熱量。
        * 遵守下列條件:
        - 只顯示答覆結果，無贅詞，無多餘換行等
        - 無法識別也明確答覆
        - 請勿幻覺答覆
        """
        res = model.generate_content([prompt, organ])
        return res.text

    def resume_chat_http(self, file1: str, file2: str) -> str:
        # 基於履歷生成字介簡述 # 網頁資源
        genai.configure(api_key=self.token)
        model = genai.GenerativeModel(MODEL_TYPE)
        prompt = f"""
        我希望你扮演 "專業的繁體中文職涯顧問" 的角色。
        我會提供一份求職者的履歷給你，你的任務是基於給予的履歷生成簡潔且符合事實的自我介紹。
        * 求職者欲投職缺: {file1}
        * 求職者履歷資源: {file2}
        * 遵守下列條件:
        - 須上網了解求職者履歷
        - 須上網了解求職者欲投職缺
        - 只顯示答覆結果，無贅詞，無多餘換行等
        - 請勿幻覺答覆
        - 字數限定 500 字內，非一定要達滿 500 字。
        """
        res = model.generate_content(prompt)
        return res.text

    def resume_chat_file(self, file1: str, file2: str) -> str:
        # 基於履歷生成字介簡述 # 線下資源
        genai.configure(api_key=self.token)
        model = genai.GenerativeModel(MODEL_TYPE)

        with open(file2, "rb") as doc_file:
            doc_data = base64.standard_b64encode(doc_file.read()).decode("utf-8")

        prompt = f"""
        我希望你扮演 "專業的繁體中文職涯顧問" 的角色。
        我會提供一份求職者的履歷給你，你的任務是基於給予的履歷生成簡潔且符合事實的自我介紹。
        * 求職者欲投職缺: {file1}
        * 遵守下列條件:
        - 只顯示答覆結果，無贅詞，無多餘換行等。
        - 請勿幻覺答覆。
        - 字數限定 500 字內，非一定要達滿 500 字。
        """
        res = model.generate_content([{'mime_type': 'application/pdf', 'data': doc_data}, prompt])
        return res.text

    def career_consultant_chat(self, msg: str) -> str:
        # 專業的繁體中文職涯顧問
        prompt = f"""
        我希望你扮演 "專業的繁體中文職涯顧問" 的角色。
        我會提供一位尋求職涯指導的個人給你，你的任務是幫助他們根據自己的技能、興趣和經驗確定最適合他們的職業。
        你還應該進行研究，解釋不同行業的就業市場趨勢，並建議追求特定領域所需的相關資格。
        * 問題內容: {msg}
        * 遵守下列條件:
        - 只顯示答覆結果，無贅詞，無多餘換行等。
        - 請勿幻覺答覆。
        - 字數限定 500 字內，非一定要達滿 500 字。
        """
        genai.configure(api_key=self.token)
        model = genai.GenerativeModel(MODEL_TYPE)
        res = model.generate_content(prompt)
        return res.text