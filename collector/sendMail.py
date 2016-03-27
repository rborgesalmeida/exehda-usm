# -*- coding: utf-8 -*-

# Autores: Ricardo Almeida, Roger Machado

from mailer import Mailer
from message import Message
import logging

class SendMail:
    """
    Classe utilizada para simplificar o envio de e-mail.
    Recebe por parâmetro o assunto e a mensagem.
    """
    from_ = None
    to = None
    stmpServer = None
    smtpPort = None
    smtpPwd = None
    smtpSSL = None
    
    def __init__(self, from_, to, stmpServer, smtpPort, smtpPwd, smtpSSL):
        """
        Construtor da classe que irá atribuir o assunto e a mensagem aos seus atributos.
        """
        try:
            self.from_ = from_
            self.to = to
            self.stmpServer = stmpServer
            self.smtpPort = smtpPort
            self.smtpPwd = smtpPwd
            self.smtpSSL = smtpSSL
        except Exception, e:
            logging.error('Falha ao contruir o módulo para envio de e-mails', exc_info=True)
            
    def send(self, subject, body):
        """
        Responsável pelo envio do e-mail.
        """
        try:
            message = Message()
            message.From = self.from_
            message.To = self.to
            message.Subject = subject
            message.Body = body
            
            mailer = Mailer(self.stmpServer, self.smtpPort, self.smtpSSL)
            mailer.login(message.From, self.smtpPwd)
            mailer.send(message)
        except Exception, e:
            logging.error('Falha ao enviar e-mail', exc_info=True)
