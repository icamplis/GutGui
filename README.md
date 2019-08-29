# GutGui

## Installation Instructions

### Package requirements and intructions
Download HyperGUI by 

To install Python, go to python.org/downloads/ and download version 3.7.4.

To install the required packages, navigate to terminal and type in `pip3 install --user -r /path/requirements.txt`, where 'path' refers to the path of directories required to reach the file `requirements.txt`. Alternatively, type the following into the terminal as separate commands:
- `pip3 install - -user certifi`
- `pip3 install - -user cycler`
- `pip3 install - -decorator`
- `pip3 install - -imageio`
- `pip3 install - -kiwisolver`
- `pip3 install - -matplotlib`
- `pip3 install - -networkx`
- `pip3 install - -numpy`
- `pip3 install - -Pillow`
- `pip3 install - -pyparsing`
- `pip3 install - -python-dateutil`
- `pip3 install - -PyWavelets`
- `pip3 install - -scikit-image`
- `pip3 install - -scipy`
- `pip3 install - -six`

Correct versions are: certifi==2019.6.16, cycler==0.10.0, decorator==4.4.0, imageio==2.5.0, kiwisolver==1.1.0, matplotlib==3.1.1, networkx==2.3, numpy==1.17.0, Pillow==6.1.0, pyparsing==2.4.2, python-dateutil==2.8.0, PyWavelets==1.0.3, scikit-image==0.15.0, scipy==1.3.0, six==1.12.0


## Development Notes
### Regarding Performance
For every folder uploaded, it's scanned for a data cube,
and that data cube is processed fully for all of the analysis patterns.
Similarly, for every change in mode (Normal vs Original, Masked vs. Whole, etc.),
every data cube will be updated accordingly.
Also, when switching between data cubes,
all the images will be re-rendered, which also takes time.

You can see the progress of the calculations in the logs.

**Currently, it's not advisable to run more than ~10 data cube directories at a time.**

If the program hangs or bugs out, press `Ctrl-C` in the console to shut it down.
