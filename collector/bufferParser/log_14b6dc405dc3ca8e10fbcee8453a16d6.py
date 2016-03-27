# -*- coding: utf-8 -*-

from pyparsing import * 

branco = ZeroOrMore(" ")
colon = Literal(":")
lbrace = Literal("(")
rbrace = Literal(")")
lbrocket = Literal("[")
rbrocket = Literal("]")
underline = Literal("_")
hyphen = Literal("-")
point = Literal(".")
less = Literal("<")
more = Literal(">")
comma = Literal(",")
integer = Word(nums)
alpha = Word(alphas)
alphaInteger = Word(nums + alphas)
pointHyphen = Word("-" + ".")
specialCaracter = Word("-" + "_" + "." + "/")
aspas = Literal('"')
bar = Literal("/")
underlineAlpha = Word("_" + alphas)
hora = Combine(integer + colon + integer + colon + integer)
date = Group(alpha + branco + integer + branco + hora)
pid = lbrocket + branco + integer + branco + rbrocket
program = Combine(ZeroOrMore(specialCaracter ^ alpha) + Optional(Suppress("-") + Suppress(integer)) + 
                              ZeroOrMore(specialCaracter + alpha) + Optional(Suppress(pid)) + 
                              Optional(lbrace + alpha + colon + alpha + rbrace) + 
                              Optional(alphaInteger) + Suppress(colon))
hostname = Combine(alphaInteger + ZeroOrMore((pointHyphen + alphaInteger)))
priority = Combine(Suppress(less)+ integer + Suppress(more))
orig_dest = alphaInteger
message = restOfLine
numProgram = Literal("[") + integer + Optional(Literal(".") + integer) + Literal("]")
policy = alpha
interface = alphaInteger
macAddress = Combine(alphaInteger + colon + alphaInteger + colon + alphaInteger + 
                                 colon +  alphaInteger + colon + alphaInteger + colon + 
                                 alphaInteger)
macType = Combine(integer + colon + integer)
ip = Combine(integer + point + integer + point + integer + point + integer) ^ Combine( Optional(Suppress(lbrocket)) + Optional( (alphaInteger + (colon ^ (colon + colon))) ^ (colon + colon)) +  Optional( (alphaInteger + (colon ^ (colon + colon))) ^ (colon + colon)) + Optional( (alphaInteger + (colon ^ (colon + colon))) ^ (colon + colon)) + Optional( (alphaInteger + (colon ^ (colon + colon))) ^ (colon + colon)) +  Optional( (alphaInteger + (colon ^ (colon + colon))) ^ colon + colon) + Optional(alphaInteger + colon) + Optional(Combine(integer + point + integer + point + integer + point + integer)) + Optional(alphaInteger) + Optional(Suppress(rbrocket)) + Optional( colon + alphaInteger) )
tosPrec = Suppress(Literal("TOS=") + integer + Optional(Literal("x") + alphaInteger) 
                               + Literal("PREC=") + integer + Literal("x") + alphaInteger)
id = Suppress(Literal("ID=") + integer)
inn = Combine(Suppress(Literal("IN=")) + Optional(interface))
out = Combine(Suppress(Literal("OUT=")) + Optional(interface))
mac = Suppress(Literal("MAC="))
source_ip = Combine(Suppress(Literal("SRC=")) + ip)
dest_ip = Combine(Suppress(Literal("DST=")) + ip)
lenn = Combine(Suppress(Literal("LEN=")) + integer)
ttl = Combine(Suppress(Literal("TTL=")) + integer)
proto = Combine(Suppress(Literal("PROTO=")) + alphaInteger)
typ = Combine(Suppress(Literal("TYPE=")) + integer)
source_port = Combine(Suppress(Literal("SPT=")) + integer)
dest_port = Combine(Suppress(Literal("DPT=")) + integer)
seq = Combine(Suppress(Literal("SEQ=")) + integer)
window = Combine(Suppress(Literal("WINDOW=")) + integer)
flag = Suppress(ZeroOrMore(Literal("DF") ^ Literal("MF") ^ Literal("CE")))
frag = Suppress(Literal("FRAG=") + integer)
cod = Suppress(Literal("COD=") + integer)
opt = Suppress(Literal("OPT(") + alphaInteger + Literal(")"))
timeZoneOffset = Word("+-", nums)
date_apache_access = Group(Suppress(lbrocket) + integer + Suppress(bar) + alpha + 
                                    Suppress(bar) + integer + Suppress(colon) + hora + 
                                    Suppress(timeZoneOffset) + Suppress(rbrocket))
userID = ("-" | Word(alphas + nums + "@._"))
method = Combine(Suppress(aspas) + (Literal("GET") ^ Literal("HEAD") ^ Literal("COOK") ^ Literal("POST") ^ Literal("TRACE") ^ Literal("DELETE") ^ Literal("OPTIONS") ^ Literal("CONNECT") ^ Literal("PACTH") ^ Literal("PUT") ^ Literal("PROPFIND") ^ Literal("MERGE") ^ Literal("CHECKOUT") ^ Literal("MKCOL") ^ Literal("PROPPATCH") ^ Literal("REPORT") ^ Literal("MKACTIVITY") ^ hyphen) + Optional(Suppress(aspas)))
url = Combine("/" + Optional(Word(alphas + nums + "/" + "?" + "'" + "." + ":" + "_" + "=" + ">" + "<" + "{" + "}" +"$" + "&" + "%" + "-" + "@" + "," + "[" + "]" + "(" + ")" + "+" + "!" + ";" + "*" + "|" + "~" + "\\"))) ^ Combine("http" +  Optional(Word(alphas + nums + "/" + "?" + "'" + "." + ":" + "_" + "=" +">" + "<" + " " + "^" + "{" + "}" + "$" + "&" + "%" + "-" + "@" + "," + "[" + "]" + "(" + ")" + "+" + "!" + ";" + "*" + "|" + "~" + "\\"))) ^ "*" ^ Combine(Word(alphas + nums + "/" + "?" + "'" + "." + ":" + "_" + "=" + "$" + "&" + "%" + "-" + "@" + "," + "[" + "]" + "(" + ")" + "+" + "!" + ";" + "*" + "|" + "~" + "\\" + "{" + "}" + "#" + "^" + '"' + "<" + ">"))
protocol = Combine(alpha + bar + integer + point + integer + Suppress(Literal('"'))) ^ Combine(Suppress(aspas) + "-" + Suppress(aspas))
bytes = integer
reffer_old = Combine(Suppress(aspas) + Optional(hyphen ^ url) + Suppress(aspas))
userAgent = Combine(branco + restOfLine)
date_apache_error = Group(Suppress(lbrocket + alpha) + alpha + branco + 
                                      integer + branco + hora + integer + Suppress(rbrocket))
level = Combine(Suppress(lbrocket) + alpha + Suppress(rbrocket))
ip_apache_error = Combine(Suppress(lbrocket) + Suppress(alpha) + Suppress(branco) + ip + Optional(Suppress(rbrocket)))
data_postgres = Combine(integer + hyphen + integer + hyphen + integer + branco + hora)
client_hostname = Combine(Suppress(lbrace) + hostname + Suppress(rbrace))
mac_dhcpd = Combine(Optional(Suppress(lbrace)) + macAddress + 
                                Optional(Suppress(rbrace)))
ip_server = Combine(Suppress(lbrace) + ip + Suppress(rbrace))
date_unix = Combine(integer + point + integer)
result_trans = Combine(alpha + Optional(underlineAlpha) )
srv_cache = Combine(Suppress(alpha+Optional(underlineAlpha) + bar) + (ip ^ hyphen ^ url))
date_vsftpd = Group(Suppress(alpha)+alpha + branco + integer + branco + hora + integer)
pid_vsftpd = Combine(lbrocket + alpha + branco+ integer + rbrocket)
user_id = Combine(Suppress(lbrocket)+ alpha  + Suppress(rbrocket)  )
velocity = Combine(integer + point + integer +alpha + bar + alpha  )
vsftpd = (date_vsftpd.setResultsName("date_coll") + Suppress(pid_vsftpd) + 
                      Optional(user_id.setResultsName("user_id") + alpha.setResultsName("status")) 
                      + alpha.setResultsName("command")+ Suppress(colon) + Suppress(alpha) + 
                      Suppress(aspas)+ ip.setResultsName("ip") +Suppress(aspas)+ 
                      Optional(Suppress(comma))+Optional(Suppress(aspas)+url.setResultsName("data") 
                                                         + Suppress(aspas))+ Optional(Suppress(comma))+
                      Optional(integer.setResultsName("bytes")+Suppress("bytes"))+ 
                      Optional(Suppress(comma)) + Optional(velocity.setResultsName("velocity"))  )
squid = (date_unix.setResultsName("date_coll") + integer.setResultsName("time_proc") 
                     + ip.setResultsName("ip") + result_trans.setResultsName("result_trans") 
                     + Suppress(bar) + integer.setResultsName("cod_return") + 
                     integer.setResultsName("bytes") + alpha.setResultsName("method") + 
                     url.setResultsName("url") + Suppress(hyphen) + 
                     srv_cache.setResultsName("srv_cache") + message.setResultsName("type"))
dhcpd = Optional(priority.setResultsName("priority"))+(date.setResultsName("date_coll") + hostname.setResultsName("hostname") + 
                    program.setResultsName("program") + Optional(alpha.setResultsName("command") + Suppress(alpha) + 
                    Optional(Optional(ip.setResultsName("ip")) + 
                             Optional(ip_server.setResultsName("ip_server")) + 
                             Optional(Suppress(alpha)) + Optional(mac_dhcpd.setResultsName("mac")) + 
                             Optional(client_hostname.setResultsName("client_hostname")) + 
                             Suppress(alpha) + interface.setResultsName("interface")) 
                                                 ) + message.setResultsName("message"))
postgresql = (data_postgres.setResultsName("date_coll") + branco + Suppress(alpha) + 
                          branco + alpha.setResultsName("level") + Suppress(colon) + branco + 
                          message.setResultsName("message"))
shorewall = Optional(priority.setResultsName("priority"))+(date.setResultsName("date_coll") + hostname.setResultsName("hostname") + Suppress(alpha + colon) + orig_dest.setResultsName("orig_dest") + Suppress(colon) + policy.setResultsName("policy") + Suppress(colon) +                          inn.setResultsName("interface_in") + out.setResultsName("interface_out") + Optional(mac + Optional(macAddress.setResultsName("mac_dest") + Suppress(colon) + macAddress.setResultsName("mac_source") + Suppress(colon) + macType.setResultsName("mac_type"))) + source_ip.setResultsName("source_ip") + dest_ip.setResultsName("dest_ip") + lenn.setResultsName("len") + tosPrec + ttl.setResultsName("ttl") + id + Optional(flag) + Optional(frag) + Optional(opt) + proto.setResultsName("proto") + Optional(typ.setResultsName("type")) + Optional(cod) + Optional(source_port.setResultsName("source_port")) + Optional(dest_port.setResultsName("dest_port")) + Optional(seq.setResultsName("sequence")) + Optional(window.setResultsName("window_")))
syslog = Optional(priority.setResultsName("priority"))+(date.setResultsName("date_coll") + hostname.setResultsName("hostname") + 
                      program.setResultsName("program") + 
                      message.setResultsName("message")) ^ (date.setResultsName("date_coll") + 
                      program.setResultsName("program") + branco + message.setResultsName("message"))
level_php = Combine(alpha + Suppress(colon))
apache_php = Optional(priority.setResultsName("priority"))+((date.setResultsName("date_coll") + hostname.setResultsName("hostname") 
                          + program.setResultsName("program")+  level_php.setResultsName("level") + branco + 
                          message.setResultsName("message")) ^ 
                          (date.setResultsName("date_coll") + program.setResultsName("program") + 
                           level_php.setResultsName("level") + branco + 
                           message.setResultsName("message")))
Status = Combine(url + branco + OneOrMore((url + branco) + (Literal("user") ) ))
Status2 = Combine(url + branco + OneOrMore((url + branco) + (Suppress(Literal("for")) ) ))
Status3 = Combine(url + branco + OneOrMore((alpha + branco) + (Suppress(Literal(";") )) ))
Status4 = Combine(url + branco + OneOrMore((url + branco) + (Suppress(Literal("from")) ) ))
url_apache = Combine("/" + Optional(Word(alphas + nums + "/" + "?" + "'" + "." + ":" + "_" + "=" + ">" + "<" + " "+ "^" + "{" + "}" +"$" + "&" + "%" + "-" + "@" + "," + "[" + "]" + "(" + ")" + "+" + "!" + ";" + "*" + "|" + "~" + "\\"))) ^ Combine("http" +  Optional(Word(alphas + nums + "/" + "?" + "'" + "." + ":" + "_" + "=" +">" + "<" + " " + "^" + "{" + "}" + "$" + "&" + "%" + "-" + "@" + "," + "[" + "]" + "(" + ")" + "+" + "!" + ";" + "*" + "|" + "~" + "\\"))) ^ "*"
url_apache2 = Combine("/" + Optional(Word(alphas + nums + "/" + "?" + "'" + "." + ":" + "_" + "=" + ">" + "<" + "{" + "}"+ "^" +"$" + "&" + "%" + "-" + "@" + "," + "[" + "]" + "(" + ")" + "+" + "!" + ";" + "*" + "|" + "~" + "\\"))) ^ Combine("http" +  Optional(Word(alphas + nums + "/" + "?" + "'" + "." + ":" + "_" + "=" +">" + "<" + "^" + "{" + "}" + "$" + "&" + "%" + "-" + "@" + "," + "[" + "]" + "(" + ")" + "+" + "!" + ";" + "*" + "|" + "~" + "\\"))) ^ "*"
reffer = Combine(Suppress(aspas) + Optional(hyphen ^ url_apache) + Suppress(aspas))
apache_access = (ip.setResultsName("ip") + Suppress(hyphen) + userID.setResultsName("user_id") + date_apache_access.setResultsName("date_coll") + Optional(method.setResultsName("method")) + Optional(url_apache2.setResultsName("url")) + Optional(protocol.setResultsName("protocol")) + Optional(integer.setResultsName("cod_return")) + Optional((bytes.setResultsName("bytes")) ^ Optional(Suppress(hyphen))) + reffer.setResultsName("ref") + userAgent.setResultsName("userAgent"))
logname = Combine(Suppress(Literal("logname=")) + Optional(url))
uid = Combine(Suppress(Literal("uid=")) + Optional(integer))
euid = Combine(Suppress(Literal("euid=")) + Optional(integer))
tty = Combine(Suppress(Literal("tty=")) + Optional(alpha))
ruser = Combine(Suppress(Literal("ruser="))+ Optional(url))
rhost = Combine(Suppress(Literal("rhost=")) + Optional(url))
user = Combine(Suppress(Literal("user="))+ Optional(url))
ssh = (date.setResultsName("date_coll") + hostname.setResultsName("hostname") + program.setResultsName("program") + Optional(program.setResultsName("auth_method")) + Optional(Status3.setResultsName("status_ssh")) +  Optional(logname.setResultsName("logname"))  + Optional(uid.setResultsName("uid") ) + Optional(euid.setResultsName("euid") ) + Optional(tty.setResultsName("tty") ) + Optional(ruser.setResultsName("ruser") ) + Optional(rhost.setResultsName("rhost") ) + Optional(user.setResultsName("user_ssh")) + Optional(program.setResultsName("auth_method") + Status.setResultsName("status_ssh") + url.setResultsName("user_ssh")) + Optional(program.setResultsName("auth_method") + Status3.setResultsName("status_ssh") ) + Optional(Status2.setResultsName("message") + url.setResultsName("domain") + Suppress(Literal("[")) + ip.setResultsName("ip") + Suppress(Literal("]"))) + Optional(program.setResultsName("auth_method") + Status2.setResultsName("status_ssh") ) + Optional(Suppress(Literal("User")) + url.setResultsName("user_ssh") + Suppress(Literal("from")) + ip.setResultsName("ip")) + Optional(Suppress(Literal("User")) + url.setResultsName("user_ssh")  + Suppress(Literal("from")) + url.setResultsName("domain")) + Optional(Status.setResultsName("status_ssh") + url.setResultsName("user_ssh") + Suppress(Literal("from")) + ip.setResultsName("ip")) + (Optional(Status2.setResultsName("status_ssh") + url.setResultsName("user_ssh") + Suppress(Literal("from")) + ip.setResultsName("ip")) ^ Optional(Status4.setResultsName("status_ssh")+ ip.setResultsName("ip"))) + Optional(branco + Suppress(Literal("port")) + integer.setResultsName("port") + alphaInteger.setResultsName("protocol")) + Optional(Suppress(Literal("user")) + url.setResultsName("user_ssh"))+ Optional(Suppress(Literal(":")) + integer.setResultsName("disconnect_reason") + Suppress(Literal(":")) )+ Optional(Suppress(branco)) +Optional(message.setResultsName("message2")))
date_assp = Group(alpha + Suppress(hyphen) + integer + Suppress(hyphen) + Suppress(integer) + hora)
assp_id = Combine(alphaInteger + hyphen + alphaInteger + hyphen+ alphaInteger)
thread = (Suppress(lbrocket) + Combine(alphaInteger+underline+alphaInteger) + Suppress(rbrocket) ) |(Combine(alphaInteger+underline+alphaInteger) )
status_assp = Combine(OneOrMore(alpha +branco))
action = Suppress(hyphen + hyphen) + branco + message
session = Suppress(Literal('session:')) + alphaInteger
name_type = Combine(alpha + branco +alpha)
message_type = (hostname+ Suppress(colon) ) | (Suppress(lbrocket) + name_type  + Suppress(rbrocket))
result_tag = Combine(Suppress(lbrocket) + alpha + Suppress(rbrocket))
assp = (date_assp.setResultsName('date_coll') + Optional(assp_id.setResultsName('assp_id')) + thread.setResultsName('thread') + Optional(result_tag.setResultsName('result_tag')) + Optional(status_assp.setResultsName('status') + action.setResultsName('action')) + Optional(status_assp.setResultsName('status')+ Suppress(colon) + session.setResultsName('session')) + Optional(ip.setResultsName('source_ip') + Suppress(colon) + integer.setResultsName('source_port') +more+ ip.setResultsName('assp_ip')+ Suppress(colon) + integer.setResultsName('assp_port')+more + ip.setResultsName('postfix_ip')+ Suppress(colon) + integer.setResultsName('postfix_port')) + Optional(ip.setResultsName('source_ip') + Suppress(less) + url.setResultsName('source_mail') + Suppress(more)+ Optional(Suppress('to:')+ url.setResultsName('dest_mail'))+ Optional(message_type.setResultsName('message_type'))+ message.setResultsName('message')) + Optional(status_assp('status') + message.setResultsName('message')))
specialCaracter_ms = Word("/" + "?" + "." + ":" + "_" + "=" + "$" + "&" + "%" + "-" + "@" + "," + "[" + "]" + "(" + ")" + "+" + "!" + ";" + "*" + "|" + "~" + "\\" + "{" + "}")
file_ms = Combine(OneOrMore(alpha + branco ^ integer + branco ^ specialCaracter_ms + branco))
pointInteger = Combine(OneOrMore((integer +point) ^ integer))
message_ms = Literal("ModSecurity: ") + OneOrMore(url +
                         Optional(Suppress(Literal('[file "')) + file_ms.setResultsName("file") + Suppress(Literal('"]')) ) +
                         Optional(Suppress(Literal('[line "')) + integer.setResultsName("line") + Suppress(Literal('"]')) ) +
                         Optional(Suppress(Literal('[id "')) + integer.setResultsName("id") + Suppress(Literal('"]')) ) +
                         Optional(Suppress(Literal('[rev "')) + pointInteger.setResultsName("rev") + Suppress(Literal('"]')) ) +
                         Optional(Suppress(Literal('[msg "')) + file_ms.setResultsName("msg") + Suppress(Literal('"]')) ) +
                         Optional(Suppress(Literal('[severity "')) + alpha.setResultsName("severity") + Suppress(Literal('"]')) ) +
                         Optional(Suppress(Literal('[hostname "')) + hostname.setResultsName("hostname") + Suppress(Literal('"]')) ) +
                         Optional(Suppress(Literal('[uri "')) + file_ms.setResultsName("uri") + Suppress(Literal('"]')) ) +
                         Optional(Suppress(Literal('[unique_id "')) + file_ms.setResultsName("unique_id") + Suppress(Literal('"]')) )
                         )
apache_error = (Optional(date_apache_error.setResultsName("date_coll") +
                                    level.setResultsName("level") +
                                    Optional(ip_apache_error.setResultsName("ip"))) + Optional(message_ms.setResultsName("message")) +
                                message.setResultsName("message"))
