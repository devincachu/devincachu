# -*- coding: utf-8 -*-
import datetime
import hashlib
import os
import random
import sys

meu_diretorio = os.path.dirname(__file__)
arquivo_saida = os.path.join(meu_diretorio, "devincachu", "settings_local.py")


def gerar_arquivo(nome_arquivo):
    fp = open(nome_arquivo, 'r')
    saida = open(arquivo_saida, 'w')
    try:
        conteudo = fp.read()
        kw = {
            'db_name': raw_input('Digite o nome do banco de dados: '),
            'db_user': raw_input('Digite o nome do usuário do banco de dados: '),
            'db_password': raw_input('Digite a senha do usuário: '),
            'secret_key': hashlib.sha1('%d%s' % (random.randint(0, 100000), datetime.datetime.now().isoformat())).hexdigest(),
        }
        saida.write(conteudo % kw)
    finally:
        fp.close()
        saida.close()


if __name__ == '__main__':
    if len(sys.argv) != 2:
        print "Você deve informar o arquivo de origem!"
        sys.exit(1)

    gerar_arquivo(sys.argv[1])
