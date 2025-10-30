#!/bin/bash
# Usage: sbatch --array=1-1001%100 job_array.slurm <start_line>
# <start_line> = 0 for the first batch, 1001 for the second, etc.

#SBATCH --job-name=dfasat_array
#SBATCH --output=logs/task_%A_%a.out
#SBATCH --error=logs/task_%A_%a.err
#SBATCH --time=20:00:00
#SBATCH --ntasks=1
#SBATCH --mem=32G
#SBATCH --array=1-1000%100   # max 1001 per array due to cluster limit

module load Python/3.11.3-GCCcore-12.3.0
source ~/myenvs/pydot_env/bin/activate

# Add minisat to PATH
export PATH=$PATH:/users/acq23aaa/.local/bin

cd $SLURM_SUBMIT_DIR
mkdir -p logs

# Default start_line to 0 if not provided
START_LINE=${1:-0}

# Compute the actual line in commands.txt
LINE=$((SLURM_ARRAY_TASK_ID + START_LINE))

# Check if line exists
TOTAL_LINES=$(wc -l < commands.txt)
if [ $LINE -gt $TOTAL_LINES ]; then
    echo "Task ${SLURM_ARRAY_TASK_ID} with line ${LINE} exceeds total commands (${TOTAL_LINES}), exiting."
    exit 0
fi

# Get command from commands.txt
cmd=$(sed -n "${LINE}p" commands.txt)

echo "Task ${SLURM_ARRAY_TASK_ID} (line ${LINE}): $cmd"
echo "----------------------------------------"

# Run the command
eval $cmd


