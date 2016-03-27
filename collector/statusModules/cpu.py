# -*- coding: utf-8 -*-

# Ponto a Ponto
# Autores: Ricardo Almeida, Roger Machado

import psutil
from statusInfo import StatusInfo
import logging

class CPU(StatusInfo):
    '''
    classdocs
    '''
        
    #=============================================================================================#
    # CPU    
    def getCPUPercent(self):
        """
        Envia aos servidores a porcentagem de uso do processador
        """
        try:
            data = psutil.cpu_percent(interval=1, percpu=False)
            self.sendLastValue(data)
        except Exception, e:
            logging.error('Falha ao coletar a percentagem de uso do processador', exc_info=True)
            self.sendErrMsg(e)
            
    def getCPUTimes(self, cpuTimeFlag):
        """
        Envia aos servidores o tempo de CPU de acordo com o parâmetro solicitado (user, nice,
        system, idle, iowait, irq, softirq)
        """
        try:
            cpuTimeFlagDict = {'user': 0, 'nice': 1, 'system': 2, 'idle': 3,
                               'iowait': 4, 'irq': 5, 'softirq': 6}
            data = psutil.cpu_times(percpu=False)[cpuTimeFlagDict.get(cpuTimeFlag)]
            self.sendLastValue(data)
        except Exception, e:
            logging.error('Falha ao coletar o tempo de CPU', exc_info=True)