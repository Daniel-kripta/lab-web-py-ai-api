from fastapi import APIRouter, HTTPException, Depends
from typing import Optional
from models.nota import Nota, NotaCrear, NotaActualizar
from auth.jwt import verificar_token

router = APIRouter(prefix="/notas", tags=["notas"])

# Base de datos en memoria
notas_db = {}
contador_id = 1


@router.get("", response_model=list[Nota])
def listar_notas(buscar: Optional[str] = None, payload: dict = Depends(verificar_token)):
    usuario_id = payload["id"]
    notas = [n for n in notas_db.values() if n["usuario_id"] == usuario_id]

    if buscar:
        notas = [n for n in notas if buscar.lower() in n["contenido"].lower() or buscar.lower() in n["titulo"].lower()]

    return notas


@router.get("/{nota_id}", response_model=Nota)
def obtener_nota(nota_id: int, payload: dict = Depends(verificar_token)):
    nota = notas_db.get(nota_id)

    if not nota or nota["usuario_id"] != payload["id"]:
        raise HTTPException(status_code=404, detail="Nota no encontrada")

    return nota


@router.post("", response_model=Nota, status_code=201)
def crear_nota(datos: NotaCrear, payload: dict = Depends(verificar_token)):
    global contador_id

    nota = {
        "id": contador_id,
        "titulo": datos.titulo,
        "contenido": datos.contenido,
        "usuario_id": payload["id"],
    }
    notas_db[contador_id] = nota
    contador_id += 1

    return nota


@router.put("/{nota_id}", response_model=Nota)
def editar_nota(nota_id: int, datos: NotaActualizar, payload: dict = Depends(verificar_token)):
    nota = notas_db.get(nota_id)

    if not nota or nota["usuario_id"] != payload["id"]:
        raise HTTPException(status_code=404, detail="Nota no encontrada")

    if datos.titulo is not None:
        nota["titulo"] = datos.titulo
    if datos.contenido is not None:
        nota["contenido"] = datos.contenido

    return nota


@router.delete("/{nota_id}", status_code=204)
def eliminar_nota(nota_id: int, payload: dict = Depends(verificar_token)):
    nota = notas_db.get(nota_id)

    if not nota or nota["usuario_id"] != payload["id"]:
        raise HTTPException(status_code=404, detail="Nota no encontrada")

    del notas_db[nota_id]
