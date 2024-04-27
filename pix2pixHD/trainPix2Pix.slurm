#!/bin/bash

# This is a sample script to run a PyTorch program on Notchpeak
# The areas that need to be changed are marked with CHANGE_ME
# This script is for a GPU job, if you need a CPU job, you will need to change the options
# Everything that comes after #SBATCH is an option to the SLURM scheduler
# The options are explained in the comments
# Place this file on the chpc cluster and run it with the command `sbatch <filename>`

# Use a GPU node:
#SBATCH --account=notchpeak-gpu
#SBATCH --partition=notchpeak-gpu

# Define the number of GPU nodes (you only need one unless you know what you are doing):
#SBATCH --nodes=1

# Define the number of tasks to run (you only need one unless you know what you are doing):
#SBATCH --ntasks-per-node=1

# Define the number of CPU cores per task: 
#SBATCH --cpus-per-task=4

# Allocate the amount of memory needed for the job:
#SBATCH --mem=64G

# Define the type of GPU you need (Use 2080ti for ML tasks, unless you know what you are doing):
#SBATCH --gres=gpu:2080ti:1

# Define the maximum time for the job to run, format: hours:minutes:seconds
#SBATCH --time=5:00:00              # walltime, abbreviated by -t

# Excluded because it has some issues:
#SBATCH --exclude=notch086

# Define the naming convention for the job, this will 2 files
# One for stdout and one for stderr, using the job number (%j) and the first node (%N)
# ex: slurm-1234.out-1, slurm-1234.err-1
#SBATCH -o /uufs/chpc.utah.edu/common/home/u1140015/pix2pixHD/log/slurm-%j.out-%N # name of the stdout, using the job number (%j) and the first node (%N)
#SBATCH -e /uufs/chpc.utah.edu/common/home/u1140015/pix2pixHD/log/slurm-%j.err-%N # name of the stderr, using job and first node values

# CHANGE_ME: Set the working directory of this script
# This must be changed to the directory where the script is located
#SBATCH --chdir=/uufs/chpc.utah.edu/common/home/u1140015/pix2pixHD/

# load appropriate modules (conda environments, ...)
# assumes micromamba is installed in $HOME/micromamba 
# see https://mamba.readthedocs.io/en/latest/installation/micromamba-installation.html

# Load the python intepreter
eval "$(conda shell.bash hook)"
module use $HOME/MyModules
module load miniconda3/latest
conda activate pix2pix_env

# Custom commands to run the program
echo "Running..."
python train.py --label_nc 0 --no_instance --name environment_pix2pix --dataroot './datasets/environment/' --niter 500 --use_dropout > training_output.out
echo "Done!"
