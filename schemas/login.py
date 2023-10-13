from pydantic import BaseModel, EmailStr


class login(BaseModel):
    username: EmailStr
    password: str

    class Config:
        orm_mode = True
