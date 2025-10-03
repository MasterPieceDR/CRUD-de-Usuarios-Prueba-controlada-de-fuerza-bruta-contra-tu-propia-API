from fastapi import FastAPI, Form, HTTPException, status
from pydantic import BaseModel
from typing import List, Optional

app = FastAPI()

class Usuario(BaseModel):
    id: int
    username: str
    password: str
    email: Optional[str] = None
    is_active: bool = True

bd: List[Usuario] = [
    Usuario(id=1, username="testuser", password="123", email="test@example.com"),
    Usuario(id=2, username="diegosantillan625@gmail.com", password="123456789", email="diegosantillan625@gmail.com"),
    Usuario(id=3, username="juanperez", password="abc123", email="test@yo.com"),
]

@app.get("/")
def mensajito():
    return {"mensaje": "probando que srive xd"}

@app.post("/users/", response_model=Usuario)
def crear_usuario(usuario: Usuario):
    bd.append(usuario)
    return usuario

@app.get("/users", response_model=List[Usuario])
def listar_usuarios(skip: int = 0, limit: int = 100):
    return bd[skip : skip + limit]

@app.get("/users/{user_id}", response_model=Usuario)
def obtener_usuario(user_id: int):
    for u in bd:
        if u.id == user_id:
            return u
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="usuario no encontrado")

@app.put("/users/{user_id}", response_model=Usuario)
def actualizar_usuario(user_id: int, datos: Usuario):
    for i, u in enumerate(bd):
        if u.id == user_id:
            bd[i].username = datos.username
            bd[i].email = datos.email
            bd[i].is_active = datos.is_active
            return bd[i]
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="usuario no encontrado")

@app.delete("/users/{user_id}")
def eliminar_usuario(user_id: int):
    for i, u in enumerate(bd):
        if u.id == user_id:
            bd.pop(i)
            return {"detalle": f"usuario {user_id} eliminado"}
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="usuario no encontrado")

@app.post("/login")
def login(username: str = Form(...), password: str = Form(...)):
    for u in bd:
        if u.username == username and u.password == password:
            if not u.is_active:
                raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="usuario inactivo")
            return {"mensaje": f"Login exitoso, bienvenido {u.username}"}
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="credenciales incorrectas")

