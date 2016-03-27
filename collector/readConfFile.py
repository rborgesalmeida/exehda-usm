# -*- coding: utf-8 -*-

# Autores: Ricardo Almeida, Roger Machado

import re
# IPy é utilizado para testar a validade dos endereços IP's
# Instalar ipy: apt-get install python-ipy
from IPy import IP
import logging
from sendMail import SendMail

class ReadConfFile(object):
    """
    Classe usada para ler o arquivo .conf, e armazenar essas configurações 
    """
    _instance = None
    confFile = None
    logFile = None
    logFileSize = None
    clientName = None
    smartLoggerIP = []
    smartLoggerPort = []
    managerIP = []
    managerPort = []
    bufferSize = None
    timeUpdateItems = None
    esperPort = None
    smtpServer = None
    smtpPort = None
    smtpPwd = None
    from_ = None
    to = None
    smtpSSL = None
    sendMail = None
    serverCommunication = None
    correlation = None
        
    def __new__(cls, *args, **kwargs):
        """
        Método que cria o singleton se esse já nao foi criado
        """
        if not cls._instance:
            cls._instance = super(ReadConfFile, cls).__new__(cls)

        return cls._instance
    
    def __init__(self, confFile):
        """
        Função usada para verificar se falta algum parâmetro obrigatório
        no arquivo .conf
        """
        try:      
            self.logFile = '/tmp/exehda-usm-collector.log'
            self.confFile = confFile
            self.logFileSize = 1
            self.smartLoggerPort = []
            self.smartLoggerIP = []
            self.managerPort = []
            self.managerIP = []
            self.bufferSize = 20
            self.timeUpdateItems = 30
        except Exception, e:
            logging.error("Falha ao construir o módulo de leitura do arquivo de configuração ", exc_info=True)

    def validConfFile(self):
        """
        Método usada para verificar se o arquivo .conf se encontra com algum erro
        esses erros são: nome do cliente vazio e lista de managers vazia
        """
        if self.clientName == None or self.managerIP == None or self.managerPort == None:
            logging.error("Por favor, verifique os parâmetros obrigatórios " + 
                                "no arquivo de configuração " + self.confFile, '')
            return False
        else:
            return True
        
    # Metodo usada para ler as informacoes de configuracao do arquivo .conf
    # e armazená-las em seus respectivos atributos, e esse metodo testa se o ip passado para
    # o servidor eh um ip valido            
    def readFile(self):
        """
        Método usada para ler as informações de configuração do arquivo .conf
        e armazená-las em seus respectivos atributos
        """
        i = 0
        try:
            f = open(self.confFile, 'r')
            for line in f :
                # Ignora linhas com comentario
                if not line.startswith('#') and line != '\n': 
                    line = re.split('\n', line)    
                    line = re.split('=', line[0])
                    if line[0] == 'LogFile':
                        self.logFile = line[1]
                    elif line[0] == 'LogFileSize':
                        try:
                            self.logFileSize = int(line[1])
                        except Exception, e:
                            return False
                    elif line[0] == 'Cliente':
                        self.clientName = line[1]
                    elif line[0] == 'SmartLogger':
                        line = re.split(',', line[1])
                        while(i < len(line)):
                            server = re.split(':', line[i])
                            if len(server) == 1:
                                server.append('8989')
                            try:
                                IP(server[0])
                                self.smartLoggerPort.append(int(server[1]))
                                self.smartLoggerIP.append (server[0])
                            except Exception, e:
                                logging.error("Parâmetro SmartLogger com valor %s inválido", 
                                                    line[1], exc_info=True)
                                return False
                            i = i + 1
                    elif line[0] == 'Manager':
                        line = re.split(',', line[1])
                        while(i < len(line)):
                            server = re.split(':', line[i])
                            if len(server) == 1:
                                server.append('8989')
                            try:
                                IP(server[0])
                                self.managerPort.append(int(server[1]))
                                self.managerIP.append (server[0])
                            except Exception, e:
                                logging.error("Parâmetro Manager com valor %s inválido", 
                                                    line[1], exc_info=True)
                                return False
                            i = i + 1
                    elif line[0] == 'BufferSize':
                        try:
                            self.bufferSize = int(line[1])
                        except Exception, e:
                            logging.error("Parâmetro BufferSize com valor %s inválido", 
                                                     line[1], exc_info=True)
                            return False
                    elif line[0] == 'TimeUpdateItems':
                        try:
                            self.timeUpdateItems = int(line[1])
                        except Exception, e:
                            logging.error("Parâmetro TimeUpdateItems com valor $s inválido", 
                                                    line[1], exc_info=True)
                            return False
                    elif line[0] == 'EsperPort':
                        try:
                            self.esperPort = int(line[1])
                        except Exception, e:
                            logging.error("Parâmetro EsperPort com valor %s inválido", 
                                                     line[1], exc_info=True)
                            return False
                    elif line[0] == 'SMTPServer':
                        try:
                            self.smtpServer = line[1]
                        except Exception, e:
                            logging.error("Parâmetro SMTPServer com valor %s inválido",
                                                    line[1], exc_info=True)
                    elif line[0] == 'SMTPPort':
                        try:
                            self.smtpPort = int(line[1])
                        except Exception, e:
                            logging.error("Parâmetro SMTPPort com valor %s inválido", 
                                                    line[1], exc_info=True)
                    elif line[0] == 'From':
                        try:
                            self.from_ = line[1]
                        except Exception, e:
                            logging.error("Parâmetro From com valor %s inválido", 
                                                    line[1], exc_info=True)
                    elif line[0] == 'FromPwd':
                        try:
                            self.smtpPwd = line[1]
                        except Exception, e:
                            logging.error("Parâmetro FromPwd com valor %s inválido", 
                                                    line[1], exc_info=True)
                    elif line[0] == 'To':
                        try:
                            self.to = line[1]
                        except Exception, e:
                            logging.error("Parâmetro To com valor %s inválido", 
                                                    line[1], exc_info=True)
                    elif line[0] == 'SMTPSSL':
                        try:
                            self.smtpSSL = line[1]
                        except Exception, e:
                            logging.error("Parâmetro SMTPSSL com valor %s inválido", 
                                                    line[1], exc_info=True)
                            
            if self.validConfFile() == True:
                self.sendMail = SendMail(self.from_, self.to, self.smtpServer, self.smtpPort, self.smtpPwd, self.smtpSSL)
                return True
            else:
                return False
                
        except Exception, e:
            logging.error('Falha ao analisar o arquivo de configuração', exc_info=True)
    
