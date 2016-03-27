# -*- coding: utf-8 -*-

# Autores: Ricardo Almeida, Roger Machado

from pyparsing import *
import time
from threading import Thread
import re
import socket

from formatLog import FormatLog

class SyslogServer(Thread):
    """
    Classe que lê os logs dos seus respectivos arquivos, e chama os métodos apropriados 
    para fazerem seu tratamento 
    """
    clientName = None
    serverCommunication = None
    formatLogDict = None
    interrupt = None
    fileExpression = None
    conn = None
    sock = None
    
    def __init__(self, fileExpression, sock, serverCommunication): 
        """
        Método de inicialização da classe, recebe por parâmetro o arquivo que está sendo
        monitorado, o nome do cliente, a tabela que vai ser inserido os logs, o arquivo 
        de relatórios, a lista de ips de servidores, a lista de portas, e o objeto da classe buffer
        """
        try:
            self.writeLog = WriteLog.__new__(WriteLog)
            Thread.__init__(self)
            self.fileExpression = fileExpression
            self.interrupt = True
            self.serverCommunication = serverCommunication
            self._is_alive = True
            self.sock = sock
            self.formatLog = FormatLog(self.fileExpression,self.serverCommunication)
            
        except Exception, e:
            self.writeLog.writeLog("", e)
        

    def run(self):
        """
        Método que todas as threads executam, aqui cada thread vai ler do seu 
        respectivo arquivo de modo a fazer o monitoramento dos logs
        """
        try:
            integer = Word(nums)

            months = (Literal("Jan") ^ Literal("Feb") ^ Literal("Mar")^ Literal("Apr")
                      ^ Literal("May")^ Literal("June")^ Literal("July")^ Literal("Aug")
                      ^ Literal("Sept")^ Literal("Oct") ^Literal("Nov")^ Literal("Dec"))
            
            validateNewLine = Combine((Suppress(Literal("<") + integer +Literal(">")) + months+ restOfLine) 
                                      ^ months + restOfLine)


            
            
            
            fullLine = ''
            newLine = ''
            firstData=True
            while self._is_alive:
                self.conn, addr = self.sock.accept()
                self.conn.setblocking(0)
                print 'Endereço de conexão:', addr
                print 'Hostname da conexão: ', socket.gethostbyaddr(addr[0])

                # testa se a thread deve ser parada, para atualizar as expressoes no arquivo
                while self.interrupt:
                    time.sleep(0.1)
                if self.formatLogDict != {}:
                    try:
                        data = self.conn.recv(1024)

                        # Necessita de um tratamento mais aprimorado: nem sempre que temos
                        # uma quebra de linha significa uma nova mensagem,...
                        print "Dados recebidos:", data
                        
                        newLines = re.split('\n', data)
                        for line in newLines:
                            if firstData:
                                fullLine = validateNewLine.parseString(line)[0]
                                firstData = False
                            else:
                                try:
                                    print "Linha: ", line  
                                    newLine = validateNewLine.parseString(line)[0]
                                   
                                    hostname = fullLine.split()[3]
                                    print hostname
                                    if self.formatLogDict.has_key(hostname):
                                        for listFormatLog in self.formatLogDict.get(hostname):
                                            print "LINHA ENVIADA: " + str(fullLine)
                                            listFormatLog.createFormatLog(fullLine)
                                    fullLine = newLine
                                except:
                                    fullLine = fullLine + line
                                         
                        #conn.send(data)  # echo
                        #conn.close()
                    except Exception, e:
                        #print e
                        if not firstData:
                            hostname = fullLine.split()[3]
                            print hostname
                            if self.formatLogDict.has_key(hostname):
                                for listFormatLog in self.formatLogDict.get(hostname):
                                    print "LINHA ENVIADA NO IF: " + str(fullLine)
                                    listFormatLog.createFormatLog(fullLine)
                            firstData = True
        except Exception, e: 
            self.writeLog.writeLog('', e)
    
    def updateConf(self, table, filterProgram, formatColumn, formatColumnType):
        """
        Método usado para atualizar os campos do formatLog, pois cada vez q forem 
        adicionados itens do mesmo arquivo é necessário essa atualização
        """
        # dicionario com as tabelas como chave e a posicao na lista como valor
        self.formatLog.dictTable[table] = len(self.formatLog.table)
        self.formatLog.table.append(table)
        self.formatLog.filterProgram.append(filterProgram)
        self.formatLog.formatColumn.append(formatColumn)
        self.formatLog.formatColumnType.append(formatColumnType)
                    
    def stop(self, deactivatedTableFile):
        """
        Metodo que retira dos items monitorados os items q forem desativados,
        retorna True se todas as threads que monitoram o arquivo foram desativados e
        False caso contrário
        """
        posDict = self.formatLog.dictTable.pop(deactivatedTableFile)
        self.formatLog.table.pop(posDict)
        self.formatLog.filterProgram.pop(posDict)
        self.formatLog.formatColumn.pop(posDict)
        self.formatLog.formatColumnType.pop(posDict)
        print 'dicionario: ' + str(self.formatLog.dictTable)
        print 'tabelas : ' + str(self.formatLog.table)
        if len(self.formatLog.table) == 0:
            self._is_alive = not self._is_alive 
            self.conn.close()
            return True
        else:
            return False
        
    def pauseStart(self, boolean):
        """
        Método que vai setar a variavel para parar as threads para atualizar o arquivo de expressões
        """       
        self.interrupt = boolean     
        
        