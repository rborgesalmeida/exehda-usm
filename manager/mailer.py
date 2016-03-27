# -*- coding: utf-8 -*-

import smtplib

class Mailer(object):
    """
    Representa a conexão SMTP connection.
    Usar login() para especificar usuário e senha para autenticação no servidor de e-mail.
    """
    host = None
    port = None
    ssl = None
    _usr = None
    _pwd = None

    def __init__(self, host="localhost", port=25, ssl=False):
        """
        Construtor que recebe por parâmetro o endereço do servidor de e-mail e a porta.
        Por padrão estes parâmetros possuem valores localhost e 25 respectivamente.
        """
        self.host = host
        self.port = port
        self.ssl = ssl
        self._usr = None
        self._pwd = None

    def login(self, usr, pwd):
        """
        Classe responsável por receber os parâmetros do usuário referentes
        a autenticação no servidor de e-mail (usuário e senha).
        """
        self._usr = usr
        self._pwd = pwd

    def send(self, msg):
        """
        Envia uma mensagem ou uma sequência de mensagens.

        Toda vez que é feita uma chamada ao método send é criada uma nova conexão
        com o servidor de e-mail, logo, caso você deseje enviar uma sequência de
        e-mails, passe as mensagens como uma lista:
        Ex.: send([mensagem1, mensagem2, mensagem3])
        """
        try:
            server = smtplib.SMTP(self.host, self.port)
    
            # Verifica se os parâmetros de autenticação foram setados
            if self._usr and self._pwd:
                # Tenta realizar o helo e iniciar a conexão segura, caso
                # o servidor não tenha suporte a conexão segura, tentará
                # seguir realizando o login normalmente.
                try:
                    server.starttls()
                    server.ehlo()                    
                except Exception:
                    pass
                server.login(self._usr, self._pwd)
    
            # Tenta enviar a lista de mensagens, caso não seja lista, entrará
            # na exceção e enviará a mensagem única.
            try:
                for m in msg:
                    self._send(server, m)
            except TypeError:
                self._send(server, msg)
    
            # Finaliza a conexão com o servidor.
            server.quit()
        except Exception, e:
            logging.error("ERRO: Falha ao enviar e-mail: ", exc_info=True)

    def _send(self, server, msg):
        """
        Envia uma única mensagem usando o servidor
        criado em send()
        """
        me = msg.From
        # Caso exista espaços nos endereços dos destinatários, estes espaços seram removidos
        you = [x.strip() for x in msg.To.split(",")]
        
        server.sendmail(me, you, msg.as_string())
