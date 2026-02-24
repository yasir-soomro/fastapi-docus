from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from fastapi.security import HTTPBasic, HTTPBasicCredentials

from app.utils.database import SessionLocal
from app.models.model import Todo, User
from app.schemas.schemas import TodoCreate, TodoOut
from app.utils.auth import verify_password

router = APIRouter(prefix="/todos", tags=["Todos"])

security = HTTPBasic()

# DB dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Current user dependency
def get_current_user(credentials: HTTPBasicCredentials = Depends(security), db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username == credentials.username).first()
    if not user or not verify_password(credentials.password, user.password):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    return user

# --- CREATE TODO ---
@router.post("/", response_model=TodoOut)
def create_todo(todo: TodoCreate, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    new_todo = Todo(title=todo.title, owner_id=current_user.id)
    db.add(new_todo)
    db.commit()
    db.refresh(new_todo)
    return new_todo

# --- GET TODOS ---
@router.get("/", response_model=list[TodoOut])
def get_todos(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    todos = db.query(Todo).filter(Todo.owner_id == current_user.id).all()
    return todos

# --- DELETE TODO ---
@router.delete("/{todo_id}")
def delete_todo(todo_id: int, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    todo = db.query(Todo).filter(Todo.id == todo_id, Todo.owner_id == current_user.id).first()
    if not todo:
        raise HTTPException(status_code=404, detail="Todo not found")
    db.delete(todo)
    db.commit()
    return {"message": "Todo deleted successfully"}