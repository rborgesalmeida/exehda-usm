# -*- coding: utf-8 -*-

# Autores: Ricardo Almeida, Roger Machado

import psutil
from statusInfo import StatusInfo
import logging

class FileSystem(StatusInfo):
    '''
    classdocs
    '''

    #=============================================================================================#
    # DISCO                    
    def getDiskPartitionFsType(self, mountPoint):
        """
        Envia aos servidores o tipo de partição, do ponto de montagem passado por parâmetro
        """
        try:
            diskPartitions = psutil.disk_partitions(all=False) 
            i=0
            while i < len(diskPartitions):
                if diskPartitions[i][1] == mountPoint:
                    data = diskPartitions[i][2]
                    self.sendLastValue(data)
                    return        
                i = i+1
        except Exception, e:
            logging.error('Falha ao coletar tipo de partição', exc_info=True)
            self.sendErrMsg(e)
                        
    def getDiskUsage(self, mountPoint, spaceFlag):
        """
        Envia aos servidores o tamanho total de disco do ponto de montagem passado por parâmetro
        """
        try:
            spaceFlagDict = {'total': 0, 'used': 1, 'free': 2, 'pused': 3}
            data = psutil.disk_usage(mountPoint)[spaceFlagDict.get(spaceFlag)]
            self.sendLastValue(data)
        except Exception, e:
            logging.error('Falha ao coletar o tamanho total da partição', exc_info=True)
            self.sendErrMsg(e)
    #=============================================================================================#

    #=============================================================================================#
    # I/O DE DISCO
    def getDiskIOCounters(self, ioCountersFlag):
        """
        Envia ao servidor a quantidade de leitura de IO no disco
        """
        try:
            ioCountersFlagDict = {'read_count': 0, 'write_count': 1, 'read_bytes': 2, 
                                  'write_bytes': 3, 'read_time': 4, 'write_time': 5}
            data = psutil.disk_io_counters()[ioCountersFlagDict.get(ioCountersFlag)]
            self.sendLastValue(data)        
        except Exception, e:
            logging.error('Falha ao coletar estatísticas de IO', exc_info=True)
            self.sendErrMsg(e)
