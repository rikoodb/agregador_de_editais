[![Build Status](https://travis-ci.org/rikoodb/agregador_de_editais.svg?branch=master)](https://travis-ci.org/rikoodb/agregador_de_editais)

# Agregador de Editais

## Ideia / o que é  :
 Existem alguns órgãos no Brasil que lançam editais com o objetivo de apoiar ideias inovadoras no âmbito tecnológico e Santa Catarina é um dos estados que mais se beneficia com esses incentivos. Os editais são lançados algumas vezes no ano e para os interessados, é necessário verificar diariamente as chamadas públicas nos sites desses órgãos.

Esse projeto, foi uma ideia que tive ao trabalhar no Laboratório de Inovação Tecnológica (Labnita) da UFSC campus Araranguá. O projeto consiste em buscar editais que estão em aberto nos sites dos órgãos cadastrados, considerando sua data de publicação e fazer o envio desses editais para o email dos usuários cadastrados no sistema. Atualmente, os editais disponíveis no sistema são dos seguintes órgãos : Capes, finep e CNPQ.

## Como baixar:
 - git clone https://github.com/rikoodb/agregador_de_editais.git

## Como instalar :
 - virtualenv --python=python3 env  --no-site-packages
 - source env/bin/activate


agregador_de_editais/
 - pip install -r requirements.txt para instalar as dependências do projeto

Encontrou algum erro relacionado a "failed twisted" na instalação do scrapy? Instale as dependências necessárias para o seu S.O em :
 https://doc.scrapy.org/en/latest/intro/install.html

## Itens necessários:
O .gitignore vai ignorar o banco de dados e o settings.ini do projeto. Nesse caso, é necessário criá-los.

Para o settings :

agregador_de_editais/projeto_parser_inovacao/spiders

 - criar um arquivo com nome de "settings.ini"
    
        [settings]
    	REMETENTE=colocar_o_email_aqui
    	SENHA=colocar_a_senha_aqui
        BANCO_DADOS=caminho/banco_dados.db

 Para o banco de dados :
  
agregador_de_editais/projeto_parser_inovacao/spiders

     python migrate.py
 
 É necessário cadastrar pelo menos um email para o script enviar os editais :

 Caminho_do_db/
 
    sqlite3 banco_dados.py
    INSERT INTO usuario (nome,email) VALUES ('nome_aqui', 'email_aqui');
    .exit


O script está configurado para receber um email da outlook. Caso queira mudar, vá até o arquivo "processa_edital.py", função "envia_email()" e altere  "server = smtplib.SMTP('smtp-mail.outlook.com', '587')":
 
- Para um email gmail :

        server = smtplib.SMTP(‘smtp.gmail.com’, 587) 

- Para um email hotmail :
 
        server = smtplib.SMTP(‘smtp.live.com’, 465)

## Como executar :
agregador_de_editais/projeto_parser_inovacao/spiders
 - sh run.sh
 
 Após o script ser rodado, dependendo do tipo de email (hotmail, gmail, etc), o script vai retornar no email algo mais ou menos assim :

![alt text](https://imagizer.imageshack.com/v2/362x711q90/923/pImORh.png)
 
Caso queira executar novamente para receber os editais no mesmo email cadastrado na tabela usuario, é necessário limpar os dados da tabela edital e usuario_edital.

agregador_de_editais/projeto_parser_inovacao/spiders

     sqlite3 banco_dados.db
     DELETE FROM edital;
     DELETE FROM usuario_edital;
	 
## Como executar os testes :
agregador_de_editais/projeto_parser_inovacao/spiders
 - python -m unittest -v 

Observações :
 - O projeto ainda não foi concluido. Estou trabalhando nos testes e no layout para cadastrar o usuario.
  - Toda a parte de front-end do projeto não foi de minha autoria. Utilizei um layout pronto e fui modificando conforme minhas necessidades.

