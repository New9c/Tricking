# Hello!

我之後再測試執行方法ok不ok，星期四後較有空
module not found 就pip install, node和npm可能要查一下。

## Run Backend
1. 拿jwt (用powershell/terminal/vscode下面東東)
```terminal
node -e "console.log(require('crypto').randomBytes(32).toString('hex'))"
```
會有神奇字串出現(e.g. 0ff...36c)

2. 把backend/config.py 修一下
```python
    SECRET_JWT: str = "your神奇字串"
    #PASSWORD: str 先不用
    #DB_NAME: str 先不用
```
3. 把backend/dependencies.py 修一下
```python
""" comment掉、也可以刪掉
URI = f"mongodb+srv://aimccccccccc:{config.PASSWORD}@clusterfluster.jzaut.mongodb.net/?retryWrites=true&w=majority&appName=ClusterFluster"
client = MongoClient(URI)
db = client[config.DB_NAME]
"""
dc_name = "your-dc-name"
uri = f"mongodb+srv://{dc_name}:{dc_name}@gdg-mongodb.chih-hao.xyz/{dc_name}?authMechanism=SCRAM-SHA-256&tls=true"
tls_ca_file = "mongodb-bundle.pem"
client = MongoClient(uri, tlsCAFile=tls_ca_file)
db = client[dc_name]
```
4. RUN
```terminal
uvicorn main:app
```
去http://127.0.0.1:8000/docs#/default玩一下
## Run Frontend (要新terminal)
在frontend裡:
```terminal
npm i
npm run dev
```
去http://localhost:3000/玩一下

-------
## Purpose
To keep a backup of files regarding the tricking website.

## Progress
- Done most of frontend homework
- Made working backend with username+password
- Made tricktionary
- Made topbar
- Made draft homepage
