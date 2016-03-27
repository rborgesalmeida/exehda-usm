# -*- coding: utf-8 -*-

# Autores: Ricardo Almeida, Roger Machado

from serverCommunication import ServerCommunication
import re
import datetime

class StatusInfo:
    """
    Classe que vai armazenar a lista de logs que ainda não foram enviados
    """
    itemid = None
    monitoredItemKey = None
    identifier = None
    serverCommunication = None
    
    def __init__(self, itemid, monitoredItemKey, identifier, serverCommunication):
        """
        Método de inicialização da classe, recebe por parâmetro o arquivo relatórios e 
        o arquivo de logs nao enviados
        """
        self.itemid = itemid
        self.identifier = identifier
        self.monitoredItemKey = monitoredItemKey
        self.serverCommunication = serverCommunication
        
    def sendLastValue(self, data):
        """
        Método que chama chama o sendLastValue para enviar os status coletados para o servidor
        """
        if data == None:
            self.sendErrMsg(data)
        else:
            # cria o formato da coluna onde vai ser inserido os dados
            formatColumn = ['lastvalue', 'errmsg', 'datecoll']
            # cria a data de coleta no formato certo
            date = datetime.datetime.now()
            date = date.strftime('%Y-%m-%d %H:%M:%S.%f')
            # cria a lista onde vai ser inserido os dados
            dataSent= []
            # insere os dados coletados 
            dataSent.append(data)
            # insere um campo vazio para altrerar o campo errmsg
            dataSent.append('')
            # insere o campo data_coll 
            dataSent.append(date)
            # chama o meotodo da classe ServerCommunication para enviar os dados para o servidor
            self.serverCommunication.sendStatus(self.identifier, self.itemid, formatColumn, dataSent)
            
    def sendErrMsg(self, data):
        """
        Método usado para enviar os status para a coluna de erro, ou porque gero alguma excessao 
        durante o processo ou retornou None o metodo de busca de status
        """
        formatColumn = ['errmsg', 'lastvalue', 'datecoll']
        date = datetime.datetime.now()
        date = date.strftime('%Y-%m-%d %H:%M:%S.%f')
        dataSent= []
        # testa se o campo passado eh None
        if data == None:
            # insere um campo vazio no lugar de None
            dataSent.append('')
        else:    
            # se entrar aqui foi passado uma excessao
            # transforma ela em string, e substitui onde tem ' por "
            newData = str(data)
            dataSent.append(newData.replace("'", "\""))
        # insere um campo vazio para atualizar o campo lastvalue
        dataSent.append('')
        # insere o campo datacoll
        dataSent.append(date)
        # chama o meotodo da classe ServerCommunication para enviar os dados para o servidor
        self.serverCommunication.sendStatus(self.identifier, self.itemid, formatColumn, dataSent)
