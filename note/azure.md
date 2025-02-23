<a href='https://github.com/Junwu0615/PC-Bot-With-GenAI'><img alt='GitHub Views' src='https://views.whatilearened.today/views/github/Junwu0615/PC-Bot-With-GenAI.svg'> 
<a href='https://github.com/Junwu0615/PC-Bot-With-GenAI'><img alt='GitHub Views' src='https://img.shields.io/badge/dynamic/json?color=success&label=Clone&query=count_total&url=https://gist.githubusercontent.com/Junwu0615/8c304a23bb8dad13ba9658dbaa3f806c/raw/PC-Bot-With-GenAI_clone.json&logo=github](https://github.com/Junwu0615/PC-Bot-With-GenAI'> <br>
[![](https://img.shields.io/badge/Project-GenAI_API-blue.svg?style=plastic)](https://github.com/Junwu0615/PC-Bot-With-GenAI) 
[![](https://img.shields.io/badge/Project-Docker-blue.svg?style=plastic)](https://github.com/Junwu0615/PC-Bot-With-GenAI)
[![](https://img.shields.io/badge/Language-Python_3.12.0-blue.svg?style=plastic)](https://www.python.org/) 
[![](https://img.shields.io/badge/Operating_System-Windows_10-blue.svg?style=plastic)](https://www.microsoft.com/zh-tw/software-download/windows10) <br>
[![](https://img.shields.io/badge/Platform-AWS-red.svg?style=plastic)](https://aws.amazon.com/) 
[![](https://img.shields.io/badge/Platform-Azure-red.svg?style=plastic)](https://azure.microsoft.com/zh-tw) 
[![](https://img.shields.io/badge/Platform-GCP-red.svg?style=plastic)](https://cloud.google.com/) 
[![](https://img.shields.io/badge/Platform-Linebot-red.svg?style=plastic)](https://developers.line.biz/zh-hant/) 
[![](https://img.shields.io/badge/Platform-Ngrok-red.svg?style=plastic)](https://ngrok.com/) <br>
[![](https://img.shields.io/badge/Database-SQL_Server-yellow.svg?style=plastic)](https://www.microsoft.com/zh-tw/sql-server/sql-server-downloads)
[![](https://img.shields.io/badge/Package-Google_Generativeai_0.8.3-green.svg?style=plastic)](https://pypi.org/project/requests/) 
[![](https://img.shields.io/badge/Package-Flask_3.0.0-green.svg?style=plastic)](https://pypi.org/project/Flask/) 
[![](https://img.shields.io/badge/Package-LineBot_SDK_3.5.1-green.svg?style=plastic)](https://pypi.org/project/line-bot-sdk/) 

<br>

## *⭐ Microsoft Azure ⭐*

### *Notice.　與 Docker 版本差異在於 `取消 DB 存取設置`*

### *A.　Directory Structure Diagram ( 部署後實際內部結構 )*
```commandline
PC-Bot-With-GenAI/deploy/azure
  ├── .gitkeep
  ├── vm-genai-bot_key.pem
  ├── app
  │   │
  │   ├── package
  │   │   ├── __init__.py
  │   │   ├── gemini.py
  │   │   ├── linebot.py
  │   │   └── git_gist.txt
  │   │
  │   ├── Entry.py
  │   ├── preprocess
  │   └── requirements.txt
  │
  └── script
      ├── .env
      ├── docker-compose.yaml
      └── Dockerfile
```

### *✔️ B.　Deploy ( VM )*

### *Notice: Linux 常見指令或快捷鍵*
```Text
# 貼上: shift + ins
# 強制刪除檔案夾: sudo rm -rf PC-Bot-With-GenAI
# 檢視當前目錄(包含隱藏檔案): ls -a
# 創建 preprocess 檔案夾: mkdir preprocess
# 檢視檔案: script/.env
# 編輯文件: # 開始編輯: cat <<EOF > script/.env # 結束編輯: EOF
# 複製檔案夾: cp -r common azure/
```

### *STEP1.　[UI 介面創立 VM](https://portal.azure.com/#home)*
![png](../sample/azure_vm_00.PNG)
![png](../sample/azure_vm_01.PNG)
![png](../sample/azure_vm_02.PNG)
![png](../sample/azure_vm_03.PNG)
![png](../sample/azure_vm_04.PNG)
![png](../sample/azure_vm_05.PNG)

### *STEP2.　儲存金鑰*
![png](../sample/azure_vm_06.PNG)

### *STEP3.　檢視 VM 創建後狀態*
![png](../sample/azure_vm_07.PNG)

### *STEP4.　安裝 CLI*
```bash
winget install -e --id Microsoft.AzureCLI
```
![png](../sample/azure_vm_08.PNG)

### *STEP5.　確認是否安裝成功*
```bash
az version
```
![png](../sample/azure_vm_09.PNG)

### *STEP6.　登入*
```bash
az login
```
![png](../sample/azure_vm_10.PNG)

### *STEP7.　連線到 Azure VM*
```bash
20.70.178.31 → [YOUR_VM_PUBLIC_IP]
ssh -i vm-genai-bot_key.pem azureuser@20.70.178.31
```
![png](../sample/azure_vm_11.PNG)

### *STEP8.　在 VM 進行必要安裝，啟動 USER 權限，最後離開 VM*
```bash
sudo apt update && sudo apt install -y docker.io docker-compose git
sudo systemctl enable docker
sudo systemctl start docker
sudo usermod -aG docker $USER
exit
```

### *STEP9.　重新進入 VM，並 Clone 專案*
```bash
ssh -i vm-genai-bot_key.pem azureuser@20.70.178.31
git clone https://github.com/Junwu0615/PC-Bot-With-GenAI.git
```

### *STEP10.　新增必要檔案並進入腳本路徑*
```bash
ls -a # 確認目錄檔案
cd PC-Bot-With-GenAI/deploy
cp -r common azure/ # 複製欲使用腳本
cd azure/common/ # 進入目錄
mkdir app/preprocess/ # 創建檔案夾
```

### *STEP11.　啟動 docker swarm 和 docker network*
```bash
docker swarm init
docker network create --driver=overlay open_network
```

### *STEP12.　新增 .env*
```bash
cat <<EOF > script/.env # 開始編輯
# -- 輸入變數 --
SQL_SERVICE_DRIVER=''
SQL_SERVICE_BROKER_HOST=''
SQL_SERVICE_LOGIN_USER=''
SQL_SERVICE_LOGIN_PASSWORD=''
SAVE_PATH=/builds/app/preprocess
LINE_ACCESS_TOKEN=[Fill In Your Access Token]
LINE_SECRET_TOKEN=[Fill In Your Secret]
GEMINI_TOKEN=[Fill In Your Token]
GITHUB_PERSONAL_TOKEN=[Fill In Your Token]
NGROK_AUTHTOKEN=[Fill In Your Token]
DOCKER_BOOL=True
# -- 輸入變數 --
EOF # 結束編輯
cat script/.env # 查看檔案
```

### *STEP13.　build images & compose up*
```bash
docker build -t pc-bot-with-genai:latest -f script/Dockerfile . --no-cache
docker stack deploy -c script/docker-compose.yaml pc-bot-with-genai
```

### *STEP14.　檢視運行狀態*
```bash
docker ps -a
docker images -a
docker stack ls
docker service ls
docker service logs -f pc-bot-with-genai_ngrok
docker service logs -f pc-bot-with-genai_task
```
![png](../sample/azure_vm_12.PNG)