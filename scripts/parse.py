import os
import re
import pandas as pd
import numpy as np

def extract_mae_from_file(filename):
    """Extract the MAE value from the last line of a file."""
    with open(filename, 'r') as file:
        lines = file.readlines()
        last_line = lines[-1].strip()
    
    # Regular expression to match " ** MAE xxxx" pattern
    match = re.search(r'\*\* MAE (-?\d+\.\d+)', last_line)
    if match:
        return float(match.group(1))
    else:
        return 0.0

def build_mae_matrix(directory):
    """Build a matrix of MAE values from all .txt files in the given directory."""
    data = []
    input_strings = set()
    output_strings = set()

    # Process each .txt file in the directory
    for filename in os.listdir(directory):
        if filename.endswith('.txt'):
            parts = filename.replace('.txt', '').split('-')
            if len(parts) == 4:
                input_str = parts[1]
                output_str = parts[2]

                # Extract the MAE value from the last line of the file
                mae_value = extract_mae_from_file(os.path.join(directory, filename))
                
                data.append((input_str, output_str, mae_value))
                input_strings.add(input_str)
                output_strings.add(output_str)

    # Convert input_strings and output_strings to sorted lists for consistent indexing
    input_strings = sorted(input_strings)
    output_strings = sorted(output_strings)

    # Create a DataFrame to hold the matrix
    mae_matrix = pd.DataFrame(0, index=input_strings, columns=output_strings, dtype=float)

    # Populate the matrix with the extracted MAE values
    for input_str, output_str, mae_value in data:
        mae_matrix.loc[input_str, output_str] = mae_value

    return mae_matrix

def save_matrix_to_file(mae_matrix, filename):
    """Save the MAE matrix to a file."""
    mae_matrix.to_csv(filename)

if __name__ == '__main__':

    for seed in [123,456,789,321,654]:
        print(seed)
        for exp_type in ['', '_masked']:
            filepath = f'/...'
            savepath = f'.....'
            matrix = build_mae_matrix(filepath)
            save_matrix_to_file(matrix, savepath)