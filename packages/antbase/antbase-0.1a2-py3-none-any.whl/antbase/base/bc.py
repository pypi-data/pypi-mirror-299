from antbase import Auth

class Bc:
    __bc = Auth.get_bc_client()

    @staticmethod
    def print_project_list():
        projects = Bc.__bc.projects.list()
        for project in projects:
            print(f"Project Name: {project.name}")


from fastapi import FastAPI, Request
from fastapi.responses import RedirectResponse
import requests

app = FastAPI()

# Данные для авторизации Basecamp
CLIENT_ID = "your_client_id"
CLIENT_SECRET = "your_client_secret"
REDIRECT_URI = "http://localhost:8000/callback"

@app.get("/login")
async def login():
    # Формируем URL для авторизации в Basecamp
    authorization_url = f"https://launchpad.37signals.com/authorization/new?type=web_server&client_id={CLIENT_ID}&redirect_uri={REDIRECT_URI}"
    
    # Перенаправляем пользователя на страницу авторизации Basecamp
    return RedirectResponse(authorization_url)

@app.get("/callback")
async def callback(request: Request):
    # Извлекаем authorization code из параметров запроса
    code = request.query_params.get("code")
    
    if code:
        # Обмен authorization code на access token и refresh token
        response = requests.post(
            "https://launchpad.37signals.com/authorization/token?type=web_server",
            data={
                "client_id": CLIENT_ID,
                "client_secret": CLIENT_SECRET,
                "redirect_uri": REDIRECT_URI,
                "code": code,
                "grant_type": "authorization_code"
            }
        )
        token_data = response.json()
        access_token = token_data.get("access_token")
        refresh_token = token_data.get("refresh_token")
        
        return {"access_token": access_token, "refresh_token": refresh_token}
    
    return {"error": "Authorization code not found"}

# Запуск приложения:
# uvicorn main:app --reload
