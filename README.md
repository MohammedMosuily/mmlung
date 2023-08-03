# MMLung: Moving Closer to Practical Lung Health Estimation using Smartphones

Welcome to the MMLung project, which is aimed at leveraging the power of smartphones for lung health estimation. Our primary script, encapsulated in the `mmlung.ipynb` Jupyter notebook, employs data from various sources to extract features and analyze different breathing tasks.

## Getting Started

### Prerequisites

To successfully run the script, you'll need:

- Python 3.x
- pandas
- numpy
- glob
- ipywidgets
- IPython.display
- tqdm

Additionally, you'll need the `pipe_scripts` module in your Python path, which contains several functions used in our script.

### Usage

Our `mmlung.ipynb` script is built to run in a Jupyter notebook environment and requires access to various data files. These include ground truth files and task files, which can be specified by setting the `ground_truth_folder` and `tasks_folder` variables respectively.

We also utilize a dictionary, `cell_locations`, to map the locations of various target variables within the data files. You may need to customize this dictionary to match the structure of your own data files.

## Data Collection

The dataset for this project will be released in the future. In the meantime, you can record your own .wav files using any smartphone. Here are a couple of examples:

- Record a cough.
- Recite the Rainbow Passage: "When the sunlight strikes raindrops in the air, they act like a prism and form a rainbow. The rainbow is a division of white light into many beautiful colors..."

Ground truth data can be collected using the Easy on-PC PC spirometer. Find more information [here](https://nddmed.com/products/spirometers/easy-on-pc).

## About the Project

![Pipline](https://github.com/MohammedMosuily/mmlung/assets/72745657/ea3e5b62-94fe-4c5b-aded-41d61a4918a4)
MMLUNG System Pipeline 

For a comprehensive understanding of our project, please refer to the `mmlung.ipynb` Jupyter notebook which contains detailed code and annotations.

Thank you for your interest in MMLung! 

## License

This project is licensed under the terms of the Educational Use License. See the [LICENSE](LICENSE) file for details.
