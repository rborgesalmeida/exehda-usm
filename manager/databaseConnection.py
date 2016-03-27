# -*- coding: utf-8 -*-

# Autores: Ricardo Almeida, Roger Machado

# Driver para conexão com o postgresql
import psycopg2

from readConfFile import ReadConfFile
from time import sleep
from datetime import datetime
import logging

# Função para conexão ao banco de dados postgresql

class DatabaseConnection:
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
            logging.error('Falha ao instanciar conexão com banco de dados relacional', exc_info=True)
           
    def connect (self):   
        """
        Função usada para criar uma conexão com o banco de dados.
        A função fica executando até conseguir criar uma conexão,
        quando consegue retorna essa conexão para ser usada
        """
        numberOfTry = 0
        while True:
            try:
                conecta=psycopg2.connect("dbname='%s' user='%s' host='%s' password='%s'" 
                                         % (self.readConf.dbRName, self.readConf.dbRUser,
                                            self.readConf.dbRServer, self.readConf.dbRPass))
                if numberOfTry != 0:
                    logging.info("Sucesso: Conexão reestabelecida.");
                return conecta
            except Exception, e:
                logging.error('Falha ao conectar com o banco de dados relacional', exc_info=True)
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
        
    def verifyCorrelation(self):
        '''
        Verifica se a correlação deve estar ativa no servidor
        '''
        try:
            #=====================================================================================#
            # Verificar se existe host com correlacao=2 (cliente e servidor) ou 3 (servidor) 
            sqlOptions = "SELECT situationid, description, epl, comments, command, commandtype, to_, \
                        subject, body, severity, identifier, formatcolumntypedata, formatcolumn, \
                        hostid FROM (SELECT * FROM (SELECT * FROM situations_hosts join \
                        items_situations_hosts USING (situationid) WHERE epl NOT LIKE '%$%') as situations \
                        join items_hosts using (itemid, hostid) WHERE situationid in (SELECT situationid FROM \
                        items_situations_hosts WHERE hostid in (SELECT hostid FROM hosts WHERE \
                        correlation=2 or correlation=3) and status=1 and correlation=2)) as situations_table"
            #=====================================================================================#
            
            #=====================================================================================#
            # Realiza a conexão com o banco de dados
            con = self.connect() 
            cur = con.cursor()
            #=====================================================================================#
            
            #=====================================================================================#
            # Executa o SQL criado, atribui a variável resposta o sucesso da execução (True ou 
            # False), e a retorna para o agente tratar
            
            cur.execute(sqlOptions)
            con.commit()
            confCollect = cur.fetchall()
            if len(confCollect) > 0:
                return True
            else:
                return False
            #=====================================================================================#
        except Exception, e:
                logging.error("ERRO: Falha ao coletar as opções do host: ", exc_info=True)
                logging.error("Consulta SQL com erro: %s", sqlOptions)
                return False
        finally:
                cur.close()
                
    def getItems(self, type_):
        try:
            if type_ == 'log':
                sql = "SELECT key_, delay, table_, filterprogram, formatcolumn, formatcolumntype, \
                     formatcolumntypedata, identifier, itemidhosts, hostid FROM items_hosts WHERE hostid in \
                    (SELECT hostid FROM hosts WHERE (correlation=2 or correlation=3)) AND status = 1 \
                    AND table_ is not NULL and table_ != '' and delay > 0 ORDER BY table_";
            elif type_ == 'status':
                sql = "SELECT key_, delay, status, table_, itemid, formatcolumntypedata, \
                       identifier, itemidhosts, hostid  FROM items_hosts WHERE hostid in (SELECT \
                       hostid FROM hosts WHERE (correlation=2 or correlation=3)) AND \
                       status = 1 AND table_ is NULL or table_ = '' ORDER BY key_";
            elif type_ == 'syslog':
                sql = "SELECT key_, table_, filterprogram, formatcolumn, formatcolumntype, \
                       formatcolumntypedata, identifier, hostid FROM items_hosts WHERE hostid in \
                       (SELECT hostid FROM hosts WHERE (correlation=2 OR correlation=3)) \
                       AND status = 1 AND table_ is not NULL and delay = -1 ORDER BY key_";
            #=====================================================================================#

            #=====================================================================================#
            # Executa o SQL e atribui o seu retorno a variável resposta
            con = self.connect() 
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
            
        return resposta
        
    def getSituations(self):
        '''
        Coleta as situações a serem identificadas no servidor.
        '''
        try:
            #=====================================================================================#
            # Montando SQL para selecionar as situações que devem ser detectadas no servidor
            sqlSituations = "SELECT situationid, description, epl, comments, command, commandtype, to_, \
                            subject, body, severity, identifier, formatcolumntypedata, formatcolumn, \
                            hostid FROM (SELECT * FROM (SELECT * FROM situations_hosts join \
                            items_situations_hosts USING (situationid) WHERE epl NOT LIKE '%$%') as situations \
                            join items_hosts using (itemid, hostid) WHERE situationid in (SELECT situationid FROM \
                            items_situations_hosts WHERE hostid in (SELECT hostid FROM hosts WHERE \
                            correlation=2 or correlation=3) and status=1 and correlation=2)) as situations_table"
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
            
            cur.execute(sqlSituations)
            con.commit()
            resposta = cur.fetchall()
            
            #=====================================================================================#
        except Exception, e:
                logging.error("ERRO: Falha ao selecionar situações: ", exc_info=True)
                logging.error("Consulta SQL com erro: %s", sqlSituations)
                return False
        finally:
                cur.close()
                con.close()
                return list(resposta)
    
    def insertSituations(self, hostname, formatTable, data):
        """
        Função usada para receber os logs analisados e inseri-los em suas respectivas tabelas,
        caso ocorra algum erro, retorna False, este retorno deverá ser tratado no agente.
        """
        try:
            #=====================================================================================#
            table = str(hostname + '_active_situations')                                                        
            #=====================================================================================#
            # Monta as colunas, e posteriormente os dados, para criar a sintaxe do SQL e realizar
            # a inserção, adicionando ao final a data de publicação
            i = 0
            column = ""
            while (i <= len(formatTable) - 1):
                column = column + str(formatTable[i]) + ","
                if formatTable[i] == 'situationid':
                    situationID = data[i]
                if formatTable[i] == 'description':   
                    description = data[i]
                if formatTable[i] == 'events':
                    startDate = self.findFirstDateColl(str(data[i]))
                    endDate = self.findLastDateColl(str(data[i]))
                i = i + 1;
            column = column + str('date_pub')
            
            #=====================================================================================#    
            # Monta os dados
            date_pub = datetime.now()
            i = 0
            dados = "'"
            while (i <= len(data) - 1):
                dados = dados + str(data[i]) + "','"
                i = i + 1;
            dados = dados + str(date_pub) + "'"
            #=====================================================================================#
            # Montando SQL
            sql = "SELECT events, occurrences, commandresult FROM " + str(table) + " WHERE situationid = " + \
                str(situationID) + " and description = '" + str(description) + "'"
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
                eventOccurrences = cur.fetchall()
                                
                if len(eventOccurrences) == 0:
                    # É a primeira vez que a situação será inserida, logo deve-se identificar nos eventos
                    # o primeiro date_coll e o último para atualizar a data inicial e final da situação
                    column = column + ",startdate, enddate"
                    dados = dados + ",'" + str(startDate) + "', '" + str(endDate) + "'"
                    sql = "INSERT INTO " + '"' + str(table) + '"' + "(" + str(column) + ") VALUES (" \
                        + str(dados) + ")"
                                                            
                else:
                    # Como já possui eventos, para situacao encontrada, a data inicial não deve ser 
                    # modificada, e a data final deve ser modificada para a data do último evento
                    # logo deve-se procurar por date_coll ou datecoll de trás para frente
                    
                    i = 0
                    updatedColumns = ''
                    while (i < len(data)):
                        if str(formatTable[i]) == 'events':
                            data[i] = str(data[i]) + '|' + str(eventOccurrences[0][0])
                        if str(formatTable[i]) == 'occurrences':
                            data[i] = eventOccurrences[0][1]     + 1
                        if str(formatTable[i]) == 'commandresult':
                            data[i] = str(data[i]) + '|' + str(eventOccurrences[0][2])
                        updatedColumns = updatedColumns + str(formatTable[i]) + "='" + str(data[i]) + "', "
                        i = i + 1
                    updatedColumns = updatedColumns + "date_pub='" + str(date_pub) + "',\
                                     endDate='" + str(endDate) + "'"
                                                        
                    sql = "UPDATE " +str(table) + " SET " + str(updatedColumns) + " WHERE situationid = " + \
                str(situationID) + " and description = '" + str(description) + "'"
                
                cur.execute(sql)
                con.commit()
                
                resposta = True    
            except Exception, e:
                logging.error("ERRO: Falha ao inserir dados no banco", exc_info=True)
                logging.error("Consulta SQL com erro: %s", sql)
                resposta = False
            finally:
                cur.close()
                con.close()
            
            return resposta
            #=====================================================================================#
        except Exception, e:
                logging.error("ERRO: Falha na análise dos dados recebidos: ", exc_info=True)
                logging.error('Dados: ' + str(data) + 'Formato: ' + str(formatTable) + 
                                       "Tabela: " + str(table))
                return False
            
    def removeSituations(self, hostname, situationid, commentsHistory):
        '''
        Move a situação identificada por seu ID para a tabela history_situations
        adicionando os comentários passados por parâmetro.
        '''
        try:
            clientName = str(hostname)
            #=====================================================================================#
            # Montando SQL para remover as situações que não são mais situações de risco
            sqlSituation = "SELECT * FROM " + str(clientName) + "_active_situations WHERE \
                            situationid=" + str(situationID)
            # e identifier = identifier
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
            
            cur.execute(sqlSituation)
            con.commit()
            situation = cur.fetchall()
            
            if len(situation) == 1:
                cur.execute("INSERT INTO history_situations (description, events, situationid, \
                date_pub, occurrences, comments, comments_history, severity, commandresult, startdate, \
                enddate) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)", (situation[0][0],
                situation[0][1], situation[0][2], situation[0][4], situation[0][5],
                situation[0][6], commentsHistory, situation[0][7], situation[0][8],
                situation[0][9], situation[0][10]))
                
                con.commit()
                
                sqlDelActiveSituation = "DELETE FROM " + str(clientName) + "_active_situations WHERE \
                                        situationid=" + str(situationID)
                                        
                
                                                        
                cur.execute(sqlDelActiveSituation)
                con.commit()
            #=====================================================================================#            
        except Exception, e:
                logging.error("ERRO: Falha ao remover situação: ", exc_info=True)
                logging.error("Consulta SQL com erro: %s", sqlSituation)
        finally:
                cur.close()
                con.close()
                return True
    
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

            
    def getHostname(self, hostid):
        '''
        Retorna o hostname associado ao hostid passado por parâmetro.
        '''
        try:
            #=====================================================================================#
            # Montando SQL para selecionar as situações que devem ser detectadas no servidor
            sqlHostname = "SELECT host FROM hosts WHERE hostid=" + str(hostid) + ";"
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
            
            cur.execute(sqlHostname)
            con.commit()
            resposta = cur.fetchall()
            #=====================================================================================#
        except Exception, e:
                logging.error("ERRO: Falha ao selecionar o hostname: ", exc_info=True)
                logging.error("Consulta SQL com erro: " + sqlHostname)
                return False
        finally:
                cur.close()
                con.close()
                return str(resposta[0][0])
        
