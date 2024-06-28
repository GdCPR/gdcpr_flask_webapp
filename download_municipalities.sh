#!/bin/bash

# Variable for resources workspace and repo dir 
resources_dir=/workspaces/web-scrapper/resources
repo_dir=8560382

# If resources dir do not exist, create it
if [ ! -d $resources_dir ]; then
    mkdir $resources_dir
fi

# Change working dir
cd $resources_dir

# clone repo
git clone https://gist.github.com/8560382.git

# Change file name and format to txt
mv -f $resources/$repo_dir/flat_puerto_rico_municipalities $resources_dir/puerto_rico_municipalities.txt

# Delete copied repo
rm -rf $repo_dir