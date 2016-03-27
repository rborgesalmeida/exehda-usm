# -*- coding: utf-8 -*-

# Autores: Ricardo Almeida, Roger Machado

import httpagentparser
import time
from IPy import IP
import datetime
import re
import geoip2.database
from time import strptime
from pyparsing import *
import logging

class FormatLog():
    """
    Classe que lê os logs dos seus respectivos arquivos, e chama os métodos apropriados 
    para fazerem seu tratamento 
    """
    table = None
    filterProgram = None
    fileExpression = None
    formatColumn = None
    formatColumnType = None
    serverCommunication = None
    dictTable = None
    
    def __init__(self, fileExpression, serverCommunication): 
        """
        Método de inicialização da classe, recebe por parâmetro o arquivo que está sendo
        monitorado, o nome do cliente, a tabela que vai ser inserido os logs, o arquivo 
        de relatórios, a lista de ips de servidores, a lista de portas, e o objeto da classe buffer
        """
        try:
            self.fileExpression = fileExpression.replace('/', '.')
            self.serverCommunication = serverCommunication
            self.table = []
            self.filterProgram = []
            self.formatColumn = []
            self.formatColumnType = []
            self.dictTable = {}
        except Exception, e:
            logging.error("Falha ao criar formatLog", exc_info=True)
        
#    def updateConf(self, table, filterProgram, formatColumn, formatColumnType):
#        """
#        Método usado para atualizar os campos, quando há mais de um item que monitora o 
#        mesmo arquivo.
#        """
#        print 'numero de items: ' + str(len(self.table))
#        self.dictTable[table] = len(self.table)
#        self.table.append(table)
#        self.filterProgram.append(filterProgram)
#        self.formatColumn.append(formatColumn)
#        self.formatColumnType.append(formatColumnType)
#        print 'numero de items: ' + str(len(self.table))
#        print 'dict:  ' + str(self.dictTable)


    # Metodo usado para verificar qual o log que esta sendo analsado, e chamar a respectiva
    # funcao para fazer o tratamento apropriado     
    def createFormatLog(self, identifier, newLine):
        """
        Método usado para verificar qual o log que esta sendo analsado, e chamar a respectiva
        função para fazer o tratamento apropriado
        """
        # testa se a expressao regular foi aceita e chama o metodo apropriado para formatar o log
	try:
            program = newLine.split()[4].split('[')[0]
            numItems = 0
            while numItems < len(self.table):
                if self.findWords(program, numItems):
                    self.formatLog(identifier, newLine, numItems)
                numItems = numItems + 1
	except Exception, e:
            logging.error("Falha ao executar createFormatLog: %s", str(newLine),exc_info=True)

    # Metodo usado para verificar se as palavaras usadas nas expressoes regulares se encontram
    # na linha lida, retorna true se a expressao foi aceita na linha lida e false caso contrario
    def findWords(self, program, numItems):
        """
        Método usado para tratar as expressões regulares
        """
        try:
            expressionProgram = "\'" + program + "\'"
            resultado = "\'"
            dict = {'|' : " or ", '&' : " and ", ')' : ")"}
            i=0
            endNot = False
            oneWord = True
            # testa se a expressao nao esta vazia
            if self.filterProgram[numItems] != None:
                while i < len(self.filterProgram[numItems]):
                    # testa se possui mais de uma palavra na expressao para inserir o ' 
                    # antes da proxima expressao 
                    if oneWord == False:
                        resultado = resultado + "\'"
                    endNot = False
                    # testa se a expressao eh para verificar se a palavra nao se encontrar na linha
                    if self.filterProgram[numItems][i] == '!' :
                        i = i+1
                        while (i < len(self.filterProgram[numItems]) and 
                               self.filterProgram[numItems][i] != '|' and 
                               self.filterProgram[numItems][i] != '&' 
                               and self.filterProgram[numItems][i] != ')'):
                            resultado = resultado + self.filterProgram[numItems][i]
                            i = i+1
                        resultado = resultado + "\'"
                        # testa se tem mais alguma palavra na expressao para ser tratada
                        if i < len(self.filterProgram[numItems]):
                            oneWord = False
                            resultado = (resultado + " not in " +  expressionProgram + 
                                        dict[self.filterProgram[numItems][i]] ) 
                        else :
                            resultado = resultado + " not in " + expressionProgram 
                        endNot = True
                    # testa se  o  caracter lido eh ) para inserir a verificacao dentro 
                    # dos parenteses
                    elif self.filterProgram[numItems][i] == ')':
                        resultado = resultado + " in " +  expressionProgram + ') '
                    # testa se a expressao anterior nao estava dentro de parenteses para inserir 
                    # a condicao da esxpressao 
                    elif self.filterProgram[numItems][i] == '|' and self.filterProgram[numItems][i-1] != ')':
                        resultado = resultado + " in " +  expressionProgram  + " or "
                    # testa se a expressao anterior nao estava dentro de parenteses para inserir 
                    # a condicao da esxpressao 
                    elif self.filterProgram[numItems][i] == '&' and self.filterProgram[numItems][i-1] != ')':
                        resultado = resultado + " in " +  expressionProgram + " and "
                    elif self.filterProgram[numItems][i] == '&':
                        oneWord = False
                        resultado = resultado + ' and ' 
                    elif self.filterProgram[numItems][i] == '|':     
                        oneWord = False
                        resultado = resultado + ' or '
                    else:    
                        resultado = resultado + self.filterProgram[numItems][i]
                    i= i+1
                # testa se a nao termino com expressao negada 
                if endNot == False:
                    resultado = str(resultado + "\'"+ " in " + expressionProgram )
                resultado = resultado
                return eval(resultado)
            else:
                return True
        except Exception, e: 
            logging.error('Falha ao procurar palavras no evento', exc_info=True)
            self.sentExceptions(e, program, numItems)
            return False
            
    def formatLog(self, identifier, newLine, numItems):
        """
        Realiza o processo de formatação do log de acordo com as expressões encontradas
        no formatColumnType e com as colunas especificadas em formatColumn
        """
        try:
            exec("from " + self.fileExpression + " import *")
            formatColumn = re.split(',', str(self.formatColumn[numItems]))
            dataColumn = ''
            self.data = []
            formatColumnFinal = []
            expressionLog = Empty()
            expression = re.split(' ', str(self.formatColumnType[numItems]))
            i = 0
            #gi = pygeoip.GeoIP('/usr/share/GeoIP/GeoLiteCity.dat', pygeoip.const.GEOIP_STANDARD)
	    reader = geoip2.database.Reader('/usr/local/share/GeoIP/GeoLite2-City.mmdb')
            while i < len(expression):
                expressionLog = expressionLog + eval(expression[i])
                i = i + 1

            data = expressionLog.parseString(newLine)
            testMessage2 = True
            i = 0
            while i < len(formatColumn) :
                column = formatColumn[i].strip() 
		if column == 'os':
                        dataColumn = data.get("userAgent")
                else:
                        dataColumn = data.get(column)
                dataColumn = data.get(column)
                ## testa se nao possuia nada no campo mensagem e atribui o conteudo do cmapo mensagem2
                if dataColumn == None and column == "message":
                    dataColumn = data.get("message2")
                    testMessage2= False
                if dataColumn != None:
                    if column != "os" and column != "browser" and column != 'date_coll':
                        formatColumnFinal.append(column)
                    if column == "date_coll":
                        if '-' in dataColumn:
                            self.data.append(dataColumn)
                            formatColumnFinal.append("date_coll")                        
                        elif '.' in dataColumn:
                            microsecond = datetime.datetime.now().microsecond
                            dateTime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(float(dataColumn)))
                            dateTime = str(dateTime) + '.' + str(microsecond)
                            self.data.append(dateTime)
                            formatColumnFinal.append("date_coll")
                        else:
                            try:
                                int(dataColumn[0])
                                self.getDateApacheAccess(identifier, dataColumn, formatColumnFinal, newLine, numItems)
                            except :    
                                self.getDate(identifier, dataColumn, formatColumnFinal, newLine, numItems)
                    elif 'ip' in column:
			try:
                            self.data.append(dataColumn)
                            #geo_codes = gi.record_by_addr(str(dataColumn).strip())
                            ip = IP(str(dataColumn).strip())
			    if ip.iptype() != 'PRIVATE' and ip.iptype() != 'LOOPBACK' and ip != '' and ip.iptype() != 'RESERVED':
			    	geo_codes = reader.city(str(dataColumn).strip())
                            	if geo_codes != {}: 
                               	    self.getGeoIP(geo_codes, formatColumnFinal)
			except Exception, e:
            		    logging.error("Falha ao aplicar a geolocalização no IP: %s", str(dataColumn), exc_info=True)
                    elif column == "bytes":
                        self.data.append('0')
                    elif column == "os":
                        agent = httpagentparser.simple_detect(dataColumn)
                        # insere os campos gerados pelo httpagentparser(sistema operacional, navegador)
                        self.data.append(agent[0])
                        formatColumnFinal.append('os')
                        self.data.append(agent[1])
                        formatColumnFinal.append('browser')
                    elif column == "message":
                        message = str(dataColumn)
                        message = message.replace("\'", "\"")
                        message2 = data.get("message2")     
                        # testa se tem algo no campo mensagem2 e se tem q concatenar o calor no campo mensagem                   
                        if message2 != None and testMessage2:
                            message2 = message2.replace("\'", "\"")
                            message = message + message2                        
                        self.data.append(message)
                    else:
                        self.data.append(dataColumn)
                i = i + 1   

            # chama a o metodo para enviar os logs para o servidor
            self.serverCommunication.sendLog(identifier, self.table[numItems], formatColumnFinal,
                                                        self.data)
        except Exception, e: 
            logging.error('Falha ao realizar a formatação do log: %s', newLine, exc_info=True)
            # chama a funcao para enviar o log para a tabela de excecao pois durante a formatacao
            # aconteceu algum erro
            self.sentExceptions(identifier, e, newLine, numItems)
            
    # Metodo usado para enviar a excecao gerada e o log para a tabela exceptions
    def sentExceptions(self, identifier, e, newLine, numItems):
        """
        Metodo usado para enviar a excecao gerada e o log para a tabela exceptions
        """
        try:
            # pega a data atual
            date = datetime.datetime.now()
            date = date.strftime('%Y-%m-%d %H:%M:%S.%f')
            # adiciona o formato da tabela
            newformatColumn = ['date_coll', 'log', 'error', 'table_']
            newData = []
            newData.append(date)
            # pega a linha que deu erro e retira o \n, troca " por '
            errorLine = newLine[0:len(newLine)-1:]
            newData.append(errorLine.replace("\'", "\""))
            # pega o erro e troca " por '
            error = str(e)
            newData.append(error.replace("\'", "\""))
            newData.append(self.table[numItems])
            self.serverCommunication.sendLog(identifier, 'exceptions', newformatColumn,newData)
        except Exception, e:
            logging.error("Falha ao enviar eventos para a tabela de exceções", exc_info=True)  
    
 
    # Metodo usado apra inserir os dados gerados pelo GeoIP nos dados a serem enviados para o servidor,
    # metodo padrao para uso do GeoIp , ele tenta inserir os campos se forem vazios, insere zero, ou ''  
    def getGeoIP(self, geo_codes, formatColumnFinal):
        """
        Método usado para inserir os dados gerados pelo GeoIP nos dados
        a serem enviados para o servidor
        """
        try:
            # insere o campo cidade convertendo ele para a codificacao utf-8
            token = geo_codes.city.name.encode('utf-8') 
            self.data.append(token)
            formatColumnFinal.append('city')
        except Exception, e:
            logging.debug('Falha na geolocalização ao coletar a cidade', exc_info=True)
        try:
            # insere o campo estado convertendo ele para a codificacao utf-8
	    token = geo_codes.subdivisions.most_specific.name.encode('utf-8')
            self.data.append(token)
            formatColumnFinal.append('region_name')
        except Exception, e:
            logging.debug('Falha na geolocalização ao coletar a região', exc_info=True)
        try:
            # insere o campo latitude
            token = geo_codes.location.latitude
            self.data.append(str(token))
            formatColumnFinal.append('latitude')
            # insere o campo longitude
            token = geo_codes.location.longitude
            self.data.append(str(token))
            formatColumnFinal.append('longitude')
        except Exception, e:
            logging.debug('Falha na geolocalização ao coletar a latitude ou longitude', exc_info=True)
        try:
            # insere o campo pais convertendo ele para a codificacao utf-8
	    namesDict = geo_codes.country.names
            #if ('pt-BR' in namesDict):
            #    token = namesDict['pt-BR'].encode('utf-8')
            #else:
            token = namesDict['en'].encode('utf-8')
            self.data.append(token)
            formatColumnFinal.append('country_name')
        except Exception, e:
            logging.debug('Falha na geolocalização ao coletar o país', exc_info=True) 
    # Metodo usado para inserir a data nos dados a serem enviados para o servidor, metodo para inserir
    # a data dos logs com o formato padrao de datas         
    def getDate(self, identifier, dat, formatColumnFinal, newLine, numItems):
        """
        Método usado para inserir a data nos dados a serem enviados para o servidor
        """
        try:
            microsecond = datetime.datetime.now().microsecond
            date = dat
            # transforma o month em numero 
            month = strptime(str(date[0]) , '%b').tm_mon
            # separa a hour em hour, minutos e segundos 
            hour = re.split(':', date[2])
            # testa se a data do log vinha com o ano
            if len(date) == 4:
                year = date[3]
            # data padrao syslog sem o ano
            else: 
                year = datetime.datetime.now().year
            # converte para formato datetime
            # parametros ano, mes, dia, hora, minutos, segundos, microsegundos
            datetimeFormat = (datetime.datetime(int(year), int(month), int(date[1]),
                                                int(hour[0]), int(hour[1]), int(hour[2]),
                                                int(microsecond)))
            datetimeFormat = datetimeFormat.strftime('%Y-%m-%d %H:%M:%S.%f')
            self.data.append(datetimeFormat)
            formatColumnFinal.append("date_coll")
        except Exception, e: 
            # chama a funcao para enviar o log para a tabela de excecao pois durante a formatacao
            # aconteceu algum erro
            logging.error('Falha ao formatar a data no evento: %s' , newLine, exc_info=True)
            self.sentExceptions(identifier, e, newLine, numItems)
        
    # Metodo usado para inserir a data nos dados a serem enviados para o servidor, metodo para inserir
    # a data dos logs com o formato padrao de datas         
    def getDateApacheAccess(self, identifier, date, formatColumnFinal, newLine, numItems): 
        """
        Método usado para inserir a data dos logs apache access nos dados a serem 
        enviados para o servidor
        """
        try:
            microsecond = datetime.datetime.now().microsecond
            hour = re.split(':', date[3])
            month = strptime(date[1] , '%b').tm_mon
            # converte para formato datetime
            # parametros ano, mes, dia, hora, minutos, segundos, microsegundos
            datetimeFormat = (datetime.datetime(int(date[2]), int(month), int(date[0]),
                                                int(hour[0]), int(hour[1]), int(hour[2]),
                                                int(microsecond)))
            datetimeFormat = datetimeFormat.strftime('%Y-%m-%d %H:%M:%S.%f')
            # insere o campo data
            self.data.append(datetimeFormat)
            formatColumnFinal.append("date_coll")
        except Exception, e: 
            # chama a funcao para enviar o log para a tabela de excecao pois durante a formatacao
            # aconteceu algum erro
            logging.error('Falha ao formatar a data no evento do apache_access: %s' , newLine, exc_info=True)
            self.sentExceptions(identifier, e, newLine, numItems)
            

        
