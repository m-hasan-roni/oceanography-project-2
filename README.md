# Project Code Repository

This repository contains two iterations of the computational model used in this academic project 2: 

1. professor_original_code_Primary Productivity.py - The baseline framework provided by my course teacher Dr.Subrata Sarker, Associate Professor, Department of Oceanography, Shahajalal University of Science and Technology, Sylhet-3314
2. my_improved_code_Primary Productivity.py - My modified, optimized version.

### My Improvements & Contributions:
* Added structured file-path management and explicit NetCDF4 engine selection for more reliable and reproducible data loading.
* Added safety checks and value constraints to prevent invalid chlorophyll values from causing mathematical errors during euphotic-depth and VGPM calculations.
* Enhanced the output workflow by creating a customized Bay of Bengal map with geographic labels and automatically exporting     both a high-resolution PNG and CSV dataset.
