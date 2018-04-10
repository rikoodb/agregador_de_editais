import os
import unittest
import sqlite3
from unittest import mock
from processa_edital import busca_usuarios_e_editais
from processa_edital import envia_mensagem_email
from processa_edital import envia_email
# from email.mime.multipart import MIMEMultipart   #usarei para testar
from email.mime.text import MIMEText
from jinja2 import Template
import settings


class TestProcessaEdital(unittest.TestCase):
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
            CREATE TABLE IF NOT EXISTS usuario
                (
                    id_usuario INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
                    nome VARCHAR(100) NOT NULL,
                    email VARCHAR(80)
                )
        """)
        self.conn.commit()

        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS usuario_edital
                (
                    usuario_id INTEGER NOT NULL,
                    edital_id INTEGER NOT NULL,
                    FOREIGN KEY (usuario_id) REFERENCES usuario(id_usuario),
                    FOREIGN KEY (edital_id) REFERENCES usuario(id_edital)
                )
        """)
        self.conn.commit()

    def tearDown(self):
        os.remove("mydatabase.db")
        self.conn.close()

    def teste_busca_usuarios_e_editais(self):
        self.cursor.execute("""
            INSERT INTO
                usuario(nome, email)
            VALUES
            (
                'joao','joao@hotmail.com'
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
                'edital inovacao teste'
            )
        """)
        self.conn.commit()
        resultado_banco = busca_usuarios_e_editais(self.conn, self.cursor)
        resultado_esperado = {
            'joao@hotmail.com': [(1,
                                 'http://finep.gov.br/chamadas-publicas/chamadapublica/611',
                                  '31/10/2017',
                                  '30/06/2019',
                                  'edital inovacao teste')]
        }

        self.assertEqual(resultado_banco, resultado_esperado)

        # aqui ele ja inseriu os dados no banco, e agora como nao
        # tem mais links diferentes, retorna uma lista vazia
        # nesse caso, ja foi testado as funcoes usuario_recebeu_edital
        # e set_edital_foi_enviado sem uso de mock

        resultado_banco2 = busca_usuarios_e_editais(self.conn, self.cursor)
        resultado_esperado2 = {'joao@hotmail.com': []}

        self.assertEqual(resultado_banco2, resultado_esperado2)

    @mock.patch('processa_edital.envia_email')
    def teste_nao_envia_email_se_nao_tem_link(self, mock_envia_email):
        envia_mensagem_email(self.conn, self.cursor)

        mock_envia_email.assert_not_called()

    @mock.patch('processa_edital.envia_email')
    @mock.patch('processa_edital.MIMEMultipart')
    def teste_verifica_se_email_foi_enviado(self, MockMIMEMultipart, mock_envia_email):
        self.cursor.execute("""
            INSERT INTO
                usuario(nome, email)
            VALUES
            (
                'joao','joao@hotmail.com'
            )
        """)
        self.conn.commit()

        self.cursor.execute("""
            INSERT INTO
                edital(url, data_publicacao, data_prazo_envio, titulo)
            VALUES
            (
                'http://www.google.com',
                '31/10/2017',
                '30/06/2019',
                'edital inovacao teste'
            )
        """)
        self.conn.commit()          

        email = 'joao@hotmail.com'
        
        texto = "Esse eh um teste python"
        html = """\
        <html>
        <head></head>
        <body>
            <p>Ola!<br>
           teste, teste<br>
            {{texto}}.
            </p>
        </body>
        </html>
        """
        
        template = Template(html)
        renderizar = template.render(texto=texto)

        mock_msg = MockMIMEMultipart('alternative')
        mock_msg['Subject'] = 'Editais em Aberto'
        mock_msg['From'] = 'contato.labnita@outlook.com'
        mock_msg['To'] = email
     
        part2 = MIMEText(renderizar, 'html')
        mock_msg.attach(part2)

        envia_mensagem_email(self.conn, self.cursor)
        mock_envia_email.assert_called_with(email, mock_msg)

    @mock.patch('processa_edital.smtplib')
    def teste_envia_email(self, mock_smtplib):
        destinatario = 'joao@hotmail.com'

        mensagem = 'teste'

        mock_mensagem = mock.MagicMock()

        # Aqui, eu finjo que a mensagem é um MimeMultipart sem precisa mockar o Mimemultpart. Por que:
        # porque eu só preciso garantir que a função .as_string foi chamada e retornou uma mensagem que eu possa
        # validar no teste
        mock_mensagem.as_string.return_value = mensagem

        envia_email(destinatario, mock_mensagem)

        mock_smtplib.SMTP().starttls.assert_called()
        mock_smtplib.SMTP().login.assert_called_with(settings.REMETENTE, settings.SENHA)
        mock_smtplib.SMTP().sendmail.assert_called_with(settings.REMETENTE, destinatario, mensagem)
        mock_smtplib.SMTP().quit.assert_called()
