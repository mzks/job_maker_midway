#!/project/lgrandi/anaconda3/bin/python3
# -*- Coding: utf-8 -*-

import os

def make_macro():

	seed = 11
	NofGen = 10
	run_macro_name = 'run_Cryostat_neutron_U238'

	oofGen = 10
	loaded_macro_fname = '/project/lgrandi/mzks/mc/mc/workdir/macros/XENONnT/' + run_macro_name + '.mac'
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

def make_shell():

	seed = 11
	NofGen = 10
	run_macro_name = 'run_Cryostat_neutron_U238'
	workdir='/project/lgrandi/mzks/mc/mc1/workdir'

	NofEvt = 1000
	NofGen = 10
	loaded_shell_fname = '/project/lgrandi/mzks/mc/job_maker/run.sh'
	output_dirname = 'shell'
	fin = open(loaded_shell_fname, mode='r')
	os.makedirs('./'+run_macro_name+'/'+output_dirname, exist_ok=True)
	foutname = './'+run_macro_name+'/'+output_dirname+'/s'+str(seed).zfill(4)+'.sh'
	fout = open(foutname, mode='w')

	for line in fin:
		
		if 0 == line.find('    -n') :
			fout.write('    -n '+str(NofEvt)+'\n')
		elif 0 == line.find('    -o') :
			fout.write('    -o ${workdir}/output'+str(seed).zfill(4)+'.root \n')
		elif 0 == line.find('workdir=') :
			fout.write('workdir='+workdir+'\n')
		else:
			fout.write(line)
	fout.close()
	os.chmod(foutname, 0o755)

def make_batch():

	seed = 11
	NofGen = 10
	run_macro_name = 'run_Cryostat_neutron_U238'
	workdir='/project/lgrandi/mzks/mc/mc1/workdir'

	NofEvt = 1000
	NofGen = 10
	job_maker_dir = '/project/lgrandi/mzks/mc/job_maker'
	loaded_batch_fname = '/project/lgrandi/mzks/mc/job_maker/batch.sh'
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
			fout.write('#SBATCH --output='+job_maker_dir+'/'+run_macro_name+'/log/'+str(seed).zfill(4)+'.o \n')
		elif 0 == line.find('#SBATCH --error=') :
			fout.write('#SBATCH --error='+job_maker_dir+'/'+run_macro_name+'/log/'+str(seed).zfill(4)+'.e \n')
		elif 0 == line.find('srun /bin/sh') :
			fout.write('srun /bin/sh '+job_maker_dir+'/'+run_macro_name+'/'+output_dirname+'/s'+str(seed).zfill(4)+'.sh \n')
		else:
			fout.write(line)
	fout.close()
	os.chmod(foutname, 0o755)

def make_throw():
	NofBatchs = 1000

	seed = 11
	NofGen = 10
	run_macro_name = 'run_Cryostat_neutron_U238'
	workdir='/project/lgrandi/mzks/mc/mc1/workdir'

	NofEvt = 1000
	NofGen = 10
	job_maker_dir = '/project/lgrandi/mzks/mc/job_maker'

	foutname = './'+run_macro_name+'/throw.sh'
	fout = open(foutname, mode='w')

	fout.write('#! /bin/bash \n')
	for i in range(1,NofBatchs+1):
		batchpath = job_maker_dir+'/'+run_macro_name+'/batch/s'+str(i).zfill(4)+'.sh'
		fout.write('sbatch '+batchpath+'\n')

	fout.close()
	os.chmod(foutname, 0o755)

if __name__ == "__main__":
	make_macro()
	make_shell()
	make_batch()
	make_throw()
