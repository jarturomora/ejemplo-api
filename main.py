from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from datetime import datetime
from pydantic import BaseModel, EmailStr, ValidationError

app = FastAPI()
templates = Jinja2Templates(directory="templates")

class UserInput(BaseModel):
    username: str
    email: EmailStr
    password: str
    birthdate: datetime

def is_adult(birthdate: datetime) -> bool:
    today = datetime.today()
    age = today.year - birthdate.year - ((today.month, today.day) < (birthdate.month, birthdate.day))
    return age >= 18

@app.get("/", response_class=HTMLResponse)
def get_register_page(request: Request):
    return templates.TemplateResponse("register.html", {"request": request})

@app.post("/register", response_class=HTMLResponse)
def register_user(
    request: Request,
    username: str = Form(...),
    email: str = Form(...),
    password: str = Form(...),
    birthdate: str = Form(...)
):
    try:
        birthdate_obj = datetime.strptime(birthdate, "%Y-%m-%d")
        user = UserInput(
            username=username,
            email=email,
            password=password,
            birthdate=birthdate_obj
        )

        if not is_adult(user.birthdate):
            return templates.TemplateResponse("register.html", {
                "request": request,
                "error": "Debes tener al menos 18 años para registrarte."
            })

        return templates.TemplateResponse("register.html", {
            "request": request,
            "success": f"¡Usuario {username} registrado exitosamente!"
        })

    except ValidationError:
        return templates.TemplateResponse("register.html", {
            "request": request,
            "error": "Datos inválidos. Verifica los campos."
        })
