#! /bin/bash

nohup python3 -u job_manager.py < /dev/null > out.log 2>out.err &
sleep 10s
head out.log
