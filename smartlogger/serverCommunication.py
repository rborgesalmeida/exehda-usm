# -*- coding: utf-8 -*-

# Autores: Ricardo Almeida, Roger Machado

import xmlrpclib
from datetime import datetime
import time
import psutil
import socket
import os
import logging
from readConfFile import ReadConfFile

class ServerCommunication:
    """
    Classe usada para para realizar a comunicação com o servidor.
    """
    serverAddress = None
    clientName= None
    tcp = None
    dest = None
    sendMail = None
    readConf = None
    #serverConnection = None


    def __init__(self, serverAddress, portEsperSend):
        """
        Método de inicialização da classe, recebe por parâmetro a lista de ips, a lista de portas
        formato da coluna da tabela, o tabela onde vai ser inserido,o arquivo de relátorio,
        e o log que vai ser inserido 
        """
        self.readConf = ReadConfFile.__new__(ReadConfFile)
        self.clientName = self.readConf.clientName
        self.serverAddress = serverAddress
        self.sendMail = self.readConf.sendMail
	#self.serverConnection = xmlrpclib.ServerProxy(self.serverAddress)
        
        try:
            # Envia logs ao Esper
            host = '127.0.0.1'     # Endereco IP do esper
            port = portEsperSend   # Porta que o esper esta
            self.tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.dest = (host, port)
        except Exception, e:
            logging.error('Falha ao criar o serverCommunication', exc_info=True)
            
    # Funcao usada para enviar os status analisados para o servidor, se tentar sem sucesso enviar
    # 3 status envia um email com sinal de alerta para o responsável pelo servidor para 
    # avisar que não está sendo possível enviar os status, se as tentativas chegarem a 10 
    # envia outro email com sinal de urgente, cada vez que um status nao pode ser enviado ele 
    # eh armazenado na lista de nao enviados, para ser enviados na proxima tentativa de enviar 
    # algum log para o servidor 
    def sendStatus(self, identifier, itemID, formatColumn, data):
        """
        Funcao usada para enviar os monitoredItemKey analisados para o servidor, se tentar sem sucesso enviar
        3 monitoredItemKey envia um email com sinal de alerta para o responsável pelo servidor para 
        avisar que não está sendo possível enviar os monitoredItemKey, se as tentativas chegarem a 10 
        envia outro email com sinal de urgente
        """  
                        
        try:
            if self.readConf.correlation == 1 or self.readConf.correlation == 3:
                statusEvent = "stream="+str(identifier) + ","
                i = 0
                while(i<len(formatColumn)):
                    if formatColumn[i] == 'datecoll':                 
                        statusEvent=statusEvent+str('date_coll')+"="+str(data[i])+","
                    elif formatColumn[i] == 'lastvalue':
                        statusEvent=statusEvent+str(formatColumn[i])+"="+str(data[i])+","
                    i = i+1                    
                statusEvent=statusEvent[0:len(statusEvent)-1]+os.linesep
                self.tcp.send(statusEvent)
                
        except Exception, e:
            logging.error("Falha ao enviar dados ao esper", exc_info=True)
           
        try:

            identifierHostnameEncrypted = str(self.clientName + '_' + identifier)
            itemIDEncrypted = str(itemID)
            formatColumnEncrypted = str(formatColumn)
            dataEncrypted = str(data)
            # Conexão com servidor
            serverConnection = xmlrpclib.Server(self.serverAddress)
            ## envia os arquivos de monitoredItemKey para o servidor de contexto
            resp = serverConnection.updateStatus(xmlrpclib.Binary(identifierHostnameEncrypted), 
                                 xmlrpclib.Binary(itemIDEncrypted), 
                                 xmlrpclib.Binary(formatColumnEncrypted) , 
                                 xmlrpclib.Binary(dataEncrypted)) 
            if resp == True:
                logging.debug('Status atualizados com sucesso')
            else:
                logging.error('Falha ao atualizar o status: %s', resp)
                
        # armazena o monitoredItemKey que nao foi enviado na lista de nao enviados e verifica quantos monitoredItemKey
        # nao conseguiram ser enviados a fim de enviar email caso necessario   
        except Exception, e:
            # Controle para escrever no log somente a primeira vez que não conseguir enviar os
            # dados ao servidor
            logging.error("Falha ao atualizar o status", exc_info=True)

            
    # Funcao usada para enviar os logs analisados para o servidor, se tentar sem sucesso enviar
    # 3 logs envia um email com sinal de alerta para o responsável pelo servidor para 
    # avisar que não está sendo possível enviar os logs, se as tentativas chegarem a 10 
    # envia outro email com sinal de urgente, cada vez que um log nao pode ser enviado ele 
    # eh armazenado na lista de nao enviados, para ser enviados na proxima tentativa de enviar 
    # algum log para o servidor 
    def sendLog(self, identifier, table, formatColumn, data):
        """
        Funcao usada para enviar os logs analisados para o servidor, se tentar sem sucesso enviar
        3 logs envia um email com sinal de alerta para o responsável pelo servidor para 
        avisar que não está sendo possível enviar os logs, se as tentativas chegarem a 10 
        envia outro email com sinal de urgente
        """
        # Envia eventos ao esper 
        try:
	    # formatColumn possui o nome das propriedades do evento
	    # data possui os valores associados as propriedades
            if self.readConf.correlation == 1 or self.readConf.correlation == 3:
                logEvent = "stream="+str(identifier)+","
                i = 0
                while(i<len(formatColumn)):
                    if formatColumn[i] == 'date_coll':                
                        logEvent=logEvent+str(formatColumn[i])+"="+str(data[i])+","
                    else:
                        logEvent=logEvent+str(formatColumn[i])+"="+str(data[i])+","
                    i = i+1
                logEvent=logEvent[0:len(logEvent)-1]+os.linesep
                self.tcp.send(logEvent)
        except Exception, e:
            logging.error("Falha ao enviar eventos ao esper", exc_info=True)
     
        try:
            tableClient = str(self.clientName + '_' + str(table))
            # Conexão com servidor
            serverConnection = xmlrpclib.ServerProxy(self.serverAddress)
            # Envia os arquivos de logs para o servidor
            resp = serverConnection.insertLogs(identifier, 
                                               tableClient, 
                                               formatColumn,
                                               data) 
            #=================================================================================#
            # Verifica se os dados a serem enviados são do CPNM para que não seja gravada
            # a mensagem de sucesso ou falha, evitando que o sistema entre em loop
            if table != 'exehda-usm-collector' and table != 'exehda-usm-manager' and table != 'exehda-usm-smartlogger' :
                if resp == True:
                    logging.debug('Logs inseridos com sucesso na tabela %s', 
                                            str(table))
                else:
                    # Envia para a tabela de exceções pois o retorno diferente de True
                    # não representa erro no servidor
                    logging.error('Falha ao inserir logs na tabela %s: %s',
                                            str(table), str(resp))
                    date = str(datetime.now())
                    newformatColumn = ['date_coll', 'log']
                    newData = []
                    newData.append(date)
                    newData.append(str(data))
                    newTable = str(self.clientName+ '_'+ 'exceptions')
		    serverConnection = xmlrpclib.ServerProxy(self.serverAddress)
                    # OBS.: talvez seja correto chamar o próprio sendLog
                    resp = serverConnection.insertLogs(identifier,
                                                       newTable, 
                                 		       newformatColumn , 
                                 		       newData)
                #=================================================================================#
        # armazena o log que nao foi enviado na lista de nao enviados e verifica quantos logs
        # nao conseguiram ser enviados a fim de enviar email caso necessario   
        except Exception, e:
            #=====================================================================================#
            # Controle para escrever no log somente a primeira vez que não conseguir enviar os
            # dados ao servidor
            logging.error("Falha ao inserir logs", exc_info=True)
            
    def sendSituations(self, table, formatColumn, data):
        """
        Funcao usada para enviar os logs analisados para o servidor, se tentar sem sucesso enviar
        3 logs envia um email com sinal de alerta para o responsável pelo servidor para 
        avisar que não está sendo possível enviar os logs, se as tentativas chegarem a 10 
        envia outro email com sinal de urgente
        """
        try:
            tableClient = str(self.clientName + '_' + str(table))
            # Conexão com servidor
            serverConnection = xmlrpclib.ServerProxy(self.serverAddress)
            # Envia os arquivos de logs para o servidor
            resp = serverConnection.insertSituations(tableClient, 
                                 		     formatColumn,
                                		     data) 
            #=================================================================================#
            # Verifica se os dados a serem enviados são do CPNM para que não seja gravada
            # a mensagem de sucesso ou falha, evitando que o sistema entre em loop
            if table != 'exehda-usm-collector' and table != 'exehda-usm-smartlogger' and table != 'exehda-usm-manager':
                if resp == True:
                    logging.debug('Logs inseridos com sucesso na tabela %s', 
                                           str(table))
                else:
                    # Envia para a tabela de exceções pois o retorno diferente de True
                    # não representa erro no servidor
                    logging.error('Falha ao inserir logs na tabela %s: %s',
                                           str(table), str(resp))
                    date = str(datetime.now())
                    newformatColumn = ['date_coll', 'log']
                    newData = []
                    newData.append(date)
                    newData.append(data)
                    newTable = str(self.clientName+ '_'+ 'exceptions')
                    identifierClient = str(self.clientName + '_Exceptions')
		    serverConnection = xmlrpclib.ServerProxy(self.serverAddress)
                    # OBS.: talvez seja correto chamar o próprio sendLog
                    resp = serverConnection.insertLogs(identifierClient, 
                                                       newTable, 
                                 		       newformatColumn, 
                                 		       newData)
            #=================================================================================#
        # armazena o log que nao foi enviado na lista de nao enviados e verifica quantos logs
        # nao conseguiram ser enviados a fim de enviar email caso necessario   
        except Exception, e:
            #=====================================================================================#
            # Controle para escrever no log somente a primeira vez que não conseguir enviar os
            # dados ao servidor
            logging.error("Falha ao enviar situações ao servidor", exc_info=True)
        
    def getExpression(self):
        """
        Retorna os items que que devem ser monitorados de acordo com o servidor
        previamente passado ao construtor.
        """
        try:
            serverConnection = xmlrpclib.ServerProxy(self.serverAddress)
            expressions = eval(serverConnection.getExpressionLogs())
            # Se não houve erro retorna os itens monitorados
            if expressions != False:
                return expressions        
            else:
                return []
        except Exception, e:
            logging.error('Falha na coleta das expressões de formatação de logs', exc_info=True)
            return False
        
    def getItems(self, type_):
        """
        Retorna os items que que devem ser monitorados de acordo com o servidor
        previamente passado ao construtor.
        """
        try:
            clientNameEncrypted = str(self.clientName)
            typeEncrypted = str(type_)
            serverConnection = xmlrpclib.ServerProxy(self.serverAddress)
            items = eval(serverConnection.getMonitoredItems(
                                            xmlrpclib.Binary(clientNameEncrypted),
                                            xmlrpclib.Binary(typeEncrypted)))
            
            # Se não houve erro retorna os itens monitorados
            if items != False:
                return items        
            else:
                return False
        except Exception, e:
            logging.error('Falha na coleta dos itens', exc_info=True)
            return False
        
    def makeDiscoveredItems(self):
        """
        Método que realiza a descoberta de itens, ou seja, verifica as variáveis
        nos itens do tipo descoberta e envia ao servidor para que ele realize a criação
        dos novos itens
        """
        try:
            clientNameEncrypted = self.clientName
            serverConnection = xmlrpclib.ServerProxy(self.serverAddress)
            # Busca do servidor os itens do tipo descoberta
            discoveredItems = eval(serverConnection.getDiscoveredItems(
                                                    xmlrpclib.Binary(clientNameEncrypted)))
            # Realiza a descoberta para cada item
            while len(discoveredItems) > 0:
                discoveredItem = discoveredItems.pop()
                # StatusInfo: recebe por parâmetro: 
                #     itemid: será utilizado para relação do novo item criado
                #     chave: onde se encontra a variável a ser descoberta
                #     ip e porta do servidor
                # Instancia a classe que realizará a descoberta 
                # 1. É realizada a detecção da variável que deve ser descoberta e gera uma lista 
                # com as novas chaves (já com a variável substituída) criptografada
                monitoredItemKey = str(discoveredItem[0])
                itemName = str(discoveredItem[2])
                identifier = str(discoveredItem[3])
                keyListNewEncrypted = str(self.getDiscoveredKeys(itemName, monitoredItemKey, identifier))
                itemidEncrypted = str(discoveredItem[1])
                # Solicita ao servidor a inserção de um novo item para a nova chave gerada apartir do
                # item de descoberta
                serverConnection.insertDiscoveredItems(xmlrpclib.Binary(itemidEncrypted),
                                                       xmlrpclib.Binary(keyListNewEncrypted))
            #else:
            #    self.getSymKeyFromServer()
        except Exception, e:
            logging.error('Falha na descoberta de itens', exc_info=True)
    
    def getHostOptions(self):
        try:
            clientNameEncrypted = self.clientName
            serverConnection = xmlrpclib.ServerProxy(self.serverAddress)
            # Busca do servidor os itens do tipo descoberta
            hostOptions = eval(serverConnection.getHostOptions(
                                                    xmlrpclib.Binary(clientNameEncrypted)))

            self.readConf.correlation = hostOptions[0][0]
            return True
                
        except Exception, e:
            logging.error('Falha ao coletar as opções do ativo', exc_info=True)
        
    def getSituations(self):
        try:
            clientNameEncrypted = self.clientName
            serverConnection = xmlrpclib.ServerProxy(self.serverAddress)

            situations = eval(serverConnection.getSituations(
                                                    xmlrpclib.Binary(clientNameEncrypted)))
            return situations

        except Exception, e:
            logging.error('Falha ao coletar as situações', exc_info=True)
            return False
            
    def removeSituations(self, identifier, situationID, commentsHistory):
        """
        Retorna os items que que devem ser monitorados de acordo com o servidor
        previamente passado ao construtor.
        """
        try:
            clientNameEncrypted = str(self.clientName)
            situationIDEncrypted = str(situationID)
            commentsHistoryEncrypted = str(commentsHistory)
            serverConnection = xmlrpclib.ServerProxy(self.serverAddress)
            success = serverConnection.removeSituations(
                                            xmlrpclib.Binary(clientNameEncrypted),
                                            xmlrpclib.Binary(situationIDEncrypted),
                                            xmlrpclib.Binary(commentsHistoryEncrypted))
            
            # Se não houve erro retorna os itens monitorados
            if success == True:
                logging.info('Situação voltou ao normal.')
            else:
                logging.error('Falha ao atualizar situação %s', str(resp))
        except Exception, e:
            logging.error('Falha na coleta dos itens', exc_info=True)
            return False
            
    #=============================================================================================#
    # MÉTODOS DE DESCOBERTA     
    def getNetworkInterfaces(self):
        """
        Retorna uma lista com as interfaces de rede
        """
        return psutil.net_io_counters(pernic=True).keys()

    def getDiskPartitions(self):
        """
        Retorna uma lista com os pontos de montagem para todas os dispositivos físicos
        """
        devices = []
        for part in psutil.disk_partitions(all=False):
            devices.append(part[1])
        return devices
            
    def getDiscoveredKeys(self, itemName, monitoredItemKey, identifier):
        """
        Realiza a descoberta de items substituindo no parâmetro itemName a variável
        nele detectada. Exemplo: itemName=network.conf[$IFACE, addr] retornará
        network.conf[eth0, addr]
        """
        # Lista que conterá o nome e a chave para o novo item
        discoveredKey = []
        discoveredKeyList = []

        if '$IFACE' in monitoredItemKey:
            interfaces = self.getNetworkInterfaces()
            while len(interfaces) > 0:
                interface = interfaces.pop()
                if interface != 'lo':
                    discoveredKey.append(itemName.replace('$IFACE', interface))
                    discoveredKey.append(monitoredItemKey.replace('$IFACE', interface))
                    discoveredKey.append(identifier.replace('$IFACE', interface))
                    discoveredKey.append(interface)
                    discoveredKeyList.append(discoveredKey)
                    discoveredKey = []
            
        elif '$PARTITION' in monitoredItemKey:
            partitions = self.getDiskPartitions()
            while len(partitions) > 0:
                partition = partitions.pop()
                discoveredKey.append(itemName.replace('$PARTITION', partition))
                discoveredKey.append(monitoredItemKey.replace('$PARTITION', partition))
                discoveredKey.append(identifier.replace('$PARTITION', partition))
                discoveredKey.append(partition)
                discoveredKeyList.append(discoveredKey)
                discoveredKey = []
        return discoveredKeyList
    #=============================================================================================#
    
    # Metodo que envia os logs que estao na lista de  nao enviados para o servidor, eh feito 10 
    # tentativas de envio para de log para cada servidor, apos essas tentativas vai para o 
    # proximo servidor

    def connectEsper(self):
        try:
            self.tcp.connect(self.dest)
            return 1
        except Exception:
            #logging.debug('Falha na conexão com Esper')
            return 0
