from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from auth.jwt import verificar_token
from routers.notas import notas_db
import logging
import json

router = APIRouter(prefix="/api", tags=["ia"])

# Logging estructurado en JSON
logger = logging.getLogger("ia")

# Historial de chat en memoria por sesión
chat_db = {}


class MensajeChat(BaseModel):
    session_id: str
    mensaje: str


@router.post("/chat")
def chat(datos: MensajeChat, payload: dict = Depends(verificar_token)):
    logger.info(json.dumps({"endpoint": "POST /api/chat", "usuario": payload["id"]}))

    if datos.session_id not in chat_db:
        chat_db[datos.session_id] = []

    chat_db[datos.session_id].append({"rol": "usuario", "mensaje": datos.mensaje})

    respuesta = f"Recibí tu mensaje: '{datos.mensaje}'. Tengo acceso a tus notas para ayudarte."

    chat_db[datos.session_id].append({"rol": "asistente", "mensaje": respuesta})

    return {"session_id": datos.session_id, "respuesta": respuesta}


@router.get("/chat/history/{session_id}")
def historial_chat(session_id: str, payload: dict = Depends(verificar_token)):
    logger.info(json.dumps({"endpoint": f"GET /api/chat/history/{session_id}", "usuario": payload["id"]}))

    historial = chat_db.get(session_id, [])
    return {"session_id": session_id, "historial": historial}


@router.get("/search")
def buscar(q: str, payload: dict = Depends(verificar_token)):
    logger.info(json.dumps({"endpoint": "GET /api/search", "usuario": payload["id"], "query": q}))

    usuario_id = payload["id"]
    resultados = [
        n for n in notas_db.values()
        if n["usuario_id"] == usuario_id
        and (q.lower() in n["titulo"].lower() or q.lower() in n["contenido"].lower())
    ]
    return {"query": q, "resultados": resultados}


@router.get("/context")
def contexto(payload: dict = Depends(verificar_token)):
    logger.info(json.dumps({"endpoint": "GET /api/context", "usuario": payload["id"]}))

    total_notas = len([n for n in notas_db.values() if n["usuario_id"] == payload["id"]])

    return {
        "descripcion": "API de notas con autenticación JWT lista para agentes IA",
        "capacidades": [
            "Crear, leer, editar y eliminar notas",
            "Buscar notas por contenido",
            "Chat con historial por sesión",
        ],
        "usuario_id": payload["id"],
        "total_notas": total_notas,
    }


@router.post("/resumir/{nota_id}")
def resumir(nota_id: int, payload: dict = Depends(verificar_token)):
    logger.info(json.dumps({"endpoint": f"POST /api/resumir/{nota_id}", "usuario": payload["id"]}))

    nota = notas_db.get(nota_id)

    if not nota or nota["usuario_id"] != payload["id"]:
        raise HTTPException(status_code=404, detail="Nota no encontrada")

    resumen = f"Resumen de '{nota['titulo']}': {nota['contenido'][:100]}..."
    return {"nota_id": nota_id, "resumen": resumen}
