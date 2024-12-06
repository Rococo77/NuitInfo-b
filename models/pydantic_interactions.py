from pydantic import BaseModel

class PydanticInteraction(BaseModel):
    id_user: int
    type: str
    timestamp: int
    