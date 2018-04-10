from processa_edital import envia_mensagem_email
import settings

envia_mensagem_email(settings.conn, settings.cursor)
