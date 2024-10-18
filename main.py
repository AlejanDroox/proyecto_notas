from fastapi import FastAPI, HTTPException, Body
import mysql.connector
from mysql.connector import Error
from pydantic import BaseModel
from typing import List, Optional
from ctrl_db import ( 
    get_all_notes,
    get_note_id,
    get_note_cag,
    create_note, 
    update_note,
    delete_note_db
)
app = FastAPI()

app.title = 'Bloc_Notas'

app.version = '1.0'

#print(get_all_notes())

app = FastAPI()

# Modelo para la creación de una nota
class NoteCreate(BaseModel):
    id_usuario: int
    titulo: str
    contenido: str
# Modelo de la nota
class Note(BaseModel):
    id: int
    id_usuario:int
    titulo: str
    contenido: str
    fecha_creacion: str
    fecha_actualizacion: str


# GET: Obtener todas las notas
@app.get("/notes/", response_model=List[Note])
def get_notes():
    notes = get_all_notes()
    if notes is None:
        raise HTTPException(status_code=500, detail="Error al conectar a la base de datos")
    
    if not notes:
        raise HTTPException(status_code=404, detail="No hay notas disponibles")
    
    return notes

# GET: Obtener una nota específica por ID
@app.get("/notes/{note_id}", response_model=Note)
def get_note(note_id: int):
    note = get_note_id(note_id)
    if note is None:
        raise HTTPException(status_code=404, detail="Nota no encontrada")
    return note

# GET: Obtener una nota específica por ID
@app.get("/notes/{categoria}", response_model=list[Note])
def get_note_category(categoria: str):
    note = get_note_cag(categoria)
    if notes is None:
        raise HTTPException(status_code=500, detail="Error al conectar a la base de datos")
    if note is None:
        raise HTTPException(status_code=404, detail="Nota no encontrada")
    return note

# POST: Crear una nueva nota
@app.post("/notes/new") # intente poner el modelo de respuesta pero peta XD
def create_new_note(note: NoteCreate):
    try:
        new_note = create_note(note.id_usuario, note.titulo, note.contenido)
        if not new_note:
            raise HTTPException(status_code=500, detail="Error al crear la nota")
        return new_note
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al crear la nota: {e}")

@app.put("/notes/update/{id_note}")
def edit_note(
    id_note:int,
    titulo:Optional[str] = Body(None),
    contenido:Optional[str] = Body(None),
    ):
    try:
        updated_note = update_note(id_note, titulo, contenido)
        if updated_note is None:
            raise HTTPException(status_code=404, detail="Nota no encontrada")
        return updated_note
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al actualizar la nota: {e}")
@app.delete("/notes/delete")
def delete_note(note_id:int):
    
    try:
        note = delete_note_db(note_id)
        if note is None:
            raise HTTPException(status_code=404, detail="Nota no encontrada")
        return note
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al actualizar la nota: {e}")