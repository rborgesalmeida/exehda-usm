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

# Assinatura
from Crypto.Hash import MD5
from Crypto import Random

import json
import ast

class ServerFunctions:
    readConf = None
    esperTCP = None
    esperDest = None
    
    def __init__(self):
        """
        Construtor
        """
        try:
            self.readConf = ReadConfFile.__new__(ReadConfFile)
            # Envia logs ao Esper
            self.esperTCP = socket.socket(socket.AF_INET, socket.SOCK_STREAM)            
            self.esperDest = (self.readConf.esperHost, self.readConf.esperPort)    
        except Exception, e:
            logging.error('', exc_info=True)
            
    def getExpressionLogs(self):
        """
        Função utilizada para coletar as expressões de formatação de logs no banco de dados
        """
        try:
            #=====================================================================================#
            # Concatena o nome do cliente (realizando a descriptografia) com "_conf" para fazer 
            # a busca pelas configurações na tabela correta, e monta o SQL
            
            sql = "SELECT name, expression  FROM library_expression ORDER BY id_name" 

            #=====================================================================================#
            
            #=====================================================================================#
            # Executa o SQL e atribui o seu retorno a variável resposta
            dbConnection = DatabaseConnection()
            con = dbConnection.connect() 
            cur = con.cursor()
            cur.execute(sql)
            con.commit()
            confCollect = cur.fetchall()
            
            resposta = confCollect
            
            #=====================================================================================#
        except Exception, e:
            logging.error("ERRO: Falha na leitura das" +
                                    " configurações do cliente no banco de dados: ", exc_info=True)
            resposta = False
        finally:
            cur.close()
            con.close()
            
        return str(resposta)
            
            
    def getMonitoredItems(self, clientName, type_):
        """
        Função usada para capturar as informações do bando de dados, de quais itens serão analisados 
        pelo agente e retorna essas informações para o agente, caso ocorra algum erro, retorna
        False, este retorno deverá ser tratado no agente.
        """
        try:
            #=====================================================================================#           
            if type_ == 'log':
                sql = "SELECT key_, delay, table_, filterprogram, formatcolumn, formatcolumntype,  " \
                    + " formatcolumntypedata, identifier, itemidhosts FROM items_hosts WHERE hostid=(SELECT hostid FROM hosts WHERE host='" \
                    + str(clientName) + "') AND status = 1 AND table_ is not NULL and table_ != '' ORDER BY table_";
            elif type_ == 'status':
                sql = "SELECT key_, delay, status, table_, itemid, formatcolumntypedata, identifier, itemidhosts  FROM items_hosts " \
                    + "WHERE hostid=(SELECT hostid FROM hosts WHERE host='" \
                    + str(clientName) + "') AND status = 1 AND (table_ is NULL or table_ = '') ORDER BY key_";
            elif type_ == 'syslog':
                sql = "SELECT key_, table_, filterprogram, formatcolumn, formatcolumntype, formatcolumntypedata, identifier FROM items_hosts " \
                    + "WHERE hostid=(SELECT hostid FROM hosts WHERE host='" \
                    + str(clientName) + "') AND status = 1 AND table_ is not NULL and delay = -1 " \
                    + "ORDER BY key_";
            #=====================================================================================#

            #=====================================================================================#
            # Executa o SQL e atribui o seu retorno a variável resposta
            dbConnection = DatabaseConnection()
            con = dbConnection.connect() 
            cur = con.cursor()
            cur.execute(sql)
            con.commit()
            confCollect = cur.fetchall()
            
            resposta = confCollect
            #=====================================================================================#
        except Exception, e:
            logging.error("ERRO: Falha na leitura das" +
                                    " configurações do cliente no banco de dados: ", exc_info=True)
            resposta = False
        finally:
            cur.close()
            con.close()
            
        return str(resposta)
    
    def getDiscoveredItems(self, clientName):
        """
        Função utilizada para coletar o itens de descoberta que serão enviados para o agente que
        irá identificar as variáveis e solicitar ao servidor a criação dos novos itens
        """
        try:
            #=====================================================================================#
            # Concatena o nome do cliente (realizando a descriptografia) com "_conf" para fazer 
            # a busca pelas configurações na tabela correta, e monta o SQL
            
            sql = "SELECT key_, itemid, name, identifier  FROM items_hosts " \
                    + "WHERE hostid=(SELECT hostid FROM hosts WHERE host='" \
                    + str(clientName) + "') AND status = 2";

            #=====================================================================================#
            
            #=====================================================================================#
            # Executa o SQL e atribui o seu retorno a variável resposta
            dbConnection = DatabaseConnection()
            con = dbConnection.connect() 
            cur = con.cursor()
            cur.execute(sql)
            con.commit()
            confCollect = cur.fetchall()
            
            resposta = confCollect
            
            #=====================================================================================#
        except Exception, e:
            logging.error("ERRO: Falha na leitura das" +
                                    " configurações do cliente no banco de dados: ", exc_info=True)
            resposta = False
        finally:
            cur.close()
            con.close()
            
        return str(resposta)
    
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

    def updateStatus (self, identifierHostnameEncrypted, itemidEncrypted, columnEncrypted, dataEncrypted):
        """
        Atualiza os dados recebidos do agente por parâmetro na tabela items_hosts (referente
        aos itens monitorados para cada host) e os insere na tabela de histórico
        """
        try:
            #=====================================================================================#
            # Descriptografa os parâmetros passados
            itemid = str(itemidEncrypted)
            data = eval(str(dataEncrypted))
            column = eval(str(columnEncrypted))
            identifierHostname = str(identifierHostnameEncrypted)
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
            #=====================================================================================#
            
        except Exception, e:
                logging.error("ERRO: Falha na análise dos dados recebidos: ", exc_info=True)
#                logging.error('Colunas: ' + column + 'Dados: ' + data + 
#                                       "ItemID: " + itemid, '')
                return False
        
    def insertDiscoveredItems (self, itemid, keyListNew):
        """
        Insere os novos itens a serem monitorados, criados pelo agente, a partir dos itens de
        descoberta
        """
        try:            
            #=====================================================================================#
            # Montando SQL para verificar quais itens já existem e quais precisam ser criados
            sql = "SELECT name, key_, identifier FROM items_hosts WHERE itemidhosts='" + str(itemid) + "'"
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
                cur.execute(sql)
                con.commit()
                keyList = cur.fetchall()
            except Exception, e:
                logging.error("ERRO: Falha ao selecionar dados do banco: ", exc_info=True)
                logging.error("Consulta SQL com erro: " + sql)
            finally:
                cur.close()
                con.close()
            #=====================================================================================#            
            iItem = 0
            iNewItem = 0
            toRemoveKeyList = []
            toRemoveKeyListNew = []
            while len(keyList) > iItem:
                while len(keyListNew) > iNewItem:
                    if str(keyList[iItem][1]) == str(keyListNew[iNewItem][1]):
                        toRemoveKeyList.append(iItem)
                        toRemoveKeyListNew.append(iNewItem)
                    iNewItem = iNewItem + 1
                iNewItem = 0
                iItem = iItem + 1
            
            # Oderna os indices a serem removidos em ordem descrescente para não dar erro de index out of range
            toRemoveKeyList.sort()
            toRemoveKeyList.reverse()
            toRemoveKeyListNew.sort()
            toRemoveKeyListNew.reverse()
           
            # Atualiza a lista dos itens a serem removidos
            for remove in toRemoveKeyList:
                keyList.pop(remove)
                
            # Atualiza a lista dos itens a serem criados
	    if len(toRemoveKeyListNew) > 0:
                for newKey in toRemoveKeyListNew:
                    keyListNew.pop(newKey)
                                     
            #=====================================================================================#
                    
            # Cria a variável resposta, que é utilizada para informar se um novo item foi criado,
            # caso seja criado novo item, o agente deverá atualizar a lista de itens analisados
            itemsModified = False            
            
            # Avalia se sobrou algum item a ser criado (que ainda não existia) e o cria
            while len(keyListNew) > 0:
                newKey = keyListNew.pop()
                if self.createNewItem(itemid, newKey[0], newKey[1], newKey[2], newKey[3]) == True:
                    itemsModified = True
            
            # Avalia se existe algum item que não deve ser mais monitorado
            while len(keyList) > 0:
                if self.removeItem(itemid, keyList.pop()[1]) == True:
                    itemsModified = True
            
            return itemsModified
            #=====================================================================================#
        except Exception, e:
                logging.error("ERRO: Falha na análise dos dados recebidos: ", exc_info=True)
                logging.error('ItemID: ' + str(itemid) + ' KeyList: ' + str(keyList))
                return False
            
    def createNewSituations(self, itemIDDiscovery, itemIDNew, hostid, valueDiscovered):
        '''
        Verifica se há situações associadas com o item, caso exista, cria
        as novas situações a serem detectadas substituindo o identificador
        na consulta epl        
        '''        
        try:
            #=====================================================================================#
            # Coleta as informações que serão necessárias para criar o novo item.
            sqlSelect = "SELECT * FROM situations_hosts WHERE situationid in (SELECT situationid FROM \
            items_situations_hosts WHERE itemid = '" + itemIDDiscovery + "')"
            #=====================================================================================#
            # Realiza a conexão com o banco de dados
            dbConnection = DatabaseConnection()
            con = dbConnection.connect() 
            cur = con.cursor()
            #=====================================================================================#
            # Executa o SQL criado, atribui a variável valuesNewItem as informações para criar o
            # novo item
            cur.execute(sqlSelect)
            con.commit()
            valuesToNewSituation = cur.fetchall()

            #=====================================================================================#
            
            #=====================================================================================#
            # Substitui possíveis variáveis, caso não exista a variável, o valor não é alterado
            for newSituation in valuesToNewSituation:
                newEPL = str(newSituation[1]).replace('$IFACE', valueDiscovered)
                newDescription = str(newSituation[0]).replace('$IFACE', valueDiscovered)
                newCommand = str(newSituation[3]).replace('$IFACE', valueDiscovered)
                
                newEPL = str(newSituation[1]).replace('$PARTITION', valueDiscovered)
                newDescription = str(newSituation[0]).replace('$PARTITION', valueDiscovered)
                newCommand = str(newSituation[3]).replace('$PARTITION', valueDiscovered)
                    
                sqlInsert = "INSERT INTO situations_hosts (description, epl, command, commandtype, \
                severity, comments, to_, subject, body, situationhostsid, occurrences) SELECT '" + \
                str(newDescription) + "', '" + str(newEPL) + "', \
                '" + str(newCommand) + "', '" + str(newSituation[4]) + "', '" + \
                str(newSituation[10]) + "', '" + str(newSituation[5]) + "', '" + \
                str(newSituation[7]) + "', '" + str(newSituation[8]) + "', '" + \
                str(newSituation[9]) + "', '" + str(newSituation[10]) + "', '" + \
                str(newSituation[11]) + "' WHERE \
                NOT EXISTS (SELECT epl FROM situations_hosts WHERE epl = '" + str(newEPL) + "')" 
                                
                #=====================================================================================#
                # Executa o SQL criado, atribui a variável resposta o sucesso da execução (True ou 
                # False), e a retorna a função insertDiscoverdItems
                cur.execute(sqlInsert)
                con.commit()
                
                sqlSelectSituationID = "SELECT situationid FROM situations_hosts WHERE epl='" + str(newEPL) + "'"
                cur.execute(sqlSelectSituationID)
                con.commit()
                situationIDNew = cur.fetchall()
                
                sqlInsertRelation = "INSERT INTO items_situations_hosts (itemid, situationid, hostid, \
                status, correlation) SELECT '" + str(itemIDNew) + "', '" +  str(situationIDNew[0][0]) + "', '" + \
                str(hostid) + "', '" + str('1') + "', '" + str(1) + "' WHERE NOT EXISTS (SELECT itemid, situationid FROM \
                items_situations_hosts WHERE itemid = '" + str(itemIDNew) + "' and situationid = '" + \
                str(situationIDNew[0][0]) + "')"
                
                cur.execute(sqlInsertRelation)
                con.commit()
            
            return True                           
        except Exception, e:
            logging.error("ERRO: Falha ao inserir nova situação: ", exc_info=True)
            return False
        finally:
            cur.close()
            con.close()            
     
    def createNewItem(self, itemid, name, key, identifier, valueDiscovered):
        """
        Cria os novos itens a serem analisados pelo agente
        """
        try:
            #=====================================================================================#
            # Coleta as informações que serão necessárias para criar o novo item.
            sqlSelect = "SELECT hostid, delay, table_, filterprogram, formatcolumn, formatcolumntype, \
            formatcolumntypedata, formatcolumnname, formatcolumnvisible FROM items_hosts WHERE \
            itemid='" + itemid + "'"
            #=====================================================================================#
            # Realiza a conexão com o banco de dados
            dbConnection = DatabaseConnection()
            con = dbConnection.connect() 
            cur = con.cursor()
            #=====================================================================================#
            # Executa o SQL criado, atribui a variável valuesNewItem as informações para criar o
            # novo item
            cur.execute(sqlSelect)
            con.commit()
            valuesToNewItem = cur.fetchall()            
            #=====================================================================================#
            valuesToNewItem = [('' if x is None else str(x)) for x in valuesToNewItem[0]]
            #=====================================================================================#
            # Insere o novo item
            sqlInsert = "INSERT INTO items_hosts (hostid, name, key_, delay, status, itemidhosts, table_, \
            filterprogram, formatcolumn, formatcolumntype, formatcolumntypedata, formatcolumnname, \
            formatcolumnvisible, identifier) VALUES ('" + str(valuesToNewItem[0]) + "', '" + str(name) + "', \
            '" + key + "', '" + str(valuesToNewItem[1]) + "', '1', '" + itemid + "', '" + \
            str(valuesToNewItem[2]) + "', '" + str(valuesToNewItem[3]) + "', '" + \
            str(valuesToNewItem[4]) + "', '" + str(valuesToNewItem[5]) + "', '" + \
            str(valuesToNewItem[6]) + "', '" + str(valuesToNewItem[7]) + "', '" + \
            str(valuesToNewItem[8]) + "', '" + identifier + "')"                    
            #=====================================================================================#
            # Executa o SQL criado, atribui a variável resposta o sucesso da execução (True ou 
            # False), e a retorna a função insertDiscoverdItems
            cur.execute(sqlInsert)
            con.commit()
            resposta = True
            
            sqlSelectItemID = "SELECT itemid FROM items_hosts WHERE key_='" + key + "'"
            cur.execute(sqlSelectItemID)
            con.commit()
            itemIDNew = cur.fetchall()            
                
            resposta = self.createNewSituations(itemid, itemIDNew[0][0], valuesToNewItem[0], valueDiscovered)
                
            return resposta
        except Exception, e:
            logging.error("ERRO: Falha ao inserir novo item: ", exc_info=True)
            logging.error('ItemID: ' + itemid + ', Chave: ' + key)
            return False
        
    def removeItem(self, itemid, key):
        """
        Remove os itens existentes que não deverão mais ser monitorados.
        """
        try:
            #=====================================================================================#
            # Seleciona o itemid dos itens a serem removidos 
            sqlSelect = "SELECT itemid FROM items_hosts WHERE itemidhosts='" + str(itemid) + "' AND key_='" + \
                    str(key) + "'"
            #=====================================================================================#
            # Realiza a conexão com o banco de dados
            dbConnection = DatabaseConnection()
            con = dbConnection.connect() 
            cur = con.cursor()
            #=====================================================================================#
            
            #=====================================================================================#
            # Executa o SQL criado, atribui a variável resposta o sucesso da execução (True ou 
            # False), e a retorna para o agente tratar
            cur.execute(sqlSelect)
            con.commit()
            itemids = cur.fetchall()
            
            for itemidremove in itemids:
                #=================================================================================#
                # Remover os itens que não devem ser mais monitorados
                sqlDelItem = "DELETE FROM items_hosts WHERE itemid='" + str(itemidremove[0]) + "'"
                cur.execute(sqlDelItem)
                con.commit()
                #=================================================================================#
                
                #=================================================================================#
                sqlDelSituation = "DELETE FROM items_situations_hosts WHERE itemid='" + \
                                    str(itemidremove[0]) + "'"
                cur.execute(sqlDelSituation)
                con.commit()            
                #=================================================================================#
            resposta = True
                
            return resposta
            #=====================================================================================#
        except Exception, e:
            logging.error("ERRO: Falha ao excluir dados do banco: ", exc_info=True)
            logging.error('ItemID: ' + str(itemid) + ', Chave: ' + str(key))
            return False
        finally:
            cur.close()
            con.close()
                  
    def getSituations(self, clientName):
        '''
        Coleta as situações de acordo com o nome do cliente.
        '''
        try:
            #=====================================================================================#
            # Montando SQL para remover os itens que não devem ser mais monitorados
	    sqlSituations = "SELECT situations_hosts.situationid, description, epl, comments, command, commandtype, to_, \
            subject, body, severity, identifier, formatcolumntypedata, formatcolumn, criticality, occurrences FROM \
            situations_hosts INNER JOIN items_situations_hosts on situations_hosts.situationid=items_situations_hosts.situationid \
	INNER JOIN items_hosts on items_situations_hosts.itemid = items_hosts.itemid and items_situations_hosts.hostid = items_hosts.hostid \
	INNER JOIN hosts on items_situations_hosts.hostid = hosts.hostid \
      WHERE items_situations_hosts.status=1 and items_situations_hosts.hostid=(SELECT hostid FROM hosts WHERE host='" + str(clientName) +  "');"
            
            #=====================================================================================#
            # Realiza a conexão com o banco de dados
            dbConnection = DatabaseConnection()
            con = dbConnection.connect() 
            cur = con.cursor()
            #=====================================================================================#
            
            #=====================================================================================#
            # Executa o SQL criado, atribui a variável resposta o sucesso da execução (True ou 
            # False), e a retorna para o agente tratar
            
            cur.execute(sqlSituations)
            con.commit()
            confCollect = cur.fetchall()
            
            resposta = confCollect
            #=====================================================================================#
        except Exception, e:
                logging.error("ERRO: Falha ao selecionar situações: ", exc_info=True)
                logging.error("Consulta SQL com erro: " + sqlSituations)
                return False
        finally:
                cur.close()
                con.close()
                return str(resposta)
            
    def getHostOptions(self, clientName):
        '''
        Coleta as opções de acordo no o nome do cliente/
        '''
        try:
            #=====================================================================================#
            # Montando SQL para remover os itens que não devem ser mais monitorados
            sqlOptions = "SELECT correlation FROM hosts WHERE host='" + str(clientName) + "'"
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
            
            cur.execute(sqlOptions)
            con.commit()
            confCollect = cur.fetchall()
            resposta = confCollect
            #=====================================================================================#
        except Exception, e:
                logging.error("ERRO: Falha ao coletar as opções do host: ", exc_info=True)
                logging.error("Consulta SQL com erro: " + sqlOptions)
                return False
        finally:
                cur.close()
                con.close()
                return str(resposta)
            
    def connectEsper(self):
        try:
            self.esperTCP.connect(self.esperDest)
            return True
        except Exception:
            return False
        
