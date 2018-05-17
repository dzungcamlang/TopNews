#!/bin/bash

# start DB service
service redis_6379 start
service mongod start
# need to fix a conf bug to bypass this line
redis-server &

pip3 install --user -r requirements.txt

cd news_pipeline
python3 news_monitor.py &
python3 news_fetcher.py &
python3 news_deduper.py &


echo '================================='
read -p $'PRESS [ENTER] TO TERMINATE PROCESSES\n' PRESSKEY

# kill all background jobs
kill $(jobs -p)
