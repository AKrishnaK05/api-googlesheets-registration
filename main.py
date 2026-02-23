from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import os
from models import UserCreate, UserResponse, MessageResponse
from sheets_service import SheetsService
from typing import List

app = FastAPI(title="User Registration System")
sheets = SheetsService()

# Ensure static directory exists
os.makedirs("static", exist_ok=True)

@app.get("/", response_class=HTMLResponse)
async def read_index():
    with open("static/index.html", "r") as f:
        return HTMLResponse(content=f.read())

@app.post("/register", response_model=MessageResponse)
async def register_user(user: UserCreate):
    success = sheets.append_user(user.email, user.password, user.role)
    if not success:
        raise HTTPException(status_code=500, detail="Failed to save user to Google Sheets")
    return {"message": "User registered successfully!"}

@app.get("/users", response_model=List[UserResponse])
async def get_users():
    users = sheets.get_users()
    return users

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
