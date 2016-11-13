#!/bin/bash
#author:joker
#created at 2016-11-12 16:38:14
#desc:build & start  docker container, save img to $SPATH 

SPATH="userdata"

docker build -t dbcraw .

if [ "$?" -eq "0" ]
then
    if [ ! -d $SPATH ] 
    then 
        mkdir $SPATH
    fi 
    docker run -itd --name db0  -v $(pwd)/userdata:/userImgs dbcraw
else
    echo "There is somthing wrong, maybe run this script aragin"
fi
