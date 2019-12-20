#!/bin/bash
echo "===================== Start ! ====================="

killProcess(){
    pid=$(ps x | grep $1 | grep -v grep | awk '{print $1}')
    kill -9 $pid
}


nohup python -u restful-run.py > ./log/restfulAPI.log 2>&1 &
if [ $? -eq 0 ]; then
    echo "restfulAPI has been started !"
else
    echo "Failed !"
    killProcess "restful-run.py"
    exit
fi