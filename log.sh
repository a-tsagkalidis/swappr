#!/bin/bash
DATE=$(date +"%Y%m%d")
TIME=$(date +"%H%M")

if [ -f app.log ]; then
    if [ ! -d "baklogs/$DATE/$TIME" ]; then
        echo "baklogs/$DATE/$TIME backup logs directory created"
        mkdir -p "baklogs/$DATE/$TIME"
    else
        echo "backup logs directory exists for today"
    fi
    echo "INFO:bash:internal.swappr.com - - [$(date +'%d/%b/%Y %H:%M:%S')]: Swappr server rebooted. app.log log file has been successfully moved to backup drive." >> "app.log"
    mv "app.log" "baklogs/$DATE/$TIME"
fi

if [ -f swappr.db ]; then
    if [ ! -d "bakdb/$DATE/$TIME" ]; then
        echo "bakdb/$DATE/$TIME backup databases directory created"
        mkdir -p "bakdb/$DATE/$TIME"
    else
        echo "backup databases directory exists for today"
    fi
    cp "swappr.db" "bakdb/$DATE/$TIME"
    echo "INFO:bash:internal.swappr.com - - [$(date +'%d/%b/%Y %H:%M:%S')]: Swappr server rebooted. swappr.db database file has been successfully copied to backup drive." >> "baklogs/$DATE/$TIME/app.log"
fi