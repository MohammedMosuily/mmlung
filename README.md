# MMLung: Moving Closer to Practical Lung Health Estimation using Smartphones​

# Breath Analysis Project
This repository contains scripts for processing and analyzing breathing patterns. The primary script is contained in the **mmlung.ipynb** Jupyter notebook. This script uses data from various sources to conduct feature extraction and analysis on different breathing tasks.

Requirements
-Python 3.x
-pandas
-numpy
-glob
-ipywidgets
-IPython.display
-tqdm

You will also need to have the pipe_scripts module available in your Python path, as the script imports several functions from this module.

# Usage
The **mmlung.ipynb** script is designed to be run in a Jupyter notebook environment. It requires access to various data files, including ground truth files and files for individual tasks.

You will need to specify the locations of your ground truth files and task files by setting the ground_truth_folder and tasks_folder variables respectively.

The script also uses a dictionary, cell_locations, to specify the locations of various target variables within the data files. You may need to adjust this dictionary according to the layout of your own data.

# Dataset
The data set used in this project consists of different breathing tasks. Each task has a corresponding folder and file suffix, as specified in the tasks_dict dictionary.

# Functionality
The main functionality of the script includes:

-Reading data from specified locations
-Conducting feature extraction on the data
-Analyzing the extracted features

Please refer to the ** mmlung.ipynb** Jupyter notebook for detailed code and explanations.
