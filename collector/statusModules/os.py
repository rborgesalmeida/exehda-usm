# -*- coding: utf-8 -*-

# Ponto a Ponto
# Autores: Ricardo Almeida, Roger Machado

import datetime
import psutil
import commands
import platform
import logging
from statusInfo import StatusInfo

class OS(StatusInfo):
    '''
    classdocs
    '''
        
    #=============================================================================================#
    # INFORMAÇÕES DO SISTEMA        
    def getBootTime(self):
        """
        Envia ao servidor o tempo de boot 
        """
        try:
            data = datetime.datetime.fromtimestamp(psutil.boot_time())
            data = data.strftime("%Y-%m-%d %H:%M")
            self.sendLastValue(data)        
        except Exception, e:
            logging.error('Falha ao coletar tempo de boot', exc_info=True)
            self.sendErrMsg(e)

    def getProgramStatus(self, program):
        """
        Envia ao servidor 1 se o programa passado por parametro esta sendo executado, e
        retorna 0 se nao esta
        """
        try:
            data = commands.getoutput('pidof %s |wc -w' % program)
            self.sendLastValue(data)        
        except Exception, e:
            logging.error('Falha ao coletar status do programa', exc_info=True)
            self.sendErrMsg(e)
    
    def getOS(self):
        """
        Envia ao servidor o sistema operacional
        """
        try:
            data = platform.platform() 
            self.sendLastValue(data)        
        except Exception, e:
            logging.error('Falha ao coletar o sistema operacional', exc_info=True)
            self.sendErrMsg(e)

