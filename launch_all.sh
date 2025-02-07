#!/bin/bash

# List of descriptors
descriptors=(
    'energy' 'energy_per_atom' 'volume'
    'formation_energy_per_atom' 'nsites' 'is_hubbard'
    'e_above_hull' 'spacegroup.crystal_system' 'spacegroup.number'
    'band_gap' 'density' 'total_magnetization' 'oxide_type'
)

# Root directory for data
root_dir="../cgcnn_data"

# Other fixed parameters
train_ratio=0.6
val_ratio=0.2
test_ratio=0.2
epochs=500
mask_other_property=0
exp_id=0

# Loop over all combinations of input and output descriptors
for input_descriptor in "${descriptors[@]}"; do
    for output_descriptor in "${descriptors[@]}"; do
        # Skip the case where input and output descriptors are the same
        #if [ "$input_descriptor" == "$output_descriptor" ]; then
        #    continue
        #fi
        
        # Create a filename for the SLURM script and output file
        slurm_file="slurm_job_${exp_id}-${input_descriptor}-${output_descriptor}.sh"
        output_file="${exp_id}-${input_descriptor}-${output_descriptor}-${mask_other_property}.txt"

        # Create the SLURM job submission script
        cat <<EOF > $slurm_file
#!/bin/bash
#SBATCH --mail-type=FAIL
#SBATCH --partition=sm3090el8
#SBATCH -N 1
#SBATCH -n 8
#SBATCH --gres=gpu:1
#SBATCH --time=2-00:00:00
#SBATCH --output=${output_file}.log
#SBATCH --error=${output_file}.err

# Load necessary modules
module purge
module load Python/3.8.6-GCCcore-10.2.0 || module swap Python/3.8.6-GCCcore-10.2.0

# Activate the virtual environment
source ~/python-envs/cgcnn/bin/activate

# Run the Python script with the appropriate parameters
python main.py \
    --train-ratio=$train_size \
    --val-ratio=$val_size \
    --test-ratio=$test_size \
    --mask_other_property=$mask_other_property \
    --root_dir=$root_dir \
    --input_descriptor=$input_descriptor \
    --output_descriptor=$output_descriptor \
    --exp_id=$exp_id \
    --epochs=$epochs \
    --random_seed=123 > ${output_file} 2>&1

EOF

        # Submit the SLURM job script
        sbatch $slurm_file
        
        # Increment the exp_id counter for the next combination
        ((exp_id++))
    done
done
