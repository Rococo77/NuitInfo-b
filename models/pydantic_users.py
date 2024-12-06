from pydantic import BaseModel

class PydanticUsers(BaseModel):
    username: str
    password: str
    iswordscloud: bool = False
    logo: int = 0
    role: str = "Visiteur"
