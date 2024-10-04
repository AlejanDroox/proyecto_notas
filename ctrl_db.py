import mysql.connector
from mysql.connector import Error
from datetime import datetime


# conectar a db
def db_connection():
    connection = None
    try:
        connection = mysql.connector.connect(
            host="localhost",
            port=3306,
            user="root",
            password="1234",
            database="notas"
        )
    except Error as e:
        print(f"Error: '{e}'")
    return connection

# Función para obtener todas las notas
def get_all_notes() -> list:
    """Devuelve todas las notas tal y como estan los datos en tabla notas"""
    connection = db_connection()
    if connection is None:
        return None
    
    cursor = connection.cursor(dictionary=True)
    query = """
        SELECT id, id_usuario, titulo, contenido, fecha_creacion, fecha_actualizacion 
        FROM notas
    """
    cursor.execute(query)
    notes = cursor.fetchall()
    for note in notes:
        note['fecha_creacion'] = format_date(note['fecha_creacion'])
        note['fecha_actualizacion'] = format_date(note['fecha_actualizacion'])
    cursor.close()
    connection.close()
    return notes

# Función para obtener una nota por ID
def get_note_id(note_id: int):
    """devuelve una unica nota por la id agregada en la url"""
    connection = db_connection()
    if connection is None:
        return None
    
    cursor = connection.cursor(dictionary=True)
    query = """
        SELECT id, id_usuario, titulo, contenido, fecha_creacion, fecha_actualizacion 
        FROM notas
        WHERE id = %s
    """
    cursor.execute(query, (note_id,))
    note = cursor.fetchone()
    if note:
        note['fecha_creacion'] = format_date(note['fecha_creacion'])
        note['fecha_actualizacion'] = format_date(note['fecha_actualizacion'])
    cursor.close()
    connection.close()
    
    return note
# Función para obtener una nota por ID
def get_note_cag(categoria: str) -> list:
    """devuelve todas las notas por categoria"""
    connection = db_connection()
    if connection is None:
        return None
    
    cursor = connection.cursor(dictionary=True)
    query = """
        SELECT id
        FROM categorias
        WHERE nombre_categoria = %s;
    """
    cursor.execute(query, (categoria,))

    id = cursor.fetchone()
    cursor = connection.cursor(dictionary=True)
    query = """
        SELECT id, id_usuario, titulo, contenido, fecha_creacion, fecha_actualizacion 
        FROM notas
        JOIN nota_categoria ON notas.id = nota_categoria.id_nota
        WHERE id_categoria = %s
    """
    cursor.execute(query, (id['id'],))
    notes = cursor.fetchall()
    for note in notes:
        note['fecha_creacion'] = format_date(note['fecha_creacion'])
        note['fecha_actualizacion'] = format_date(note['fecha_actualizacion'])
    cursor.close()
    connection.close()
    
    return notes

def create_note(id_usuario: int, titulo: str, contenido: str):
    connection = db_connection()
    if connection is None:
        return None
    
    cursor = connection.cursor(dictionary=True)
    

    fecha_actual = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    

    query = """
        INSERT INTO notas (id_usuario, titulo, contenido, fecha_creacion, fecha_actualizacion)
        VALUES (%s, %s, %s, %s, %s)
    """
    values = (id_usuario, titulo, contenido, fecha_actual, fecha_actual)
    
    try:
        cursor.execute(query, values)
        connection.commit()
        
        new_note_id = cursor.lastrowid
        cursor.execute("SELECT * FROM notas WHERE id = %s", (new_note_id,))
        new_note = cursor.fetchone()
    except Exception as e:
        connection.rollback()
        print(f"Error al insertar la nota: {e}")
        return None
    finally:
        cursor.close()
        connection.close()
    return new_note

def format_date(date: datetime) -> str:
    return date.strftime("%Y-%m-%d %H:%M:%S")
if __name__ == '__main__':
    create_note(1,'1','1')
    get_all_notes()
    get_note_cag('universidad')