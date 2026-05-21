from fastapi import FastAPI
from routers import auth, notas, ia
from config import PORT
import uvicorn

app = FastAPI(title="API IA-ready con autenticación")

app.include_router(auth.router)
app.include_router(notas.router)
app.include_router(ia.router)


@app.get("/")
def raiz():
    return {"mensaje": "API funcionando"}


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=PORT, reload=True)
