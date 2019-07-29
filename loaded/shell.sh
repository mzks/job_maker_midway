#!/bin/bash
#SBATCH --job-name=run.sh
#SBATCH --output=run.sh.o
#SBATCH --error=run.sh.e
#SBATCH --time=24:00:00
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=1
#SBATCH --account=pi-lgrandi
#SBATCH --mem-per-cpu=10000
#SBATCH --qos=dali
#SBATCH --partition=dali

# start time
SECONDS=0

# specify the project name

workdir=/dali/lgrandi/mzks/mc/mc1/workdir
job_dir=/dali/lgrandi/mzks/mc/job_maker

# load modules required by XENON G4
module load midway2
module load ROOT/6.06.08
module load clhep/2.3
module load geant4/10.03.p02

cd ${job_dir}
source ${job_dir}/loaded/geant4make.sh
source /software/geant4-10.03.p02-el7-x86_64/bin/geant4.sh

cd ${workdir}

# execute XENON G4
${workdir}/xenon1t_G4 \
    -d XENONnT \
    -p ${workdir}/macros/XENONnT/preinit_TPC_GdWater.mac \
    -b ${workdir}/macros/XENONnT/preinit_B_none.mac \
    -s ${workdir}/macros/XENONnT/setup_optical.mac \
    -f ${workdir}/macros/XENONnT/run_Cryostat_neutron_U238.mac \
    -n 1000 \
    -o ${workdir}/output.root

# execute nSort
# /project/lgrandi/ryuichi/xenonnt/mc/${version}/${name}/mc/nSort/nSort \
    # -d XENONnT \
    # -i /scratch/midway2/ryuichi/mc/${version}/${name}/${name}_${param}_0 \
    # -s 3

# cp output files to disk
# mv -f /scratch/midway2/ryuichi/mc/${version}/${name}/${name}_${param}_0.root      /project/lgrandi/ryuichi/xenonnt/mc/${version}/${name}/g4_out/${param}
# mv -f /scratch/midway2/ryuichi/mc/${version}/${name}/${name}_${param}_0_Sort.root /project/lgrandi/ryuichi/xenonnt/mc/${version}/${name}/nSort_out/${param}
# mv -f /scratch/midway2/ryuichi/mc/${version}/${name}/${name}_${param}_0_Time.dat  /project/lgrandi/ryuichi/xenonnt/mc/${version}/${name}/time_out/${param}

# print out the execution time
echo "The execution time is $SECONDS sec."
