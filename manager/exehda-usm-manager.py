#!/usr/bin/python
# -*- coding: utf-8 -*-

# Autores: Ricardo Almeida, Roger Machado

# Leitura do arquivo de configuração
from readConfFile import ReadConfFile

# Funcões do servidor que serão disponibilizadas ao EXEHDA-USM Collector ou SmartLogger
from serverFunctions import ServerFunctions

from databaseConnection import DatabaseConnection
from esper import Esper

import logging

from SocketServer import ForkingMixIn
from SimpleXMLRPCServer import SimpleXMLRPCServer,SimpleXMLRPCRequestHandler

class AsyncXMLRPCServer(ForkingMixIn, SimpleXMLRPCServer): pass


if __name__ == "__main__":
    try:
        #=========================================================================================#
        # Realiza a leitura do arquivo de configuração, caso encontre erro,
        # este é retornado e o programa é finalizado
        confFile = 'exehda-usm-manager.conf'
        readConf = ReadConfFile(confFile)
        if readConf.readFile() == False:
            print "Por favor, verifique o arquivo de log para identificar " + \
            "parâmetros no arquivo de configuração inválidos."
            exit()
        #=========================================================================================#
        
        #=========================================================================================#
        # Cria a variável writeLog adquirindo a instância previamente criada pelo
        # readConfFile, e anuncia a inicialização do servidor
	logging.basicConfig(filename=readConf.logFile, format='%(asctime)s debian exehda-usm-manager[%(process)d]: %(message)s',
                            datefmt='%b %d %H:%M:%S', level=logging.INFO)
        logging.info("Inicializando exehda-usm-manager...")
        #=========================================================================================#
        
        #=========================================================================================#
        # Inicializa as funções que serão disponibilizadas pelo servidor
        serverFunction = ServerFunctions()
        
        dbConnection = DatabaseConnection()
        procEsper = None
        if dbConnection.verifyCorrelation():
            readConf.correlation = True        
            procEsper = Esper(readConf.esperPort)
            procEsper.daemon = True
            procEsper.start()                                        
            
            # Aguarda o esper iniciar para poder iniciar as threads de monitoramento                     
            while serverFunction.connectEsper() == False:   
                pass        
        #=========================================================================================#
        
        #=========================================================================================#
        # Cria a conexao
        serverAddress = (readConf.listenIP, readConf.listenPort)
	server = AsyncXMLRPCServer(serverAddress, SimpleXMLRPCRequestHandler, logRequests=False)
        #=========================================================================================#
        
        #=========================================================================================#
        # Disponibiliza as funções que serão requisitadas pelos clientes
        server.register_function(serverFunction.getMonitoredItems)
        server.register_function(serverFunction.getDiscoveredItems)
        server.register_function(serverFunction.insertLogs)
        server.register_function(serverFunction.updateStatus)
        server.register_function(serverFunction.insertDiscoveredItems)
        server.register_function(serverFunction.getExpressionLogs)
        server.register_function(serverFunction.getSituations)
        server.register_function(serverFunction.insertSituations)
        server.register_function(serverFunction.getHostOptions)
        #=========================================================================================#
        
        #=========================================================================================#
        # Anuncia a disponibilidade do serviço no IP e porta especificados, e coloca o servidor
        # na escuta
        sockName = server.socket.getsockname()
	logging.info("Servindo HTTP no IP %s porta %s", str(sockName[0]), str(sockName[1]))
        server.serve_forever()
        #=========================================================================================#
    #=========================================================================================#    
    # Caso o servidor seja finalizado, registra uma mensagem
    except KeyboardInterrupt:
	logging.info("Fechando exehda-usm-manager...")
        if procEsper != None:
            procEsper.stop()
	    procEsper.join()
        exit(0)
    #=========================================================================================#
    # Caso ocorra alguma exceção, está é registrada no log
    except Exception, e:
        logging.info("exehda-usm-manager finalizado inesperadamente", exc_info=True)
    #=========================================================================================#
