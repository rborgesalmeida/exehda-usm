# -*- coding: utf-8 -*-

# Autores: Ricardo Almeida, Roger Machado

from readConfFile import ReadConfFile
from logAnalyzer import LogAnalyzer
from syslogServer import SyslogServer
from statusAnalyzer import StatusAnalyzer
import logging
import socket
import os
import time
import pickle
import multiprocessing


class MonitoredItems(multiprocessing.Process):
    """
    Classe que vai criar as threads para cada item que irá ser monitorado
    """
    managerCommunication = None
    nexthopCommunication = None
    type_ = None
    hashFileName = None
    timeUpdateItems = None
    syslogThread = None
    expression = None
    fileExpression = None
    sock = None
    
    def __init__(self, hashFileName, nexthopCommunication, managerCommunication,  type_):
        """
        Método de inicialização da classe.
        """
        multiprocessing.Process.__init__(self)
        
        readConf = ReadConfFile.__new__(ReadConfFile)
        self.timeUpdateItems = readConf.timeUpdateItems
        
        self.type_ = type_
                
        self.managerCommunication = managerCommunication
        self.nexthopCommunication = nexthopCommunication
        
        self._is_alive = True
        
        # cria o nome do arquivo com o ip usando md5
        self.hashFileName = hashFileName
        self.fileExpression = 'bufferParser/'+ self.type_ + '_'+ self.hashFileName
        if self.type_ == 'log' or self.type_ == 'syslog' :
            self.expression =  self.managerCommunication.getExpression()
            if self.expression != False:
                self.writeExpression(self.expression)
            if self.type_ == 'syslog':
                self.sock=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                self.sock.bind(("0.0.0.0",1000))
                self.sock.listen(5)
        
    def run(self):
        """
        Método que cria as threads de coleta de logs/status.
        """
        try:
            p = multiprocessing.current_process()    
            logging.info('Inicializando processos de %s: %d', self.type_, p.pid)
        
            threadDict = {}
            oldItems = []
            newExpression = []
            isFirst = True
            #=====================================================================================#
            # Busca do buffer local de itens os itens monitorados
            oldItems = self.getItemsBufferFile(self.type_)
            oldItemsLogClone = oldItems[:]
            #self.createThreads(oldItemsLogClone, threadDict, self.type_)
            #=====================================================================================#
            while self._is_alive:
                #=============================================================================#
                # Reliza a descoberta de itens, para posteriormente verificar se novos itens 
                # foram gerados ou modificados               
                self.managerCommunication.makeDiscoveredItems()
                # Busca os novos items
                newItems = self.managerCommunication.getItems(self.type_)
                while newItems == False:
                    newItems = self.managerCommunication.getItems(self.type_)
                # Cria uma cópia completa dos novos itens
                newItemsLogClone = newItems[:]
                #=============================================================================#
                # Caso os novos itens sejam diferentes dos anteriores:
                if isFirst == False and str(newItems) != str(oldItems) and newItems != False:                    
                    #print "Diferentes"
                    #=============================================================================#
                    # Atualiza o arquivo de buffer com os itens monitorados
                    self.updateFileItemsMonitored(newItems, self.type_)
                    #=============================================================================#
                    #=========================================================================#
                    # Verifica para cada item da lista de novos itens, se ele ja era monitorado, 
                    # e a remove da lista de novos itens e dos antigos itens
                    i = 0
                    while len(oldItems) > i:
                        if oldItems[i] in newItems:
                            newItems.remove(oldItems[i])
                            oldItems.remove(oldItems[i])
                        else:
                            i = i + 1
                    #=========================================================================#
                    
                    #=========================================================================#
                    # Caso tenha sobrado itens na lista de novos itens, uma thread é criada
                    # para monitorar cada um destes itens
                    if len(newItems) > 0:
                        self.createThreads(newItems, threadDict, self.type_)
                    #=========================================================================#
                        
                    #=========================================================================#
                    # Caso tenha sobrado algum item na lista dos items previamente monitorados,
                    # a thread que monitorava o item é finalizada
                    if len(oldItems) > 0:
                        self.killThreads(oldItems, threadDict, self.type_)
                    #=========================================================================#
                    # Atualiza a lista de itens previamente monitorados para ser a nova lista
                    oldItems = newItemsLogClone[:]
                    #=========================================================================#
                elif isFirst == True and newItems != False:
                    self.createThreads(newItems, threadDict, self.type_)
                    oldItems = newItemsLogClone[:]
                    isFirst = False
                elif isFirst == True:
                    self.createThreads(oldItemsLogClone, threadDict, self.type_)
                    isFirst = False                        
                        
                if self.type_ == 'log':
                    # busca as expressoes de formatacao de logs no banco de dados
                    newExpression =  self.managerCommunication.getExpression()
                    # testa se foi mudada alguma expressao
                    if str(self.expression) != str(newExpression) and newExpression != False :
                        # para todas as threads para poder alterar o arquivo de expressao
                        for threadKey in threadDict.keys():
                            threadDict[threadKey].pauseStart(True)
                        expressionClone = newExpression[:]
                        # altera o arquivo de expressao
                        self.writeExpression(expressionClone)
                        self.expression = newExpression[:]
                        # recomeca a execucao de todas as threads
                        for threadKey in threadDict.keys():
                            threadDict[threadKey].pauseStart(False)
                elif self.type_ == 'syslog' and newExpression != False:
                    # busca as expressoes de formatacao de logs no banco de dados
                    newExpression =  self.managerCommunication.getExpression()
                    # testa se foi mudada alguma expressao
                    if str(self.expression) != str(newExpression) :
                        self.syslogThread.pauseStart(True)
                        expressionClone = newExpression[:]
                        # altera o arquivo de expressao
                        self.writeExpression(expressionClone)
                        self.expression = newExpression[:]
                        self.syslogThread.pauseStart(False)
                #=================================================================================#
                # Espera para atualizar os itens monitorados ou realizar uma nova tentativa de 
                # adquirir a chave simétrica
                #print self.readConf.timeUpdateItems
                time.sleep(self.timeUpdateItems)
                #=================================================================================#
            # Ao sair do while (thread foi finalizada), realiza o processo de finalização das
            # threads "filhas" (responsáveis pela coleta dos logs)
            #print "Finalizando threads de " + self.type_ + " ..."
            for threadKey in threadDict.keys():
                threadDict[threadKey].stop()
            
        except Exception, e:
            logging.error('Falha ao criar processo de monitoramento', exc_info=True)
        except KeyboardInterrupt:
            return
                
    def writeExpression(self, expressionClone):
        """
        Método usado para escrever as expressões lidas do banco no arquivo de expressões,
        para serem usadas na formatação dos logs
        """
        f = open(self.fileExpression + '.py', 'w')
        f.write("# -*- coding: utf-8 -*-\n\n")
        f.write("from pyparsing import * \n\n")
        while len(expressionClone) > 0:    
            f.write(str(expressionClone[0][0].strip()) + " = " + str(expressionClone[0][1].strip()) + '\n')
            expressionClone.pop(0)
        f.close
    
    def createThreads(self, monitoredItems, threadDict, type_):
        """
        Cria threads adicionando ao dicionário de threads (threadDict) com os nomes
        passados na lista por parâmetro (monitoredItems)
        """        
        #print type_
        while len(monitoredItems) > 0:
            newItem = monitoredItems.pop()
            if type_ == 'log':
                newMonitoredFile = str(newItem[0]).strip()
                newMonitoredFile = newMonitoredFile[4:len(newMonitoredFile)-1:]
                table = str(newItem[2]).strip()
                delay = newItem[1]
                identifier = str(newItem[7]).strip()
                #=====================================================================================#
                # Verifica se o item do tipo log possui alguma expressão regular
                if newItem[3] != None:
                    filterProgram = str(newItem[3]).strip()
                else:
                    filterProgram = None
                # Remove os espaços do final das colunas (formatcolumn e formatcolumntype) caso estas
                # não estejam em branco    
                if newItem[4] != None:
                    formatColumn = str(newItem[4]).strip()
                if newItem[5] != None:
                    formatColumnType = str(newItem[5]).strip()
                #=====================================================================================#
                # verifica se ja possui alguma thread monitorando o arquivo
                if threadDict.has_key(newMonitoredFile):
                    # como ja possui alguma thread monitorando o arquivo, pega a thread no 
                    # dicionario e chama o metodo para atualizar os campos da thread
                    thread = threadDict[newMonitoredFile]
                    thread.updateConf(table, filterProgram, formatColumn, formatColumnType)
                else:
                    # como nao possui nenhuma thread monitorando o arquivo, cria a thread 
                    # e chama o metodo para atualizar os dados
                    thread = LogAnalyzer(newMonitoredFile, identifier, delay, self.nexthopCommunication, self.fileExpression)
                    thread.updateConf(table, filterProgram, formatColumn, formatColumnType)
                    thread.daemon = True
                    thread.start()
                    # adiciona a thread criada no dicionario de threads 
                    threadDict[newMonitoredFile] = thread
                #print "Thread de log ativa: " + str(newMonitoredFile) + ". Tabela: " + str(table)
		logging.info("Thread de log ativa: %s Tabela: %s", str(newMonitoredFile), str(table))
            elif type_ == 'status':
                monitoredKey = str(newItem[0]).strip()
                itemID = newItem[4]
                delay = newItem[1]
                identifier = str(newItem[6]).strip()
                thread = StatusAnalyzer(monitoredKey, identifier,
                                        itemID, delay, self.nexthopCommunication)
                thread.daemon = True
                thread.start()
                threadDict[monitoredKey] = thread
		logging.info("Thread de status ativa: %s", str(monitoredKey))
            elif type_ == 'syslog':
                hostname = str(newItem[0]).strip()
                hostname = hostname[7:len(hostname)-1:]
                table = str(newItem[1]).strip()
                #=====================================================================================#
                # Verifica se o item do tipo log possui alguma expressão regular
                if newItem[2] != None:
                    filterProgram = str(newItem[2]).strip()
                else:
                    filterProgram = None
                # Remove os espaços do final das colunas (formatcolumn e formatcolumntype) caso estas
                # não estejam em branco    
                if newItem[3] != None:
                    formatColumn = str(newItem[3]).strip()
                if newItem[4] != None:
                    formatColumnType = str(newItem[4]).strip()
                #=====================================================================================#
                #=====================================================================================#
                # verifica se ja possui alguma thread monitorando o arquivo
                if threadDict.has_key(hostname):
                    # como ja possui alguma thread monitorando o arquivo, pega a thread no 
                    # dicionario e chama o metodo para atualizar os campos da thread
                    thread = threadDict[hostname]
                    thread.updateConf(table, filterProgram, formatColumn, formatColumnType)
                else:
                    # como nao possui nenhuma thread monitorando o arquivo, cria a thread 
                    # e chama o metodo para atualizar os dados
                    thread = SyslogServer(self.fileExpression, self.sock, self.nexthopCommunication)
                    thread.updateConf(table, filterProgram, formatColumn, formatColumnType)
                    thread.daemon = True
                    thread.start()
                    # adiciona a thread criada no dicionario de threads 
                    threadDict[hostname] = thread
                #logging.info("Thread de syslog ativa: %s + str(hostname) + ' ' + str(filterProgram)
                
    def killThreads(self, deactivatedItems, threadDict, type_):
        """
        Finaliza as threads que estão no dicionário de threads (threadDict) com
        os nomes passados na lista por parâmetro (deactivatedItems)
        """
        try:
            i = 0
            while len(deactivatedItems) > i:
                deactivatedItem = deactivatedItems[i]
                if type_ == 'log':
                    # pega o campo arquivo monitorado retirando os espacos 
                    deactivatedMonitoredFile = str(deactivatedItem[0]).strip()
                    deactivatedMonitoredFile = deactivatedMonitoredFile[4:len(deactivatedMonitoredFile)-1:]
                    # pega o campo tabela
                    deactivatedTableFile = deactivatedItem[2].strip()
                    # chama o metodo para parar a thread
                    stopThread = threadDict[deactivatedMonitoredFile].stop(deactivatedTableFile)
                    logging.info("Thread de log: %s finalizada.", deactivedTableFile)
                    # testa se ainda possui algum arquivo sendo monitorado na thread
                    if stopThread: 
                        # apaga a thread do dicionario pois, ja nao possui mais nenhum arquivo
                        # sendo monitorado
                        del threadDict[deactivatedMonitoredFile]
                elif type_ == 'status':
                    deactivatedMonitoredKey = str(deactivatedItem[0]).strip()
                    threadDict[deactivatedMonitoredKey].stop()
                    logging.info("Thread de status: %s desativada.", deactivedMonitoredKey)
                elif type_ == 'syslog':
                    hostname = deactivatedItem[0].strip()
                    hostname = hostname[7:len(hostname)-1:]
                    filterProgram = str(deactivatedItem[2]).strip()
                    # chama o metodo para parar a thread
                    stopThread = threadDict[hostname].stop(deactivatedTableFile)
                    # testa se ainda possui algum arquivo sendo monitorado na thread
                    if stopThread: 
                        # apaga a thread do dicionario pois, ja nao possui mais nenhum arquivo
                        # sendo monitorado
                        del threadDict[deactivatedMonitoredFile]
                i = i + 1
        except Exception, e:
            logging.error('Falha ao finalizar thread', exc_info=True)
                
    def getItemsBufferFile(self, type_):
        """
        Retorna os itens localizados nos arquivos de buffer de itens.
        """
        # Verifica se possui um buffer dos itens monitorados localmente, caso contrátio
        # retornará uma lista em branco
        if type_ == 'log':
            fullFileName = 'bufferItems/' + self.hashFileName + '.cbl'
        elif type_ == 'status':
            fullFileName = 'bufferItems/' + self.hashFileName + '.cbs'
        elif type_ == 'syslog':
            fullFileName = 'bufferItems/' + self.hashFileName + '.cbsy'
        if os.path.isfile(fullFileName):
            monitoredLogsRecovered = open(fullFileName, 'rb')
            dataLogsEncryptedFromFile = pickle.load(monitoredLogsRecovered)
            monitoredLogsRecovered.close()
            oldItemsLog = eval(str(dataLogsEncryptedFromFile))
            return oldItemsLog
        else:
            return []
            
    def updateFileItemsMonitored(self, newMonitoredItems, type_):
        """
        Atualiza o arquivo local dos itens monitorados
        """
        if type_ == 'log':
            fullFileName = 'bufferItems/' + self.hashFileName + '.cbl'
        elif type_ == 'status':
            fullFileName = 'bufferItems/' + self.hashFileName + '.cbs'
        elif type_ == 'syslog':
            fullFileName = 'bufferItems/' + self.hashFileName + '.cbsy'
        if os.path.isfile(fullFileName):
            monitoredItemsRecovered = open(fullFileName, 'r')
            dataLogsEncryptedFromFile = pickle.load(monitoredItemsRecovered)
            monitoredItemsRecovered.close()
            oldMonitoredItems = dataLogsEncryptedFromFile
    
            if str(newMonitoredItems) != str(oldMonitoredItems):
                monitoredLogsFile = open(fullFileName, 'w')
                pickle.dump(str(newMonitoredItems), monitoredLogsFile)
                monitoredLogsFile.close()
        else:
            monitoredLogsNewFile = open(fullFileName, 'w')
            pickle.dump(str(newMonitoredItems), monitoredLogsNewFile)
            monitoredLogsNewFile.close()    
    
    def stop(self):
        """
        Finaliza a thread
        """
        self._is_alive = not self._is_alive
