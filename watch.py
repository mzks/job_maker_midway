#!/project/lgrandi/anaconda3/bin/python3
# -*- Coding: utf-8 -*-

from warnings import filterwarnings
filterwarnings('ignore')
from datetime import datetime
from subprocess import check_output
import pandas as pd
import argparse

def run_command():
    out = check_output('squeue > output_squeue.txt', shell=True)

def rm_tmp():
    out = check_output('rm -rf output_squeue.txt', shell=True)

def read_csv():

    df = pd.read_csv('./output_squeue.txt', delim_whitespace=True, names=('jobid', 'partition', 'name','user','status','time','nodes','nodelist','others1','others2'))
    df = df.drop("others1", axis=1)
    df = df.drop("others2", axis=1)
    return df

def summary(df, me, part):

    df_part = df.query('partition==@part')
    df_me = df.query('user==@me')

    print('Current time', datetime.now())
    print('')

    print('Status of', part )
    print(df_part['user'].value_counts())

    print('')
    print('Status of my jobs', me)
    print(df_me['status'].value_counts())

    print('')
    print('My Latest and Earliest jobs')
    df_me['len']  = df_me.time.str.len()
    df_me = df_me.sort_values(by=['len','time'])
    df_me = df_me.drop("len", axis=1)

    print(df_me.head())
    print('. . . . . . . . . . . . . . . . . . . . . . . ')
    print(df_me.tail())


    print('')

if __name__ == "__main__":

    parser = argparse.ArgumentParser(description='Job-watcher')

    parser.add_argument('-u','--user', default = 'mzks', help='user name')
    parser.add_argument('-p','--partition', default = 'dali', help='partition name')

    args = parser.parse_args()

    run_command()
    df = read_csv()
    summary(df, args.user, args.partition)
    rm_tmp()

