from ninja import Schema
from typing import Optional

class TokenPayload(Schema):
    user_id: int = None
  
    
class UserRegistrationSchema(Schema):
    username: str
    email: str
    first_name: str
    last_name: str
    password: str


class UserPasswordUpdateSchema(Schema):
    username: str
    password: str
    new_password: str


class UserUpdateSchema(Schema):
    username: Optional[str]
    email: Optional[str]
    first_name: Optional[str]
    last_name: Optional[str]
 