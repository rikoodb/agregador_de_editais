
def lista_editais(conn, cursor):
    cursor.execute('SELECT * FROM edital')
    return cursor.fetchall()


def procura_edital_db(conn, cursor, link):
    cursor.execute("""
        SELECT url FROM
            edital
            WHERE
            url = ?
    """, (link,))
    return cursor.fetchone()


def insere_no_db_edital(conn, cursor, link, data_publicacao, data_prazo_envio, titulo):
    cursor.execute("""
        INSERT INTO
            edital(url, data_publicacao, data_prazo_envio, titulo)
            VALUES
            (?,?,?,?)
    """, (link, data_publicacao,
          data_prazo_envio, titulo))
    conn.commit()
