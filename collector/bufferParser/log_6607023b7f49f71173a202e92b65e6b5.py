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
program = Combine(alpha + Optional(Suppress("-") + Suppress(integer)) + 
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
ip = Combine(integer + point + integer + point + integer + point + integer)
tosPrec = Suppress(Literal("TOS=") + integer + Optional(Literal("x") + integer) 
                               + Literal("PREC=") + integer + Literal("x") + integer)
id = Suppress(Literal("ID=") + integer)
inn = Combine(Suppress(Literal("IN=")) + interface)
out = Combine(Suppress(Literal("OUT=")) + Optional(interface))
mac = Suppress(Literal("MAC="))
source_ip = Combine(Suppress(Literal("SRC=")) + ip)
dest_ip = Combine(Suppress(Literal("DST=")) + ip)
lenn = Combine(Suppress(Literal("LEN=")) + integer)
ttl = Combine(Suppress(Literal("TTL=")) + integer)
proto = Combine(Suppress(Literal("PROTO=")) + alpha)
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
method = Combine(Suppress(aspas) + (Literal("GET") ^ Literal("HEAD") ^ Literal("POST") ^ 
                                       Literal("TRACE") ^ Literal("DELETE") ^ Literal("OPTIONS") ^ 
                                       Literal("CONNECT") ^ Literal("PACTH") ^ Literal("PUT") ^ 
                                       Literal("PROPFIND") ^ Literal("MERGE") ^ 
                                       Literal("CHECKOUT") ^ Literal("MKCOL") ^ 
                                       Literal("PROPPATCH") ^ Literal("REPORT") ^ 
                                       Literal("MKACTIVITY")))
url = Word(alphas + nums + "/" + "?" + "." + ":" + "_" + "=" + "$" + "&" + "%" + 
                       "-" + "@" + "," + "[" + "]" + "(" + ")" + "+" + "!" + ";" + "*")
protocol = Combine(alpha + bar + integer + point + integer + Suppress(Literal('"')))
bytes = integer
reffer = Combine(Suppress(aspas) + (hyphen ^ url) + Suppress(aspas))
userAgent = Combine(branco + restOfLine)
date_apache_error = Group(Suppress(lbrocket + alpha) + alpha + branco + 
                                      integer + branco + hora + integer + Suppress(rbrocket))
level = Combine(Suppress(lbrocket) + alpha + Suppress(rbrocket))
ip_apache_error = Combine(Suppress(lbrocket) + Suppress(alpha) + branco + ip + 
                                      Suppress(rbrocket))
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
apache_error = (Optional(date_apache_error.setResultsName("date_coll") + 
                                    level.setResultsName("level") + 
                                    Optional(ip_apache_error.setResultsName("ip"))) + 
                            message.setResultsName("message"))
apache_access = (ip.setResultsName("ip") + Suppress(hyphen) + 
                            userID.setResultsName("user_id") + 
                            date_apache_access.setResultsName("date_coll") + 
                            method.setResultsName("method") + url.setResultsName("url") + 
                            protocol.setResultsName("protocol") + 
                            integer.setResultsName("cod_return") + (bytes.setResultsName("bytes") 
                                                                    ^ Suppress(hyphen))+ 
                            reffer.setResultsName("ref") + userAgent.setResultsName("userAgent"))
shorewall = Optional(priority.setResultsName("priority"))+(date.setResultsName("date_coll") + hostname.setResultsName("hostname") + 
                         Suppress(alpha + colon) + orig_dest.setResultsName("orig_dest") + 
                         Suppress(colon) + policy.setResultsName("policy") + Suppress(colon) + 
                         inn.setResultsName("interface_in") + out.setResultsName("interface_out") 
                         + Optional(mac + macAddress.setResultsName("mac_dest") + Suppress(colon) 
                         + macAddress.setResultsName("mac_source") + Suppress(colon) + 
                         macType.setResultsName("mac_type")) + source_ip.setResultsName("source_ip")
                         + dest_ip.setResultsName("dest_ip") + lenn.setResultsName("len") + tosPrec 
                         + ttl.setResultsName("ttl") + id + Optional(flag) + Optional(frag) + 
                         Optional(opt) + proto.setResultsName("proto") + 
                         Optional(typ.setResultsName("type")) + Optional(cod) + 
                         Optional(source_port.setResultsName("source_port")) + 
                         Optional(dest_port.setResultsName("dest_port")) + 
                         Optional(seq.setResultsName("sequence")) + 
                         Optional(window.setResultsName("window_")))
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
status = ZeroOrMore((url + branco) ^ (url + branco + Literal("user") ) )
status2 = ZeroOrMore((url + branco) ^ (url + branco + Suppress(Literal("for")) ) )
status3 = ZeroOrMore((alpha + branco) ^ (alpha + Suppress(Literal(";") )) )
status4 = ZeroOrMore((url + branco) ^ (url + branco + Suppress(Literal("from")) ) )
Status = Combine(status)
Status2 = Combine(status2)
Status3 = Combine(status3)
Status4 = Combine(status4)
logname = Combine(Suppress(Literal("logname=")) + Optional(url))
uid = Combine(Suppress(Literal("uid=")) + Optional(integer))
euid = Combine(Suppress(Literal("euid=")) + Optional(integer))
tty = Combine(Suppress(Literal("tty=")) + Optional(alpha))
ruser = Combine(Suppress(Literal("ruser="))+ Optional(url))
rhost = Combine(Suppress(Literal("rhost=")) + Optional(url))
user = Combine(Suppress(Literal("user="))+ Optional(url))
ssh = (date.setResultsName("date_coll")+ hostname.setResultsName("hostname") + program.setResultsName("program") + Optional(Suppress(Literal("User")) + url.setResultsName("user_ssh") + Suppress(Literal("from")) + ip.setResultsName("ip")) + Optional(Suppress(Literal("User")) + url.setResultsName("user_ssh")  + Suppress(Literal("from")) + url.setResultsName("domain")) + Optional(Status.setResultsName("status_ssh") + url.setResultsName("user_ssh") + Suppress(Literal("from")) + ip.setResultsName("ip")) + Optional(Status2.setResultsName("status_ssh") + url.setResultsName("user_ssh") + Suppress(Literal("from")) + ip.setResultsName("ip")) + Optional(Status4.setResultsName("message")+ ip.setResultsName("ip")) + Optional(branco + Suppress(Literal("port")) + integer.setResultsName("port") + alphaInteger.setResultsName("protocol")) + Optional(program.setResultsName("auth_method") + Status3.setResultsName("status_ssh") +  logname.setResultsName("logname")  + Optional(uid.setResultsName("uid") ) + Optional(euid.setResultsName("euid") ) + Optional(tty.setResultsName("tty") ) + Optional(ruser.setResultsName("ruser") ) + Optional(rhost.setResultsName("rhost") ) + Optional(user.setResultsName("user_ssh"))) + Optional(program.setResultsName("auth_method") + Status.setResultsName("status_ssh") + url.setResultsName("user_ssh")) + Optional(program.setResultsName("auth_method") + Status3.setResultsName("status_ssh") ) + Optional(Status2.setResultsName("message") + url.setResultsName("domain") + Suppress(Literal("[")) + ip.setResultsName("ip") + Suppress(Literal("]"))) + Optional(message.setResultsName("message2")))
