from pydantic import BaseModel
from typing import Optional


class NotaCrear(BaseModel):
    titulo: str
    contenido: str


class NotaActualizar(BaseModel):
    titulo: Optional[str] = None
    contenido: Optional[str] = None


class Nota(BaseModel):
    id: int
    titulo: str
    contenido: str
    usuario_id: int
