#!/bin/sh

# Script to run named window query example and benchmark
#

# A note to cygwin users: please replace "-cp ${CLASSPATH}" with "-cp `cygpath -wp $CLASSPATH`"
#

cd ./esper-5.3.0/cpnm-agent/etc/
. ./setenv.sh

MEMORY_OPTIONS="-Xms512m -Xmx512m -server -XX:+UseParNewGC"

$JAVA_HOME/bin/java $MEMORY_OPTIONS -Dlog4j.configuration=log4j.xml -cp ${CLASSPATH} com.espertech.esperio.socket.EsperSocket $1 $2 $3
