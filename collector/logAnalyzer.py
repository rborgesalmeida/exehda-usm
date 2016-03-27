# -*- coding: utf-8 -*-

# Autores: Ricardo Almeida, Roger Machado

import httpagentparser
import time
import datetime
import re
from time import strptime
from formatLog import FormatLog
import logging
import os
from threading import Thread

from pyparsing import *

class LogAnalyzer(Thread):
    """
    Classe que lê os logs dos seus respectivos arquivos, e chama os métodos apropriados 
    para fazerem seu tratamento 
    """
    monitoredFile = None
    newLine = None
    delay = None
    serverCommunication = None
    interrupt = None
    formatLog = None
    identifier = None
    fileExpression = None
    
    def __init__(self, monitoredFile, identifier, delay, serverCommunication, fileExpression): 
        """
        Método de inicialização da classe, recebe por parâmetro o arquivo que está sendo
        monitorado, o nome do cliente, a tabela que vai ser inserido os logs, o arquivo 
        de relatórios, a lista de ips de servidores, a lista de portas, e o objeto da classe buffer
        """
        try:
            Thread.__init__(self)
            self.monitoredFile = monitoredFile
            self.delay = delay
            self.identifier = identifier
            self.serverCommunication = serverCommunication
            self.interrupt = False
            self._is_alive = True
            self.formatLog = FormatLog(fileExpression,self.serverCommunication)
        except Exception, e:
            logging.error("Falha ao construir o analisador de logs", exc_info=True)
            
        
    # Metodo estatico usaddo para ler algumas propriedades do arquivo,
    # usado para verificar se o arquivo foi renomeado

    @staticmethod
    def get_file_id(st):
        """
         Método usada para ler algumas propriedades do arquivo,
         usada para verificar se o arquivo foi renomeado
        """
        return "%xg%x" % (st.st_dev, st.st_ino)
    
    # Metodo que todas as threads executam, aqui cada thread vai ler do seu 
    # respectivo arquivo de modo a fazer o monitoramento dos logs, esse metodo executa
    # infinitamente e fica testando se o arquivo foi renomeado para poder abrir novamente
    # o arquivo de modo a continuar o monitoramento, eh lido varias linhas de cada vez 
    # e dentro do for vamos olhando linha a linha, e feito um tratamento para verificar se o
    # log esta contido em mais de uma linha afim de manter o mesmo formato do log,
    # aqui eh testado qual log esta sendo, monitorado de forma a chamar o metodo apropriado 
    # para cada log afim de ser separado em suas partes e depoiso codigo aguarda um tempo para 
    # ler novamente do arquivo,

    def run(self):
        """
        Método que todas as threads executam, aqui cada thread vai ler do seu 
        respectivo arquivo de modo a fazer o monitoramento dos logs
        """
        try:
            f = open(self.monitoredFile, 'r')
            # Vai para o final do monitoredFile
            f.seek(0, os.SEEK_END) 
            fid = self.get_file_id(os.stat(self.monitoredFile))
            logRotate = False
            isNewLIne = False
            while self._is_alive:
                try:
                    if fid != self.get_file_id(os.stat(self.monitoredFile)):
                        fid = self.get_file_id(os.stat(self.monitoredFile))
                        f = open(self.monitoredFile, 'r')
                        # Vai para o final do monitoredFile
                        f.seek(0, os.SEEK_END)
                        logRotate = False
                except Exception, e:
                    if logRotate == False:
                        logging.error('O arquivo de log foi rotacionado', exc_info=True)
                        logRotate = True
                    #time.sleep(self.delay)
                self.newLine=''
                isNewLIne=False
                for line in f.readlines():
                    # testa se a thread deve ser parada, para atualizar as expressoes no arquivo
                    while self.interrupt:
			#pass
                        time.sleep(1)
                    if self._is_alive == False:
                        break;
                        # testa se a linha esta em  branco
                    if line[0:1:] != '\n':
                        # testa se a newLine esta vazia 
                        if self.newLine == '':
                            self.newLine=line
                            isNewLIne=True
                            
                        # testa se a linha lida eh continuacao da anterior
                        elif line.startswith('\t') or line.startswith(' ') : 
                            self.newLine = self.newLine + line
                        # entra aqui para enviar a linha anterior e guardar a ultima linha lida
                        else:
                            self.formatLog.createFormatLog(self.identifier, str(self.newLine))
                            self.newLine=line
        # testa se possui linha para enviar para o servidor
                if isNewLIne:
                    self.formatLog.createFormatLog(self.identifier, str(self.newLine))
                time.sleep(self.delay)
        except Exception, e: 
            logging.error('Falha durante a análise dos logs', exc_info=True)
            
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
#        print 'dicionario: ' + str(self.formatLog.dictTable)
#        print 'tabelas : ' + str(self.formatLog.table)
        if len(self.formatLog.table) == 0:
            self._is_alive = not self._is_alive 
            return True
        else:
            return False
        
    def pauseStart(self, boolean):
        """
        Método que vai setar a variavel para parar as threads para atualizar o arquivo de expressões
        """       
        self.interrupt = boolean
        
