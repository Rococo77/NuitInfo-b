from fastapi import FastAPI, HTTPException, status
from models.users import session, Users
from models.pydantic_users import PydanticUsers
from utils.mongo_client import db
from typing import List

app = FastAPI()

def serialize_document(doc):
    doc['_id'] = str(doc['_id'])  # Convertir ObjectId en string
    return doc

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
def update_user(user_id: int, user: PydanticUsers):
    db_user = session.query(Users).where(Users.id == user_id).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    
    if user.iswordscloud:
        db_user.iswordscloud = user.iswordscloud
    if user.logo:
        db_user.logo = user.logo
    if user.role:
        db_user.role = user.role

    session.commit()    
    return db_user

@app.delete("/user/delete/{user_id}")
def delete_user(user_id: int):
    db_user = session.query(Users).where(Users.id == user_id).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    
    session.delete(db_user)
    session.commit()


@app.get("/interactions/{type}", response_model=List[dict])
async def get_interaction_by_type(type: str):
    collection = db["Interactions"]
    query = collection.find({"type": type})
    interactions = [serialize_document(doc) async for doc in query]
    return interactions

@app.get("/interactions/{user_id}", response_model=List[dict])
async def get_interaction_by_user(user_id: int):
    collection = db["Interactions"]
    query = collection.find({"id_user": user_id})
    interactions = [serialize_document(doc) async for doc in query]
    return interactions