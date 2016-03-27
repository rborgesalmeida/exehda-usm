# -*- coding: utf-8 -*-

# Autores: Ricardo Almeida, Roger Machado

# Driver para conexão com o mongodb
from pymongo import MongoClient

from readConfFile import ReadConfFile
from time import sleep
import logging

# Função para conexão ao banco de dados mongodb

class EventDatabaseConnection:
    """
    Classe que realiza a conexão com o banco de dados
    """
    readConf = None
       
    def __init__(self):
        """
        Método de inicialização da classe
        """
        try:
            self.readConf = ReadConfFile.__new__(ReadConfFile)
        except Exception, e:
            logging.error('Falha ao inicializar conexão com banco não relacional', exc_info=True)
           
    def connect (self):   
        """
        Função usada para criar uma conexão com o banco de dados.
        A função fica executando até conseguir criar uma conexão,
        quando consegue retorna essa conexão para ser usada
        """
        numberOfTry = 0
        while True:
            try:
                # Falta autenticacao
                strMongoConnection = 'mongodb://' + str(self.readConf.dbNServer) + \
                                    ':' + str(self.readConf.dbNPort) + '/'
                client = MongoClient(strMongoConnection)
                db = client[self.readConf.dbNName]
                
                if numberOfTry != 0:
                    logging.info("Sucesso: Conexão reestabelecida." );
                return db
            except Exception, e:
                logging.error('Falha ao conectar com banco não relacional', exc_info=True)
                #=================================================================================#
                # Caso 3 tentativas de conexão sejam executadas sem sucesso, a próxima tentativa
                # será após 10 segundos, e um e-mail é enviado informando o a falha, caso 10
                # tentativas ocorram sem sucesso, o mesmo acontecerá porém aguardará por 20 
                # segundos para realizar as próximas tentativas. Após 10 tentativas, nada
                # acontecerá até que a conexão seja reestabelecida, e então, um e-mail é enviado.
                if numberOfTry <= 10:
                    numberOfTry = numberOfTry + 1
                if numberOfTry == 3:
                    logging.warning("Alerta: Não foi possível realizar conexão com " + 
                                           " o banco. Próxima tentativa em 10 segundos...");
                    sleep(10)
                    #enviarEmail('USUARIO','SENHA', 'DESTINATARIO','Status= ALERTA',
                        #         'Nao esta sendo possivel enviar os logs!!', 'SERVIDORSMTP', 'PORTA')
                elif numberOfTry == 10:
                    logging.warning("Urgente: Ainda há problema na comunicação com o banco"+
                                           " de dados. Próxima tentativa em 20 segundos...");
                    #enviarEmail('USUARIO','SENHA', 'DESTINATARIO','Status= URGENTE',
                        #          'Nao esta sendo possivel enviar os logs!!, 'SERVIDORSMTP', 'PORTA')
                    sleep(20)
