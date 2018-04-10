import os
import unittest
import sqlite3
from usuario.usuario import lista_usuarios


class test_db_usuario(unittest.TestCase):

    def setUp(self):
        self.conn = sqlite3.connect("mydatabase.db")
        self.cursor = self.conn.cursor()

        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS usuario
                (
                    id_usuario INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
                nome VARCHAR(100) NOT NULL,
                email VARCHAR(80) NOT NULL
                )
        """)
        self.conn.commit()

        self.cursor.execute("""
            INSERT INTO
                usuario(nome, email)
            VALUES
            (
                'joao','joao@hotmail.com'
            )
        """)
        self.conn.commit()

    def tearDown(self):
        os.remove("mydatabase.db")
        self.conn.close()

    def teste_lista_usuarios(self):
        """
        testando a funcao lista_usuarios
        """
        resultado_bd = lista_usuarios(self.conn, self.cursor)
        
        self.assertEqual(len(resultado_bd), 1)
        resultado_esperado = [(1, 'joao', 'joao@hotmail.com')]
        self.assertEqual(resultado_bd, resultado_esperado)
             