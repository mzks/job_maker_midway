#!/project/lgrandi/anaconda3/bin/python3
# -*- Coding: utf-8 -*-

import os
import time
import datetime
import subprocess

# global variables

mc_dir_name = 'mc44'
NevtEachBatch = 10000 # Number of Event in each batch
NBatch = 500 # total batch number
run_macro_name = 'run_Cryostat_neutron_U238' # run macro name of Geant4

workdir='/dali/lgrandi/mzks/mc/'+mc_dir_name+'/workdir' # Geant4 working directory witch has binary
job_maker_dir = '/dali/lgrandi/mzks/mc/job_maker' # ROOT of this script

job_assign_thre = 100
n_submit_job_once = 10
SeedStartNumber = 1
sleeping_second = 300


def make_macro(seed):

    loaded_macro_fname = workdir+'/macros/XENONnT/' + run_macro_name + '.mac'
    output_dirname = 'macro'
    fin = open(loaded_macro_fname, mode='r')
    os.makedirs('./product/'+run_macro_name+'/'+mc_dir_name+'/'+output_dirname, exist_ok=True)
    fout = open('./product/'+run_macro_name+'/'+mc_dir_name+'/'+output_dirname+'/s'+str(seed).zfill(4)+'.mac', mode='w')

    for line in fin:

        # If you want to add options, please add elif blocks here
        if 0 == line.find('/run/random/setRandomSeed') :
            fout.write('/run/random/setRandomSeed '+str(seed)+'\n')
        else:
            fout.write(line)
    fout.close()

def make_shell(seed):

    loaded_shell_fname = job_maker_dir+'/loaded/shell.sh'
    output_dirname = 'shell'
    fin = open(loaded_shell_fname, mode='r')
    os.makedirs('./product/'+run_macro_name+'/'+mc_dir_name+'/'+output_dirname, exist_ok=True)
    foutname = './product/'+run_macro_name+'/'+mc_dir_name+'/'+output_dirname+'/s'+str(seed).zfill(4)+'.sh'
    fout = open(foutname, mode='w')

    for line in fin:

        # If you want to add options, please add elif blocks here
        if 0 == line.find('    -n') :
            fout.write('    -n '+str(NevtEachBatch)+'\\\n')
        elif 0 == line.find('    -o') :
            fout.write('    -o ${workdir}/output'+str(seed).zfill(4)+'.root \n')
        elif 0 == line.find('    -f') :
            fout.write('    -f '+job_maker_dir+'/product/'+run_macro_name+'/'+mc_dir_name+'/macro/s'+str(seed).zfill(4)+'.mac \\\n')
        elif 0 == line.find('workdir=') :
            fout.write('workdir='+workdir+'\n')
        elif 0 == line.find('#SBATCH --job-name=') :
            fout.write('#SBATCH --job-name=s'+str(seed).zfill(4)+'.sh\n')
        elif 0 == line.find('#SBATCH --output=') :
            #fout.write('#SBATCH --output='+job_maker_dir+'/product/'+run_macro_name+'/'+mc_dir_name+'/log/s'+str(seed).zfill(4)+'.o \n')
            fout.write('#SBATCH --output='+workdir+'/s'+str(seed).zfill(4)+'.o \n')
        elif 0 == line.find('#SBATCH --error=') :
            #fout.write('#SBATCH --error='+job_maker_dir+'/product/'+run_macro_name+'/'+mc_dir_name+'/log/s'+str(seed).zfill(4)+'.e \n')
            fout.write('#SBATCH --error='+workdir+'/s'+str(seed).zfill(4)+'.e \n')
        elif 0 == line.find('   -i ${workdir}/output') :
            fout.write('    -i ${workdir}/output'+str(seed).zfill(4)+' \\\n')
        else:
            fout.write(line)

    fout.close()
    os.chmod(foutname, 0o755)
    #os.makedirs('./product/'+run_macro_name+'/'+mc_dir_name+'/'+'log', exist_ok=True)


def print_config():

    print('.........................................................')
    print('Target mc dir name:', mc_dir_name)
    print('Total', '{:.1E}'.format(NBatch*NevtEachBatch), 'evt. generated')
    print('Run macro: ', run_macro_name)
    print('Working dir:',workdir)
    print('Total Batch:', NBatch, '*', NevtEachBatch, 'evt. generated')
    print('Seeds start from ', SeedStartNumber, 'to', SeedStartNumber+NBatch-1)
    print('MaxSubmissionJobs:', job_assign_thre,'checked in each', sleeping_second, 'sec.')
    print('.........................................................')


def submit_jobs(iSeed):

        print('submit', iSeed)
        batchpath = 'sbatch '+job_maker_dir+'/product/'+run_macro_name+'/'+mc_dir_name+'/shell/s'+str(iSeed).zfill(4)+'.sh'
        print(batchpath)
        out = subprocess.check_output(batchpath, shell=True)
        print(out)

if __name__ == "__main__":

    print_config()
    # Prepare Scripts
    for i in range(SeedStartNumber, NBatch+SeedStartNumber):

        make_macro(i)
        make_shell(i)

    i_job_seed = SeedStartNumber

    while(True):
        print(datetime.datetime.now())
        num_stored_jobs = int(subprocess.check_output("squeue -u mzks | wc -l", shell=True)) - 1
        print('the current stored jobs', num_stored_jobs)

        if num_stored_jobs < job_assign_thre:
            for i in range(n_submit_job_once):
                submit_jobs(i_job_seed)
                i_job_seed += 1

        if i_job_seed >= SeedStartNumber + NBatch:
            break

        time.sleep(sleeping_second)

    print('Done!')

