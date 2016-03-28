## EXEHDA-USM SmartLogger

O SmartLogger foi projetado para receber eventos de diferentes Collector's e/ou SmartLogger's, com o objetivo de fornecer a Ciência de Situação sobre os dispositivos sob a sua coordenação. Em outras palavras, ele oferece a visão sobre a segurança considerando a abrangência da célula (EXEHDACel) onde ele está inserido, ou ainda, a amplitude de células subordinadas a sua dentro da hierarquia. Este componente foi concebido para ser implantado preferencialmente em um dispositivo dedicado e, além de oferecer a percepção, compreensão e projeção dos eventos e situações recebidas, ele oferece um repositório para armazenamento dessas informações, permitindo que elas sejam disponibilizadas em uma interface aos analistas de segurança.

A figura abaixo apresenta uma abstração do componente de software proposto e desenvolvido para o EXEHDA-USM SmartLogger.

<p align="center">
  <img src="https://github.com/rborgesalmeida/exehda-usm/raw/prototipo-dissertacao/smartlogger/exehda-usm-smartlogger.png" width="450"/>
</p>

### Pré-requisitos

O EXEHDA-USM SmartLogger possui alguns pré-requisitos para seu funcionamento que podem ser instalados automaticamente ou manualmente caso ocorra algum erro na execução do script de instalação. A lista de pré-requisitos é apresentada a seguir:

* [mongodb](https://www.mongodb.org/):  is a cross-platform document-oriented database. (GNU AGPL v3.0 e Apache License v2.0)
* [ipy](https://pypi.python.org/pypi/IPy/): class and tools for handling of IPv4 and IPv6 addresses and networks. (BSD License). 
* [openjdk-7-jdk](https://packages.debian.org/en/wheezy/openjdk-7-jdk): OpenJDK is a development environment for building applications, applets, and components using the Java programming language. (GNU GPLv2).
* [esper](http://www.espertech.com/products/index.php) esper is a Complex Event Processing (CEP) written entirely in Java. (GNU GPLv2).

### Instalação Automática
Pode-se utilizar o script install.sh. Ele irá baixar as bibliotecas python citadas acima, o openjdk-7-jdk e os SGBD's postgresql e mongodb. Observação: este script de instalação está homologado apenas para o Debian Jessie (8).

 1. Instalar o git e criar um clone deste repositório:	
 
 	`user@hostname:~$: sudo apt-get install git && cd Downloads && git clone https://github.com/rborgesalmeida/exehda-usm.git`

 1. Acessar o diretório onde estão os arquivos de instalação do EXEHDA-USM SmartLogger:
 
 	`user@hostname:~/Downloads/$: cd exehda-usm/smartlogger/`

 1. Conceder permissão de execução ao script de instalação:
 
	`user@hostname:~/Downloads/exehda-usm/smartlogger/$: chmod +x install.sh`

 1. Executar a instalação: 
 
	`user@hostname:~/Downloads/exehda-usm/smartlogger/$: ./install.sh`

### Instalação Manual
Em caso de erros no script de instalação, considerar a instalação manual dos pré-requisitos que falharam. Certificar-se de que o passo 1 da instalação automática foi executado.

1. Instalar o python e requisitos para as demais bibliotecas:

	`user@hostname:~$: apt-get install build-essentials libcurl4-gnutls-dev python python-dev gcc make python-setuptools openjdk-7-jdk`
	
1. Instalar mongodb:

```
user@hostname:~$: sudo apt-key adv --keyserver hkp://keyserver.ubuntu.com:80 --recv EA312927
user@hostname:~$: echo "deb http://repo.mongodb.org/apt/debian wheezy/mongodb-org/3.2 main" | sudo tee /etc/apt/sources.list.d/mongodb-org-3.2.list
user@hostname:~$: sudo apt-get update
user@hostname:~$: sudo apt-get install -y mongodb-org=3.2.4 mongodb-org-server=3.2.4 mongodb-org-shell=3.2.4 mongodb-org-mongos=3.2.4 mongodb-org-tools=3.2.4
user@hostname:~$: sudo service mongod start
```

1. Criar o usuário e a base de dados não-relacional para os eventos e situações da EXEHDA-USM. Substituir $EXEHDAUSMDBN e $EXEHDAUSMUSER pelo nome do usuário e senha para a base não-relacional. Não esquecer de alterar as configurações no arquivo exehda-usm-smartlogger.conf: 

`user@hostname:~$: sudo mongo --eval "db.getSiblingDB('$EXEHDAUSMDBN').createUser({user: '$EXEHDAUSMUSER', pwd: '$EXEHDAUSMDBNP', roles: ['readWrite', 'dbAdmin']})"`

	
1. Instalar as bibliotecas manualmente: 

	`user@hostname:~$: easy_install ipy pymongo`
	
1. Configurar a variável de ambiente do java: 
 
	```
	user@hostname:~$: sudo echo 'JAVA_HOME="/usr/lib/jvm/java-7-openjdk-amd64/"' >> /etc/environment
	user@hostname:~$: JAVA_HOME="/usr/lib/jvm/java-7-openjdk-amd64/"
  user@hostname:~$: export JAVA_HOME
	```

1. Copiar os os arquivos do EXEHDA-USM SmartLogger para o diretório desejado e criar o diretório para armazenamento dos logs:

 	`root@hostname:~#: mkdir -p /etc/exehda-usm/smartlogger && mkdir -p /var/log/exehda-usm/ && cp -a /home/user/Downloads/exehda-usm/smartlogger/ /etc/exehda-usm/smartlogger/`
