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

### *STEP.1　Clone*
```python
git clone https://github.com/Junwu0615/PC-Bot-With-GenAI.git
```

### *STEP.2　進入腳本路徑*
```bash
cd docker
```

### *STEP.3　新增檔案 : `./script/.env`*
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
NGROK_AUTHTOKEN=[Fill In Your Token]
DOCKER_BOOL=True
```

### *STEP.4　安裝 Dockerfile*
```bash
docker build -t pc-bot-with-genai:latest -f script/Dockerfile . --no-cache
```

### *STEP.5　安裝 docker-compose*
```bash
docker stack deploy -c script/docker-compose.yaml pc-bot-with-genai
```
![jpg](/sample/docker_00.jpg)

### *STEP.6　檢視 docker service 清單*
```bash
docker service ls
```
![jpg](/sample/docker_01.jpg)

### *STEP.7　查看 stack service 數量是否正確*
```bash
docker stack ls
```
![jpg](/sample/docker_02.jpg)

### *STEP.8　查看專案 log 打印*
```bash
docker service logs -f pc-bot-with-genai_ngrok
```
![jpg](/sample/docker_03.jpg)
```bash
docker service logs -f pc-bot-with-genai_task
```
![jpg](/sample/docker_04.jpg)