from fastapi import APIRouter, HTTPException, status
from passlib.context import CryptContext
from models.usuario import UsuarioRegistro, UsuarioLogin, UsuarioPublico
from auth.jwt import crear_token

router = APIRouter(prefix="/auth", tags=["auth"])

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Base de datos en memoria
usuarios_db = {}
contador_id = 1


def hashear_password(password: str) -> str:
    return pwd_context.hash(password)


def verificar_password(password: str, hashed: str) -> bool:
    return pwd_context.verify(password, hashed)


@router.post("/registro", response_model=UsuarioPublico, status_code=status.HTTP_201_CREATED)
def registro(datos: UsuarioRegistro):
    global contador_id

    if datos.email in usuarios_db:
        raise HTTPException(status_code=400, detail="El email ya está registrado")

    usuario = {
        "id": contador_id,
        "email": datos.email,
        "password": hashear_password(datos.password),
    }
    usuarios_db[datos.email] = usuario
    contador_id += 1

    return UsuarioPublico(id=usuario["id"], email=usuario["email"])


@router.post("/login")
def login(datos: UsuarioLogin):
    usuario = usuarios_db.get(datos.email)

    if not usuario or not verificar_password(datos.password, usuario["password"]):
        raise HTTPException(status_code=401, detail="Credenciales incorrectas")

    token = crear_token({"sub": datos.email, "id": usuario["id"]})
    return {"access_token": token, "token_type": "bearer"}
