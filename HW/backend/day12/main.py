from fastapi import FastAPI, Form

app = FastAPI()

fake_user_db = [
    {
        "username": "ithome",
        "password": "secret"
    }, {
        "username": "ironman",
        "password": "password"
    }
]

@app.post("/login")
async def login(username: str = Form(), password: str = Form()):
    is_user = False
    for user in fake_user_db:
        if username == user["username"] and password == user["password"]:
            is_user = True
            break
    return {"is_user": is_user}
