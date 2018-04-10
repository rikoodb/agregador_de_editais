
def usuario_recebeu_edital(conn, cursor, usuario_id, edital_id):
    cursor.execute("""
        SELECT * FROM
            usuario_edital
            WHERE
            usuario_id = ?
            and
            edital_id = ?
    """, (usuario_id, edital_id))
    return cursor.fetchone()


def set_edital_foi_enviado(conn, cursor, usuario_id, edital_id):
    cursor.execute("""
        INSERT INTO
            usuario_edital(usuario_id, edital_id)
        VALUES
            (?,?)
    """, (usuario_id, edital_id))
    conn.commit()
