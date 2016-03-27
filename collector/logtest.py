#!/usr/bin/python
# -*- coding: utf-8 -*-

from pyparsing import * 
import logging
import geoip2.database
from IPy import IP


def geoip(s, l, t):
	reader = geoip2.database.Reader('/usr/local/share/GeoIP/GeoLite2-City.mmdb')
	try:	
        	ip = IP(str(t[0]))
                if ip.iptype() != 'PRIVATE' and ip.iptype() != 'LOOPBACK' and ip != '' and ip.iptype() != 'RESERVED':
                	geo_codes = reader.city(t[0])
                        if geo_codes != {}:
            			# insere o campo pais convertendo ele para a codificacao utf-8
            			namesDict = geo_codes.country.names
            			token = namesDict['pt-BR'].encode('utf-8')
            			t['country_name'] = token
				token = geo_codes.location.latitude
				t['latitude'] = token
				token = geo_codes.location.longitude
				t['longitude'] = token
	except Exception, e:
		logging.error("Falha ao aplicar a geolocalização no IP", exc_info=True)	

def setVar(var_name, var_value):
    def parseAction(tokens):
        tokens[var_name] = var_value
    return parseAction

integer = Word(nums)
alpha = Word(alphas)
alphaInteger = Word(alphanums)
pointHyphen = Word("-" + ".")
specialCaracter = Word("-" + "_" + "." + "/")
ipv4 = Combine(integer + "." + integer + "." + integer + "." + integer)
timestamp = Word(nums, max=10 )
hostname = Combine(alphaInteger + ZeroOrMore((pointHyphen + alphaInteger)))
specialCaracter = Word("-" + "_" + "." + "/")
linuxpath = Combine(OneOrMore(specialCaracter + alpha))
beginning = Suppress(Literal("AV - Alert - "))
ruleIDName = Suppress(SkipTo('RID: "', include=True))
ruleLevelName = Suppress(Literal('"; RL: "'))
ruleGroupName = Suppress(Literal('"; RG: '))
ruleCommentName = Suppress(Literal("; RC: "))
userName = Suppress(Literal("; USER: "))
srcipName = Suppress(Literal('; SRCIP: "'))
hostnameName = Suppress(Literal('"; HOSTNAME: "('))
locationName = Suppress(Literal('"; LOCATION: '))
eventName = Suppress(SkipTo("; EVENT: ", include=True))
ossec = beginning + dblQuotedString.setResultsName("timestamp").setParseAction(removeQuotes) + ruleIDName + integer.setResultsName("rule_id") + ruleLevelName + integer.setResultsName("rule_level") + ruleGroupName + dblQuotedString.setResultsName("rule_group").setParseAction(removeQuotes) + ruleCommentName + dblQuotedString.setResultsName("rule_comment").setParseAction(removeQuotes) + userName +  dblQuotedString.setResultsName("user").setParseAction(removeQuotes) + srcipName + ipv4.setResultsName("srcip").setParseAction(geoip) + hostnameName + hostname.setResultsName("hostname") + Suppress(Literal(") ")) + ipv4.setResultsName("dstip") + Suppress(Literal("->")) + linuxpath.setResultsName("location") + locationName + eventName + dblQuotedString.setResultsName("event").setParseAction(removeQuotes) + Suppress(Literal(";")) + Empty().setParseAction(setVar("category","authentication")) + Empty().setParseAction(setVar("sub_category","failed")) + Empty().setParseAction(setVar("priority","5"))

log = 'AV - Alert - "1445109839" --> RID: "11306"; RL: "10"; RG: "syslog,pure-ftpd,authentication_failures,"; RC: "FTP brute force (multiple failed logins)."; USER: "None"; SRCIP: "200.17.160.80"; HOSTNAME: "(webserver2) 192.168.0.2->/var/log/messages"; LOCATION: "(webserver2) 192.168.0.2->/var/log/messages"; EVENT: "[INIT]Oct 17 16:11:27 webserver2 pure-ftpd: (?@192.168.0.10) [WARNING] Authentication failed for user [webmaster][END]";' 

print ossec.parseString(log).asDict()
