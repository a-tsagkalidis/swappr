#!/bin/bash
# System file backup script - back ups application database and logs

DATE=$(date +"%Y%m%d")
TIME=$(date +"%H%M")

if [ -f app.log ]; then
    if [ ! -d "bak.logs/$DATE/$TIME" ]; then
        echo "bak.logs/$DATE/$TIME backup logs directory created"
        mkdir -p "bak.logs/$DATE/$TIME"
    else
        echo "backup logs directory exists for today"
    fi

    echo "INFO:bash:internal.swappr.com - - [$(date +'%d/%b/%Y %H:%M:%S')]: Swappr server rebooted. app.log log file has been successfully moved to backup drive." >> "app.log"
    mv "app.log" "bak.logs/$DATE/$TIME"
fi

if [ -f swappr.db ]; then
    if [ ! -d "bak.db/$DATE/$TIME" ]; then
        echo "bak.db/$DATE/$TIME backup databases directory created"
        mkdir -p "bak.db/$DATE/$TIME"
    else
        echo "backup databases directory exists for today"
    fi

    cp "swappr.db" "bak.db/$DATE/$TIME"
    cp "locations.json" "bak.db/$DATE/$TIME"

    if [ -f "bak.logs/$DATE/$TIME/app.log" ]; then
        echo "INFO:bash:internal.swappr.com - - [$(date +'%d/%b/%Y %H:%M:%S')]: Swappr server rebooted. swappr.db database file has been successfully copied to backup drive." >> "bak.logs/$DATE/$TIME/app.log"
    else
        echo "INFO:bash:internal.swappr.com - - [$(date +'%d/%b/%Y %H:%M:%S')]: Swappr server initial boot. Initial app.log file created. swappr.db database file has been successfully copied to backup drive." > "app.log"
    fi
fi
