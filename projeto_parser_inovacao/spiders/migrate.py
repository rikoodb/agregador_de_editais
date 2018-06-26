import sqlite3
import settings


conn = sqlite3.connect(settings.BANCO_DADOS)
cursor = conn.cursor()


cursor.execute("""CREATE TABLE IF NOT EXISTS "edital" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, 
                "data_publicacao" varchar(30) NULL, "data_prazo_envio" varchar(30) NULL, 
                "titulo" varchar(30) NULL, "url" varchar(30) NULL);
               """)
conn.commit()


cursor.execute("""CREATE TABLE IF NOT EXISTS "usuario" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, 
                "nome" varchar(30) NOT NULL, "email" varchar(50) NOT NULL);

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
