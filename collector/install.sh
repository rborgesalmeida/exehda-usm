#!/bin/bash

# Declaração de variáveis #
###############################################################################################################
# Variáveis utilizadas somente se deseja enviar a chave pública através do SCP para o servidor CPNM_Server    #
#SERVERIP="200.132.102.195"
#PORT="50000"
#SERVERUSER="exehda-usm-user"
#DIRCPNMSERVER="/etc/exehda-usm/manager"
# Adquire o nome da máquina para nomear a chave pública enviada ao servidor       #
HOSTNAME=$(hostname -s)                                                           #
###################################################################################
# Linha para adição no cron da atualização das bases de dados de geolocalização   #
#CRONTABGEOIP="00 01 * * * sh /etc/cpnm/cpnm-agent/geoipupdate.sh"                 #
DIREXEHDAUSMCOLL="/etc/exehda-usm/collector"                                               #
###################################################################################

#mkdir -p $DIRCPNMAGENT
#cp -a src/cpnm-agent/* $DIRCPNMAGENT

# Geração da chave pública e da chave privada
#echo "Gerando a chave privada..."
#openssl genrsa -out $DIRCPNMAGENT/privateKey.key 1024

#RETORNO="$?"
#if [ "$RETORNO" -ne 0 ]; then
#    echo "ERRO: Não foi possível gerar a chave privada. Realize este processo manualmente, assim como a geração da chave pública."
#elif [ "$RETORNO" -eq 0 ]; then
#    echo "Chave privada gerada com sucesso. Gerando a chave pública..."
#    openssl rsa -in $DIRCPNMAGENT/privateKey.key -pubout > $DIRCPNMAGENT/publicKey.key 2>/dev/null
#    RETORNO="$?"
#    if [ "$RETORNO" -ne 0 ]; then
#        echo "ERRO: Não foi possível gerar a chave pública. Realize este processo manualmente."
#    elif [ "$RETORNO" -eq 0 ]; then
#        echo "Chave pública gerada com sucesso."
#    fi
#fi
# Envio da chave pública para o servidor
# Pede uma confirmaça~Co do usua~Ario antes de executar
#echo "Você deseja enviar a chave pública para o servidor utilizando o scp? [S/N]: "
#read RESPOSTA
#while [ "$RESPOSTA" != "S" ] && [ "$RESPOSTA" != "N" ]; do
#        echo "Por favor, entre com uma opção válida [S/N]: "
#        read RESPOSTA
#done

#if [ "$RESPOSTA" == "S" ]; then
#    scp -P $PORT $DIRCPNMAGENT/publicKey.key $SERVERUSER@$SERVERIP:$DIRCPNMSERVER/pubKeyClients/$HOSTNAME.key
#fi


# Executa a instalação de todas as bibliotecas necessárias para o funcionamento do CPNM_Agent #
apt-get install python-pip curl libcurl4-gnutls-dev
apt-get install python2.7-dev

apt-get install zlib1g-dev make
# apt-get install python-pip
# apt-get install python2.7-dev
echo "Instalando netifaces..."
easy_install netifaces

RETORNO="$?"
if [ "$RETORNO" -ne 0 ]; then
    echo "ERRO: Não foi possível realizar a instalação do netifaces. Por favor, realize a instalação manualmente."
elif [ "$RETORNO" -eq 0 ]; then
    echo "Instalação concluída."
fi
echo "Instalando ipy..."
easy_install ipy

RETORNO="$?"
if [ "$RETORNO" -ne 0 ]; then
    echo "ERRO: Não foi possível realizar a instalação do ipy. Por favor, realize a instalação manualmente."
elif [ "$RETORNO" -eq 0 ]; then
    echo "Instalação concluída."
fi
echo "Instalando pympler..."
easy_install pympler


RETORNO="$?"
if [ "$RETORNO" -ne 0 ]; then
    echo "ERRO: Não foi possível realizar a instalação do pympler. Por favor, realize a instalação manualmente."
elif [ "$RETORNO" -eq 0 ]; then
    echo "Instalação concluída."
fi

echo "Instalando psutil..."
easy_install psutil

RETORNO="$?"
if [ "$RETORNO" -ne 0 ]; then
    echo "ERRO: Não foi possível realizar a instalação do psutil. Por favor, realize a instalação manualmente."
elif [ "$RETORNO" -eq 0 ]; then
    echo "Instalação concluída."
fi

echo "Instalando httpagentparser..."
easy_install httpagentparser

RETORNO="$?"
if [ "$RETORNO" -ne 0 ]; then
    echo "ERRO: Não foi possível realizar a instalação do httpagentparser. Por favor, realize a instalação manualmente."
elif [ "$RETORNO" -eq 0 ]; then
    echo "Instalação concluída."
fi

echo "Instalando geoip2..."
easy_install geoip2

RETORNO="$?"
if [ "$RETORNO" -ne 0 ]; then
    echo "ERRO: Não foi possível realizar a instação do geoip2. Por favor, realize a instalação manualmente."
elif [ "$RETORNO" -eq 0 ]; then
    echo "Instalação concluída."
fi

echo "Instalando pycrypto..."
easy_install pycrypto

RETORNO="$?"
if [ "$RETORNO" -ne 0 ]; then
    echo "ERRO: Não foi possível realizar a instalação do pycrypto. Por favor, realize a instalação manualmente."
elif [ "$RETORNO" -eq 0 ]; then
    echo "Instalação concluída."
fi

#################################################################################################

# Baixando as bases de dados para a geolocalização #
echo "Baixando as bases de dados para geolocalização..."
#sh $DIREXEHDAUSMCOLL/geoipupdade.sh
#zlib

cd $DIREXEHDAUSMCOLL

wget https://github.com/maxmind/geoipupdate/releases/download/v2.2.1/geoipupdate-2.2.1.tar.gz

tar -zxvf geoipupdate-2.2.1.tar.gz

cd geoipupdate-2.2.1/
./configure
make
make install

> /usr/local/etc/GeoIP.conf

echo "# The following UserId and LicenseKey are required placeholders:
UserId 999999
LicenseKey 000000000000

# Include one or more of the following ProductIds:
# * GeoLite2-City - GeoLite 2 City
# * GeoLite2-Country - GeoLite2 Country
# * 506 - GeoLite Legacy Country
# * 517 - GeoLite Legacy ASN
# * 533 - GeoLite Legacy City
ProductIds GeoLite2-City GeoLite2-Country 506 517 533" > /usr/local/etc/GeoIP.conf

mkdir /usr/local/share/GeoIP

geoipupdate

RETORNO="$?"
if [ "$RETORNO" -ne 0 ]; then
echo "ERRO: Não foi possível realizar o download das bases de dados para geolocalização. Por favor, realize o download e configuração manualmente."
elif [ "$RETORNO" -eq 0 ]; then
    echo "Download realizado com sucesso."
fi

echo "Configurando o agendador de tarefas para atualização automática das bases de dados para geolocalização..."
(crontab -l; echo "$CRONTABGEOIP") | crontab -

RETORNO="$?"
if [ "$RETORNO" -ne 0 ]; then
    echo "ERRO: Não foi possível configurar o cron para atualização automática das bases de dados para geolocalização. Por favor, realize está configuração manualmente."
elif [ "$RETORNO" -eq 0 ]; then
    echo "Configuração realizada com sucesso."
fi

#PYPARSING
#apt-get install python-pyparsing
easy_install pyparsing
RETORNO="$?"
if [ "$RETORNO" -ne 0 ]; then
    echo "ERRO: Não foi possível realizar a instalação dparsing. Por favor, realize a instalação manualmente."
elif [ "$RETORNO" -eq 0 ]; then
    echo "Instalação concluída."
fi

apt-get install openjdk-7-jdk
JAVA_HOME="/usr/lib/jvm/java-7-openjdk-amd64/"
export JAVA_HOME
# passar para /etc/enviroment

#if [ -z "${JAVA_HOME}" ]
#then
#  echo "JAVA_HOME not set"
#  exit 0
#fi
####################################################

echo "Parabéns, processo de instalação concluído. Caso alguma mensagem de erro tenha sido gerada, corrija o erro. Indicamos fortemente a leitura da documentação no item de Instalação Manual."
echo "Obrigado. Bom trabalho."
