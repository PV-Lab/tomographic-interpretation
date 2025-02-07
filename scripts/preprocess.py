import pandas as pd
from tqdm import tqdm
import json

if __name__ == '__main__':


    infile = 'materials_project.csv'

    data = pd.read_csv(infile)
    print(data.columns.to_list())

    data = data.drop(columns=['icsd_id', 'elasticity']) # this columns contain almost always NaNs, drop them
    data = data.dropna() # drop materials with missing property values (removes 17 materials)
    data = data.drop_duplicates(subset='material_id') # just in case, but it doesnt remove any material.

    # remove other columns that are not descriptors
    data = data.drop(columns=['icsd_ids', 'created_at', 'created year', 'task_ids', 'tags', 'unit_cell_formula', 'spacegroup', 'is_compatible', 'hubbards', 'nelements', 'elements']) # this columns do not contain relevent info, drop them

    stats = {}
    for column in data.columns:
        if column not in ['material_id', 'cif', 'pretty_formula', 'is_hubbard', 'oxide_type', 'spacegroup.number', 'spacegroup.crystal_system']:
            stats[column] = {
                'mean': data[column].mean(),
                'std': data[column].std()
            }

    # Convert the dictionary to a JSON string and write it to a file
    with open('column_stats.json', 'w') as json_file:
        json.dump(stats, json_file, indent=4)

    # prepare inputs and outputs in the cgcnn format
    for descriptor in data.columns:
        if descriptor not in ['material_id', 'cif', 'pretty_formula']:
            print(descriptor)

            with open(f'id_{descriptor}.csv', 'w') as f:

                for index, row in tqdm(data.iterrows(), total=data.shape[0], desc=f'Creating {descriptor} file'):
                    print(row['material_id'], row[descriptor], sep=',', file=f)

