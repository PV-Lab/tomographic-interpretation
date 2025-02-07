import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from pathlib import Path
from collections import defaultdict

def load_matrix_from_file(filename):
    """Load a matrix from a CSV file."""

    df = pd.read_csv(filename, index_col=0)

    # Specify the columns to move to the end
    columns_to_move = ['is_hubbard', 'oxide_type', 'spacegroup.crystal_system', 'spacegroup.number']
    remaining_columns = [col for col in df.columns if col not in columns_to_move]
    new_column_order = remaining_columns + columns_to_move
    df = df[new_column_order]
    df = df.loc[new_column_order]

    df = df.drop(columns=columns_to_move)

    return df



if __name__ == "__main__":

    experiment = 'masked_composition_vs_unmasked_composition'
    title = None

    # Options:
    # masked_composition_vs_unmasked_composition
    # masked_geometry_vs_unmasked_geometry

    if experiment == 'masked_composition_vs_unmasked_composition':

        ''''
        Reference: composition-restricted CGCNN (without extra descriptors)
        Comparison: composition-restricted CGCNN augmented with extra descriptors 
        Result: Influence of every 'extra' descriptor within composition-restriced CGCNN
        '''
        # load all the already parsed results, matrices where on each entry we have MAE
        # on the test set
        ### these matrices are used as the reference
        matrix_reference_1 = load_matrix_from_file('result_masked_123_exp3_comp.csv')
        matrix_reference_2 = load_matrix_from_file('result_masked_456_exp3_comp.csv')
        matrix_reference_3 = load_matrix_from_file('result_masked_789_exp3_comp.csv')
        matrix_reference_4 = load_matrix_from_file('result_masked_321_exp3_comp.csv')
        matrix_reference_5 = load_matrix_from_file('result_masked_654_exp3_comp.csv')

        ### these matrices are used as comparison
        matrix_comparison_1 = load_matrix_from_file('result_123_exp3_comp.csv')
        matrix_comparison_2 = load_matrix_from_file('result_456_exp3_comp.csv')
        matrix_comparison_3 = load_matrix_from_file('result_789_exp3_comp.csv')
        matrix_comparison_4 = load_matrix_from_file('result_321_exp3_comp.csv')
        matrix_comparison_5 = load_matrix_from_file('result_654_exp3_comp.csv')

        ylabel = 'Extra feature'
        title = 'Composition-restricted baseline'

    elif experiment == 'masked_geometry_vs_unmasked_geometry':

        ''''
        Reference: CGCNN (without extra descriptors)
        Comparison: CGCNN augmented with extra descriptors 
        Result: Influence of every 'extra' descriptor within (geometry-aware) CGCNN
        '''
        # load all the already parsed results, matrices where on each entry we have MAE
        # on the test set
        ### these matrices are used as the reference
        matrix_reference_1 = load_matrix_from_file('mae_matrix_masked_1.csv')
        matrix_reference_2 = load_matrix_from_file('mae_matrix_masked_2.csv')
        matrix_reference_3 = load_matrix_from_file('mae_matrix_masked_3.csv')
        matrix_reference_4 = load_matrix_from_file('mae_matrix_masked_4.csv')
        matrix_reference_5 = load_matrix_from_file('mae_matrix_masked_5.csv')

        ### these matrices are used as comparison
        matrix_comparison_1 = load_matrix_from_file('mae_matrix_unmasked_1.csv')
        matrix_comparison_2 = load_matrix_from_file('mae_matrix_unmasked_2.csv')
        matrix_comparison_3 = load_matrix_from_file('mae_matrix_unmasked_3.csv')
        matrix_comparison_4 = load_matrix_from_file('mae_matrix_unmasked_4.csv')
        matrix_comparison_5 = load_matrix_from_file('mae_matrix_unmasked_5.csv')

        ylabel = 'Extra feature'
        title = 'Composition-Structure baseline'

    dfs = [matrix_reference_1, matrix_reference_2, matrix_reference_3, matrix_reference_4, matrix_reference_5]
    matrix_reference = pd.concat(dfs).groupby(level=0).mean()  # Mean across the list of DataFrames
    max_matrix_reference = pd.concat(dfs).groupby(level=0).max()    # Max across the list of DataFrames
    min_matrix_reference = pd.concat(dfs).groupby(level=0).min()    # Min across the list of DataFrames

    dfs = [matrix_comparison_1, matrix_comparison_2, matrix_comparison_3, matrix_comparison_4, matrix_comparison_5]
    matrix_comparison = pd.concat(dfs).groupby(level=0).mean()  # Mean across the list of DataFrames
    max_matrix_comparison = pd.concat(dfs).groupby(level=0).max()    # Max across the list of DataFrames
    min_matrix_comparison = pd.concat(dfs).groupby(level=0).min()    # Min across the list of DataFrames

    # Step 1: Calculate the relative change (delta)
    delta = 100 * (matrix_comparison - matrix_reference) / matrix_reference

    # Step 2: Calculate the upper and lower bounds for delta
    delta_upper = 100 * (max_matrix_comparison - min_matrix_reference) / (min_matrix_reference)
    delta_lower = 100 * (min_matrix_comparison - max_matrix_reference) / (max_matrix_reference)

    # Step 3: Calculate the error bars (upper and lower errors)
    upper_error = delta_upper - delta
    lower_error = delta - delta_lower

    # Specify the columns to move to the end
    columns_to_move = ['is_hubbard', 'oxide_type', 'spacegroup.crystal_system', 'spacegroup.number']
    remaining_columns = [col for col in delta.columns if col not in columns_to_move]
    new_column_order = remaining_columns + columns_to_move

    delta = delta.loc[new_column_order]
    upper_error = upper_error.loc[new_column_order]
    lower_error = lower_error.loc[new_column_order]

    # make the heatmap visualization
    annotations = delta.copy()
    annotations = annotations.astype(str) # cast to str to avoid warning, it will be overwritten
    for i in range(delta.shape[0]):
        for j in range(delta.shape[1]):
            a = str(round(delta.iloc[i, j],1))
            b = str(round(upper_error.iloc[i, j], 1))
            c = str(round(lower_error.iloc[i, j], 1))
            # format as a^{+b}_{-c}
            annotations.iloc[i, j] = f"${a}^{{+{b}}}_{{-{c}}}$"

    plt.figure(figsize=(10, 6))

    sns.heatmap(delta, annot=annotations, fmt="", cmap='coolwarm', center=0, 
                annot_kws={'size': 10}, cbar=True, linewidths=0.0, vmin=-10, vmax=+10)

    # adjust x-tick labels to split long labels into two lines
    new_labels = []
    for label in delta.columns:
        # split the label if it exceeds a certain length 10 characters
        if len(label) > 10:
            label_split = label[:len(label)//2] + '\n' + label[len(label)//2:]
            new_labels.append(label_split)
        else:
            new_labels.append(label)

    # set the new x-tick labels with line breaks
    plt.xticks(ticks=plt.gca().get_xticks(), labels=new_labels, rotation=0)

    # adjust y-tick labels to split long row index labels into two lines
    new_y_labels = []
    for label in delta.index:
        if len(label) > 10:
            label_split = label[:len(label)//2] + '\n' + label[len(label)//2:]
            new_y_labels.append(label_split)
        else:
            new_y_labels.append(label)

    # Set the new y-tick labels with line breaks
    plt.yticks(ticks=plt.gca().get_yticks(), labels=new_y_labels, rotation=0)

    plt.xlabel('Target', fontsize=10)
    plt.ylabel(ylabel, fontsize=10)
    plt.xticks(rotation=75, fontsize=10)
    plt.yticks(rotation=0, fontsize=10)
    if title:
        plt.title(title, fontsize=14)

    # save figure
    plt.savefig(f'figures/{experiment}/{experiment}.png', dpi=800, bbox_inches='tight')

