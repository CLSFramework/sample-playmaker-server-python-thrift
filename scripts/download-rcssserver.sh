#!/bin/sh

# check rcssserver directory exists, if exists, remove it
if [ -d rcssserver ]; then
    echo "rcssserver directory exists, remove it"
    rm -rf rcssserver
fi

mkdir rcssserver

cd rcssserver

# download soccer simulation server App Image
wget $(curl -s https://api.github.com/repos/clsframework/rcssserver/releases/latest | grep -oP '"browser_download_url": "\K(.*rcssserver-x86_64-.*\.AppImage)' | head -n 1)

# check download is successful
if [ ! -f *.AppImage ]; then
    echo "Download failed"
    exit 1
fi

mv rcssserver-x86_64-*.AppImage rcssserver

chmod +x rcssserver