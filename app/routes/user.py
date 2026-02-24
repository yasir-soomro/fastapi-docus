from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.utils.database import SessionLocal
from app.models.model import User
from app.schemas.schemas import UserCreate, UserOut
from app.utils.auth import hash_password
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from app.utils.auth import verify_password



router = APIRouter(prefix="/users", tags=["User"])



def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/")
def get_all_users(db: Session = Depends(get_db)):
    users = db.query(User).all()
    return users


@router.post("/signup", response_model=UserOut)
def signup(user: UserCreate, db: Session = Depends(get_db)):

    existing = db.query(User).filter(
        User.username == user.username
    ).first()

    if existing:
        raise HTTPException(status_code=400, detail="Username already exists")

    hashed_pw = hash_password(user.password)

    new_user = User(
        username=user.username,
        password=hashed_pw
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user



security = HTTPBasic()

@router.post("/login")
def login(credentials: HTTPBasicCredentials = Depends(security), db: Session = Depends(get_db)):
    # fetch user from DB
    user = db.query(User).filter(User.username == credentials.username).first()
    if not user:
        raise HTTPException(status_code=401, detail="Invalid username or password")

    # verify password
    if not verify_password(credentials.password, user.password):
        raise HTTPException(status_code=401, detail="Invalid username or password")

    return {"message": f"Welcome {user.username}!"}