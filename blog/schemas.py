from pydantic import BaseModel
from datetime import datetime
class Blog(BaseModel):
    title: str
    content: str
    created_at: datetime | None = None

class User(BaseModel):
    username: str = None 
    email: str = None
    password: str 


