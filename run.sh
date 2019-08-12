#! /bin/bash

#Job-manager of mc at midway2
#
#optional arguments:
#  -h, --help            show this help message and exit
#  -d DIRNAME, --dirname DIRNAME
#                        MC source root directory name
#  -e EACH, --each EACH  Number of events generated in each bunch
#  -n NBATCH, --nbatch NBATCH
#                        Number of bunches submitted
#  -m MACRO, --macro MACRO
#                        Run macro name
#  -l LIMIT, --limit LIMIT
#                        Limitation of job submission
#  -o ONCE, --once ONCE  Number of jobs submitted at one loop
#  -i INIT, --init INIT  Initial seed number
#  -s SLEEP, --sleep SLEEP
#                        sleeping second in each loop
#
nohup sh -c ' \
python3 -u job_manager.py -d mc41 < /dev/null > out.log 2>out.err; \
python3 -u job_manager.py -d mc45 < /dev/null > out.log 2>out.err; \
python3 -u job_manager.py -d mc46 < /dev/null > out.log 2>out.err; \
' &
