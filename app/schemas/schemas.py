
from pydantic import BaseModel


# ---------- USER SCHEMAS ----------

class UserCreate(BaseModel):
    username: str
    password: str


class UserLogin(BaseModel):
    username: str
    password: str


class UserOut(BaseModel):
    id: int
    username: str

    class Config:
        from_attributes = True


# ---------- TODO SCHEMAS ----------

class TodoCreate(BaseModel):
    title: str


class TodoOut(BaseModel):
    id: int
    title: str
    completed: bool

    class Config:
        from_attributes = True