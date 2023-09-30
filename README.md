# Robust frame-to-frame camera rotation estimation in crowded scenes


This is the code repository for the paper "Robust frame-to-frame camera rotation estimation in crowded scenes". The code estimates the camera rotation given an optical flow field.

[Project page](https://fabiendelattre.com/robust-rotation-estimation) | [PDF](https://fabiendelattre.com/robust-rotation-estimation/pdf/robust-rotation-estimation.pdf) | [ArXiv](https://arxiv.org/abs/2309.08588) | [Dataset](https://drive.google.com/file/d/17bLA5g7O5ruPpV8YgaAfgyyxgL6aV2jS/view?usp=sharing)


## Requirements

The code has been tested using python 3.11.

Create a new conda environment by running


    conda env create -n rotation_estimation --file environment.yml

and activate it using 

    conda activate rotation_estimation

## Demo


Run the demo on ``flow.npy`` using:

    python demo.py --flow=flow.npy


## Evaluate

To evaluate the code on BUSS, run


    python evaluate.py --buss_path=/path/to/buss



