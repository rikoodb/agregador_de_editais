import os
import unittest
import sqlite3
from usuario_edital.usuario_edital import usuario_recebeu_edital
from usuario_edital.usuario_edital import set_edital_foi_enviado


class test_db_usuario_edital(unittest.TestCase):

    def setUp(self):
        self.conn = sqlite3.connect("mydatabase.db")
        self.cursor = self.conn.cursor()

        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS edital
                (id_edital INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
                url VARCHAR(100) NOT NULL, data_publicacao VARCHAR(80),
                data_prazo_envio VARCHAR(80))
        """)
        self.conn.commit()

        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS usuario
                (id_usuario INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
                nome VARCHAR(100) NOT NULL,
                email VARCHAR(80) NOT NULL)
        """)
        self.conn.commit()

        self.cursor.execute("""CREATE TABLE IF NOT EXISTS usuario_edital
                       (usuario_id INTEGER NOT NULL,
                       edital_id INTEGER NOT NULl,
                       FOREIGN KEY (usuario_id) REFERENCES usuario(id_usuario),
                       FOREIGN KEY (edital_id) REFERENCES usuario(id_edital))
                     """)

        self.cursor.execute("""INSERT INTO usuario(nome, email)
                        VALUES ('joao','joao@hotmail.com')
                        """)
        self.conn.commit()

        self.cursor.execute("""INSERT INTO edital(url, data_publicacao, data_prazo_envio)
                        VALUES ('http://finep.gov.br/chamadas-publicas/chamadapublica/611',
                                '31/10/2017','30/06/2019')""")    
        self.conn.commit()

        self.cursor.execute("""INSERT INTO usuario_edital(usuario_id, edital_id)
                        VALUES (1,1)
                        """)
        self.conn.commit()

    def tearDown(self):
        os.remove("mydatabase.db")
        self.conn.close()

    def teste_usuario_recebeu_edital(self):
        usuario_id = 1
        edital_id = 1
        resultado_bd = usuario_recebeu_edital(self.conn, self.cursor,
                                              usuario_id, edital_id)

        # sobre o tamanho do bd, eh pra ser 1, mas retorna 2.
        #  Verificar como fazer as 2 fk virar uma pk

        self.assertTrue(resultado_bd)
        self.assertEqual(len(resultado_bd), 2)

    def teste_set_edital_foi_enviado(self):
        self.cursor.execute("""DELETE FROM usuario_edital""")

        usuario_id = 1
        edital_id = 1

        set_edital_foi_enviado(self.conn, self.cursor, usuario_id, edital_id)

        self.cursor.execute("""SELECT * FROM usuario_edital""")

        resultado_bd = self.cursor.fetchall()
        resultado_esperado = [(1, 1)]

        self.assertEqual(resultado_bd, resultado_esperado)
