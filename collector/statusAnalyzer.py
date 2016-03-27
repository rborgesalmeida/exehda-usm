# -*- coding: utf-8 -*-

# Autores: Ricardo Almeida, Roger Machado

from statusModules  import cpu, os, memory, filesystem, network, security
import re
import logging
from threading import Thread
from time import sleep

class StatusAnalyzer(Thread):
    """
    Classe que chama o metodo apropiado para realizar a  coleta os dados de acordo com o item a 
    ser  monitorados. 
    """
    
    monitoredItemKey = None
    identifier = None
    itemid = None
    delay = None
    serverCommunication = None
    
    def __init__(self, monitoredItem, identifier, itemid, delay,  serverCommunication): 
        """
        Método de inicialização da classe, recebe por parametro o item a ser monitorado, 
        identificador do item
        """
        try:
            Thread.__init__(self)
            self.monitoredItemKey = monitoredItem
            self.itemid = itemid
            self.identifier = identifier
            self.delay = delay
            self.serverCommunication = serverCommunication
            self._is_alive = True
        except Exception, e:
            logging.error("Falha ao contruir módulo de análise de status", exc_info=True)

    def run(self):
        while self._is_alive:
            self.getMethod()
            sleep(self.delay)

    def getMethod(self):
        """
        Metodo que verifica qual metodo do status info deve ser executado
        """
        try:
            # dicionario com keys como chave e os metodos como valores
            func = {'cpu.percent[used]' : cpu.CPU(self.itemid, self.monitoredItemKey, self.identifier, self.serverCommunication).getCPUPercent,
                    'network.publicip' : network.Network(self.itemid, self.monitoredItemKey,  self.identifier, self.serverCommunication).getPublicIP,
                    'os.uname' : os.OS(self.itemid, self.monitoredItemKey,  self.identifier, self.serverCommunication).getOS, 
                    'os.boottime' : os.OS(self.itemid, self.monitoredItemKey, self.identifier, self.serverCommunication).getBootTime,
                    'security.users' : security.Security(self.itemid, self.monitoredItemKey, self.identifier, self.serverCommunication).getUsers
                    }
            func2 = {'security.checksum' : security.Security(self.itemid, self.monitoredItemKey, self.identifier, self.serverCommunication).checkMD5, 
                     'network.io' : network.Network(self.itemid, self.monitoredItemKey, self.identifier, self.serverCommunication).getNetworkIOCounters,
                     'network.conf' : network.Network(self.itemid, self.monitoredItemKey, self.identifier, self.serverCommunication).getNetworkConf,
                     'filesystem.fstype' : filesystem.FileSystem(self.itemid, self.monitoredItemKey, self.identifier, self.serverCommunication).getDiskPartitionFsType,
                     'filesystem.size' : filesystem.FileSystem(self.itemid, self.monitoredItemKey, self.identifier, self.serverCommunication).getDiskUsage,
                     'filesystem.io' : filesystem.FileSystem(self.itemid, self.monitoredItemKey, self.identifier, self.serverCommunication).getDiskIOCounters,
                     'memory.phy.size' : memory.Memory(self.itemid, self.monitoredItemKey, self.identifier, self.serverCommunication).getPhysicalMemory,
                     'cpu.times' : cpu.CPU(self.itemid, self.monitoredItemKey, self.identifier, self.serverCommunication).getCPUTimes,
                     'memory.virt.size' : memory.Memory(self.itemid, self.monitoredItemKey, self.identifier, self.serverCommunication).getVirtualMemory
                     }
            
            if func.has_key(self.monitoredItemKey):
                return func.get(self.monitoredItemKey)()
            else:    
                method = re.split('\[', self.monitoredItemKey)
                parameter = re.split('\]', method[1])[0]
                if ',' in parameter:
                    parameter= re.split('\,', parameter)
                    return func2.get(method[0])(parameter[0].strip(), parameter[1].strip())
                else:
                    return func2.get(method[0])(parameter.strip())
                
        except Exception, e:
            logging.error('Falha ao determinar o método de status a ser executado para a chave: %s', self.monitoredItemKey, exc_info=True)
    
    
    def stop(self):
        self._is_alive = not self._is_alive
