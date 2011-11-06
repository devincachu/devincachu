# -*- coding: utf-8 -*-
import datetime
import hashlib
import random
import sys


def gerar_arquivo(nome_arquivo):
    fp = open(nome_arquivo, 'r')
    try:
        conteudo = fp.read()
        kw = {
            'db_name': raw_input('Digite o nome do banco de dados: '),
            'db_user': raw_input('Digite o nome do usuário do banco de dados: '),
            'db_password': raw_input('Digite a senha do usuário: '),
            'secret_key': hashlib.sha1('%d%s' % (random.randint(0, 100000), datetime.datetime.now().isoformat())).hexdigest(),
        }
        print conteudo % kw
    finally:
        fp.close()


if __name__ == '__main__':
    if len(sys.argv) != 2:
        print "Você deve informar o arquivo de origem!"
        sys.exit(1)

    gerar_arquivo(sys.argv[1])
