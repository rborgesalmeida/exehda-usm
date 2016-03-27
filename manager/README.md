# EXEHDA-USM Manager

O Manager foi concebido no intuito de centralizar a visualização da Ciência de Situação sobre a segurança do ambiente ubíquo como um todo. Assim como o SmartLogger, por ser baseado no EXEHDAbase, ele poderá empregar estratégias de distribuição dos serviços, fornecendo escalabilidade. Esta característica também poderá ser explorada pelos aspectos arquiteturais, onde por exemplo, caso ocorra uma sobrecarga do Manager, poderão ser instanciados dois SmartLoggers para divisão da atual carga de responsabilidade exclusiva do Manager, passando os novos SmartLogger's a enviar os eventos e/ou situações já tratados para o Manager.

A figura abaixo apresenta uma abstração do componente de software proposto e desenvolvido para o EXEHDA-USM Manager.

<p align="center">
  <img src="https://github.com/rborgesalmeida/exehda-usm/raw/prototipo-dissertacao/manager/exehda-usm-manager.png" width="350"/>
</p>

Conforme pode ser observado, o módulo "Percepção - Nível n"  foi projetado para receber eventos de diferentes Collector's e/ou SmartLogger's, com o objetivo de aprimorar o nível de Ciência de Situação sobre os diversos dispositivos sob a sua coordenação na hierarquia da arquitetura. Igualmente ao SmartLogger, este componente foi concebido para ser implementado preferencialmente em um hardware dedicado.

Os módulos "Compreensão - Nível n" e "Projeção - Nível n" também foram projetados com características similares as disponíveis no SmartLogger, incluindo a correlação cruzada e a atuação distribuída.

Para suportar o armazenamento de eventos e situações no Manager, e as configurações dos perfis de execução dos demais componentes por meio das templates, foi proposto o ``Repositório Híbrido de Informações Contextuais'', o qual, em sua implementação foi composto de: modelo não-relacional e relacional.

## Pré-requisitos

O EXEHDA-USM Manager possui alguns pré-requisitos para seu funcionamento que podem ser instalados automaticamente ou manualmente caso ocorra algum erro na execução do script de instalação. A lista de pré-requisitos é apresentada a seguir:

* [postgresql](http://www.postgresql.org/): PostgreSQL is a powerful, open source object-relational database system. (PostgreSQL License).
* [mongodb](https://www.mongodb.org/):  is a cross-platform document-oriented database. (GNU AGPL v3.0 e Apache License v2.0)
* [ipy](https://pypi.python.org/pypi/IPy/): class and tools for handling of IPv4 and IPv6 addresses and networks. (BSD License). 
* [openjdk-7-jdk](https://packages.debian.org/en/wheezy/openjdk-7-jdk): OpenJDK is a development environment for building applications, applets, and components using the Java programming language. (GNU GPLv2).
* [esper](http://www.espertech.com/products/index.php) esper is a Complex Event Processing (CEP) written entirely in Java. (GNU GPLv2).

