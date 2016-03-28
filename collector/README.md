## EXEHDA-USM Collector

Este componente de software foi projetado para ser implantado em um hardware dedicado, internamente a um dispositivo de segurança (IDS, WAF, entre outros), ou a servidores que oferecem serviços de rede (web, e-mail, banco de dados, entre outros). A figura abaixo apresenta uma abstração do componente de software proposto e desenvolvido para o Collector, demonstrando o fluxo de comunicação entre os módulos. Cada um dos módulos presentes na figura será descrito nas subseções seguintes.

<p align="center">
  <img src="https://github.com/rborgesalmeida/exehda-usm/raw/prototipo-dissertacao/collector/exehda-usm-collector.png" width="350"/>
</p>


### Pré-requisitos

O EXEHDA-USM Collector possui alguns pré-requisitos para seu funcionamento que podem ser instalados automaticamente ou manualmente caso ocorra algum erro na execução do script de instalação. A lista de pré-requisitos é apresentada a seguir:

* [geoip2](https://pypi.python.org/pypi/geoip2): This package provides an API for the GeoIP2 web services and databases. The API also works with MaxMind’s free GeoLite2 databases. (Apache License, Version 2.0).
* [geoipupdate](https://github.com/maxmind/geoipupdate): The GeoIP Update program performs automatic updates of GeoIP2 and GeoIP Legacy binary databases. Currently the program only supports Linux and other Unix- like systems. (GNU GPLv2).
* [httpagentparser](https://pypi.python.org/pypi/httpagentparser/): Extracts OS Browser etc information from http user agent string. (MIT License).
* [psutil](https://pypi.python.org/pypi/psutil/): psutil is a cross-platform library for retrieving information on running processes and system utilization (CPU, memory, disks, network) in Python. (BSD License).
* [ipy](https://pypi.python.org/pypi/IPy/): class and tools for handling of IPv4 and IPv6 addresses and networks. (BSD License).
* [netifaces](https://pypi.python.org/pypi/netifaces/): portable network interface information. (MIT License).
* [pyparsing](https://pypi.python.org/pypi/pyparsing/): the pyparsing module is an alternative approach to creating and executing  simple grammars, vs. the traditional lex/yacc approach, or the use of  regular expressions. (MIT License).
* [openjdk-7-jdk](https://packages.debian.org/en/wheezy/openjdk-7-jdk): OpenJDK is a development environment for building applications, applets, and components using the Java programming language. (GNU GPLv2).
* [esper](http://www.espertech.com/products/index.php) esper is a Complex Event Processing (CEP) written entirely in Java. (GNU GPLv2).
 
### Instalação Automática
Pode-se utilizar o script install.sh. Ele irá baixar as bibliotecas python citadas acima e a base de dados para geolocalização. Realizará a adição no agendador de tarefas de uma rotina para atualização desta base de dados. Observação: este script de instalação está homologado apenas para o Debian Jessie (8).

 1. Instalar o git e criar um clone deste repositório:	
 
 	`user@hostname:~$: sudo apt-get install git && cd Downloads && git clone https://github.com/rborgesalmeida/exehda-usm.git`

 1. Acessar o diretório onde estão os arquivos de instalação do EXEHDA-USM Collector:
 
 	`user@hostname:~/Downloads/$: cd exehda-usm/collector/`

 1. Conceder permissão de execução ao script de instalação:
 
	`user@hostname:~/Downloads/exehda-usm/collector/$: chmod +x install.sh`

 1. Executar a instalação: 
 
	`user@hostname:~/Downloads/exehda-usm/collector/$: ./install.sh`

### Instalação Manual
Em caso de erros no script de instalação, considerar a instalação manual dos pré-requisitos que falharam. Certificar-se de que o passo 1 da instalação automática foi executado.

1. Instalar o python e requisitos para as demais bibliotecas:

	`user@hostname:~$: apt-get install curl build-essentials libcurl4-gnutls-dev python python-dev zlib1g-dev gcc make python-setuptools openjdk-7-jdk`
	
1. Instalar as bibliotecas manualmente: 

	`user@hostname:~$: easy_install netifaces ipy psutil httpagentparser geoip2 pyparsing`
	
1. Instalar o geoipupdate:

	`user@hostname:~$: wget https://github.com/maxmind/geoipupdate/releases/download/v2.2.1/geoipupdate-2.2.1.tar.gz && tar -zxvf geoipupdate-2.2.1.tar.gz && cd geoipupdate-2.2.1/ && sudo ./configure && sudo make && sudo make install`

1. Criar arquivo de configuração para o geoipupdate:

	```
	user@hostname:~$: sudo > /usr/local/etc/GeoIP.conf
	user@hostname:~$: sudo echo "# The following UserId and LicenseKey are required placeholders:
		UserId 999999
		LicenseKey 000000000000 
		# Include one or more of the following ProductIds:
		# * GeoLite2-City - GeoLite 2 City
		# * GeoLite2-Country - GeoLite2 Country
		# * 506 - GeoLite Legacy Country
		# * 517 - GeoLite Legacy ASN
		# * 533 - GeoLite Legacy City
		ProductIds GeoLite2-City GeoLite2-Country 506 517 533" > /usr/local/etc/GeoIP.conf
	```
	
1. Criar diretório padrão de armazenamento das bases e executar a primeira atualização:	
	 
	`user@hostname:~$: sudo mkdir -p /usr/local/share/GeoIP && geoipupdate`
	
1. Configurar o agendador de tarefas:

	```
	user@hostname:~$: sudo echo "#!/bin/bash
	geoipupdate" > /etc/cron.daily/geoipupdate
	user@hostname:~$: sudo chmod +x /etc/cron.daily/geoipupdate
  ```

1. Configurar a variável de ambiente do java: 
 
	```
	user@hostname:~$: sudo echo 'JAVA_HOME="/usr/lib/jvm/java-7-openjdk-amd64/"' >> /etc/environment
	user@hostname:~$: JAVA_HOME="/usr/lib/jvm/java-7-openjdk-amd64/"
  user@hostname:~$: export JAVA_HOME
	```

1. Copiar os os arquivos do EXEHDA-USM Collector para o diretório desejado e criar o diretório para armazenamento dos logs:

 	`root@hostname:~#: mkdir -p /etc/exehda-usm/collector && mkdir -p /var/log/exehda-usm/ && cp -a /home/user/Downloads/exehda-usm/collector/ /etc/exehda-usm/collector/`

