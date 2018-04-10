#!/bin/sh

# Executa spiders
scrapy runspider finep_parser.py
scrapy runspider cnpq_parser.py
scrapy runspider capes_parser.py

# Envia emails
python envia_emails.py