from fastapi import FastAPI
from app.api.v1 import login
from app.api.v1.endpoints import users
app = FastAPI(title="Employee Management System")

@app.get("/")
def read_root():
    return {"message": "Welcome to FastAPI reference app"}

app.include_router(users.router)
app.include_router(login.router)