#!/bin/bash

# ###### Zona de Parámetros de solicitud de recursos a SLURM ############################
#
#SBATCH --job-name=NuclearReactostest		#Nombre del job
#SBATCH -p bigmem			#Cola a usar, Default=short (Ver colas y límites en /hpcfs/shared/README/partitions.txt)
#SBATCH -N 1				#Nodos requeridos, Default=1
#SBATCH -n 2				#Tasks paralelos, recomendado para MPI, Default=1
#SBATCH --cpus-per-task=2		#Cores requeridos por task, recomendado para multi-thread, Default=1
#SBATCH --mem=40G		#Memoria en Mb por CPU, Default=2048
#SBATCH --time=10-00:00:00			#Tiempo máximo de corrida, Default=2 horas
#SBATCH --mail-user=fw.garcia@uniandes.edu.co
#SBATCH --mail-type=ALL			
#SBATCH -o test_nr.o%j			#Nombre de archivo de salida
#SBATCH -e test_nr_error.e%j			#Nombre de archivo de salida
#
########################################################################################

# ################## Zona Carga de Módulos ############################################

module load openmc
export OPENMC_CROSS_SECTIONS="/hpcfs/home/fisica/fw.garcia/Data/endfb-viii.0-hdf5/cross_sections.xml"
#export OPENMC_CROSS_SECTIONS="/hpcfs/home/fisica/fw.garcia/Data/jeff33/jeff-3.3-hdf5/cross_sections.xml"
#export OPENMC_CROSS_SECTIONS="/hpcfs/home/fisica/fw.garcia/Data/cross_sections.xml"
########################################################################################


# ###### Zona de Ejecución de código y comandos a ejecutar secuencialmente #############
host=`/bin/hostname`
date=`/bin/date`

echo "Host: $(/bin/hostname)" # info
echo "Started at: $(/bin/date)" # info

# código a correr
#mpiexec python ../../Simulation/Simulator_test.py 
python ../../Simulation/run_reactor_multi_thread.py

echo "Finished at: $(/bin/date)" # info

########################################################################################

