# -*- coding: utf-8 -*-

# Ponto a Ponto
# Autores: Ricardo Almeida, Roger Machado

import urllib2
import psutil
import netifaces
from statusInfo import StatusInfo
import logging

class Network(StatusInfo):
    '''
    classdocs
    '''

        
    #=============================================================================================#
    # INFORMAÇÕES DE REDE
    def getPublicIP(self):
        """
        Envia ao servidor o ip publico utilizando a porta 80 para descobrí-lo
        """
        try:
            data = urllib2.urlopen('http://ip.42.pl/raw').read()
            self.sendLastValue(data)        
        except Exception, e:
            logging.error('', exc_info=True)
            self.sendErrMsg(e)
    
    def getNetworkIOCounters(self, interface, ioCountersFlag):
        """
        Envia ao servidor as informações disponíveis da interface de rede passada por 
        parâmetro, de acordo com a requisição do parâmetro ioCountersFlag (bytes_sent, 
        bytes_recv, packets_sent, errin, errout, dropin, dropout)
        """
        try:
            ioCountersFlagDict = {'bytes_sent': 0, 'bytes_recv': 1, 'packets_sent': 2, 
                                  'packets_recv': 3, 'errin': 4, 'errout': 5, 
                                  'dropin': 6, 'dropout': 7}
            data = psutil.net_io_counters(pernic=True)[interface][ioCountersFlagDict.get(ioCountersFlag)]
            self.sendLastValue(data)
        except Exception, e:
            logging.error('', exc_info=True)
            self.sendErrMsg(e)
          
    def getNetworkConf(self, interface, parameter):
        """
        Envia ao servidor o IP, MAC, ou broadcast da interface passada por parametro,
        de acordo com o parametro solicitado (IP, ...), se não houver retorna None
        """
        try:
            for ifname in iter(psutil.net_io_counters(pernic=True)):      
                if (ifname == interface):
                    try:
                        data = netifaces.ifaddresses(ifname)[2][0].get(parameter)                
                        self.sendLastValue(data) 
                    except:
                        self.sendLastValue(None)
        except Exception, e:
            logging.error('', exc_info=True)
            self.sendErrMsg(e)
    #=============================================================================================#
