#!/bin/bash

###################################################################################
DIREXEHDAUSMCOLL="/etc/exehda-usm/collector"                                      #
###################################################################################

mkdir -p $DIREXEHDAUSMCOLL
mkdir -p /var/log/exehda-usm/

echo "Copiando os arquivos para o diretorio padrao..." 
cp -a * $DIREXEHDAUSMCOLL

# Executa a instalação de todas as bibliotecas necessárias para o funcionamento do EXEHDA-USM Collector #
apt-get install python-pip curl build-essentials libcurl4-gnutls-dev python2.7-dev zlib1g-dev gcc make python-setuptools

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

mkdir -p /usr/local/share/GeoIP

# Baixando as bases de dados para a geolocalização #
echo "Baixando as bases de dados para geolocalização..."
geoipupdate

RETORNO="$?"
if [ "$RETORNO" -ne 0 ]; then
echo "ERRO: Não foi possível realizar o download das bases de dados para geolocalização. Por favor, realize o download e configuração manualmente."
elif [ "$RETORNO" -eq 0 ]; then
    echo "Download realizado com sucesso."
fi

echo "Configurando o agendador de tarefas para atualização automática das bases de dados para geolocalização..."

> /etc/cron.daily/geoipupdate

chmod +x /etc/cron.daily/geoipupdate

echo "#!/bin/bash

geoipupdate" > /etc/cron.daily/geoipupdate

RETORNO="$?"
if [ "$RETORNO" -ne 0 ]; then
    echo "ERRO: Não foi possível configurar o cron para atualização automática das bases de dados para geolocalização. Por favor, realize está configuração manualmente."
elif [ "$RETORNO" -eq 0 ]; then
    echo "Configuração realizada com sucesso."
fi

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

if [ -z "${JAVA_HOME}" ]
then
  echo 'JAVA_HOME="/usr/lib/jvm/java-7-openjdk-amd64/"' >> /etc/environment
fi
####################################################

echo "Parabéns, processo de instalação concluído. Caso alguma mensagem de erro tenha sido gerada, corrija o erro. Indicamos fortemente a leitura da documentação no item de Instalação Manual."
echo "Obrigado. Bom trabalho."
