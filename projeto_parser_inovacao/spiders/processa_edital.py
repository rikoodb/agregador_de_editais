# -*- coding: utf-8 -*-
import smtplib
from jinja2 import Template
from edital.edital import lista_editais
from usuario.usuario import lista_usuarios
from usuario_edital.usuario_edital import usuario_recebeu_edital
from usuario_edital.usuario_edital import set_edital_foi_enviado
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import settings


def busca_usuarios_e_editais(conn, cursor):
    informacoes = {
        'lista_edital': lista_editais(conn, cursor),
        'lista_email': lista_usuarios(conn, cursor),
    }
    destinatario = ''
    dados = {}

    for usuario in informacoes['lista_email']:
        id_usuario, nome_usuario, email_usuario = usuario
        # 2 = email do usuario
        destinatario = email_usuario
        dados[destinatario] = []

        # para mostrar as urls uma embaixo da outra
        for edital in informacoes['lista_edital']:
            id_edital, edital_link, edital_data_publicacao, edital_data_prazo_envio, edital_titulo = edital

            # Se nao tiver usuario_edital o link é inserido na
            # tabela usuario_edital e armazenado
            # em dados[destinatario]
            usuario_edital = usuario_recebeu_edital(conn, cursor, id_usuario, id_edital)

            if not usuario_edital:
                set_edital_foi_enviado(conn, cursor, id_usuario, id_edital)
                dados[destinatario].append(edital)
    return dados


def envia_email(destinatario, mensagem):
    # Enviando o email   
    mensagem = mensagem.as_string()
    server = smtplib.SMTP('smtp-mail.outlook.com', '587')
    server.starttls()
    server.login(settings.REMETENTE, settings.SENHA)
    server.sendmail(settings.REMETENTE, destinatario, mensagem)
    server.quit()


def envia_mensagem_email(conn, cursor):
    assunto = 'Editais em Aberto'
    dados = busca_usuarios_e_editais(conn, cursor)

    for email, editais in dados.items():

        if not editais:
            continue

        capes = []
        finep = []
        cnpq = []

        for edital in editais:
            id_edital, edital_data_publicacao, edital_data_prazo_envio, edital_titulo,  edital_link  = edital
           
            if 'capes' in edital_link:
                capes.append({'titulo': edital_titulo, 'link': edital_link})
            elif 'cnpq' in edital_link:
                cnpq.append({'titulo': edital_titulo, 'link': edital_link})
            elif 'finep' in edital_link:
                finep.append({'titulo': edital_titulo, 'link': edital_link})
    

        input = open("components.html", "r")
        arquivo = input.read()

        template = Template(arquivo)
        renderizar = template.render(capes=capes, cnpq=cnpq, finep=finep)

        # Preparando a mensagem
        msg = MIMEMultipart('alternative')
        msg['Subject'] = assunto
        msg['From'] = settings.REMETENTE
        msg['To'] = email

        # part1 = MIMEText(links, 'plain')
        part2 = MIMEText(renderizar, 'html')

        # msg.attach(part1)
        msg.attach(part2)

        envia_email(email, msg)
        input.close()
