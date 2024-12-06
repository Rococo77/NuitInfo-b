from fastapi import FastAPI
from models.users import session, Users
from models.pydantic_users import PydanticUsers
import sys
print(f"Python executable: {sys.executable}")

app = FastAPI()

@app.get("/user/{user_id}")
def read_user(user_id: int):
    pass

@app.post("/user/create/")
def create_user(user: PydanticUsers):
    new_user = Users(
        username = user.username,
        password = user.password,
        iswordscloud = user.iswordscloud,
        logo = user.logo,
        role = user.role
    )
    session.add(new_user)
    session.commit()
    return new_user