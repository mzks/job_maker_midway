#!/project/lgrandi/anaconda3/bin/python3
# -*- Coding: utf-8 -*-

import os

#global variables
run_macro_name = 'run_Cryostat_neutron_U238'
workdir='/project/lgrandi/mzks/mc/mc3/workdir'
job_maker_dir = '/project/lgrandi/mzks/mc/job_maker'
NevtEachBatch = 10
NBatch = 10

def make_macro(seed):

	loaded_macro_fname = workdir+'/macros/XENONnT/' + run_macro_name + '.mac'
	output_dirname = 'macro'
	fin = open(loaded_macro_fname, mode='r')
	os.makedirs('./'+run_macro_name+'/'+output_dirname, exist_ok=True)
	fout = open('./'+run_macro_name+'/'+output_dirname+'/s'+str(seed).zfill(4)+'.mac', mode='w')

	for line in fin:
		
		if 0 == line.find('/run/random/setRandomSeed') :
			fout.write('/run/random/setRandomSeed '+str(seed)+'\n')
		else:
			fout.write(line)
	fout.close()

def make_shell(seed):

	loaded_shell_fname = job_maker_dir+'/shell.sh'
	output_dirname = 'shell'
	fin = open(loaded_shell_fname, mode='r')
	os.makedirs('./'+run_macro_name+'/'+output_dirname, exist_ok=True)
	foutname = './'+run_macro_name+'/'+output_dirname+'/s'+str(seed).zfill(4)+'.sh'
	fout = open(foutname, mode='w')

	for line in fin:
		
		if 0 == line.find('    -n') :
			fout.write('    -n '+str(NevtEachBatch)+'\\\n')
		elif 0 == line.find('    -o') :
			fout.write('    -o ${workdir}/output'+str(seed).zfill(4)+'.root \n')
		elif 0 == line.find('    -f') :
			fout.write('    -f '+job_maker_dir+'/'+run_macro_name+'/macro/s'+str(seed).zfill(4)+'.mac \\\n')
		elif 0 == line.find('workdir=') :
			fout.write('workdir='+workdir+'\n')
		elif 0 == line.find('#SBATCH --job-name=') :
			fout.write('#SBATCH --job-name=s'+str(seed).zfill(4)+'.sh\n')
		elif 0 == line.find('#SBATCH --output=') :
			fout.write('#SBATCH --output='+job_maker_dir+'/'+run_macro_name+'/log/s'+str(seed).zfill(4)+'.o \n')
		elif 0 == line.find('#SBATCH --error=') :
			fout.write('#SBATCH --error='+job_maker_dir+'/'+run_macro_name+'/log/s'+str(seed).zfill(4)+'.e \n')
		else:
			fout.write(line)
	fout.close()
	os.chmod(foutname, 0o755)
	os.makedirs('./'+run_macro_name+'/'+'log', exist_ok=True)

def make_batch(seed):

	loaded_batch_fname = job_maker_dir+'/batch.sh'
	output_dirname = 'batch'
	fin = open(loaded_batch_fname, mode='r')
	os.makedirs('./'+run_macro_name+'/'+output_dirname, exist_ok=True)
	os.makedirs('./'+run_macro_name+'/'+'log', exist_ok=True)
	foutname = './'+run_macro_name+'/'+output_dirname+'/s'+str(seed).zfill(4)+'.sh'
	fout = open(foutname, mode='w')

	for line in fin:
		
		if 0 == line.find('#SBATCH --job-name=') :
			fout.write('#SBATCH --job-name=s'+str(seed).zfill(4)+'.sh\n')
		elif 0 == line.find('#SBATCH --output=') :
			fout.write('#SBATCH --output='+job_maker_dir+'/'+run_macro_name+'/log/s'+str(seed).zfill(4)+'.o \n')
		elif 0 == line.find('#SBATCH --error=') :
			fout.write('#SBATCH --error='+job_maker_dir+'/'+run_macro_name+'/log/s'+str(seed).zfill(4)+'.e \n')
		elif 0 == line.find('srun /bin/sh') :
			fout.write('srun /bin/sh '+job_maker_dir+'/'+run_macro_name+'/'+output_dirname+'/s'+str(seed).zfill(4)+'.sh \n')
		else:
			fout.write(line)
	fout.close()
	os.chmod(foutname, 0o755)

def make_throw(NofBatchs):

	foutname = './'+run_macro_name+'/throw.sh'
	fout = open(foutname, mode='w')

	fout.write('#! /bin/bash \n')
	for i in range(1,NofBatchs+1):
		batchpath = job_maker_dir+'/'+run_macro_name+'/shell/s'+str(i).zfill(4)+'.sh'
		fout.write('sbatch '+batchpath+'\n')

	fout.close()
	os.chmod(foutname, 0o755)

if __name__ == "__main__":

	
	for i in range(1, NBatch+1):
	
		make_macro(i)
		make_shell(i)
		#make_batch(i)

	make_throw(NBatch)
