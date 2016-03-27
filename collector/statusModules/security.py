# -*- coding: utf-8 -*-

# Ponto a Ponto
# Autores: Ricardo Almeida, Roger Machado

import psutil
import hashlib
from statusInfo import StatusInfo
import logging

class Security(StatusInfo):
    '''
    classdocs
    '''
        
    #=============================================================================================#
    # INFORMAÇÕES DE SEGURANÇA  
    def getUsers(self):
        """
        Envia ao servidor os usuários 
        """
        try:
            data = psutil.users()
            data = str(data)
            data = data.replace("'", "\"")
            self.sendLastValue(data)        
        except Exception, e:
            logging.error('', exc_info=True)
            self.sendErrMsg(e)       
            
    def checkMD5(self, file_):
        """
        Envia ao servidor a soma de verificação
        """
        try:
            check = hashlib.md5()
            check.update(open(file_, 'rb').read())
            data = check.hexdigest()
            self.sendLastValue(data)        
        except Exception, e:
            logging.error('', exc_info=True)
            self.sendErrMsg(e)
            
