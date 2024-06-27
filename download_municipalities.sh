#!/bin/bash

# Clone repo to temporary folder
if [ ! -d /path/to/directory ]; then
    mkdir resources
fi


cd resources/
git clone https://gist.github.com/8560382.git


mv -f /workspaces/web-scrapper/resources/8560382/flat_puerto_rico_municipalities /workspaces/web-scrapper/resources/puerto_rico_municipalities.txt

rm -r -f /workspaces/web-scrapper/resources/8560382/