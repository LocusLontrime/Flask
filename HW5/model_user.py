from fastapi import FastAPI, Request, HTTPException, Form
from pydantic import BaseModel, EmailStr, Field
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from pathlib import Path

app = FastAPI()
BASE_DIR = Path(__file__).resolve().parent
templates = Jinja2Templates(directory=str(Path(BASE_DIR, 'templates')))


class UserModel(BaseModel):
    id: int
    name: str
    email: EmailStr = Field(..., description='Email field')
    password: str = Field(..., min_length=6)


class User(BaseModel):
    name: str
    email: EmailStr = Field(..., description='Email field')
    password: str = Field(..., min_length=6)


users = [UserModel(id=_, name=f'user{_}', email=f'user{_}@mail.ru', password=f'qwerty{_}') for _ in range(1, 10)]


@app.get('/users', response_class=HTMLResponse)
async def get_users(request: Request):
    if users:
        return templates.TemplateResponse('index.html', {'request': request, 'users': users})
    raise HTTPException(status_code=404, detail='Users are not found')


@app.get('/', response_class=HTMLResponse)
def get_form(request: Request):
    return templates.TemplateResponse('add_user.html', {'request': request})


@app.post('/add_user/')
async def add_user(request: Request, name=Form(...), email=Form(...), password=Form(...)):
    new_user_id = max(users, key=lambda x: x.id).id + 1
    new_user = UserModel(id=new_user_id, name=name, email=email, password=password)
    users.append(new_user)
    return templates.TemplateResponse('index.html', {'request': request, 'users': users})
