from pydantic import BaseModel, EmailStr


class UsuarioRegistro(BaseModel):
    email: EmailStr
    password: str


class UsuarioLogin(BaseModel):
    email: EmailStr
    password: str


class UsuarioPublico(BaseModel):
    id: int
    email: EmailStr
