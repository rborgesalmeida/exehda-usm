# EXEHDA-USM Collector

Este componente de software foi projetado para ser implantado em um hardware dedicado, internamente a um dispositivo de segurança (IDS, WAF, entre outros), ou a servidores que oferecem serviços de rede (web, e-mail, banco de dados, entre outros). A figura abaixo apresenta uma abstração do componente de software proposto e desenvolvido para o Collector, demonstrando o fluxo de comunicação entre os módulos. Cada um dos módulos presentes na figura será descrito nas subseções seguintes.

<p align="center">
  <img src="https://github.com/rborgesalmeida/exehda-usm/raw/prototipo-dissertacao/collector/exehda-usm-collector.png" width="350"/>
</p>


## Pré-requisitos

O CPNM Agent possui alguns pré-requisitos para seu funcionamento que podem ser instalados automaticamente ou manualmente caso ocorra algum erro na execução do script de instalação. A lista de pré-requisitos é apresentada a seguir:

* [geoip2](https://pypi.python.org/pypi/geoip2): This package provides an API for the GeoIP2 web services and databases. The API also works with MaxMind’s free GeoLite2 databases. (Apache License, Version 2.0).
* [geoipupdate](https://github.com/maxmind/geoipupdate): The GeoIP Update program performs automatic updates of GeoIP2 and GeoIP Legacy binary databases. Currently the program only supports Linux and other Unix- like systems. (GNU GPLv2).
* [httpagentparser](https://pypi.python.org/pypi/httpagentparser/): Extracts OS Browser etc information from http user agent string. (MIT License).
* [psutil](https://pypi.python.org/pypi/psutil/): psutil is a cross-platform library for retrieving information on running processes and system utilization (CPU, memory, disks, network) in Python. (BSD License).
* [ipy](https://pypi.python.org/pypi/IPy/): class and tools for handling of IPv4 and IPv6 addresses and networks.
* [netifaces](https://pypi.python.org/pypi/netifaces/): portable network interface information. (MIT License).
* [pyparsing](https://pypi.python.org/pypi/pyparsing/): the pyparsing module is an alternative approach to creating and executing  simple grammars, vs. the traditional lex/yacc approach, or the use of  regular expressions. (MIT License).
* [openjdk-7-jdk](https://packages.debian.org/en/wheezy/openjdk-7-jdk): OpenJDK is a development environment for building applications, applets, and components using the Java programming language.
* [esper](http://www.espertech.com/products/index.php) esper is a Complex Event Processing (CEP) written entirely in Java.
 
## Instalação Automática
Pode-se utilizar o script install.sh. Ele irá baixar as bibliotecas python citadas acima e a base de dados para geolocalização. Realizará a adição no agendador de tarefas de uma rotina para atualização desta base de dados. Observação: este script de instalação está homologado apenas para o Debian Jessie (8).

 1. Logar como root:
 2. `user@hostname:~$: sudo su -` ou `user@hostname:~$: su -`
 1. Acessar o diretório onde estão os arquivos de instalação do EXEHDA-USM Collector:
    `root@hostname:~#: cd /home/user/Downloads/exehda-usm/collector/`
 1. Conceder permissão de execução ao script de instalação:
		`root@hostname:/home/user/Downloads/exehda-usm/collector/#: chmod +x install.sh`
 1. Executar a instalação: 
		root@hostname:~#: ./install.sh

## Instalação Manual
Em caso de erros no script de instalação, considerar a instalação manual dos pré-requisitos que falharam.


