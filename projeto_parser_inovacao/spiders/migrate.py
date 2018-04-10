import sqlite3
import settings


conn = sqlite3.connect(settings.BANCO_DADOS)
cursor = conn.cursor()


cursor.execute("""CREATE TABLE edital
                       (id_edital INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
                        url VARCHAR(100) NOT NULL, data_publicacao VARCHAR(80),
                        data_prazo_envio VARCHAR(80), titulo VARCHAR(80));
               """)
conn.commit()


cursor.execute("""CREATE TABLE usuario
                       (id_usuario INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
                        nome VARCHAR(80) NOT NULL, email VARCHAR(80) NOT NULL);
               """)
conn.commit()


cursor.execute("""CREATE TABLE usuario_edital
                       (usuario_id INTEGER NOT NULL,
                       edital_id INTEGER NOT NULl,
                       FOREIGN KEY (usuario_id) REFERENCES usuario(id_usuario),
                       FOREIGN KEY (edital_id) REFERENCES usuario(id_edital));
               """)
conn.commit()
conn.close()
