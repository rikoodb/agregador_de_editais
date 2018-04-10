import sqlite3
from decouple import config


REMETENTE = config('REMETENTE', default='')
SENHA = config('SENHA', default='')
BANCO_DADOS = config('BANCO_DADOS', default='banco_dados.db')

conn = sqlite3.connect(BANCO_DADOS)
cursor = conn.cursor()