#!/bin/bash
echo "===================== Stop ! ====================="

killProcess(){
    pid=$(ps x | grep $1 | grep -v grep | awk '{print $1}')
    kill -9 $pid
}

killProcess "restful-run.py"

echo "Stop Completed !"