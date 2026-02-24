from fastapi import FastAPI
from app.utils.database import engine, Base
from app.models.model import User, Todo
from app.routes import user, todo

app = FastAPI()

# include routers
app.include_router(user.router)
app.include_router(todo.router)

@app.get("/")
def home():
    return {"message": "Todo API running"}