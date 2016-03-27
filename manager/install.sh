#!/bin/bash

###################################################################################
DIREXEHDAUSMMANAGER="/etc/exehda-usm/manager"         				  #
EXEHDAUSMUSER="exehdausmadmin"         				  #
EXEHDAUSMDBR="exehdausm"
EXEHDAUSMDBN="exehdausmevents"
EXEHDAUSMDBNP="exehdausmdbnpassword"
###################################################################################

sudo mkdir -p $DIREXEHDAUSMMANAGER
sudo mkdir -p /var/log/exehda-usm/

echo "Copiando arquivos para diretório padrão" 
sudo cp -a * $DIREXEHDAUSMMANAGER

# Executa a instalação de todas as bibliotecas necessárias para o funcionamento do EXEHDA-USM Manager #
read -e -p "Install PostgreSQL database? [y/n] " -i "n" installpg
if [ "$installpg" = "y" ]; then
  sudo apt-get install postgresql
  echo
  echo "You will now set the default password for the postgres user."
  echo "This will open a psql terminal, enter:"
  echo
  echo "\\password postgres"
  echo
  echo "and follow instructions for setting postgres admin password."
  echo "Press Ctrl+D or type \\q to quit psql terminal"
  echo "START psql --------"
  sudo -u postgres psql postgres
  echo "END psql --------"
  echo
fi

read -e -p "Create EXEHDA-USM relational database and user? [y/n] " -i "n" createdb
if [ "$createdb" = "y" ]; then
	sudo -u postgres createuser -D -A -P $EXEHDAUSMUSER
	sudo -u postgres createdb -O $EXEHDAUSMUSER $EXEHDAUSMDBR
	echo
	echo "Lembre de atualizar o arquivo exehda-usm-manager.conf!"
	echo
fi

echo
echo "You must update postgresql configuration to allow password based authentication"
echo "(if you have not already done this)."
echo
echo "Add the following to pg_hba.conf or postgresql.conf (depending on version of postgresql installed)"
echo "located in folder /etc/postgresql/<version>/main/"
echo
echo "host all all 127.0.0.1/32 md5"
echo
echo "After you have updated, restart the postgres server: sudo service postgresql restart"
echo

read -e -p "If you already configured pg_hba.conf, do you want import database? [y/n] " -i "n" importdb
if [ "$importdb" = "y" ]; then
	sudo psql -U $EXEHDAUSMUSER -h 127.0.0.1 $EXEHDAUSMDBR < exehdausmdbr.sql
fi


sudo apt-key adv --keyserver hkp://keyserver.ubuntu.com:80 --recv EA312927
echo "deb http://repo.mongodb.org/apt/debian wheezy/mongodb-org/3.2 main" | sudo tee /etc/apt/sources.list.d/mongodb-org-3.2.list
sudo apt-get update
sudo apt-get install -y mongodb-org=3.2.4 mongodb-org-server=3.2.4 mongodb-org-shell=3.2.4 mongodb-org-mongos=3.2.4 mongodb-org-tools=3.2.4
sudo service mongod start

echo "Criando usuário e base de dados para eventos e situacões..."
sudo mongo --eval "db.getSiblingDB('$EXEHDAUSMDBN').createUser({user: '$EXEHDAUSMUSER', pwd: '$EXEHDAUSMDBNP', roles: ['readWrite', 'dbAdmin']})"

sudo apt-get install python-setuptools python-dev python
echo "Instalando ipy..."
sudo easy_install ipy

RETORNO="$?"
if [ "$RETORNO" -ne 0 ]; then
    echo "ERRO: Não foi possível realizar a instalação do ipy. Por favor, realize a instalação manualmente."
elif [ "$RETORNO" -eq 0 ]; then
    echo "Instalação concluída."
fi

echo "Instalando psycopg2..."
sudo apt-get install python-psycopg2

RETORNO="$?"
if [ "$RETORNO" -ne 0 ]; then
    echo "ERRO: Não foi possível realizar a instalação do psycopg2. Por favor, realize a instalação manualmente."
elif [ "$RETORNO" -eq 0 ]; then
    echo "Instalação concluída."
fi


echo "Instalando pymongo..."
sudo easy_install pymongo

RETORNO="$?"
if [ "$RETORNO" -ne 0 ]; then
    echo "ERRO: Não foi possível realizar a instalação do pymongo. Por favor, realize a instalação manualmente."
elif [ "$RETORNO" -eq 0 ]; then
    echo "Instalação concluída."
fi


#################################################################################################

sudo apt-get install openjdk-7-jdk
JAVA_HOME="/usr/lib/jvm/java-7-openjdk-amd64/"
export JAVA_HOME

if [ -z "${JAVA_HOME}" ]
then
  sudo echo 'JAVA_HOME="/usr/lib/jvm/java-7-openjdk-amd64/"' >> /etc/environment
fi
####################################################

echo "Parabéns, processo de instalação concluído. Caso alguma mensagem de erro tenha sido gerada, corrija o erro. Indicamos fortemente a leitura da documentação no item de Instalação Manual."
echo "Obrigado. Bom trabalho."

