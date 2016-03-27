# -*- coding: utf-8 -*-

# Autores: Ricardo Almeida, Roger Machado

from datetime import datetime
from os import linesep
import socket
import ast
import logging

from readConfFile import ReadConfFile

from databaseConnection import DatabaseConnection
from eventDatabaseConnection import EventDatabaseConnection

from serverCommunication import ServerCommunication

import json
import ast

class ServerFunctions:
    readConf = None
    esperTCP = None
    esperDest = None
    managerCommunication = None
    nexthopCommunication = None
    
    def __init__(self):
        """
        Construtor
        """
        try:
            self.readConf = ReadConfFile.__new__(ReadConfFile)
            # Envia logs ao Esper
            self.esperTCP = socket.socket(socket.AF_INET, socket.SOCK_STREAM)            
            self.esperDest = (self.readConf.esperHost, self.readConf.esperPort)  
            
            if (len(self.readConf.SmartLoggerIP) > 0):
                nexthopIP = self.readConf.SmartLoggerIP
                nexthopPort = self.readConf.SmartLoggerPort
            else:
                nexthopIP = self.readConf.ManagerIP
                nexthopPort = self.readConf.ManagerPort

            managerAddress = str("http://" + str(self.readConf.managerIP[iServer]) + ":" + 
                                    str(self.readConf.managerPort[iServer]))
            self.managerCommunication = ServerCommunication(managerAddress, portEsperSend)


            nexthopAddress = str("http://" + str(nexthopIP[iServer]) + ":" + 
                                    str(nexthopPort[iServer]))
            self.nexthopCommunication = ServerCommunication(nexthopAddress, portEsperSend)

        except Exception, e:
            logging.error('', exc_info=True)
                
    def insertLogs(self, identifierHostname, table, formatTable, data):
        """
        Função usada para receber os logs analisados e inseri-los em suas respectivas tabelas,
        caso ocorra algum erro, retorna False, este retorno deverá ser tratado no agente.
        """     
        # Envia dados ao esper 
        try:
            if self.readConf.correlation:
                logEvent = "stream="+str(identifierHostname)+","
                i = 0
                while(i<len(formatTable)):
                    if formatTable[i] == 'date_coll':                
                        logEvent=logEvent+formatTable[i]+"="+data[i]+","
                    else:
                        logEvent=logEvent+formatTable[i]+"="+data[i]+","
                    i = i+1
                logEvent=logEvent[0:len(logEvent)-1]+linesep
                self.esperTCP.send(logEvent.encode('utf-8'))
        except Exception, e:
            logging.error("ERRO: Falha ao enviar dados ao esper: ", exc_info=True)
        
	try:
            eventDB = EventDatabaseConnection()
            db = eventDB.connect()
            collection = db[table]
            
            i = 0
            document = "{"
            while(i <= len(data) - 1):
		if isinstance(data[i], int):
		    data[i] = int(data[i])	
                    document = document + '"' + str(formatTable[i]) + '": ' + str(data[i]) + ', '
                elif isinstance(data[i], str):
		    data[i] = data[i].encode('utf-8').replace('"', "'")
                    document = document + '"' + str(formatTable[i]) + '": ' + '"' + str(data[i]) + '", '
                i = i + 1
            document = document + '"date_pub": "' + str(datetime.now()) + '"}'
	
            collection.insert(ast.literal_eval(document))
            resposta = True                                  
            
            resp = self.nexthopCommunication.sendLog(identifierHostname, table, formatTable, data) 
            if resp == True:
                logging.debug('Log enviado com sucesso')
            else:
                logging.error('Falha ao enviar log: %s', resp)
            
            return resposta
            #=====================================================================================#
        except Exception, e:
                logging.error("Falha ao inserir logs no banco", exc_info=True)
		logging.error("Identificador: %s, Tabela: %s, Formato da Tabela: %s, Dados: %s",
				str(identifierHostname), str(table), 
				str(formatTable), str(data))
                return False
        
    def insertSituations(self, table, formatTable, data):
        """
        Função usada para receber os logs analisados e inseri-los em suas respectivas tabelas,
        caso ocorra algum erro, retorna False, este retorno deverá ser tratado no agente.
        """
        try:
            situationID = data[2]
            description = data[0]
            startDate = self.findFirstDateColl(str(data[1]))
            endDate = self.findLastDateColl(str(data[1]))
            
            
            eventDB = EventDatabaseConnection()
            db = eventDB.connect()
            collection = db[table]
            
            i = 0
            document = "{"
            while(i <= len(data) - 1):
		if isinstance(data[i], int):
		    data[i] = int(data[i])	
                    document = document + '"' + str(formatTable[i]) + '": ' + str(data[i]) + ', '
                elif isinstance(data[i], str):
		    data[i] = data[i].encode('utf-8').replace('"', "'")
                    document = document + '"' + str(formatTable[i]) + '": ' + '"' + str(data[i]) + '", '
                i = i + 1
            document = document + '"date_pub": "' + str(datetime.now()) + '"}'
	
            collection.insert(ast.literal_eval(document))
            resposta = True   
                               
            
            resp = self.nexthopCommunication.sendSituations(table, formatTable, data) 
            if resp == True:
                logging.debug('Situacao enviada com sucesso')
            else:
                logging.error('Falha ao enviar situacao: %s', resp)
            
            return resposta
            #=====================================================================================#
        except Exception, e:
                logging.error("Falha ao inserir situacoes no banco", exc_info=True)
                return False
            
    def findFirstDateColl (self, events):
        try:
            startDatePos = events.find("date_coll") 
            if startDatePos > 0:
                startDatePos = startDatePos + 10
                return events[startDatePos:startDatePos+26]
            else:
                startDatePos = events.find("datecoll")
                if startDatePos > 0:
                    startDatePos = startDatePos + 9
                    return events[startDatePos:startDatePos+26]
                else:
                    return ''
        except Exception, e:
            logging.error("ERRO: Falha ao identificar a data inicial da situação: ", exc_info=True)
            
    def findLastDateColl (self, events):
        try:
            endDatePos = events.rfind("date_coll") 
            if endDatePos > 0:
                endDatePos = endDatePos + 10
                return events[endDatePos:endDatePos+26]
            else:
                endDatePos = events.rfind("datecoll")
                if endDatePos > 0:
                    endDatePos = endDatePos + 9
                    return events[endDatePos:endDatePos+26]
                else:
                    return ''
        except Exception, e:
            logging.error("ERRO: Falha ao identificar a data final da situação: ", exc_info=True)

    def updateStatus (self, identifierHostname, itemid, column, data):
        """
        Atualiza os dados recebidos do agente por parâmetro na tabela items_hosts (referente
        aos itens monitorados para cada host) e os insere na tabela de histórico
        """
        try:
            #=====================================================================================#
            value = ''
            
            try:
                if self.readConf.correlation:                           
                    statusEvent = "stream="+str(identifierHostname) + ","
                    i = 0
                    while(i<len(column)):
                        if column[i] == 'datecoll':                 
                            statusEvent=statusEvent+str('date_coll')+"="+str(data[i])+","
                        elif column[i] == 'lastvalue':
                            statusEvent=statusEvent+str(column[i])+"="+str(data[i])+","
                        i = i+1                    
                    statusEvent=statusEvent[0:len(statusEvent)-1]+linesep
                    self.esperTCP.send(statusEvent)
        
            except Exception, e:
                logging.error("ERRO: Falha ao enviar dados ao esper: ", exc_info=True)
            
            # Cria a data de publicação
            date_pub = datetime.now()
            
            #=====================================================================================#
            # Monta as colunas com os valores a serem atualizados, para criar a sintaxe do SQL
            # e realizar a atualização, adicionando ao final a data de publicação
            i = 0
            updatedColumns = ''
            errorFound = False
            while (i < len(data)):
                updatedColumns = updatedColumns + str(column[i]) + "='" + str(data[i]) + "', "
                #=================================================================================#
                # Separa a data de coleta e o valor do item, para inserção na tabela de histórico
                # e identifica se ocorreu algum erro ao coletar dado, para que a tabela de
                # histórico não seja atualizada
                if column[i] == "datecoll":
                    datecoll = data[i]
                elif column[i] == "lastvalue":
                    value = data[i]
                elif column[i] == "errmsg" and data[i] != '':
                    errorFound = True
                #=================================================================================#
                i = i + 1;
            updatedColumns = updatedColumns + "datepub='" + str(date_pub) + "'"
            #=====================================================================================#
            
            #=====================================================================================#
            # Montando SQL para atualização
            sqlUpdate = "UPDATE items_hosts SET " + str(updatedColumns) + " WHERE itemid=" + \
                        str(itemid)
            #=====================================================================================#
            #=====================================================================================#
            # Realiza a conexão com o banco de dados
            dbConnection = DatabaseConnection()
            con = dbConnection.connect() 
            cur = con.cursor()
            #=====================================================================================#
            
            #=====================================================================================#
            # Executa o SQL criado, atribui a variável resposta o sucesso da execução (True ou 
            # False), e a retorna para o agente tratar
            try:
                cur.execute(sqlUpdate)
                con.commit()
                respostaUpdate = True    
            except Exception, e:
                logging.error("ERRO: Falha ao atualizar dados no banco: ", exc_info=True)
                logging.error("Consulta SQL com erro: " + sqlUpdate)
                respostaUpdate = False
            finally:
                cur.close()
                con.close()
            #=====================================================================================#
            
            respostaHistory = True
            #=====================================================================================#
            # Insere na tabela history somente se não ocorreu erro na coleta do dado pelo agente
            # (quando isso ocorre, o campo errmsg da tabela items_hosts deverá ser populado com
            # uma mensagem de erro, passada do agente para o servidor)
            if errorFound == False:
                sqlHistory = "INSERT INTO history (itemid, datecoll, value) VALUES ('" + str(itemid) \
                        + "', '" + str(datecoll) + "', '" + str(value) + "')"
                #=================================================================================#
                # Realiza a conexão com o banco de dados
                dbConnection = DatabaseConnection()
                con = dbConnection.connect() 
                cur = con.cursor()
                #=================================================================================#
                
                #=================================================================================#
                # Executa o SQL criado, atribui a variável respostaHistory o sucesso da execução
                # (True ou False)
                try:
                    cur.execute(sqlHistory)
                    con.commit()
                    respostaHistory = True    
                except Exception, e:
                    logging.error("ERRO: Falha ao inserir dados no banco: ", exc_info=True)
                    logging.error("Consulta SQL com erro: " + sqlHistory)
                    respostaHistory = False
                finally:
                    cur.close()
                    con.close()
            #=====================================================================================#
            
            #=====================================================================================#
            # Verifica se a execução das duas query SQL foram realizadas com sucesso e retorna
            # o resultado total para o agente
            if respostaHistory == True & respostaUpdate == True:
                return True
            else:
                return False
            
            resp = self.nexthopCommunication.sendStatus(identifierHostname, itemid, column, data) 
            if resp == True:
                logging.debug('Status enviado com sucesso')
            else:
                logging.error('Falha ao enviar o status: %s', resp)
            #=====================================================================================#
            
        except Exception, e:
                logging.error("ERRO: Falha na análise dos dados recebidos: ", exc_info=True)
                return False
                    
    def connectEsper(self):
        try:
            self.esperTCP.connect(self.esperDest)
            return True
        except Exception:
            return False
        
