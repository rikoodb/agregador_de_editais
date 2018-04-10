import os
import unittest
import sqlite3
from edital.edital import lista_editais
from edital.edital import procura_edital_db
from edital.edital import insere_no_db_edital


class TestDbEdital(unittest.TestCase):
    """
    testa todas as funções de test_db_edital
    """
    def setUp(self):
        self.conn = sqlite3.connect("mydatabase.db")
        self.cursor = self.conn.cursor()

        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS edital
                (
                    id_edital INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
                    url VARCHAR(100) NOT NULL,
                    data_publicacao VARCHAR(80),
                    data_prazo_envio VARCHAR(80),
                    titulo VARCHAR(80)
                )
        """)

        self.conn.commit()

        self.cursor.execute("""
            INSERT INTO
                edital(url, data_publicacao, data_prazo_envio, titulo)
            VALUES
            (
                'http://finep.gov.br/chamadas-publicas/chamadapublica/611',
                '31/10/2017',
                '30/06/2019',
                'Chamada Pública Bilateral Finep'
            )
        """)

        self.conn.commit()

    def tearDown(self):
        os.remove("mydatabase.db")
        self.conn.close()

    def teste_lista_editais(self):
        """
        testando a funcao lista_editais
        """
        resultado_bd = lista_editais(self.conn, self.cursor)

        self.assertEqual(len(resultado_bd), 1)
        resultado_esperado = [(1, 'http://finep.gov.br/chamadas-publicas/chamadapublica/611',
                                  '31/10/2017',
                                  '30/06/2019',
                                  'Chamada Pública Bilateral Finep')]

        self.assertEqual(resultado_bd, resultado_esperado)

    def teste_procura_edital(self):
        link = 'http://finep.gov.br/chamadas-publicas/chamadapublica/611'
        resultado_bd = procura_edital_db(self.conn, self.cursor, link)

        self.assertTrue(resultado_bd)

    def teste_insere_no_edital(self):
        link = 'http://www.google.com.br'
        data_publicacao = '15/03/2018'
        data_prazo_envio = '27/10/2018'
        titulo = 'google teste'

        insere_no_db_edital(self.conn, self.cursor, link,
                            data_publicacao, data_prazo_envio, titulo)

        self.cursor.execute('SELECT * FROM edital WHERE id_edital = 2')
        resultado_bd = self.cursor.fetchall()

        resultado_esperado = [(2, 'http://www.google.com.br',
                                  '15/03/2018',
                                  '27/10/2018',
                                  'google teste')]

        self.assertEqual(resultado_bd, resultado_esperado)
