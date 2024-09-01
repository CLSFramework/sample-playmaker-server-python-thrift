#!/bin/sh

# check proxy directory exists, if exists, remove it
if [ -d proxy ]; then
    echo "proxy directory exists, remove it"
    rm -rf proxy
fi

mkdir proxy

cd proxy

# download soccer simulation proxy
wget $(curl -s "https://api.github.com/repos/clsframework/soccer-simulation-proxy/releases/latest" | grep -oP '"browser_download_url": "\K[^"]*' | grep "soccer-simulation-proxy.tar.gz")

tar -xvf soccer-simulation-proxy.tar.gz

mv soccer-simulation-proxy/* .

rm -rf soccer-simulation-proxy

rm soccer-simulation-proxy.tar.gz
