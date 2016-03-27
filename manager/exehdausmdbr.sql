--
-- PostgreSQL database dump
--

-- Dumped from database version 9.4.6
-- Dumped by pg_dump version 9.4.6
-- Started on 2016-03-27 01:07:34 BRT

SET statement_timeout = 0;
SET lock_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SET check_function_bodies = false;
SET client_min_messages = warning;

--
-- TOC entry 1 (class 3079 OID 11861)
-- Name: plpgsql; Type: EXTENSION; Schema: -; Owner: -
--

CREATE EXTENSION IF NOT EXISTS plpgsql WITH SCHEMA pg_catalog;


--
-- TOC entry 2127 (class 0 OID 0)
-- Dependencies: 1
-- Name: EXTENSION plpgsql; Type: COMMENT; Schema: -; Owner: -
--

COMMENT ON EXTENSION plpgsql IS 'PL/pgSQL procedural language';


SET search_path = public, pg_catalog;

--
-- TOC entry 173 (class 1259 OID 16728)
-- Name: id_sequence_hosts; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE id_sequence_hosts
    START WITH 10054
    INCREMENT BY 1
    MINVALUE 10001
    NO MAXVALUE
    CACHE 1;


SET default_tablespace = '';

SET default_with_oids = false;

--
-- TOC entry 174 (class 1259 OID 16730)
-- Name: hosts; Type: TABLE; Schema: public; Owner: -; Tablespace: 
--

CREATE TABLE hosts (
    hostid bigint DEFAULT nextval('id_sequence_hosts'::regclass) NOT NULL,
    host character varying(64) NOT NULL,
    name character varying(255),
    available integer NOT NULL,
    status integer NOT NULL,
    correlation smallint NOT NULL,
    criticality smallint NOT NULL
);


--
-- TOC entry 175 (class 1259 OID 16734)
-- Name: id_sequence_hosts_templates; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE id_sequence_hosts_templates
    START WITH 10043
    INCREMENT BY 1
    MINVALUE 10001
    NO MAXVALUE
    CACHE 1;


--
-- TOC entry 176 (class 1259 OID 16736)
-- Name: hosts_templates; Type: TABLE; Schema: public; Owner: -; Tablespace: 
--

CREATE TABLE hosts_templates (
    hosttemplateid bigint DEFAULT nextval('id_sequence_hosts_templates'::regclass) NOT NULL,
    hostid bigint NOT NULL,
    templateid bigint NOT NULL
);


--
-- TOC entry 177 (class 1259 OID 16742)
-- Name: id_sequence_exceptions; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE id_sequence_exceptions
    START WITH 7486
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- TOC entry 178 (class 1259 OID 16744)
-- Name: id_sequence_items_hosts; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE id_sequence_items_hosts
    START WITH 11938
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- TOC entry 179 (class 1259 OID 16746)
-- Name: id_sequence_items_situations_hosts; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE id_sequence_items_situations_hosts
    START WITH 40
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- TOC entry 180 (class 1259 OID 16748)
-- Name: id_sequence_items_situations_templates; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE id_sequence_items_situations_templates
    START WITH 10028
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- TOC entry 181 (class 1259 OID 16750)
-- Name: id_sequence_items_templates; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE id_sequence_items_templates
    START WITH 10100
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- TOC entry 182 (class 1259 OID 16752)
-- Name: id_sequence_library_expression; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE id_sequence_library_expression
    START WITH 90
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- TOC entry 183 (class 1259 OID 16754)
-- Name: id_sequence_situations_hosts; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE id_sequence_situations_hosts
    START WITH 46
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- TOC entry 184 (class 1259 OID 16756)
-- Name: id_sequence_situations_templates; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE id_sequence_situations_templates
    START WITH 18
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- TOC entry 185 (class 1259 OID 16758)
-- Name: id_sequence_template; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE id_sequence_template
    START WITH 10003
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- TOC entry 186 (class 1259 OID 16769)
-- Name: items_hosts; Type: TABLE; Schema: public; Owner: -; Tablespace: 
--

CREATE TABLE items_hosts (
    itemid bigint DEFAULT nextval('id_sequence_items_hosts'::regclass) NOT NULL,
    hostid bigint NOT NULL,
    name character varying(255) NOT NULL,
    key_ character varying(255) NOT NULL,
    delay integer NOT NULL,
    lastvalue text,
    datecoll timestamp(6) without time zone,
    datepub timestamp(6) without time zone,
    status integer NOT NULL,
    errmsg character varying(255),
    table_ character varying(30),
    filterprogram character varying(255),
    itemiditemstemplate bigint,
    itemidhosts bigint,
    formatcolumn text,
    formatcolumntype character varying(255),
    formatcolumntypedata text,
    formatcolumnname text,
    formatcolumnvisible character varying(255),
    identifier character varying(255)
);


--
-- TOC entry 187 (class 1259 OID 16776)
-- Name: items_situations_hosts; Type: TABLE; Schema: public; Owner: -; Tablespace: 
--

CREATE TABLE items_situations_hosts (
    itemid integer NOT NULL,
    situationid integer NOT NULL,
    itemsituationid integer DEFAULT nextval('id_sequence_items_situations_hosts'::regclass) NOT NULL,
    hostid bigint NOT NULL,
    status smallint NOT NULL,
    correlation smallint NOT NULL
);


--
-- TOC entry 188 (class 1259 OID 16780)
-- Name: items_situations_templates; Type: TABLE; Schema: public; Owner: -; Tablespace: 
--

CREATE TABLE items_situations_templates (
    itemid integer NOT NULL,
    situationid integer NOT NULL,
    itemsituationid integer DEFAULT nextval('id_sequence_items_situations_templates'::regclass) NOT NULL
);


--
-- TOC entry 189 (class 1259 OID 16784)
-- Name: items_templates; Type: TABLE; Schema: public; Owner: -; Tablespace: 
--

CREATE TABLE items_templates (
    itemid bigint DEFAULT nextval('id_sequence_items_templates'::regclass) NOT NULL,
    templateid bigint NOT NULL,
    name character varying(255) NOT NULL,
    key_ character varying(255) NOT NULL,
    delay integer NOT NULL,
    status integer NOT NULL,
    table_ character varying(30),
    filterprogram character varying(255),
    formatcolumn text,
    formatcolumntype character(255),
    formatcolumntypedata text,
    formatcolumnname text,
    formatcolumnvisible character varying(255),
    identifier character varying(255)
);


--
-- TOC entry 190 (class 1259 OID 16791)
-- Name: library_expression; Type: TABLE; Schema: public; Owner: -; Tablespace: 
--

CREATE TABLE library_expression (
    name character(255) NOT NULL,
    expression text NOT NULL,
    id_name bigint DEFAULT nextval('id_sequence_library_expression'::regclass) NOT NULL
);


--
-- TOC entry 191 (class 1259 OID 16857)
-- Name: situations_hosts; Type: TABLE; Schema: public; Owner: -; Tablespace: 
--

CREATE TABLE situations_hosts (
    description text NOT NULL,
    epl text NOT NULL,
    situationid integer DEFAULT nextval('id_sequence_situations_hosts'::regclass) NOT NULL,
    command text,
    commandtype character varying(255),
    comments text,
    to_ character(255),
    subject character(255),
    body text,
    situationhostsid integer,
    severity smallint NOT NULL,
    occurrences smallint NOT NULL
);


--
-- TOC entry 192 (class 1259 OID 16864)
-- Name: situations_templates; Type: TABLE; Schema: public; Owner: -; Tablespace: 
--

CREATE TABLE situations_templates (
    description text NOT NULL,
    epl text NOT NULL,
    situationid integer DEFAULT nextval('id_sequence_situations_templates'::regclass) NOT NULL,
    command text,
    commandtype character varying(255),
    comments text,
    status smallint NOT NULL,
    to_ character(255),
    subject character(255),
    body text,
    correlation smallint NOT NULL,
    severity smallint NOT NULL,
    occurrences smallint
);


--
-- TOC entry 193 (class 1259 OID 16871)
-- Name: templates; Type: TABLE; Schema: public; Owner: -; Tablespace: 
--

CREATE TABLE templates (
    templateid bigint DEFAULT nextval('id_sequence_template'::regclass) NOT NULL,
    name character varying(255)
);


--
-- TOC entry 2101 (class 0 OID 16730)
-- Dependencies: 174
-- Data for Name: hosts; Type: TABLE DATA; Schema: public; Owner: -
--

COPY hosts (hostid, host, name, available, status, correlation, criticality) FROM stdin;
\.


--
-- TOC entry 2103 (class 0 OID 16736)
-- Dependencies: 176
-- Data for Name: hosts_templates; Type: TABLE DATA; Schema: public; Owner: -
--

COPY hosts_templates (hosttemplateid, hostid, templateid) FROM stdin;
\.


--
-- TOC entry 2128 (class 0 OID 0)
-- Dependencies: 177
-- Name: id_sequence_exceptions; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('id_sequence_exceptions', 7486, false);


--
-- TOC entry 2129 (class 0 OID 0)
-- Dependencies: 173
-- Name: id_sequence_hosts; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('id_sequence_hosts', 10073, true);


--
-- TOC entry 2130 (class 0 OID 0)
-- Dependencies: 175
-- Name: id_sequence_hosts_templates; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('id_sequence_hosts_templates', 10065, true);


--
-- TOC entry 2131 (class 0 OID 0)
-- Dependencies: 178
-- Name: id_sequence_items_hosts; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('id_sequence_items_hosts', 13421, true);


--
-- TOC entry 2132 (class 0 OID 0)
-- Dependencies: 179
-- Name: id_sequence_items_situations_hosts; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('id_sequence_items_situations_hosts', 200, false);


--
-- TOC entry 2133 (class 0 OID 0)
-- Dependencies: 180
-- Name: id_sequence_items_situations_templates; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('id_sequence_items_situations_templates', 10028, false);


--
-- TOC entry 2134 (class 0 OID 0)
-- Dependencies: 181
-- Name: id_sequence_items_templates; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('id_sequence_items_templates', 10102, true);


--
-- TOC entry 2135 (class 0 OID 0)
-- Dependencies: 182
-- Name: id_sequence_library_expression; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('id_sequence_library_expression', 90, true);


--
-- TOC entry 2136 (class 0 OID 0)
-- Dependencies: 183
-- Name: id_sequence_situations_hosts; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('id_sequence_situations_hosts', 60, true);


--
-- TOC entry 2137 (class 0 OID 0)
-- Dependencies: 184
-- Name: id_sequence_situations_templates; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('id_sequence_situations_templates', 18, false);


--
-- TOC entry 2138 (class 0 OID 0)
-- Dependencies: 185
-- Name: id_sequence_template; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('id_sequence_template', 10003, true);


--
-- TOC entry 2113 (class 0 OID 16769)
-- Dependencies: 186
-- Data for Name: items_hosts; Type: TABLE DATA; Schema: public; Owner: -
--

COPY items_hosts (itemid, hostid, name, key_, delay, lastvalue, datecoll, datepub, status, errmsg, table_, filterprogram, itemiditemstemplate, itemidhosts, formatcolumn, formatcolumntype, formatcolumntypedata, formatcolumnname, formatcolumnvisible, identifier) FROM stdin;
\.


--
-- TOC entry 2114 (class 0 OID 16776)
-- Dependencies: 187
-- Data for Name: items_situations_hosts; Type: TABLE DATA; Schema: public; Owner: -
--

COPY items_situations_hosts (itemid, situationid, itemsituationid, hostid, status, correlation) FROM stdin;
\.


--
-- TOC entry 2115 (class 0 OID 16780)
-- Dependencies: 188
-- Data for Name: items_situations_templates; Type: TABLE DATA; Schema: public; Owner: -
--

COPY items_situations_templates (itemid, situationid, itemsituationid) FROM stdin;
10017	1	10001
10021	3	10003
10025	12	10022
10053	13	10023
10053	18	10026
10100	19	10028
\.


--
-- TOC entry 2116 (class 0 OID 16784)
-- Dependencies: 189
-- Data for Name: items_templates; Type: TABLE DATA; Schema: public; Owner: -
--

COPY items_templates (itemid, templateid, name, key_, delay, status, table_, filterprogram, formatcolumn, formatcolumntype, formatcolumntypedata, formatcolumnname, formatcolumnvisible, identifier) FROM stdin;
10014	10001	VsFTPd	log[/var/log/vsftpd.log]	1	0	vsftpd	\N	date_coll,user_id,status,command,ip,data,bytes,velocity,city,region_name,latitude,longitude,country_name	vsftpd                                                                                                                                                                                                                                                         	String,String,String,String,String,String,int,String,String,String,String,String,String	Data da Coleta,Usuário,Status,Comando,IP,Dados,Bytes,Velocidade,Cidade,Região,Latitude,Longitude,País	1,1,1,1,1,1,1,1,1,1,1,1,1	\N
10067	10001	Auth Log [Syslog]	syslog[ricardo-VirtualBox]	-1	0	auth	su	date_coll,hostname,program,message	syslog                                                                                                                                                                                                                                                         	String,String,String,String	Data da Coleta,Hostname,Programa,Mensagem	1,1,1,1	\N
10022	10001	Memória [Total]	memory.phy.size[total]	300	1	\N	\N	\N	\N	double	\N	\N	\N
10035	10001	Área de Troca [Livre]	memory.virt.size[free]	300	1	\N	\N	\N	\N	double	\N	\N	\N
10036	10001	Área de Troca [Utilizada] (%)	memory.virt.size[pused]	300	1	\N	\N	\N	\N	double	\N	\N	\N
10063	10001	Erros de Tráfego de Entrada [$IFACE]	network.io[$IFACE, errin]	300	2	\N	\N	\N	\N	int	\N	\N	\N
10064	10001	Erros de Tráfego de Saída [$IFACE]	network.io[$IFACE, errout]	300	2	\N	\N	\N	\N	int	\N	\N	\N
10040	10001	Tráfego de Entrada [$IFACE]	network.io[$IFACE, packets_recv]	300	2	\N	\N	\N	\N	int	\N	\N	\N
10041	10001	Tráfego de Saída [$IFACE]	network.io[$IFACE, packets_sent]	300	2	\N	\N	\N	\N	int	\N	\N	\N
10037	10001	Memória [Utilizada] (%)	memory.phy.size[pused]	300	1	\N	\N	\N	\N	double	\N	\N	\N
10046	10001	Verificação do Passwd	security.checksum[/etc/passwd]	300	1	\N	\N	\N	\N	\N	\N	\N	\N
10047	10001	Usuários logados	security.users	300	1	\N	\N	\N	\N	\N	\N	\N	\N
10024	10001	Memória [Utilizada]	memory.phy.size[used]	300	1	\N	\N	\N	\N	double	\N	\N	\N
10033	10001	Área de Troca [Total]	memory.virt.size[total]	300	1	\N	\N	\N	\N	double	\N	\N	\N
10034	10001	Área de Troca [Utilizada]	memory.virt.size[used]	300	1	\N	\N	\N	\N	double	\N	\N	\N
10042	10001	Endereço IP [$IFACE]	network.conf[$IFACE, addr]	300	2	\N	\N	\N	\N	String	\N	\N	\N
10044	10001	Broadcast [$IFACE]	network.conf[$IFACE, broadcast]	300	2	\N	\N	\N	\N	String	\N	\N	\N
10043	10001	Máscara de Rede [$IFACE]	network.conf[$IFACE, netmask]	300	2	\N	\N	\N	\N	String	\N	\N	\N
10038	10001	Tráfego de Entrada [$IFACE]	network.io[$IFACE, bytes_recv]	300	2	\N	\N	\N	\N	int	\N	\N	\N
10039	10001	Tráfego de Saída [$IFACE]	network.io[$IFACE, bytes_sent]	300	2	\N	\N	\N	\N	int	\N	\N	\N
10065	10001	Pacotes de Entrada Ignorados [$IFACE]	network.io[$IFACE, dropin]	300	2	\N	\N	\N	\N	int	\N	\N	\N
10066	10001	Pacotes de Saída Ignorados [$IFACE]	network.io[$IFACE, dropout]	300	2	\N	\N	\N	\N	int	\N	\N	\N
10045	10001	Endereço IP Externo	network.publicip	300	1	\N	\N	\N	\N	String	\N	\N	\N
10049	10001	Horário de Inicialização do SO	os.boottime	300	1	\N	\N	\N	\N	String	\N	\N	\N
10048	10001	Sistema Operacional	os.uname	300	1	\N	\N	\N	\N	String	\N	\N	\N
10025	10001	CPU [Utilizada] (%)	cpu.percent[used]	300	1	\N	\N	\N	\N	double	\N	\N	CPUUsage
10029	10001	CPU [Inativo]	cpu.times[idle]	300	1	\N	\N	\N	\N	double	\N	\N	CPUIdle
10030	10001	CPU [I/O]	cpu.times[iowait]	300	1	\N	\N	\N	\N	double	\N	\N	CPUIOWait
10031	10001	CPU [Interrupções Efetivas]	cpu.times[irq]	300	1	\N	\N	\N	\N	double	\N	\N	CPUIrq
10027	10001	CPU [Prioridades]	cpu.times[nice]	300	1	\N	\N	\N	\N	double	\N	\N	CPUNice
10032	10001	CPU [Interrupções Postergadas]	cpu.times[softirq]	300	1	\N	\N	\N	\N	double	\N	\N	CPUSoftIrq
10028	10001	CPU [Sistema]	cpu.times[system]	300	1	\N	\N	\N	\N	double	\N	\N	CPUSystem
10026	10001	CPU [Usuário]	cpu.times[user]	300	1	\N	\N	\N	\N	double	\N	\N	CPUUser
10051	10001	Tipo da Partição [$PARTITION]	filesystem.fstype[$PARTITION]	300	2	\N	\N	\N	\N	String	\N	\N	\N
10057	10001	I/O de Disco [Bytes Lidos]	filesystem.io[read_bytes]	300	1	\N	\N	\N	\N	double	\N	\N	\N
10055	10001	I/O de Disco [Quantidade de Leitura]	filesystem.io[read_count]	300	1	\N	\N	\N	\N	double	\N	\N	\N
10059	10001	I/O de Disco [Tempo de Leitura]	filesystem.io[read_time]	300	1	\N	\N	\N	\N	double	\N	\N	\N
10058	10001	I/O de Disco [Bytes Escritos]	filesystem.io[write_bytes]	300	1	\N	\N	\N	\N	double	\N	\N	\N
10056	10001	I/O de Disco {Quantidade de Escrita]	filesystem.io[write_count]	300	1	\N	\N	\N	\N	double	\N	\N	\N
10060	10001	I/O de Disco [Tempo de Escrita]	filesystem.io[write_time]	300	1	\N	\N	\N	\N	double	\N	\N	\N
10053	10001	Espaço Livre da Partição [$PARTITION]	filesystem.size[$PARTITION, free]	300	2	\N	\N	\N	\N	long	\N	\N	FreeSpace$PARTITION
10052	10001	Tamanho Total da Partição [$PARTITION]	filesystem.size[$PARTITION, total]	300	2	\N	\N	\N	\N	double	\N	\N	\N
10050	10001	Utilização da Partição [$PARTITION]	filesystem.size[$PARTITION, used]	300	2	\N	\N	\N	\N	double	\N	\N	\N
10023	10001	Memória [Livre]	memory.phy.size[free]	300	1	\N	\N	\N	\N	double	\N	\N	\N
10019	10001	PostgreSQL	log[/var/log/postgresql/postgresql-9.1-main.log]	1	0	postgresql	!LOG	date_coll,level,message	postgresql                                                                                                                                                                                                                                                     	String,String,String	Data de Coleta,Grau,Mensagem	1,1,1	\N
10015	10001	EXEHDA-USM Collector	log[/var/log/exehda-usm/collector.log]	1	0	exehda-usm-collector	\N	date_coll,hostname,message	syslog                                                                                                                                                                                                                                                         	String,String,String	Data da Coleta,Hostname,Mensagem	1,1,1	\N
10018	10001	DHCP	log[/var/log/syslog]	1	0	dhcpd	dhcpd	date_coll,hostname,message,ip,mac,interface,client_hostname,command,ip_server	dhcpd                                                                                                                                                                                                                                                          	String,String,String,String,String,String,String,String,String	Data da Coleta,Hostname,Mensagem,IP do Cliente,MAC,Interface,Hostname do Cliente,Comando,IP do Servidor	1,1,1,1,1,1,1,1,1	\N
10061	10001	Bind	log[/var/log/syslog]	1	0	bind	named	date_coll,hostname,message	syslog                                                                                                                                                                                                                                                         	String,String,String	Data da Coleta,Hostname,Mensagem	1,1,1	\N
10013	10001	Squid	log[/var/log/squid/access.log]	1	0	squid	\N	date_coll,time_proc,result_trans,cod_return,bytes,url,srv_cache,type,metodo,ip	squid                                                                                                                                                                                                                                                          	String,int,String,int,int,String,String,String,String,String	Data da Coleta,Tempo de Proc.,Resultado,Retorno,Bytes,URL,Cache,Tipo,Método,IP	1,1,1,1,1,1,1,1,1,1	\N
10099	10002	Log de teste	log[/var/log/teste.log]	1	1	apache_error	!ssh		syslog                                                                                                                                                                                                                                                         				\N
10017	10001	Firewall	log[/var/log/ulog/syslogemu.log]	1	1	firewall		host,date_coll,orig_dest,policy,source_ip,source_port,dest_ip,dest_port,proto,type,city,region_name,latitude,longitude,country_name,interface_in,interface_out,mac_source,mac_dest,mac_type,ttl,window_,len,sequence	shorewall                                                                                                                                                                                                                                                      	String,String,String,String,String,int,String,int,String,String,String,String,String,String,String,String,String,String,String,String,int,int,int,long	Hostname,Data de Coleta,Orig./Dest.,Política,IP de Orig.,Porta de Orig.,IP de Dest.,Porta de Dest.,Protocolo,Tipo,Cidade de Orig.,Região de Orig.,Latitude,Longitude,País de Orig.,Interface (In),Interface (Out),MAC (Orig.),MAC (Dest.),MAC (Tipo),TTL,Window,Tamanho,Sequência	0,1,1,1,1,1,1,1,1,1,0,0,0,0,0,1,1,0,0,0,0,0,1,1	FirewallLog
10021	10001	Auth Log	log[/var/log/auth.log]	1	1	auth	su	date_coll,hostname,program,message	syslog                                                                                                                                                                                                                                                         	String,String,String,String	Data de Coleta,Hostname,Programa,Mensagem	1,1,1,1	\N
10062	10001	Auditoria Snoopy	log[/var/log/auth.log]	1	1	auditing	snoopy	date_coll,hostname,message	syslog                                                                                                                                                                                                                                                         	Date,String,String	Data de Coleta,Hostname,Mensagem	1,1,1	\N
10011	10001	Kernel Log	log[/var/log/kern.log]	1	1	kern	!Shorewall	date_coll,hostname,message	syslog                                                                                                                                                                                                                                                         	String,String,String	Data de Coleta,Hostname,Mensagem	1,1,1	KernelLog
10012	10001	Syslog	log[/var/log/syslog]	1	1	syslog	!dhcpd&!kern&!apache_php&!named	date_coll,hostname,program,message	syslog                                                                                                                                                                                                                                                         	String,String,String,String	Data da Coleta,Hostname,Programa,Mensagem	1,1,1,1	\N
10009	10001	Apache - Access Log	log[/var/log/apache2/access.log]	1	1	apache_access	\N	ip,city,date_coll,method,url,protocol,ref,bytes,cod_return,user_id,region_name,latitude,longitude,country_name,os,browser	apache_access                                                                                                                                                                                                                                                  	String,String,String,String,String,String,String,int,int,String,String,String,String,String,String,String	IP de Origem,Cidade,Data de Coleta,Método,URL,Protocolo,Referência,Bytes,Retorno,Usuário,Região,Latitude,Longitude,País,S.O.,Navegador	1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1	ApacheAccessLog
10054	10001	Utilização da Partição [$PARTITION] (%)	filesystem.size[$PARTITION, pused]	300	2	\N	\N	\N	\N	double	\N	\N	\N
10020	10001	Apache - PHP	log[/var/log/syslog]	1	1	apache_php	apache_php	date_coll,hostname,level,message	apache_php                                                                                                                                                                                                                                                     	String,String,String,String	Data da Coleta,Hostname,Grau,Mensagem	1,1,1,1	\N
10100	10001	SSH	log[/var/log/auth.log]	0	1	ssh	sshd	message,date_coll,hostname,program,date_pub,id_pub,status_ssh,user_ssh,ip,port,protocol,auth_method,logname,uid,euid,tty,ruser,rhost,domain,city,region_name,latitude,longitude,country_name	ssh                                                                                                                                                                                                                                                            	String,String,String,String,String,long,String,String,String,int,String,String,String,String,String,String,String,String,String,String,String,String,String,String	Mensagem,Data de Coleta,Hostname,Programa,Data de Publicação,ID de Publicação,Status,Usuário,IP,Porta,Protocolo,Método de Autenticação,Nome do Log,UID,EUID,TTY,Usuário Remoto,Host Remoto,Domínio,Cidade,Região,Latitude,Longitude,País	0,1,0,0,0,0,1,1,1,1,1,0,0,0,0,0,1,1,1,0,0,0,0,0	SSHLog
10010	10001	Apache - Error Log	log[/var/log/apache2/error.log]	1	1	apache_error	\N	date_coll,level,ip,message,city,region_name,latitude,longitude,country_name,file,line,id,rev,msg,severity,hostname,uri,unique_id	apache_error                                                                                                                                                                                                                                                   	String,String,String,String,String,String,String,String,String,String,String,String,String,String,String,String,String,String	Data de Coleta,Grau,IP de Origem,Mensagem,Cidade,Região,Latitude,Longitude,País,ModSec Arquivo,ModSec Linha,ModSec ID,ModSec Versão,ModSec Mensagem,ModSec Severidade,ModSec Nome do Host,ModSec URI,ModSec ID Único	1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1	ApacheErrorLog
10102	10001	ModSecurity Debug Log	log[/var/log/apache2/modsec_debug.log]	0	1	apache_error		date_coll,level,ip,message,city,region_name,latitude,longitude,country_name,file,line,id,rev,msg,severity,hostname,uri,unique_id	apache_error                                                                                                                                                                                                                                                   	String,String,String,String,String,String,String,String,String,String,String,String,String,String,String,String,String,String	Data de Coleta,Grau,IP de Origem,Mensagem,Cidade,Região,Latitude,Longitude,País,ModSec Arquivo,ModSec Linha,ModSec ID,ModSec Versão,ModSec Mensagem,ModSec Severidade,ModSec Nome do Host,ModSec URI,ModSec ID Único	1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1	ApacheErrorLog
10101	10003	ASSP Maillog	log[/usr/share/assp/logs/maillog.txt]	1	1	assp_maillog		date_coll,assp_id,thread,result_tag,status,action,session,source_ip,source_port,assp_ip,assp_port,postfix_ip,postfix_port,source_mail,dest_mail,message_type,message	assp                                                                                                                                                                                                                                                           	String,String,String,String,String,String,String,String,String,String,String,String,String,String,String,String,String	Data de Coleta,ASSP-ID,Thread,Resultado,Status,Ação,Sessão,IP de Origem,Porta de Origem,ASSP IP,ASSP Porta,Postfix IP,Postfix Porta,Remetente,Destinatário,Tipo da Mensagem,Mensagem	1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1	ASSPMailLog
10016	10001	EXEHDA-USM Manager	log[/var/log/exehda-usm/manager.log]	1	0	exehda-usm-manager	\N	date_coll,hostname,message	syslog                                                                                                                                                                                                                                                         	String,String,String	Data da Coleta,Hostname,Mensagem	1,1,1	\N
\.


--
-- TOC entry 2117 (class 0 OID 16791)
-- Dependencies: 190
-- Data for Name: library_expression; Type: TABLE DATA; Schema: public; Owner: -
--

COPY library_expression (name, expression, id_name) FROM stdin;
colon                                                                                                                                                                                                                                                          	Literal(":")	2
lbrace                                                                                                                                                                                                                                                         	Literal("(")	3
rbrace                                                                                                                                                                                                                                                         	Literal(")")	4
lbrocket                                                                                                                                                                                                                                                       	Literal("[")	5
rbrocket                                                                                                                                                                                                                                                       	Literal("]")	6
underline                                                                                                                                                                                                                                                      	Literal("_")	7
point                                                                                                                                                                                                                                                          	Literal(".")	9
integer                                                                                                                                                                                                                                                        	Word(nums)	13
alpha                                                                                                                                                                                                                                                          	Word(alphas)	14
alphaInteger                                                                                                                                                                                                                                                   	Word(nums + alphas)	15
pointHyphen                                                                                                                                                                                                                                                    	Word("-" + ".")	16
specialCaracter                                                                                                                                                                                                                                                	Word("-" + "_" + "." + "/") 	17
aspas                                                                                                                                                                                                                                                          	Literal('"')	18
bar                                                                                                                                                                                                                                                            	Literal("/")	19
underlineAlpha                                                                                                                                                                                                                                                 	Word("_" + alphas)	20
hora                                                                                                                                                                                                                                                           	Combine(integer + colon + integer + colon + integer)	21
date                                                                                                                                                                                                                                                           	Group(alpha + branco + integer + branco + hora)	22
pid                                                                                                                                                                                                                                                            	lbrocket + branco + integer + branco + rbrocket	23
message                                                                                                                                                                                                                                                        	restOfLine	28
hostname                                                                                                                                                                                                                                                       	Combine(alphaInteger + ZeroOrMore((pointHyphen + alphaInteger)))	25
numProgram                                                                                                                                                                                                                                                     	Literal("[") + integer + Optional(Literal(".") + integer) + Literal("]")	29
comma                                                                                                                                                                                                                                                          	Literal(",")	12
macType                                                                                                                                                                                                                                                        	Combine(integer + colon + integer)	33
reffer_old                                                                                                                                                                                                                                                     	Combine(Suppress(aspas) + Optional(hyphen ^ url) + Suppress(aspas))	61
id                                                                                                                                                                                                                                                             	Suppress(Literal("ID=") + integer)	36
policy                                                                                                                                                                                                                                                         	alpha	30
out                                                                                                                                                                                                                                                            	Combine(Suppress(Literal("OUT=")) + Optional(interface))	38
mac                                                                                                                                                                                                                                                            	Suppress(Literal("MAC="))	39
source_ip                                                                                                                                                                                                                                                      	Combine(Suppress(Literal("SRC=")) + ip)	40
dest_ip                                                                                                                                                                                                                                                        	Combine(Suppress(Literal("DST=")) + ip)	41
lenn                                                                                                                                                                                                                                                           	Combine(Suppress(Literal("LEN=")) + integer)	42
ttl                                                                                                                                                                                                                                                            	Combine(Suppress(Literal("TTL=")) + integer)	43
typ                                                                                                                                                                                                                                                            	Combine(Suppress(Literal("TYPE=")) + integer)	45
source_port                                                                                                                                                                                                                                                    	Combine(Suppress(Literal("SPT=")) + integer)	46
seq                                                                                                                                                                                                                                                            	Combine(Suppress(Literal("SEQ=")) + integer) 	48
dest_port                                                                                                                                                                                                                                                      	Combine(Suppress(Literal("DPT=")) + integer)	47
window                                                                                                                                                                                                                                                         	Combine(Suppress(Literal("WINDOW=")) + integer)  	49
frag                                                                                                                                                                                                                                                           	Suppress(Literal("FRAG=") + integer)	51
interface                                                                                                                                                                                                                                                      	alphaInteger	31
timeZoneOffset                                                                                                                                                                                                                                                 	Word("+-", nums)	54
userID                                                                                                                                                                                                                                                         	("-" | Word(alphas + nums + "@._"))	56
bytes                                                                                                                                                                                                                                                          	integer	60
userAgent                                                                                                                                                                                                                                                      	Combine(branco + restOfLine)	62
date_apache_error                                                                                                                                                                                                                                              	Group(Suppress(lbrocket + alpha) + alpha + branco + \r\n                                      integer + branco + hora + integer + Suppress(rbrocket))	63
inn                                                                                                                                                                                                                                                            	Combine(Suppress(Literal("IN=")) + Optional(interface))	37
proto                                                                                                                                                                                                                                                          	Combine(Suppress(Literal("PROTO=")) + alphaInteger)	44
level                                                                                                                                                                                                                                                          	Combine(Suppress(lbrocket) + alpha + Suppress(rbrocket))	64
data_postgres                                                                                                                                                                                                                                                  	Combine(integer + hyphen + integer + hyphen + integer + branco + hora)	66
client_hostname                                                                                                                                                                                                                                                	Combine(Suppress(lbrace) + hostname + Suppress(rbrace))	67
mac_dhcpd                                                                                                                                                                                                                                                      	Combine(Optional(Suppress(lbrace)) + macAddress + \r\n                                Optional(Suppress(rbrace)))	68
ip_server                                                                                                                                                                                                                                                      	Combine(Suppress(lbrace) + ip + Suppress(rbrace))	69
date_unix                                                                                                                                                                                                                                                      	Combine(integer + point + integer)	70
result_trans                                                                                                                                                                                                                                                   	Combine(alpha + Optional(underlineAlpha) )	71
cod                                                                                                                                                                                                                                                            	Suppress(Literal("COD=") + integer)	52
date_apache_access                                                                                                                                                                                                                                             	Group(Suppress(lbrocket) + integer + Suppress(bar) + alpha + \r\n                                    Suppress(bar) + integer + Suppress(colon) + hora + \r\n                                    Suppress(timeZoneOffset) + Suppress(rbrocket))	55
pid_vsftpd                                                                                                                                                                                                                                                     	Combine(lbrocket + alpha + branco+ integer + rbrocket)	74
user_id                                                                                                                                                                                                                                                        	Combine(Suppress(lbrocket)+ alpha  + Suppress(rbrocket)  )	75
velocity                                                                                                                                                                                                                                                       	Combine(integer + point + integer +alpha + bar + alpha  )	76
squid                                                                                                                                                                                                                                                          	(date_unix.setResultsName("date_coll") + integer.setResultsName("time_proc") \r\n                     + ip.setResultsName("ip") + result_trans.setResultsName("result_trans") \r\n                     + Suppress(bar) + integer.setResultsName("cod_return") + \r\n                     integer.setResultsName("bytes") + alpha.setResultsName("method") + \r\n                     url.setResultsName("url") + Suppress(hyphen) + \r\n                     srv_cache.setResultsName("srv_cache") + message.setResultsName("type"))	78
postgresql                                                                                                                                                                                                                                                     	(data_postgres.setResultsName("date_coll") + branco + Suppress(alpha) + \r\n                          branco + alpha.setResultsName("level") + Suppress(colon) + branco + \r\n                          message.setResultsName("message"))	80
srv_cache                                                                                                                                                                                                                                                      	Combine(Suppress(alpha+Optional(underlineAlpha) + bar) + (ip ^ hyphen ^ url))	72
ip_apache_error                                                                                                                                                                                                                                                	Combine(Suppress(lbrocket) + Suppress(alpha) + Suppress(branco) + ip + Optional(Suppress(rbrocket)))	65
level_php                                                                                                                                                                                                                                                      	Combine(alpha + Suppress(colon))	83
pointInteger                                                                                                                                                                                                                                                   	Combine(OneOrMore((integer +point) ^ integer))	113
dhcpd                                                                                                                                                                                                                                                          	Optional(priority.setResultsName("priority"))+(date.setResultsName("date_coll") + hostname.setResultsName("hostname") + \r\n                    program.setResultsName("program") + Optional(alpha.setResultsName("command") + Suppress(alpha) + \r\n                    Optional(Optional(ip.setResultsName("ip")) + \r\n                             Optional(ip_server.setResultsName("ip_server")) + \r\n                             Optional(Suppress(alpha)) + Optional(mac_dhcpd.setResultsName("mac")) + \r\n                             Optional(client_hostname.setResultsName("client_hostname")) + \r\n                             Suppress(alpha) + interface.setResultsName("interface")) \r\n                                                 ) + message.setResultsName("message"))	79
date_vsftpd                                                                                                                                                                                                                                                    	Group(Suppress(alpha)+alpha + branco + integer + branco + hora + integer)	73
branco                                                                                                                                                                                                                                                         	ZeroOrMore(" ")	1
hyphen                                                                                                                                                                                                                                                         	Literal("-")	8
orig_dest                                                                                                                                                                                                                                                      	alphaInteger	27
opt                                                                                                                                                                                                                                                            	Suppress(Literal("OPT(") + alphaInteger + Literal(")"))	53
less                                                                                                                                                                                                                                                           	Literal("<")	10
more                                                                                                                                                                                                                                                           	Literal(">")	11
flag                                                                                                                                                                                                                                                           	Suppress(ZeroOrMore(Literal("DF") ^ Literal("MF") ^ Literal("CE")))	50
syslog                                                                                                                                                                                                                                                         	Optional(priority.setResultsName("priority"))+(date.setResultsName("date_coll") + hostname.setResultsName("hostname") + \r\n                      program.setResultsName("program") + \r\n                      message.setResultsName("message")) ^ (date.setResultsName("date_coll") + \r\n                      program.setResultsName("program") + branco + message.setResultsName("message"))	82
method                                                                                                                                                                                                                                                         	Combine(Suppress(aspas) + (Literal("GET") ^ Literal("HEAD") ^ Literal("COOK") ^ Literal("POST") ^ Literal("TRACE") ^ Literal("DELETE") ^ Literal("OPTIONS") ^ Literal("CONNECT") ^ Literal("PACTH") ^ Literal("PUT") ^ Literal("PROPFIND") ^ Literal("MERGE") ^ Literal("CHECKOUT") ^ Literal("MKCOL") ^ Literal("PROPPATCH") ^ Literal("REPORT") ^ Literal("MKACTIVITY") ^ hyphen) + Optional(Suppress(aspas)))	57
Status                                                                                                                                                                                                                                                         	Combine(url + branco + OneOrMore((url + branco) + (Literal("user") ) ))	85
url_apache                                                                                                                                                                                                                                                     	Combine("/" + Optional(Word(alphas + nums + "/" + "?" + "'" + "." + ":" + "_" + "=" + ">" + "<" + " "+ "^" + "{" + "}" +"$" + "&" + "%" + "-" + "@" + "," + "[" + "]" + "(" + ")" + "+" + "!" + ";" + "*" + "|" + "~" + "\\\\"))) ^ Combine("http" +  Optional(Word(alphas + nums + "/" + "?" + "'" + "." + ":" + "_" + "=" +">" + "<" + " " + "^" + "{" + "}" + "$" + "&" + "%" + "-" + "@" + "," + "[" + "]" + "(" + ")" + "+" + "!" + ";" + "*" + "|" + "~" + "\\\\"))) ^ "*"	89
ssh                                                                                                                                                                                                                                                            	(date.setResultsName("date_coll") + hostname.setResultsName("hostname") + program.setResultsName("program") + Optional(program.setResultsName("auth_method")) + Optional(Status3.setResultsName("status_ssh")) +  Optional(logname.setResultsName("logname"))  + Optional(uid.setResultsName("uid") ) + Optional(euid.setResultsName("euid") ) + Optional(tty.setResultsName("tty") ) + Optional(ruser.setResultsName("ruser") ) + Optional(rhost.setResultsName("rhost") ) + Optional(user.setResultsName("user_ssh")) + Optional(program.setResultsName("auth_method") + Status.setResultsName("status_ssh") + url.setResultsName("user_ssh")) + Optional(program.setResultsName("auth_method") + Status3.setResultsName("status_ssh") ) + Optional(Status2.setResultsName("message") + url.setResultsName("domain") + Suppress(Literal("[")) + ip.setResultsName("ip") + Suppress(Literal("]"))) + Optional(program.setResultsName("auth_method") + Status2.setResultsName("status_ssh") ) + Optional(Suppress(Literal("User")) + url.setResultsName("user_ssh") + Suppress(Literal("from")) + ip.setResultsName("ip")) + Optional(Suppress(Literal("User")) + url.setResultsName("user_ssh")  + Suppress(Literal("from")) + url.setResultsName("domain")) + Optional(Status.setResultsName("status_ssh") + url.setResultsName("user_ssh") + Suppress(Literal("from")) + ip.setResultsName("ip")) + (Optional(Status2.setResultsName("status_ssh") + url.setResultsName("user_ssh") + Suppress(Literal("from")) + ip.setResultsName("ip")) ^ Optional(Status4.setResultsName("status_ssh")+ ip.setResultsName("ip"))) + Optional(branco + Suppress(Literal("port")) + integer.setResultsName("port") + alphaInteger.setResultsName("protocol")) + Optional(Suppress(Literal("user")) + url.setResultsName("user_ssh"))+ Optional(Suppress(Literal(":")) + integer.setResultsName("disconnect_reason") + Suppress(Literal(":")) )+ Optional(Suppress(branco)) +Optional(message.setResultsName("message2")))	100
vsftpd                                                                                                                                                                                                                                                         	(date_vsftpd.setResultsName("date_coll") + Suppress(pid_vsftpd) + \r\n                      Optional(user_id.setResultsName("user_id") + alpha.setResultsName("status")) \r\n                      + alpha.setResultsName("command")+ Suppress(colon) + Suppress(alpha) + \r\n                      Suppress(aspas)+ ip.setResultsName("ip") +Suppress(aspas)+ \r\n                      Optional(Suppress(comma))+Optional(Suppress(aspas)+url.setResultsName("data") \r\n                                                         + Suppress(aspas))+ Optional(Suppress(comma))+\r\n                      Optional(integer.setResultsName("bytes")+Suppress("bytes"))+ \r\n                      Optional(Suppress(comma)) + Optional(velocity.setResultsName("velocity"))  ) 	77
priority                                                                                                                                                                                                                                                       	Combine(Suppress(less)+ integer + Suppress(more))	26
macAddress                                                                                                                                                                                                                                                     	Combine(alphaInteger + colon + alphaInteger + colon + alphaInteger + \r\n                                 colon +  alphaInteger + colon + alphaInteger + colon + \r\n                                 alphaInteger) 	32
reffer                                                                                                                                                                                                                                                         	Combine(Suppress(aspas) + Optional(hyphen ^ url_apache) + Suppress(aspas))	91
logname                                                                                                                                                                                                                                                        	Combine(Suppress(Literal("logname=")) + Optional(url))	93
uid                                                                                                                                                                                                                                                            	Combine(Suppress(Literal("uid=")) + Optional(integer))	94
Status2                                                                                                                                                                                                                                                        	Combine(url + branco + OneOrMore((url + branco) + (Suppress(Literal("for")) ) ))	86
Status3                                                                                                                                                                                                                                                        	Combine(url + branco + OneOrMore((alpha + branco) + (Suppress(Literal(";") )) ))	87
Status4                                                                                                                                                                                                                                                        	Combine(url + branco + OneOrMore((url + branco) + (Suppress(Literal("from")) ) ))	88
apache_access                                                                                                                                                                                                                                                  	(ip.setResultsName("ip") + Suppress(hyphen) + userID.setResultsName("user_id") + date_apache_access.setResultsName("date_coll") + Optional(method.setResultsName("method")) + Optional(url_apache2.setResultsName("url")) + Optional(protocol.setResultsName("protocol")) + Optional(integer.setResultsName("cod_return")) + Optional((bytes.setResultsName("bytes")) ^ Optional(Suppress(hyphen))) + reffer.setResultsName("ref") + userAgent.setResultsName("userAgent"))	92
euid                                                                                                                                                                                                                                                           	Combine(Suppress(Literal("euid=")) + Optional(integer))	95
tty                                                                                                                                                                                                                                                            	Combine(Suppress(Literal("tty=")) + Optional(alpha))	96
ruser                                                                                                                                                                                                                                                          	Combine(Suppress(Literal("ruser="))+ Optional(url))	97
rhost                                                                                                                                                                                                                                                          	Combine(Suppress(Literal("rhost=")) + Optional(url))	98
user                                                                                                                                                                                                                                                           	Combine(Suppress(Literal("user="))+ Optional(url))	99
tosPrec                                                                                                                                                                                                                                                        	Suppress(Literal("TOS=") + integer + Optional(Literal("x") + alphaInteger) \r\n                               + Literal("PREC=") + integer + Literal("x") + alphaInteger)	35
program                                                                                                                                                                                                                                                        	Combine(ZeroOrMore(specialCaracter ^ alpha) + Optional(Suppress("-") + Suppress(integer)) + \r\n                              ZeroOrMore(specialCaracter + alpha) + Optional(Suppress(pid)) + \r\n                              Optional(lbrace + alpha + colon + alpha + rbrace) + \r\n                              Optional(alphaInteger) + Suppress(colon))	24
protocol                                                                                                                                                                                                                                                       	Combine(alpha + bar + integer + point + integer + Suppress(Literal('"'))) ^ Combine(Suppress(aspas) + "-" + Suppress(aspas))	59
apache_error                                                                                                                                                                                                                                                   	(Optional(date_apache_error.setResultsName("date_coll") +\n                                    level.setResultsName("level") +\n                                    Optional(ip_apache_error.setResultsName("ip"))) + Optional(message_ms.setResultsName("message")) +\n                                message.setResultsName("message"))	115
ip                                                                                                                                                                                                                                                             	Combine(integer + point + integer + point + integer + point + integer) ^ Combine( Optional(Suppress(lbrocket)) + Optional( (alphaInteger + (colon ^ (colon + colon))) ^ (colon + colon)) +  Optional( (alphaInteger + (colon ^ (colon + colon))) ^ (colon + colon)) + Optional( (alphaInteger + (colon ^ (colon + colon))) ^ (colon + colon)) + Optional( (alphaInteger + (colon ^ (colon + colon))) ^ (colon + colon)) +  Optional( (alphaInteger + (colon ^ (colon + colon))) ^ colon + colon) + Optional(alphaInteger + colon) + Optional(Combine(integer + point + integer + point + integer + point + integer)) + Optional(alphaInteger) + Optional(Suppress(rbrocket)) + Optional( colon + alphaInteger) )	34
shorewall                                                                                                                                                                                                                                                      	Optional(priority.setResultsName("priority"))+(date.setResultsName("date_coll") + hostname.setResultsName("hostname") + Suppress(alpha + colon) + orig_dest.setResultsName("orig_dest") + Suppress(colon) + policy.setResultsName("policy") + Suppress(colon) +                          inn.setResultsName("interface_in") + out.setResultsName("interface_out") + Optional(mac + Optional(macAddress.setResultsName("mac_dest") + Suppress(colon) + macAddress.setResultsName("mac_source") + Suppress(colon) + macType.setResultsName("mac_type"))) + source_ip.setResultsName("source_ip") + dest_ip.setResultsName("dest_ip") + lenn.setResultsName("len") + tosPrec + ttl.setResultsName("ttl") + id + Optional(flag) + Optional(frag) + Optional(opt) + proto.setResultsName("proto") + Optional(typ.setResultsName("type")) + Optional(cod) + Optional(source_port.setResultsName("source_port")) + Optional(dest_port.setResultsName("dest_port")) + Optional(seq.setResultsName("sequence")) + Optional(window.setResultsName("window_")))	81
apache_php                                                                                                                                                                                                                                                     	Optional(priority.setResultsName("priority"))+((date.setResultsName("date_coll") + hostname.setResultsName("hostname") \r\n                          + program.setResultsName("program")+  level_php.setResultsName("level") + branco + \r\n                          message.setResultsName("message")) ^ \r\n                          (date.setResultsName("date_coll") + program.setResultsName("program") + \r\n                           level_php.setResultsName("level") + branco + \r\n                           message.setResultsName("message")))	84
url_apache2                                                                                                                                                                                                                                                    	Combine("/" + Optional(Word(alphas + nums + "/" + "?" + "'" + "." + ":" + "_" + "=" + ">" + "<" + "{" + "}"+ "^" +"$" + "&" + "%" + "-" + "@" + "," + "[" + "]" + "(" + ")" + "+" + "!" + ";" + "*" + "|" + "~" + "\\\\"))) ^ Combine("http" +  Optional(Word(alphas + nums + "/" + "?" + "'" + "." + ":" + "_" + "=" +">" + "<" + "^" + "{" + "}" + "$" + "&" + "%" + "-" + "@" + "," + "[" + "]" + "(" + ")" + "+" + "!" + ";" + "*" + "|" + "~" + "\\\\"))) ^ "*"	90
assp_id                                                                                                                                                                                                                                                        	Combine(alphaInteger + hyphen + alphaInteger + hyphen+ alphaInteger)	102
date_assp                                                                                                                                                                                                                                                      	Group(alpha + Suppress(hyphen) + integer + Suppress(hyphen) + Suppress(integer) + hora)	101
thread                                                                                                                                                                                                                                                         	(Suppress(lbrocket) + Combine(alphaInteger+underline+alphaInteger) + Suppress(rbrocket) ) |(Combine(alphaInteger+underline+alphaInteger) )	103
status_assp                                                                                                                                                                                                                                                    	Combine(OneOrMore(alpha +branco))	104
action                                                                                                                                                                                                                                                         	Suppress(hyphen + hyphen) + branco + message	105
name_type                                                                                                                                                                                                                                                      	Combine(alpha + branco +alpha)	107
message_type                                                                                                                                                                                                                                                   	(hostname+ Suppress(colon) ) | (Suppress(lbrocket) + name_type  + Suppress(rbrocket))	108
result_tag                                                                                                                                                                                                                                                     	Combine(Suppress(lbrocket) + alpha + Suppress(rbrocket))	109
specialCaracter_ms                                                                                                                                                                                                                                             	Word("/" + "?" + "." + ":" + "_" + "=" + "$" + "&" + "%" + "-" + "@" + "," + "[" + "]" + "(" + ")" + "+" + "!" + ";" + "*" + "|" + "~" + "\\\\" + "{" + "}")	111
file_ms                                                                                                                                                                                                                                                        	Combine(OneOrMore(alpha + branco ^ integer + branco ^ specialCaracter_ms + branco))	112
session                                                                                                                                                                                                                                                        	Combine(Suppress(Literal('session:')) + alphaInteger)	106
message_ms                                                                                                                                                                                                                                                     	Literal("ModSecurity: ") + OneOrMore(url +\n                         Optional(Suppress(Literal('[file "')) + file_ms.setResultsName("file") + Suppress(Literal('"]')) ) +\n                         Optional(Suppress(Literal('[line "')) + integer.setResultsName("line") + Suppress(Literal('"]')) ) +\n                         Optional(Suppress(Literal('[id "')) + integer.setResultsName("id") + Suppress(Literal('"]')) ) +\n                         Optional(Suppress(Literal('[rev "')) + pointInteger.setResultsName("rev") + Suppress(Literal('"]')) ) +\n                         Optional(Suppress(Literal('[msg "')) + file_ms.setResultsName("msg") + Suppress(Literal('"]')) ) +\n                         Optional(Suppress(Literal('[severity "')) + alpha.setResultsName("severity") + Suppress(Literal('"]')) ) +\n                         Optional(Suppress(Literal('[hostname "')) + hostname.setResultsName("hostname") + Suppress(Literal('"]')) ) +\n                         Optional(Suppress(Literal('[uri "')) + file_ms.setResultsName("uri") + Suppress(Literal('"]')) ) +\n                         Optional(Suppress(Literal('[unique_id "')) + file_ms.setResultsName("unique_id") + Suppress(Literal('"]')) )\n                         )	114
url                                                                                                                                                                                                                                                            	Combine("/" + Optional(Word(alphas + nums + "`" + "/" + "?" + "'" + "." + ":" + "_" + "=" + ">" + "<" + "{" + "}" +"$" + "&" + "%" + "-" + "@" + "," + "[" + "]" + "(" + ")" + "+" + "!" + ";" + "*" + "|" + "~" + "\\\\"))) ^ Combine("http" +  Optional(Word(alphas + nums + "/" + "?" + "`" + "'" + "." + ":" + "_" + "=" +">" + "<" + " " + "^" + "{" + "}" + "$" + "&" + "%" + "-" + "@" + "," + "[" + "]" + "(" + ")" + "+" + "!" + ";" + "*" + "|" + "~" + "\\\\"))) ^ "*" ^ Combine(Word(alphas + nums + "/" + "?" + "'" + "." + ":" + "_" + "=" + "$" + "&" + "%" + "-" + "@" + "," + "[" + "]" + "(" + ")" + "+" + "!" + ";" + "*" + "|" + "~" + "\\\\" + "{" + "}" + "#" + "^" + '"' + "<" + ">" + "`"))	58
assp                                                                                                                                                                                                                                                           	(date_assp.setResultsName('date_coll') + Optional(assp_id.setResultsName('assp_id')) + thread.setResultsName('thread') + Optional(result_tag.setResultsName('result_tag')) + Optional(status_assp.setResultsName('status') + action.setResultsName('action')) + Optional(status_assp.setResultsName('status')+ Suppress(colon) + session.setResultsName('session')) + Optional(ip.setResultsName('source_ip') + Suppress(colon) + integer.setResultsName('source_port') +more+ ip.setResultsName('assp_ip')+ Suppress(colon) + integer.setResultsName('assp_port')+more + ip.setResultsName('postfix_ip')+ Suppress(colon) + integer.setResultsName('postfix_port')) + Optional(ip.setResultsName('source_ip') + Suppress(less) + url.setResultsName('source_mail') + Suppress(more)+ Optional(Suppress('to:')+ url.setResultsName('dest_mail'))+ Optional(message_type.setResultsName('message_type'))+ message.setResultsName('message')) + Optional(status_assp('status')) + Optional(ip.setResultsName('source_ip') + Suppress(hyphen + branco)) + message.setResultsName('message'))	110
\.


--
-- TOC entry 2118 (class 0 OID 16857)
-- Dependencies: 191
-- Data for Name: situations_hosts; Type: TABLE DATA; Schema: public; Owner: -
--

COPY situations_hosts (description, epl, situationid, command, commandtype, comments, to_, subject, body, situationhostsid, severity, occurrences) FROM stdin;
Repeat Attack-Login Target for $USER_SSH	select window(*) as events, * from ssh(user_ssh!='null').win:time(1 min) group by user_ssh having count(*) >= 3	3	\N	\N	\N	\N	\N	\N	\N	1	0
Espaço Livre (<10GB)	SELECT * FROM `FreeSpace$PARTITION`(lastvalue<236223201280)	41	df -h -x tmpfs -x devtmpfs	shellcommand	Pouco espaço livre em disco.	                                                                                                                                                                                                                                                               	                                                                                                                                                                                                                                                               		\N	1	1
Espaço Livre (<10GB)	SELECT * FROM `FreeSpace/`(lastvalue<236223201280)	43	df -h -x tmpfs -x devtmpfs	shellcommand	Pouco espaço livre em disco.	                                                                                                                                                                                                                                                               	                                                                                                                                                                                                                                                               		41	2	1
Espaço Livre (< 2GB)	SELECT * FROM `FreeSpace$PARTITION`(lastvalue<2147483648)	45	df -h -x tmpfs -x devtmpfs	shellcommand	Pouco espaço disponível em disco.	                                                                                                                                                                                                                                                               	                                                                                                                                                                                                                                                               		\N	3	1
Espaço Livre (< 2GB)	SELECT * FROM `FreeSpace/`(lastvalue<2147483648)	46	df -h -x tmpfs -x devtmpfs	shellcommand	Pouco espaço disponível em disco.	                                                                                                                                                                                                                                                               	                                                                                                                                                                                                                                                               	None	3	3	1
Espaço Livre (<10GB)	SELECT * FROM `FreeSpace/boot`(lastvalue<236223201280)	47	df -h -x tmpfs -x devtmpfs	shellcommand	Pouco espaço livre em disco.	                                                                                                                                                                                                                                                               	                                                                                                                                                                                                                                                               	None	1	1	1
Espaço Livre (< 2GB)	SELECT * FROM `FreeSpace/boot`(lastvalue<2147483648)	48	df -h -x tmpfs -x devtmpfs	shellcommand	Pouco espaço disponível em disco.	                                                                                                                                                                                                                                                               	                                                                                                                                                                                                                                                               	None	3	3	1
Espaço Livre (<10GB)	SELECT * FROM `FreeSpace/tmp`(lastvalue<236223201280)	49	df -h -x tmpfs -x devtmpfs	shellcommand	Pouco espaço livre em disco.	                                                                                                                                                                                                                                                               	                                                                                                                                                                                                                                                               	None	1	1	1
Espaço Livre (< 2GB)	SELECT * FROM `FreeSpace/tmp`(lastvalue<2147483648)	50	df -h -x tmpfs -x devtmpfs	shellcommand	Pouco espaço disponível em disco.	                                                                                                                                                                                                                                                               	                                                                                                                                                                                                                                                               	None	3	3	1
Várias tentativas de autenticação ao SSH apartir do endereço $IP	SELECT * FROM SSHLog(ip!='null').win:time(1 min) GROUP BY ip HAVING count(*) >= 3	2	echo $IP >> ipsssh.txt	shellcommand	Por favor, verifique o serviço SSHD, possível tentativa de ataque de força bruta, esquecimento de senha ou erro de configuração.	\N	\N	\N	\N	3	0
Espaço Livre (<10GB)	SELECT * FROM `FreeSpace/squid`(lastvalue<236223201280)	51	df -h -x tmpfs -x devtmpfs	shellcommand	Pouco espaço livre em disco.	                                                                                                                                                                                                                                                               	                                                                                                                                                                                                                                                               	None	1	1	1
Espaço Livre (< 2GB)	SELECT * FROM `FreeSpace/squid`(lastvalue<2147483648)	52	df -h -x tmpfs -x devtmpfs	shellcommand	Pouco espaço disponível em disco.	                                                                                                                                                                                                                                                               	                                                                                                                                                                                                                                                               	None	3	3	1
Espaço Livre (<10GB)	SELECT * FROM `FreeSpace/home`(lastvalue<236223201280)	53	df -h -x tmpfs -x devtmpfs	shellcommand	Pouco espaço livre em disco.	                                                                                                                                                                                                                                                               	                                                                                                                                                                                                                                                               	None	1	1	1
Espaço Livre (< 2GB)	SELECT * FROM `FreeSpace/home`(lastvalue<2147483648)	54	df -h -x tmpfs -x devtmpfs	shellcommand	Pouco espaço disponível em disco.	                                                                                                                                                                                                                                                               	                                                                                                                                                                                                                                                               	None	3	3	1
Espaço Livre (<10GB)	SELECT * FROM `FreeSpace/var`(lastvalue<236223201280)	55	df -h -x tmpfs -x devtmpfs	shellcommand	Pouco espaço livre em disco.	                                                                                                                                                                                                                                                               	                                                                                                                                                                                                                                                               	None	1	1	1
Espaço Livre (< 2GB)	SELECT * FROM `FreeSpace/var`(lastvalue<2147483648)	56	df -h -x tmpfs -x devtmpfs	shellcommand	Pouco espaço disponível em disco.	                                                                                                                                                                                                                                                               	                                                                                                                                                                                                                                                               	None	3	3	1
Espaço Livre (<10GB)	SELECT * FROM `FreeSpace/usr`(lastvalue<236223201280)	57	df -h -x tmpfs -x devtmpfs	shellcommand	Pouco espaço livre em disco.	                                                                                                                                                                                                                                                               	                                                                                                                                                                                                                                                               	None	1	1	1
Espaço Livre (< 2GB)	SELECT * FROM `FreeSpace/usr`(lastvalue<2147483648)	58	df -h -x tmpfs -x devtmpfs	shellcommand	Pouco espaço disponível em disco.	                                                                                                                                                                                                                                                               	                                                                                                                                                                                                                                                               	None	3	3	1
Espaço Livre (<10GB)	SELECT * FROM `FreeSpace/usr/share/assp`(lastvalue<236223201280)	59	df -h -x tmpfs -x devtmpfs	shellcommand	Pouco espaço livre em disco.	                                                                                                                                                                                                                                                               	                                                                                                                                                                                                                                                               	None	1	1	1
Espaço Livre (< 2GB)	SELECT * FROM `FreeSpace/usr/share/assp`(lastvalue<2147483648)	60	df -h -x tmpfs -x devtmpfs	shellcommand	Pouco espaço disponível em disco.	                                                                                                                                                                                                                                                               	                                                                                                                                                                                                                                                               	None	3	3	1
Uso de CPU elevado (%)	SELECT * FROM CPUUsage(lastvalue>80)	40	ps -eo pcpu,pid,user,args | sort -k 1 -r | head -6	shellcommand	Por favor, verifique os processos em execução.	r.borges.almeida@gmail.com                                                                                                                                                                                                                                     	Uso de CPU elevado                                                                                                                                                                                                                                             	Por favor, verifique os processos em execução.	\N	2	1
Espaço Livre (< 2GB)	SELECT * FROM `FreeSpace/usr/share/assp`(lastvalue<2147483648)	61	df -h -x tmpfs -x devtmpfs	shellcommand	Pouco espaço disponível em disco.	                                                                                                                                                                                                                                                               	                                                                                                                                                                                                                                                               	None	3	3	1
Espaço Livre (<10GB)	SELECT * FROM `FreeSpace/usr/share/assp`(lastvalue<236223201280)	62	df -h -x tmpfs -x devtmpfs	shellcommand	Pouco espaço livre em disco.	                                                                                                                                                                                                                                                               	                                                                                                                                                                                                                                                               	None	1	1	1
Ataque repetido ao firewall a partir de $SOURCE_IP 	SELECT * FROM FirewallLog(source_ip!='null' and policy in ('reject', 'REJECT', 'DROP')).win:time(1 min) GROUP BY source_ip HAVING count(*) >= 10	1	echo $SOURCE_IP >> ipsfirewall.txt	shellcommand	Caso seja uma máquina da rede interna, considere a avaliação do comprometimento da máquina (malware, ...)	r.borges.almeida@gmail.com                                                                                                                                                                                                                                     	Escâner de portas a partir do enderenço IP $SOURCE_IP                                                                                                                                                                                                          	Foi identificado um escaneamento de portas a partir do endereço IP $SOURCE_IP .	\N	4	0
Apache - várias tentativas de acesso à arquivo inexistente a partir do endereço $ip	SELECT * FROM ApacheErrorLog(ip!='null' and message like '%File does not exist%').win:time(1 min) GROUP BY ip HAVING count(*) >= 10	63	echo $ip >> ipsapacheerror.txt	shellcommand	Muitas tentativas de acessar arquivo que não existe	\N	\N	\N	\N	3	0
ModSec - várias tentativas consideradas suspeitas a partir do endereço $ip	SELECT * FROM ApacheErrorLog(ip!='null' and severity in ('EMERGENCY', 'ALERT', 'CRITICAL')).win:time(1 min) GROUP BY ip HAVING count(*) >= 10	64	echo $ip >> ipsmodsec.txt	shellcommand	ModSecurity detectou atividades possivelmente maliciosas de acesso web ao servidor	\N	\N	\N	\N	4	0
\.


--
-- TOC entry 2119 (class 0 OID 16864)
-- Dependencies: 192
-- Data for Name: situations_templates; Type: TABLE DATA; Schema: public; Owner: -
--

COPY situations_templates (description, epl, situationid, command, commandtype, comments, status, to_, subject, body, correlation, severity, occurrences) FROM stdin;
Ataque repetido ao firewall a partir de $SOURCE_IP 	SELECT * FROM FirewallLog(source_ip!='null' and policy in ('reject', 'REJECT', 'DROP')).win:time(1 min) GROUP BY source_ip HAVING count(*) >= 15	1	echo $SOURCE_IP >> ipsfirewall.txt	shellcommand	Caso seja uma máquina da rede interna, considere a avaliação do comprometimento da máquina (malware, ...)	0	r.borges.almeida@gmail.com                                                                                                                                                                                                                                     	Escâner de portas a partir do enderenço IP $SOURCE_IP                                                                                                                                                                                                          	Foi identificado um escaneamento de portas a partir do endereço IP $SOURCE_IP .	1	4	0
Espaço Livre (< 2GB)	SELECT * FROM `FreeSpace$PARTITION`(lastvalue<2147483648)	18	df -h -x tmpfs -x devtmpfs	shellcommand	Pouco espaço disponível em disco.	0	                                                                                                                                                                                                                                                               	                                                                                                                                                                                                                                                               		1	3	1
Espaço Livre (<10GB)	SELECT * FROM `FreeSpace$PARTITION`(lastvalue<236223201280)	13	df -h -x tmpfs -x devtmpfs	shellcommand	Pouco espaço livre em disco.	0	                                                                                                                                                                                                                                                               	                                                                                                                                                                                                                                                               		1	2	1
Repeat Attack-Login Target for $USER_SSH	select window(*) as events, * from ssh(user_ssh!='null').win:time(1 min) group by user_ssh having count(*) >= 3	3				0	\N	\N	\N	1	1	0
Uso de CPU elevado (%)	SELECT * FROM teste_CPUUsage(lastvalue>80)	12	ps -eo pcpu,pid,user,args | sort -k 1 -r | head -6	shellcommand	Por favor, verifique os processos em execução.	0	usuario@inf.ufpel.edu.br                                                                                                                                                                                                                                       	Uso de CPU elevado                                                                                                                                                                                                                                             	Por favor, verifique os processos em execução.	2	2	1
Várias tentativas de autenticação ao SSH apartir do endereço $IP	SELECT * FROM SSHLog(ip!='null').win:time(1 min) GROUP BY ip HAVING count(*) >= 3	19	echo $IP >> ipsssh.txt	shellcommand	Por favor, verifique o serviço SSHD, possível tentativa de ataque de força bruta, esquecimento de senha ou erro de configuração.	0	\N	\N	\N	1	3	0
\.


--
-- TOC entry 2120 (class 0 OID 16871)
-- Dependencies: 193
-- Data for Name: templates; Type: TABLE DATA; Schema: public; Owner: -
--

COPY templates (templateid, name) FROM stdin;
10002	Template Vazia
10001	Template Linux
10003	Template MX
\.


--
-- TOC entry 1978 (class 2606 OID 16923)
-- Name: hosts_pkey; Type: CONSTRAINT; Schema: public; Owner: -; Tablespace: 
--

ALTER TABLE ONLY templates
    ADD CONSTRAINT hosts_pkey PRIMARY KEY (templateid);


--
-- TOC entry 1960 (class 2606 OID 16925)
-- Name: hosts_templates_pkey; Type: CONSTRAINT; Schema: public; Owner: -; Tablespace: 
--

ALTER TABLE ONLY hosts_templates
    ADD CONSTRAINT hosts_templates_pkey PRIMARY KEY (hosttemplateid);


--
-- TOC entry 1965 (class 2606 OID 16931)
-- Name: item_situation_pkey; Type: CONSTRAINT; Schema: public; Owner: -; Tablespace: 
--

ALTER TABLE ONLY items_situations_hosts
    ADD CONSTRAINT item_situation_pkey PRIMARY KEY (itemsituationid);


--
-- TOC entry 1969 (class 2606 OID 16933)
-- Name: items_pkey; Type: CONSTRAINT; Schema: public; Owner: -; Tablespace: 
--

ALTER TABLE ONLY items_templates
    ADD CONSTRAINT items_pkey PRIMARY KEY (itemid);


--
-- TOC entry 1967 (class 2606 OID 16935)
-- Name: items_situation_template_pkey; Type: CONSTRAINT; Schema: public; Owner: -; Tablespace: 
--

ALTER TABLE ONLY items_situations_templates
    ADD CONSTRAINT items_situation_template_pkey PRIMARY KEY (itemsituationid);


--
-- TOC entry 1963 (class 2606 OID 16937)
-- Name: items_template_copy_pkey; Type: CONSTRAINT; Schema: public; Owner: -; Tablespace: 
--

ALTER TABLE ONLY items_hosts
    ADD CONSTRAINT items_template_copy_pkey PRIMARY KEY (itemid);


--
-- TOC entry 1972 (class 2606 OID 16939)
-- Name: lib_expression_pkey; Type: CONSTRAINT; Schema: public; Owner: -; Tablespace: 
--

ALTER TABLE ONLY library_expression
    ADD CONSTRAINT lib_expression_pkey PRIMARY KEY (name);


--
-- TOC entry 1976 (class 2606 OID 16947)
-- Name: situation_template_pkey; Type: CONSTRAINT; Schema: public; Owner: -; Tablespace: 
--

ALTER TABLE ONLY situations_templates
    ADD CONSTRAINT situation_template_pkey PRIMARY KEY (situationid);


--
-- TOC entry 1974 (class 2606 OID 16949)
-- Name: situations_hosts_copy_pkey; Type: CONSTRAINT; Schema: public; Owner: -; Tablespace: 
--

ALTER TABLE ONLY situations_hosts
    ADD CONSTRAINT situations_hosts_copy_pkey PRIMARY KEY (situationid);


--
-- TOC entry 1958 (class 2606 OID 16951)
-- Name: template_copy_pkey; Type: CONSTRAINT; Schema: public; Owner: -; Tablespace: 
--

ALTER TABLE ONLY hosts
    ADD CONSTRAINT template_copy_pkey PRIMARY KEY (hostid, host);


--
-- TOC entry 1956 (class 1259 OID 16958)
-- Name: host_hostid_key; Type: INDEX; Schema: public; Owner: -; Tablespace: 
--

CREATE UNIQUE INDEX host_hostid_key ON hosts USING btree (hostid);


--
-- TOC entry 1961 (class 1259 OID 16959)
-- Name: items_hosts_itemid_key; Type: INDEX; Schema: public; Owner: -; Tablespace: 
--

CREATE UNIQUE INDEX items_hosts_itemid_key ON items_hosts USING btree (itemid);


--
-- TOC entry 1970 (class 1259 OID 16960)
-- Name: items_templates_itemid_key; Type: INDEX; Schema: public; Owner: -; Tablespace: 
--

CREATE UNIQUE INDEX items_templates_itemid_key ON items_templates USING btree (itemid);


--
-- TOC entry 1979 (class 1259 OID 16961)
-- Name: template_templateid_key; Type: INDEX; Schema: public; Owner: -; Tablespace: 
--

CREATE UNIQUE INDEX template_templateid_key ON templates USING btree (templateid);


--
-- TOC entry 1982 (class 2606 OID 16967)
-- Name: fk_hostid_items_hosts; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY items_hosts
    ADD CONSTRAINT fk_hostid_items_hosts FOREIGN KEY (hostid) REFERENCES hosts(hostid) ON UPDATE CASCADE ON DELETE CASCADE;


--
-- TOC entry 1984 (class 2606 OID 16977)
-- Name: fk_item_situation_hostid; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY items_situations_hosts
    ADD CONSTRAINT fk_item_situation_hostid FOREIGN KEY (hostid) REFERENCES hosts(hostid) ON DELETE CASCADE;


--
-- TOC entry 1985 (class 2606 OID 16982)
-- Name: fk_item_situation_items_hosts; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY items_situations_hosts
    ADD CONSTRAINT fk_item_situation_items_hosts FOREIGN KEY (itemid) REFERENCES items_hosts(itemid) ON DELETE CASCADE;


--
-- TOC entry 1986 (class 2606 OID 16987)
-- Name: fk_item_situation_situation_host; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY items_situations_hosts
    ADD CONSTRAINT fk_item_situation_situation_host FOREIGN KEY (situationid) REFERENCES situations_hosts(situationid) ON DELETE CASCADE;


--
-- TOC entry 1983 (class 2606 OID 16992)
-- Name: fk_itemid_items_template; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY items_hosts
    ADD CONSTRAINT fk_itemid_items_template FOREIGN KEY (itemiditemstemplate) REFERENCES items_templates(itemid) ON UPDATE CASCADE ON DELETE CASCADE;


--
-- TOC entry 1987 (class 2606 OID 16997)
-- Name: fk_items_situation_template_items_templates_1; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY items_situations_templates
    ADD CONSTRAINT fk_items_situation_template_items_templates_1 FOREIGN KEY (itemid) REFERENCES items_templates(itemid) ON DELETE CASCADE;


--
-- TOC entry 1988 (class 2606 OID 17002)
-- Name: fk_items_situation_template_template_situation_1; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY items_situations_templates
    ADD CONSTRAINT fk_items_situation_template_template_situation_1 FOREIGN KEY (situationid) REFERENCES situations_templates(situationid) ON DELETE CASCADE;


--
-- TOC entry 1990 (class 2606 OID 17007)
-- Name: fk_situationshosts_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY situations_hosts
    ADD CONSTRAINT fk_situationshosts_id FOREIGN KEY (situationhostsid) REFERENCES situations_hosts(situationid) ON DELETE CASCADE;


--
-- TOC entry 1980 (class 2606 OID 17012)
-- Name: fk_template_hostid; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY hosts_templates
    ADD CONSTRAINT fk_template_hostid FOREIGN KEY (hostid) REFERENCES hosts(hostid) ON DELETE CASCADE;


--
-- TOC entry 1981 (class 2606 OID 17017)
-- Name: fk_template_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY hosts_templates
    ADD CONSTRAINT fk_template_id FOREIGN KEY (templateid) REFERENCES templates(templateid) ON DELETE CASCADE;


--
-- TOC entry 1989 (class 2606 OID 17022)
-- Name: fk_template_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY items_templates
    ADD CONSTRAINT fk_template_id FOREIGN KEY (templateid) REFERENCES templates(templateid) ON DELETE CASCADE;


-- Completed on 2016-03-27 01:07:35 BRT

--
-- PostgreSQL database dump complete
--

