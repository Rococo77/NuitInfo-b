from fastapi import FastAPI, HTTPException, status
from models.users import session, Users
from models.pydantic_users import PydanticUsers
import sys
print(f"Python executable: {sys.executable}")

app = FastAPI()

@app.get("/user/{user_id}")
def read_user(user_id: int):
    user = session.query(Users).where(Users.id == user_id).first()
    if user:
        return user
    raise HTTPException(status_code=404, detail="User not found")

@app.post("/user/create/")
def create_user(user: PydanticUsers):
    user = session.query(Users).where(Users.username == user.username).first()
    if user:
        raise HTTPException(status_code=409, detail="Username taken")
    if len(user.password) < 5:
        raise HTTPException(status_code=422, detail="Password too short")
    if len(user.username) < 4:
        raise HTTPException(status_code=422, detail="Username too short")
    
    new_user = Users(
        username = user.username,
        password = user.password,
        iswordscloud = user.iswordscloud,
        logo = user.logo,
        role = user.role
    )
    
    session.add(new_user)
    session.commit()
    return user

@app.put("/user/update/{user_id}")
def update_user(user_id: int, user: Users):
    db_user = session.query(Users).where(Users.id == user_id).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    
    if user.iswordscloud:
        db_user.iswordscloud = user.iswordscloud
    if user.logo:
        db_user.logo = user.logo
    if user.role:
        db_user.role = user.role

    return db_user
