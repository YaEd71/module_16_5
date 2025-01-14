from fastapi import FastAPI, HTTPException, Request
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from typing import List

app = FastAPI()
templates = Jinja2Templates(directory="templates")

class User(BaseModel):
    id: int
    username: str
    age: int


users: List[User] = []

@app.get('/')
async def root(request: Request):
    return templates.TemplateResponse("users.html", {"request": request, "users": users})


@app.get('/user/{user_id}')
async def get_user(request: Request, user_id: int):
    for user in users:
        if user.id == user_id:
            return templates.TemplateResponse("users.html", {"request": request, "user": user})
    raise HTTPException(status_code=404, detail="User not found")

@app.post('/user/{username}/{age}', response_model=User)
async def create_user(username: str, age: int):
    new_id = users[-1].id + 1 if users else 1
    new_user = User(id=new_id, username=username, age=age)
    users.append(new_user)
    return new_user

@app.put('/user/{user_id}/{username}/{age}', response_model=User)
async def update_user(user_id: int, username: str, age: int):
    for user in users:
        if user.id == user_id:
            user.username = username
            user.age = age
            return user
    raise HTTPException(status_code=404, detail="User not found")

@app.delete('/user/{user_id}', response_model=User)
async def delete_user(user_id: int):
    for user in users:
        if user.id == user_id:
            users.remove(user)
            return user
    raise HTTPException(status_code=404, detail="User not found")

if __name__ == '__main__':
    # Создаем тестовых пользователей
    users.append(User(id=1, username="UrbanUser", age=24))
    users.append(User(id=2, username="UrbanTest", age=22))
    users.append(User(id=3, username="Capybara", age=60))

    import uvicorn

    uvicorn.run(app, host='127.0.0.1', port=8000)