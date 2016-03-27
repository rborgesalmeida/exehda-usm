# -*- coding: utf-8 -*-

# Autores: Ricardo Almeida, Roger Machado

from readConfFile import ReadConfFile
from sendMail import SendMail
import commands
from os import linesep
import logging

class Situations:
    '''
    Classe que representa as situações a serem detectadas.
    '''
    epl = None
    id = None
    description = None
    comments = None
    commandType = None
    command = None
    from_ = None
    commandTo = None
    smtpServer = None
    smtpPort = None
    smtpPwd = None
    commandSubject = None
    commandBody = None
    priority = None
    occurrences = None
    occurred = None
    smtpSSL = None 
    descriptionSubs = None
    commandSubs = None
    commandBodySubs = None
    commandSubjectSubs = None
    commentsSubs = None

    def __init__(self, id, description, epl, comments, command, commandType, commandTo, commandSubject, commandBody, priority, occurrences):
        '''
        Construtor que recebe por parâmetro as propriedades referentes a situação.
        '''
        self.id = id
        self.epl = epl
        self.description = description
        self.comments = comments
        self.command = command
        self.commandType = commandType
        self.priority = priority
        self.occurrences = occurrences
        self.occurred = 0
        readConf = ReadConfFile.__new__(ReadConfFile)
        self.from_ = readConf.from_
        self.commandTo = commandTo
        self.commandSubject = commandSubject
        self.commandBody = commandBody
        self.smtpServer = readConf.smtpServer
        self.smtpPort = readConf.smtpPort
        self.smtpPwd = readConf.smtpPwd
        self.smtpSSL = readConf.smtpSSL
        
        
    def executeCommand(self):
        '''
        Executa o comando configurado para a situação e retorna a saída dele.
        '''
        if self.commandType == 'mail':
            try:
                mail = SendMail(self.from_, self.commandTo, self.smtpServer, self.smtpPort, self.smtpPwd, self.smtpSSL)
                mail.send(self.commandSubjectSubs, self.commandBodySubs)
                out = "E-mail enviado com sucesso para " + self.commandTo + "."
            except Exception, e:
                logging.error("Falha ao enviar e-mail de situação detectada", exc_info=True)
                out = "ERRO: Falha ao enviar e-mail de situação detectada para" + self.commandTo + ": " + str(e)
        elif self.commandType == 'shellcommand':
            try:
                out = commands.getoutput(self.commandSubs)
                if out == '' or out == 'None':
                    out = 'Comando ' + self.commandSubs + ' executado com sucesso.'
            except Exception, e:
                logging.error("Falha ao executar comando %s", self.commandSubs, exc_info=True)
                out = "ERRO: Falha ao executar comando '" + self.commandSubs + "': " + str(e)
        return out
        
    def applySubsVariable(self, events):
        '''
        Aplica a substituição das variáveis 
        '''
        try:
            self.descriptionSubs = self.subsVariable(events, self.description)
            self.commandSubs = self.subsVariable(events, self.command)
            self.commandBodySubs = self.subsVariable(events, self.commandBody)
            self.commandSubjectSubs = self.subsVariable(events, self.commandSubject)
            self.commentsSubs = self.subsVariable(events, self.comments)
        except Exception, e:
            logging.error('Falha ao substituir variáveis para montar situação', exc_info=True)       
        
    def subsVariable(self, events, field):
        '''
        Procura variável no campo passado por parâmetro, caso exista, procura pelo mesmo nome de 
        variável nos eventos que geraram uma situação.
        '''
        try:
            variablePosition = str(field).find('$')
            if variablePosition != -1:
                variable = ''
                # Monta uma variável com a string a ser substituida (ex.: $IP)
                while (variablePosition < len(field)) and (field[variablePosition] != ' ') and \
                      (field[variablePosition] != linesep) and (field[variablePosition] != '"'):
                    variable = str(variable) + str(field[variablePosition])
                    variablePosition = variablePosition + 1
                
                toFind = str(variable[1:]).lower()
                toFind = '[' + toFind + '='
                
                position = events.find(toFind) + len(toFind)
                
                variableSubs = ''
                while events[position] != ']':
                    variableSubs = str(variableSubs) + str(events[position])
                    position = position + 1
                                
                return field.replace(variable, variableSubs)
            else:
                return field
                
        except Exception, e:
            logging.error('Falha ao substituir variáveis para montar situação', exc_info=True)