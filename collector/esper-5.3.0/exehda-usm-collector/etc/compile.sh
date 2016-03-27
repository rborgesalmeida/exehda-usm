#!/bin/sh

# A note to cygwin users: please replace "-cp ${CLASSPATH}" with "-cp `cygpath -wp $CLASSPATH`"
#

cd ./esper-5.3.0/cpnm-agent/etc/
. ./setenv.sh

if [ ! -d "../target" ]
then
    mkdir ../target
fi
if [ ! -d "../target/classes" ]
then
    mkdir ../target/classes
fi

SOURCEPATH=../src/main/java

${JAVA_HOME}/bin/javac -cp ${CLASSPATH} -d ../target/classes -source 1.6 -sourcepath ${SOURCEPATH} ${SOURCEPATH}/com/espertech/esperio/socket/EsperSocket.java
