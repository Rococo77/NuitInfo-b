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
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f'User not found',
    )

@app.post("/user/create/")
def create_user(user: PydanticUsers):
    user = session.query(Users).where(Users.username == user.username).first()
    if user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f'Username already taken',
        )
    if len(user.password) < 5:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=f'Password too short',
        )
    if len(user.username) < 4:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=f'Username too short',
        )
    new_user = Users(
        username = user.username,
        password = user.password,
        iswordscloud = user.iswordscloud,
        logo = user.logo,
        role = user.role
    )
    session.add(new_user)
    session.commit()
    print("created user")
    return user