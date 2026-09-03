from fastapi import FastAPI

app = FastAPI(title="Employee Management System")

@app.get("/")
def read_root():
    return {"message": "Welcome to FastAPI reference app"}
