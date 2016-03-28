## EXEHDA-USM Manager

O Manager foi concebido no intuito de centralizar a visualização da Ciência de Situação sobre a segurança do ambiente ubíquo como um todo. Assim como o SmartLogger, por ser baseado no EXEHDAbase, ele poderá empregar estratégias de distribuição dos serviços, fornecendo escalabilidade. Esta característica também poderá ser explorada pelos aspectos arquiteturais, onde por exemplo, caso ocorra uma sobrecarga do Manager, poderão ser instanciados dois SmartLoggers para divisão da atual carga de responsabilidade exclusiva do Manager, passando os novos SmartLogger's a enviar os eventos e/ou situações já tratados para o Manager.

A figura abaixo apresenta uma abstração do componente de software proposto e desenvolvido para o EXEHDA-USM Manager.

<p align="center">
  <img src="https://github.com/rborgesalmeida/exehda-usm/raw/prototipo-dissertacao/manager/exehda-usm-manager.png" width="350"/>
</p>

Conforme pode ser observado, o módulo "Percepção - Nível n"  foi projetado para receber eventos de diferentes Collector's e/ou SmartLogger's, com o objetivo de aprimorar o nível de Ciência de Situação sobre os diversos dispositivos sob a sua coordenação na hierarquia da arquitetura. Igualmente ao SmartLogger, este componente foi concebido para ser implementado preferencialmente em um hardware dedicado.

Os módulos "Compreensão - Nível n" e "Projeção - Nível n" também foram projetados com características similares as disponíveis no SmartLogger, incluindo a correlação cruzada e a atuação distribuída.

Para suportar o armazenamento de eventos e situações no Manager, e as configurações dos perfis de execução dos demais componentes por meio das templates, foi proposto o ``Repositório Híbrido de Informações Contextuais'', o qual, em sua implementação foi composto de: modelo não-relacional e relacional.

### Pré-requisitos

O EXEHDA-USM Manager possui alguns pré-requisitos para seu funcionamento que podem ser instalados automaticamente ou manualmente caso ocorra algum erro na execução do script de instalação. A lista de pré-requisitos é apresentada a seguir:

* [postgresql](http://www.postgresql.org/): PostgreSQL is a powerful, open source object-relational database system. (PostgreSQL License).
* [mongodb](https://www.mongodb.org/):  is a cross-platform document-oriented database. (GNU AGPL v3.0 e Apache License v2.0)
* [ipy](https://pypi.python.org/pypi/IPy/): class and tools for handling of IPv4 and IPv6 addresses and networks. (BSD License). 
* [openjdk-7-jdk](https://packages.debian.org/en/wheezy/openjdk-7-jdk): OpenJDK is a development environment for building applications, applets, and components using the Java programming language. (GNU GPLv2).
* [esper](http://www.espertech.com/products/index.php) esper is a Complex Event Processing (CEP) written entirely in Java. (GNU GPLv2).

### Instalação Automática
Pode-se utilizar o script install.sh. Ele irá baixar as bibliotecas python citadas acima, o openjdk-7-jdk e os SGBD's postgresql e mongodb. Observação: este script de instalação está homologado apenas para o Debian Jessie (8).

 1. Instalar o git e criar um clone deste repositório:	
 
 	`user@hostname:~$: sudo apt-get install git && cd Downloads && git clone https://github.com/rborgesalmeida/exehda-usm.git`

 1. Acessar o diretório onde estão os arquivos de instalação do EXEHDA-USM Collector:
 
 	`user@hostname:~/Downloads/$: cd exehda-usm/manager/`

 1. Conceder permissão de execução ao script de instalação:
 
	`user@hostname:~/Downloads/exehda-usm/manager/$: chmod +x install.sh`

 1. Executar a instalação: 
 
	`user@hostname:~/Downloads/exehda-usm/manager/$: ./install.sh`

### Instalação Manual
Em caso de erros no script de instalação, considerar a instalação manual dos pré-requisitos que falharam. Certificar-se de que o passo 1 da instalação automática foi executado.

1. Instalar o python, postgresql e requisitos para as demais bibliotecas:

	`user@hostname:~$: apt-get install build-essentials libcurl4-gnutls-dev python python-dev gcc make python-setuptools openjdk-7-jdk postgresql python-psycopg2`
	
1. Instalar mongodb:

```
user@hostname:~$: sudo apt-key adv --keyserver hkp://keyserver.ubuntu.com:80 --recv EA312927
user@hostname:~$: echo "deb http://repo.mongodb.org/apt/debian wheezy/mongodb-org/3.2 main" | sudo tee /etc/apt/sources.list.d/mongodb-org-3.2.list
user@hostname:~$: sudo apt-get update
user@hostname:~$: sudo apt-get install -y mongodb-org=3.2.4 mongodb-org-server=3.2.4 mongodb-org-shell=3.2.4 mongodb-org-mongos=3.2.4 mongodb-org-tools=3.2.4
user@hostname:~$: sudo service mongod start
```

1. Configurar a senha para o usuário postgres:

`user@hostname:~$: sudo -u postgres psql postgres `

1. Criar o usuário e a base de dados relacional para a EXEHDA-USM. Substituir $EXEHDAUSMUSER e $EXEHDAUSMDBR pelo nome do usuário e senha para a base relacional. Não esquecer de alterar as configurações no arquivo exehda-usm-manager.conf:

```
user@hostname:~$: sudo -u postgres createuser -D -A -P $EXEHDAUSMUSER
user@hostname:~$: sudo -u postgres createdb -O $EXEHDAUSMUSER $EXEHDAUSMDBR
user@hostname:~$: sudo psql -U $EXEHDAUSMUSER -h 127.0.0.1 $EXEHDAUSMDBR < exehdausmdbr.sql
```

1. Criar o usuário e a base de dados não-relacional para os eventos e situações da EXEHDA-USM. Substituir $EXEHDAUSMDBN e $EXEHDAUSMUSER pelo nome do usuário e senha para a base não-relacional. Não esquecer de alterar as configurações no arquivo exehda-usm-manager.conf: 

`user@hostname:~$: sudo mongo --eval "db.getSiblingDB('$EXEHDAUSMDBN').createUser({user: '$EXEHDAUSMUSER', pwd: '$EXEHDAUSMDBNP', roles: ['readWrite', 'dbAdmin']})"`

	
1. Instalar as bibliotecas manualmente: 

	`user@hostname:~$: easy_install ipy pymongo`
	
1. Configurar a variável de ambiente do java: 
 
	```
	user@hostname:~$: sudo echo 'JAVA_HOME="/usr/lib/jvm/java-7-openjdk-amd64/"' >> /etc/environment
	user@hostname:~$: JAVA_HOME="/usr/lib/jvm/java-7-openjdk-amd64/"
  user@hostname:~$: export JAVA_HOME
	```

1. Copiar os os arquivos do EXEHDA-USM Manager para o diretório desejado e criar o diretório para armazenamento dos logs:

 	`root@hostname:~#: mkdir -p /etc/exehda-usm/manager && mkdir -p /var/log/exehda-usm/ && cp -a /home/user/Downloads/exehda-usm/manager/ /etc/exehda-usm/manager/`
