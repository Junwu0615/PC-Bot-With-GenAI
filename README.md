<a href='https://github.com/Junwu0615/PC-Bot-With-GenAI'><img alt='GitHub Views' src='https://views.whatilearened.today/views/github/Junwu0615/PC-Bot-With-GenAI.svg'> <br> 
[![](https://img.shields.io/badge/Project-GenAI-blue.svg?style=plastic)](https://github.com/Junwu0615/PC-Bot-With-GenAI) 
[![](https://img.shields.io/badge/Project-Docker-blue.svg?style=plastic)](https://github.com/Junwu0615/PC-Bot-With-GenAI) 
[![](https://img.shields.io/badge/Platform-Linebot-blue.svg?style=plastic)](https://developers.line.biz/zh-hant/) 
[![](https://img.shields.io/badge/Platform-Ngrok-blue.svg?style=plastic)](https://ngrok.com/)
[![](https://img.shields.io/badge/Language-Python_3.12.0-blue.svg?style=plastic)](https://www.python.org/) <br>
[![](https://img.shields.io/badge/Package-Google_Generativeai_0.8.3-green.svg?style=plastic)](https://pypi.org/project/requests/) 
[![](https://img.shields.io/badge/Package-Flask_3.0.0-green.svg?style=plastic)](https://pypi.org/project/Flask/) 
[![](https://img.shields.io/badge/Package-LineBot_SDK_3.5.1-green.svg?style=plastic)](https://pypi.org/project/line-bot-sdk/) 

<br>


## *A.　Showcase Results*
### *STEP.1　Add Linebot*
<img width='200' height='200' src="https://github.com/Junwu0615/PC-Bot-With-GenAI/blob/main/sample/linebot_qrcode.png"/>

<br>

## *B.　How To Use*

### *STEP.1　Clone*
```python
git clone https://github.com/Junwu0615/PC-Bot-With-GenAI.git
```
### *STEP.2　Requirements*
```python
pip install -r requirements.txt
```
### *STEP.3　Run*
```python
python Entry.py
```
### *STEP.4　Open ngrok.exe*
```python
# Flask's Port: 5000
ngrok http 5000
```
- `Forwarding` 後面的網址複製起來，ex: https://xxxx.ngrok-free.app
- 到 [LINE Developer](https://developers.line.biz/zh-hant/) 中 Channel 的 `Messaging API`，找到標籤 `Webhook URL` 將網址更新上去。

<br>

## *C.　Dockerization*

### *Directory Structure Diagram*
```commandline
PC-Bot-With-GenAI/docker
  ├── app
  │   ├── package
  │   │   ├── __init__.py
  │   │   ├── gemini.py
  │   │   ├── linebot.py
  │   │   └── git_gist.txt
  │   ├── Entry.py
  │   └── requirements.txt
  └── script
      ├── .env
      ├── docker-compose.yaml
      └── Dockerfile
```

### *STEP.1　進入腳本路徑*
```bash
cd docker
```

### *STEP.2　新增檔案 : `./script/.env`*
```commandline
SQL_SERVICE_DRIVER=17
SQL_SERVICE_BROKER_HOST=<Your SQL Server IP>,<YOUR SQL Server Port>
SQL_SERVICE_LOGIN_USER=<Your User Name>
SQL_SERVICE_LOGIN_PASSWORD=<Your User Password>
SAVE_PATH=/builds/rep/preprocess
LINE_ACCESS_TOKEN=[Fill In Your Access Token]
LINE_SECRET_TOKEN=[Fill In Your Secret]
GEMINI_TOKEN=[Fill In Your Token]
GITHUB_PERSONAL_TOKEN=[Fill In Your Token]
```

### *STEP.3　安裝 Dockerfile*
```bash
docker build -t pc-bot-with-genai:latest -f script/Dockerfile . --no-cache
```

### *STEP.4　安裝 docker-compose*
```bash
docker stack deploy -c script/docker-compose.yaml pc-bot-with-genai
```

### *STEP.5　檢視 docker service 清單*
```bash
docker service ls
```

### *STEP.6　查看專案 log 打印*
```bash
docker service logs -f pc-bot-with-genai-task
```

![docker_01.jpg](/sample/docker_01.jpg)