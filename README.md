# About
This repository is aimed to document the small modifications I made on CGCNN for a set of experiments. For the original implementation I redirect to his own repository: https://github.com/txie-93/cgcnn

# Changes
* Changed the property scalers so they take the global mean and variance instead of dynamically scaling based on batch-statistics
* Added option to concatente a property in the representation after the readout function of the graph model.
* Added option for 'fooling' the bond-perception algorithm to remove structure in the way the graph is constructed.

# Requirements

This code was tested on Python 3.7.17 and Python 3.8.6. To set up the environment use the requirements in `requirements.txt`
```
python -m venv ~/python-envs/cgcnn
source ~/python-envs/cgcnn/bin/activate
python -m pip install -r requirements.txt
```
