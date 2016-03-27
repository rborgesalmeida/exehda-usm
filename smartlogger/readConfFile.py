# -*- coding: utf-8 -*-

# Autores: Ricardo Almeida, Roger Machado

# Utilizado para divisão da linha através de um caracter
import re
import logging
# IPy para testar a validade dos endereços IP's
# Instalar ipy: apt-get install python-ipy
from IPy import IP

from sendMail import SendMail

class ReadConfFile(object):
    _instance = None
    confFile = None
    logFile = None
    logFileSize = None
    listenPort = None
    listenIP = None
    dbNServer = None
    dbNPort = None
    dbNUser = None
    dbNPass = None
    dbNName = None
    correlation = None
    esperHost = None
    esperPort = None
    smtpServer = None
    smtpPort = None
    smtpPwd = None
    from_ = None
    to = None
    smtpSSL = None
    sendMail = None
    
    def __new__(cls, *args, **kwargs):
        """
        Método que cria o singleton se esse já nao foi criado
        """
        if not cls._instance:
            cls._instance = super(ReadConfFile, cls).__new__(
                                cls, *args, **kwargs)

        return cls._instance

    def __init__(self, confFile):
        """
        Método usado para inicializar as variáveis com seus valores padrão, e
        recebe por parametro o arquivo de configuração que deve ser lido
        Obs.: as variáveis que não são inicializadas, deverão ter seus valores
        declarados no arquivo de configuração
        """
        try:
            self.logFile = '/tmp/exehda-usm-smartlogger.log'
            self.confFile = confFile
            self.logFileSize = 1
            self.listenPort = 8989
            self.listenIP = '127.0.0.1'
            self.esperHost = '127.0.0.1'
            self.esperPort = '8890'
            self.correlation = False
        except Exception, e:
            logging.error('Falha ao construir leitor do arquivo .conf', exc_info=True)    
    
    def validConfFile(self):
        """
        Função usada para verificar se falta algum parâmetro obrigatório
        no arquivo .conf
        """
        try:
            if self.managerIP == None or self.managerPort == None:
                logging.error("Por favor, verifique os parâmetros obrigatórios " + 
                                "no arquivo de configuração " + self.confFile, '')
                return False
            else:
                return True
        except Exception, e:
            logging.error('', exc_info=True)  
            
# Metodo usada para ler as informacoes de configuracao do arquivo .conf
# e armazená-las em seus respectivos atributos, e esse metodo testa se o ip passado para
# o servidor eh um ip valido
          
    def readFile(self):        
        """
        Funcao usada para ler as informações de configuração do arquivo .conf
        e armazená-las em seus respectivos atributos
        """
        try:
            f = open(self.confFile, 'r')
            for line in f :
                # Ignora linhas com comentario e em branco
                if not line.startswith('#') and line != '\n': 
                    line = re.split('\n', line)    
                    line = re.split('=', line[0])
                    if line[0] == 'LogFile':
                        self.logFile = line[1]
                        
                    elif line[0] == 'LogFileSize':
                        try:
                            self.logFileSize = int(line[1])
                        except Exception, e:
                            logging.error("ERRO: Parâmetro LogFileSize com valor " + line[1] + 
                                              " inválido")
                            self.sendEmail()
                            return False
                    elif line[0] == 'ListenPort':
                        try:
                            self.listenPort = int(line[1])
                        except Exception, e:
                            logging.error("ERRO: Parâmetro ListenPort com valor " + line[1] + 
                                              " inválido")
                            return False
                    elif line[0] == 'ListenIP':
                        try:
                            IP(line[1])
                            self.listenIP = line[1]
                        except Exception:
                            logging.error("ERRO: Parâmetro ListenIP com valor " + line[1] + 
                                              " inválido")
                            return False
                    elif line[0] == 'BufferSize':
                        try:
                            self.bufferSize = line[1]
                        except Exception:
                            logging.error("ERRO: Parâmetro BufferSize com valor " + line[1] + 
                                              " inválido")
                            return False
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
                    elif line[0] == 'DBNServer':
                        try:
                            IP(line[1])
                            self.dbNServer = line[1]
                        except Exception:
                            logging.error("ERRO: Parâmetro DBNServer com valor " + line[1] +
                                              " inválido")
                            return False
                    elif line[0] == 'DBNPort':
                        try:
                            if int(line[1]) > 0 and int(line[1]) < 65535:
                                self.dbNPort = int(line[1])
                        except Exception:
                            logging.error("ERRO: Parâmetro DBNPort com valor " + line[1] +
                                              " inválido")
                            return False
                    elif line[0] == 'DBNUser':
                            self.dbNUser = line[1]
                    elif line[0] == 'DBNPass':
                        self.dbNPass = line[1]
                    elif line[0] == 'DBNName':
                        self.dbNName = line[1]
                    elif line[0] == 'EsperHost':
                        try:
                            IP(line[1])
                            self.esperHost = line[1]
                        except Exception:
                            logging.error("ERRO: Parâmetro EsperHost com valor " + line[1] +
                                              " inválido")
                            return False
                    elif line[0] == 'EsperPort':
                        try:
                            self.esperPort = int(line[1])
                        except Exception, e:
                            logging.error("ERRO: Parâmetro EsperPort com valor " 
                                                    + line[1] + " inválido")
                            return False
                    elif line[0] == 'SMTPServer':
                        try:
                            self.smtpServer = line[1]
                        except Exception, e:
                            logging.error("ERRO: Parâmetro SMTPServer com valor " 
                                                    + line[1] + " inválido")
                    elif line[0] == 'SMTPPort':
                        try:
                            self.smtpPort = int(line[1])
                        except Exception, e:
                            logging.error("ERRO: Parâmetro SMTPPort com valor " 
                                                    + line[1] + " inválido")
                    elif line[0] == 'From':
                        try:
                            self.from_ = line[1]
                        except Exception, e:
                            logging.error("ERRO: Parâmetro From com valor " 
                                                    + line[1] + " inválido")
                    elif line[0] == 'FromPwd':
                        try:
                            self.smtpPwd = line[1]
                        except Exception, e:
                            logging.error("ERRO: Parâmetro FromPwd com valor " 
                                                    + line[1] + " inválido")
                    elif line[0] == 'to':
                        try:
                            self.to = line[1]
                        except Exception, e:
                            logging.error("ERRO: Parâmetro To com valor " 
                                                    + line[1] + " inválido")
                    elif line[0] == 'SMTPSSL':
                        try:
                            self.smtpSSL = line[1]
                        except Exception, e:
                            logging.error("ERRO: Parâmetro SMTPSSL com valor " 
                                                    + line[1] + " inválido")
                    
            if self.validConfFile() == True:
                self.sendMail = SendMail(self.from_, self.to, self.smtpServer, self.smtpPort, self.smtpPwd, self.smtpSSL)
                return True
            else:
                return False
                
        except Exception, e:
            logging.error('', exc_info=True)
            return False
    
