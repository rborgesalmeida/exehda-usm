# -*- coding: utf-8 -*-

# Importação dos módulos de email necessários
from email import encoders
from email.mime.audio import MIMEAudio
from email.mime.base import MIMEBase
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

# MIME type baseado na extensão do arquivo
import mimetypes

from os import path

class Message(object):
    """
    Representa um e-mail.

    Utilizada para configurar o destinatário, remetente, assunto e mensagem como
    texto plano. É possível setar o atributo Html para enviar um e-mail usando HTML,
    ou usar o método attach() para anexar arquivos.

    Sempre quando estiver enviando um e-mail HTML, você pode usar o atributo Body
    como um e-mail alternativo em texto plano.

    Enviar o e-mail usando a classe mailer.
    """

    def __init__(self):
        self.attachments = []
        self.To = None
        self.From = None
        self.Subject = None
        self.Body = None
        self.Html = None

    def _get_to(self):
        addrs = self.To.replace(";", ",").split(",")
        return ", ".join([x.strip()
                          for x in addrs])
#    def _set_to(self, to):
#        self._to = to

#    To = property(_get_to, _set_to,
#                  doc="""Destinatário(s) do e-mail.
#                  Separar múltiplos destinatários com vírgula ou ponto-vírgula""")

    def as_string(self):
        """
        Retorna o e-mail como uma string para enviar para a classe mailer
        """

        if not self.attachments:
            return self._plaintext()
        else:
            return self._multipart()

    def _plaintext(self):
        """
        E-mail como texto plano, sem anexos.
        """

        if not self.Html:
            msg = MIMEText(self.Body, 'plain', 'utf-8')
        else:
            msg  = self._with_html()

        self._set_info(msg)
        return msg.as_string()

    def _with_html(self):
        """
        E-mail com código HTML
        """

        outer = MIMEMultipart('alternative')

        part1 = MIMEText(self.Body, 'plain')
        part2 = MIMEText(self.Html, 'html')

        outer.attach(part1)
        outer.attach(part2)

        return outer

    def _set_info(self, msg):
        msg['Subject'] = self.Subject
        msg['From'] = self.From
        msg['To'] = self.To

    def _multipart(self):
        """
        E-mail com anexo.
        """

        msg = MIMEMultipart()

        msg.attach(MIMEText(self.Body, 'plain'))

        self._set_info(msg)
        msg.preamble = self.Subject

        for filename in self.attachments:
            self._add_attachment(msg, filename)
        return msg.as_string()

    def _add_attachment(self, outer, filename):
        ctype, encoding = mimetypes.guess_type(filename)
        if ctype is None or encoding is not None:
            # Codificação não pode ser detectada, ou o arquivo está codificado (comprimido),
            # logo, devemos usar tipo genérico.
            ctype = 'application/octet-stream'
        maintype, subtype = ctype.split('/', 1)
        fp = open(filename, 'rb')
        if maintype == 'text':
            # Obs.: devemos realizar o cálculo da codificação
            msg = MIMEText(fp.read(), _subtype=subtype)
        elif maintype == 'image':
            msg = MIMEImage(fp.read(), _subtype=subtype)
        elif maintype == 'audio':
            msg = MIMEAudio(fp.read(), _subtype=subtype)
        else:
            msg = MIMEBase(maintype, subtype)
            msg.set_payload(fp.read())
            # Codifica o payload usando Base64
            encoders.encode_base64(msg)
        fp.close()
        # Seta o parâmetro filename
        msg.add_header('Content-Disposition',
                'attachment',
                filename=path.basename(filename))
        outer.attach(msg)

    def attach(self, filename):
        """
        Anexa o arquivo ao e-mail. Passar por parâmetro o nome do arquivo.
        A classe irá descobrir o tipo MIME e carregará o arquivo.
        """

        self.attachments.append(filename)
