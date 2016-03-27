#!/usr/bin/python
# -*- coding: utf-8 -*-

# Autores: Ricardo Almeida, Roger Machado

from readConfFile import ReadConfFile
from monitoredItems import MonitoredItems
from serverCommunication import ServerCommunication
from esper import Esper
import logging
import time
import hashlib

if __name__ == "__main__":
    """
    Código princial - para cada servidor ele instancia os objetos relacionados a criptografia, 
    buffer (temporariamente desativados), conexao com o servidor e itens a serem monitorados. 
    """
    try:
        
        #=========================================================================================#
        confFile = 'exehda-usm-collector.conf'
        readConf = ReadConfFile(confFile)
        if readConf.readFile() == False:
            print "Por favor, verifique o arquivo de log para identificar " + \
            "parâmetros inválidos no arquivo de configuração."
            exit()
        
        logging.basicConfig(filename=readConf.logFile, format='%(asctime)s debian exehda-usm-collector[%(process)d]: %(message)s',
                            datefmt='%b %d %H:%M:%S', level=logging.INFO)
        
        logging.info("Inicializando exehda-usm-collector...")
        #=========================================================================================#
        
        #=========================================================================================#
        # Cria os processos, um para o analisador de logs, e um para o analisador de status
        pLog = []
        pStatus = []
        pSyslog = []
        pEsper = []
        iServer = 0
        portEsperSend = readConf.esperPort
        
        # se possui smartlogger, entao o 
        # ServerCommunication do Manager sera apenas para coleta de dados
        # e o do SmartLogger sera para envio dos dados
        
        # Define quais serao os proximos servidores para enviar os dados
        # (proximo passo na hierarquia)
        if (len(readConf.SmartLoggerIP) > 0):
            nexthopIP = readConf.SmartLoggerIP
            nexthopPort = readConf.SmartLoggerPort
        else:
            nexthopIP = readConf.ManagerIP
            nexthopPort = readConf.ManagerPort
        
        while (len(readConf.serverIP) > iServer):
            
            # Instância os objetos que devem ser únicos para cada servidor
            # O nome server nao necessariamente significa o EXEHDA-USM Manager, mas sim
            # o proximo nivel na hierarquia
            managerAddress = str("http://" + str(readConf.managerIP[iServer]) + ":" + 
                                str(readConf.managerPort[iServer]))
            hashFileName = hashlib.md5(managerAddress).hexdigest()
            managerCommunication = ServerCommunication(managerAddress, portEsperSend)
            
            nexthopAddress = str("http://" + str(nexthopIP[iServer]) + ":" + 
                                str(nexthopPort[iServer]))
            nexthopCommunication = ServerCommunication(nexthopAddress, portEsperSend)
        
            # Só prossegue caso consiga ler as opções de configuração armazenadas no BD do Manager
            while managerCommunication.getHostOptions() != True:                
                time.sleep(5)
            
                                                
            if readConf.correlation == 1 or readConf.correlation == 3:            
                procEsper = Esper(hashFileName, portEsperSend, nexthopCommunication, managerCommunication)
                procEsper.daemon = True
                procEsper.start()
                            
                pEsper.append(procEsper)
                
                # Aguarda o esper iniciar para poder iniciar as threads de monitoramento                     
                while managerCommunication.connectEsper() != 1:                     
                    time.sleep(5)
            
            procLog = MonitoredItems(hashFileName, nexthopCommunication, managerCommunication, 'log')
            procLog.daemon = True
            procLog.start()
                        
            pLog.append(procLog)
            
            procStatus = MonitoredItems(hashFileName, nexthopCommunication, managerCommunication, 'status')
            procStatus.daemon = True
            procStatus.start()
                        
            pStatus.append(procStatus)
            
            threadSyslog = MonitoredItems(hashFileName, nexthopCommunication, managerCommunication, 'syslog')
            threadSyslog.daemon = True
            threadSyslog.start()
            
            pSyslog.append(threadSyslog)
            
            portEsperSend = portEsperSend +1
            iServer = iServer + 1
        #=========================================================================================#
        while True:
            time.sleep(100)
            
    except KeyboardInterrupt:
        logging.info('Fechando exehda-usm-collector... Finalizando processos...')
        logging.info("Finalizando processos de status")
        while len(pStatus) > 0:
            statusProc = pStatus.pop()
            statusProc.terminate()
            statusProc.join()
        logging.info("Finalizando processos de log")
        while len(pLog) > 0:
            logProc = pLog.pop()
            logProc.terminate()
            logProc.join()
        logging.info("Finalizando processos de syslog")
        while len(pSyslog) > 0:
            syslogThread = pSyslog.pop()
            syslogThread.terminate()
            syslogThread.join()
        if readConf.correlation == 1 or readConf.correlation == 3:
            logging.info("Finalizando processos do esper")
            while len(pEsper) > 0:
                esperProc = pEsper.pop()
                esperProc.terminate()
                esperProc.join()
            
        logging.info('exehda-usm-collector finalizado com sucesso')
        
    except Exception, e:
        logging.error('exehda-usm-collector finalizado inesperadamente',  exc_info=True)
    
