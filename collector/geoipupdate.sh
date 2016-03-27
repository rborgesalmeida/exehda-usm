#!/bin/bash

for i in curl wget ftp; do
	if which $i &>/dev/null; then 
		prg=$i
		break
	fi
done

if [ -z "$prg" ]; then
	echo Não foi possível encontrar uma ferramenta para download. Verifique a possibilidade de instalação de uma destas ferramentas: curl ou wget >&2
	exit 1
fi

case $prg in 
curl)
	prg="curl -s -O"
	;;
wget)
	prg="wget --quiet"
	;;
esac

set -e

if [ -d /usr/share/GeoIP/ ]; then
	cd /usr/share/GeoIP/ 2>/dev/null
elif [ -d /var/lib/GeoIP/ ]; then
	cd /var/lib/GeoIP 2>/dev/null
else
	mkdir -p /usr/share/GeoIP 2>/dev/null
	cd /usr/share/GeoIP/ 2>/dev/null
fi

$prg http://geolite.maxmind.com/download/geoip/database/GeoLiteCountry/GeoIP.dat.gz
gunzip -c GeoIP.dat.gz > GeoIP.dat.updated
mv GeoIP.dat.updated GeoIP.dat
rm -f GeoIP.dat.gz

$prg http://geolite.maxmind.com/download/geoip/database/GeoLiteCity.dat.gz
gunzip -c GeoLiteCity.dat.gz > GeoLiteCity.dat.updated
mv GeoLiteCity.dat.updated GeoLiteCity.dat
rm -f GeoLiteCity.dat.gz

$prg http://geolite.maxmind.com/download/geoip/database/GeoIPv6.dat.gz
gunzip -c GeoIPv6.dat.gz > GeoIPv6.dat.updated.new
mv GeoIPv6.dat.updated.new GeoIPv6.dat
rm -f GeoIPv6.dat.gz

