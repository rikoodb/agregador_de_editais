
def lista_usuarios(conn, cursor):
    cursor.execute('SELECT * FROM usuario')
    return cursor.fetchall()
