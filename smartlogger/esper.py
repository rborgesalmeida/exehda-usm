# -*- coding: utf-8 -*-

# Autores: Ricardo Almeida, Roger Machado

import logging
from subprocess import Popen, PIPE
from time import sleep
from os import rename, linesep
from sys import path
from situations import Situations
from databaseConnection import DatabaseConnection
from multiprocessing import Process
from readConfFile import ReadConfFile
from serverCommunication import ServerCommunication

import socket

class Esper(Process):
    '''
    Classe responsável pela comunicação com o Esper
    '''
    crypto = None
    portEsperSend = None
    itemsFile = None
    situationsDict = None
    situationsStatusDict = None
    itemsLogs = None
    managerCommunication = None
    itemsStatus = None
    dbConnection = None

    def __init__(self, portEsperSend, managerCommunication):
        '''
        Construtor que recebe o hash criado de acordo com o endereço do servidor,
        porta de escuta do esper (por onde os eventos coletados serão enviados), 
        comunicação com o servidor, e a criptografia.
        '''
        Process.__init__(self)
        self.readConf = ReadConfFile.__new__(ReadConfFile)
        self.portEsperSend = portEsperSend
        self.managerCommunication = managerCommunication
        
        if (len(self.readConf.SmartLoggerIP) > 0):
                nexthopIP = self.readConf.SmartLoggerIP
                nexthopPort = self.readConf.SmartLoggerPort
            else:
                nexthopIP = self.readConf.ManagerIP
                nexthopPort = self.readConf.ManagerPort
                
        nexthopAddress = str("http://" + str(nexthopIP[iServer]) + ":" + 
                                    str(nexthopPort[iServer]))
        self.nexthopCommunication = ServerCommunication(nexthopAddress, portEsperSend)
            
        self._is_alive = True
        self.dbConnection = DatabaseConnection()
        
        self.local = path[0]
        self.itemsFile = str(self.local) + '/esper-5.3.0/exehda-usm-smartlogger/serverItems.csv'
        
        # Iniciliza o dicionário que armazena as situações a serem detectadas
        self.situationsDict = {}
        self.situationsStatusDict = {}
        
    def run(self):
        '''
        Método executado ao iniciar a thread. Inicialmente coleta as propriedades
        dos itens que são armazenadas em um arquivo que será lido ao iniciar o esper,
        na sequência coleta as situações a serem detectadas e o arquivo java do esper 
        é atualizado com as regras em epl. Finalmente inicia o esper.
        '''
        itemsOld = []
        situationsOld = []
        situationsNew = False
        restart = True
        while self._is_alive:
            
            itemsNew = self.getItemsToEsper()
            
            situationsNew = self.managerCommunication.getSituations()
            while situationsNew == False:
                situationsNew = self.managerCommunication.getSituations()
                
            pid = 0
            # Buscar a lista de itens monitorados para passar ao esper com o "nome da classe"
            # e suas propriedades (formatColumn no BD para os logs; valor, date_coll e error
            # para status) - ter um parametro no .conf para atualizacao dos itens


            if str(situationsOld) != str(situationsNew):
                situationsOld = situationsNew
                situationsNew = self.verifySituations(situationsNew, itemsNew)
                self.createEsperJavaFile(situationsNew)
                self.createDictSituations(situationsNew)
                restart = True

            if str(itemsOld) != str(itemsNew):                
                itemsOld = itemsNew
                itemsFile = open(self.itemsFile, 'wb')
                
                for item in itemsNew:
                    for itemField in item:
                        itemsFile.write(str(itemField) + ",")
                itemsFile.close()
                restart = True
                
            if restart == True:
                restart = False
                try:
                    if pid != 0:
                        pid.terminate()
                        pid.kill()
                    # Só inicia o esper se o houver situações a serem identificas
                    if len(situationsNew) > 0:    
                        setenv = Popen(["sh", str(self.local) + "/esper-5.3.0/exehda-usm-smartlogger/etc/setenv.sh"])
                        setenv.wait()
                        compile_ = Popen(["sh", str(self.local) + "/esper-5.3.0/exehda-usm-smartlogger/etc/compile.sh"])
                        compile_.wait()                
                        cmd = "sh " + str(self.local) + "/esper-5.3.0/exehda-usm-smartlogger/etc/run_namedwin.sh " + str(self.itemsFile) + ' ' + str(self.portEsperSend)
                        running_procs = [Popen(cmd.split(), close_fds=False, stdout=PIPE, bufsize=1)]

                        pid = running_procs[0].pid        
                                        
                        # Inicializa a lista formatColumn que contém o formato da tabela ...active_situations
                        formatColumn = []
                        formatColumn.append('description')
                        formatColumn.append('events')
                        formatColumn.append('situationid')
                        formatColumn.append('comments')
                        formatColumn.append('priority')
                        formatColumn.append('occurrences')
                        formatColumn.append('commandresult')
                    
                        while running_procs:
                            for proc in running_procs:
                                retcode = proc.poll()
                                if retcode is not None: # Processo finalizado
                                    running_procs.remove(proc)
                                    break
                                else:
                                    
                                    while True:
                                        next_line = proc.stdout.readline()
                                        if next_line == '' and proc.poll() != None:
                                            break
                                        
                                        #print "DADOS RECEBIDOS: ", next_line
                                        # Reinicializa a lista de dados a serem enviados ao servidor
                                        data = []
                                        msgList = str(next_line).split('^')
                                        # Não encontrou ^, logo dividi por ~ pois é status e deve ser tratado
                                        # de maneira diferente.
                                        if len(msgList) != 1:
                                            situation = self.situationsDict[msgList[0]]
                                            events = msgList[1]   
                                              
                                            # Substituir variáveis
                                            situation.applySubsVariable(events)
                                                                                                                                  
                                            commandresult = situation.executeCommand()
                                            data.append(situation.descriptionSubs)
                                            data.append(events)
                                            data.append(situation.id)
                                            data.append(situation.commentsSubs)
                                            data.append(situation.priority)
                                            data.append(1)
                                            data.append(commandresult)
                                                         
                                            if self.dbConnection.insertSituations(situation.hostname, formatColumn, data):
                                                logging.info('Situação inserida com sucesso: %s', str(data[0]))
                                            else:
                                                logging.info('ERRO: Falha ao inserir situação.')
                                            
                                            if self.nexthopCommunication.sendSituations(situation.hostname, formatColumn, data):
                                                logging.info('Situação enviada com sucesso: %s', str(data[0]))
                                            else:
                                                logging.info('ERRO: Falha ao enviar situação.')
                                                                                                                      
                                        else:
                                            try:
                                                # só entrará neste else quando não encontrar situações simples
                                                # (de monitoramento de status)                                            
                                                msgList = str(next_line).split('~')                                                                                        
                                                situation = self.situationsStatusDict[msgList[0]]
                                                events = msgList[1]
                                                                                                                                         
                                                self.dbConnection.removeSituations(situation.hostname, msgList[0], situation.id, events)
                                            except Exception:
                                                pass                                                                                                                                                   
                except Exception, e:
                    logging.error('ERRO: Falha ao executar o Esper', exc_info=True)
            sleep(30)
       
    # Funcao auxiliar         
    def between(self, left,right,s):
        before,_,a = s.partition(left)
        a,_,after = a.partition(right)
        return a
        
    def verifySituations(self, situations, items):
        situationWithItem = []
        for situation in situations:
            situation = list(situation)
            hostname = self.managerCommunication.getHostname(situation[13])
            situation[13] = hostname   
            situation[10] = hostname + '_' + str(situation[10])
            for item in items:
                if str(item[0])[2:] == situation[10]:                     
                     situationWithItem.append(situation)
                    
        if len(situations) != len(situationWithItem):
            logging.info('Atenção: Situações foram desativadas pois não há itens de coleta de dados ativos associados à elas ')
#         print situationWithItem
        return situationWithItem
        
    def createDictSituations(self, situations):
        '''Mantém o dicionário indexado pela regra epl. Caso as situações sejam alterados,
        o dicionário é reconstruído.
        '''
        try:
            # Apaga os itens do dicionário para liberar memória
            for situation in self.situationsDict:
                del(situation)
            for situation in self.situationsStatusDict:
                del(situation)
            self.situationsDict = {}  
            self.situationsStatusDict = {}  
            for situation in situations: 
                priority = situation[9] * situation[13]
                self.situationsDict['@Priority (' + str(priority) + ') ' + situation[2]] = Situations(situation[0], situation[1], situation[2], 
                                                                   situation[3], situation[4], situation[5],
                                                                   situation[6], situation[7], situation[8], 
                                                                   priority, situation[13])
                    
                if not 'Log' in situation[10]:
#                     identifierEPL = self.between('`', '`', str(situation[2]))
                    self.situationsStatusDict[situation[10]] = Situations(situation[0], situation[1], situation[2], 
                                                                   situation[3], situation[4], situation[5],
                                                                   situation[6], situation[7], situation[8], 
                                                                   priority, situation[13])
        except Exception, e:
            logging.info('ERRO: Falha ao criar dicionário com situações: ', exc_info=True)     
                    
    
    def createEsperJavaFile(self, situationsNew):
        """
        Cria um novo arquivo java baseado nas situações a serem detectadas recebidas por parâmetro.
        Obs.: Este arquivo deverá ser compilado posteriormente.
        """
        try:
            esperStatementsFile = open(str(self.local) + "/esper-5.3.0/exehda-usm-smartlogger/src/main/java/com/espertech/esperio/socket/EsperSocketDefault.java", "r")
            lines = esperStatementsFile.readlines()
            newLines = []
            for line in lines:
                if "// Statements" not in line:
                    newLines.append(line)
                else:
                    newLines.append(line)
                    i = 0
                    for situation in situationsNew:
                        priority = situation[9] * situation[13]
                        newLines.append("\tEPStatement stmt" + str(i) + ' = provider.getEPAdministrator().createEPL("@Priority (' + str(priority) + ') ' +  str(situation[2]) + '");\n')
                        newLines.append("\tstmt" + str(i) + '.addListener(new CEPListener("L' + str(i) + '" ));\n')
                        i = i + 1
            esperStatementsFile.close()
            rename(str(self.local) + "/esper-5.3.0/exehda-usm-smartlogger/src/main/java/com/espertech/esperio/socket/EsperSocket.java", str(self.local) + "/esper-4.9.0/cpnm-server/src/main/java/com/espertech/esperio/socket/EsperSocketOld.java")
            esperStatementsFile = open(str(self.local) + "/esper-5.3.0/exehda-usm-smartlogger/src/main/java/com/espertech/esperio/socket/EsperSocket.java", "w")
            esperStatementsFile.writelines(newLines)
            esperStatementsFile.close()
        except Exception, e:
            logging.info('ERRO: Falha ao criar arquivo java para o esper: ', exc_info=True)
        
    def getItemsToEsper(self):
        '''
        Coleta os itens do servidor, e chama o método itemsProperty para formatar
        as propriedades de acordo com a entrada necessária pelo Esper.
        '''
        try:            
            self.itemsLogs = self.managerCommunication.getItems("log")
            while self.itemsLogs == False:
                self.itemsLogs = self.managerCommunication.getItems("log") 
            itemsLogs = self.itemsLogs[:] # copia
            itemsLogList = self.itemsProperty(itemsLogs, "log")
            
            
            self.itemsStatus = self.managerCommunication.getItems("status")
            while self.itemsStatus == False:
                self.itemsStatus = self.managerCommunication.getItems("status")
            itemsStatus = self.itemsStatus[:] # copia
            itemsStatusList = self.itemsProperty(itemsStatus, "status")
            
            
            return itemsLogList + itemsStatusList
        except Exception, e:
            logging.error('ERRO: Falha ao adquirir itens', exc_info=True)
        
                
    def itemsProperty(self, monitoredItems, type_):
        """
        Retorna os itens com o nome da classe e as propriedades a serem repassadas ao Esper.
        """
        try:        
            itemsReturn = []
            while len(monitoredItems) > 0:
                newItem = monitoredItems.pop()
                if type_ == 'log':
                    items = []
                    hostname = self.managerCommunication.getHostname(newItem[len(newItem)-1])
                    eventType = "&!" + str(hostname) + '_' + str(newItem[7]).strip()
                    items.append(eventType)
                    # Remove os espaços do final das colunas (formatcolumn e formatcolumntypedata) caso estas
                    # não estejam em branco    
                    if newItem[4] != None:
                        formatColumn = "&" + str(newItem[4]).strip()
                        items.append(formatColumn)
                    if newItem[6] != None:
                        formatColumnTypeData = "&" + str(newItem[6]).strip()
                        items.append(formatColumnTypeData)
                    itemsReturn.append(items)
                elif type_ == 'status':
                    items = []
                    hostname = self.managerCommunication.getHostname(newItem[len(newItem)-1])
                    eventType = "&!" + str(hostname) + '_' + str(newItem[6]).strip()
                    formatColumnTypeData = "&" + str(newItem[5]).strip() + ",string"
                    items.append(eventType)
                    items.append('&lastvalue,date_coll')
                    items.append(formatColumnTypeData)
                    itemsReturn.append(items)
            return itemsReturn
        except Exception, e:
            logging.error('ERRO: Falha ao selecionar as propriedades dos itens a serem repassadas ao esper', exc_info=True)
    
    def stop(self):
        """
        Finaliza a thread
        """
        self._is_alive = not self._is_alive
