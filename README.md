<a href='https://github.com/Junwu0615/PC-Bot-With-GenAI'><img alt='GitHub Views' src='https://views.whatilearened.today/views/github/Junwu0615/PC-Bot-With-GenAI.svg'> <br> 
[![](https://img.shields.io/badge/Platform-Line_Bot-blue.svg?style=plastic)](https://developers.line.biz/zh-hant/) 
[![](https://img.shields.io/badge/Platform-Ngrok-blue.svg?style=plastic)](https://ngrok.com/) 
[![](https://img.shields.io/badge/Project-Web_Crawler-blue.svg?style=plastic)](https://github.com/Junwu0615/PC-Bot-With-GenAI) 
[![](https://img.shields.io/badge/Language-Python_3.12.0-blue.svg?style=plastic)](https://www.python.org/) <br>
[![](https://img.shields.io/badge/Package-Requests_2.31.0-green.svg?style=plastic)](https://pypi.org/project/requests/) 
[![](https://img.shields.io/badge/Package-Flask_3.0.0-green.svg?style=plastic)](https://pypi.org/project/Flask/) 
[![](https://img.shields.io/badge/Package-LineBot_SDK_3.5.1-green.svg?style=plastic)](https://pypi.org/project/line-bot-sdk/) 

<br>


## A.　Showcase Results
### I.　Add LineBot
<img width='200' height='200' src="https://github.com/Junwu0615/PC-Bot-With-GenAI/blob/main/sample/linebot_qrcode.png"/>

<br>

## B.　How To Use
### STEP.1　CLONE
```python
git clone https://github.com/Junwu0615/PC-Bot-With-GenAI.git
```
### STEP.2　Change Content
#### 將 package `token_.txt` -> `token.txt` 修改內容。
```python
access_token,[Fill In Your Access Token]
secret,[Fill In Your Secret]
```
### STEP.3　Open CMD
```python
pip install -r requirements.txt
```
```python
python Entry.py
```
### STEP.4　Open ngrok.exe
```python
# Python 套件 Flask 的 port 為 5000
ngrok http 5000
```
- `Forwarding` 後面的網址複製起來，ex: https://xxxx.ngrok-free.app
- 到 [LINE Developer](https://developers.line.biz/zh-hant/) 中 Channel 的 `Messaging API`，找到標籤 `Webhook URL` 將網址更新上去。