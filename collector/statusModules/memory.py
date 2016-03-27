# -*- coding: utf-8 -*-

# Ponto a Ponto
# Autores: Ricardo Almeida, Roger Machado

import psutil
from statusInfo import StatusInfo
import logging

class Memory(StatusInfo):
    '''
    classdocs
    '''
    
    #=============================================================================================#
    # MEMÓRIA VIRTUAL                                     
    def getVirtualMemory(self, spaceFlag):
        """
        Envia aos servidores o espaço requisitado através do parâmetro spaceFlag de utilização da
        memória virtual
        """
        try:
            spaceFlagDict = {'total': 0, 'used': 1, 'free': 2, 'pused': 3}
            data = psutil.swap_memory()[spaceFlagDict.get(spaceFlag)]
            self.sendLastValue(data)        
        except Exception, e:
            logging.error('Falha ao coletar estatísticas da memória virtual', exc_info=True)
            self.sendErrMsg(e)
    #=============================================================================================#
 
    #=============================================================================================#
    # MEMÓRIA FÍSICA            
    def getPhysicalMemory(self, spaceFlag):
        """
        Envia aos servidores o espaço requisitado através do parâmetro spaceFlag de utilização da
        memória física
        """
        try:
            spaceFlagDict = {'total': 0, 'used': 1, 'free': 2, 'pused': 3}
            data = psutil.virtual_memory()[spaceFlagDict.get(spaceFlag)]
            self.sendLastValue(data)        
        except Exception, e:
            logging.error('Falha ao coletar estatísticas da memória física', exc_info=True)
            self.sendErrMsg(e)
    #=============================================================================================#
