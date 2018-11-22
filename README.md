# sas_tools
Simple SAXS/SANS utilities for data processing and visualisation 
with minimum maintanace effort.
Scripts will be mantained as requsted. 

## Instalation
For the basic functionality requires python and numpy package only

## Scripts
The code for scripts is hosted on github. 
They can be downloaded directly from there or can be cloned to your computer
```
git clone https://github.com/Andre-lab/sas_tools.git
```
-----------------------------------------------------------------------
### Average and substract
Averaging frames from the given range and substracts buffer. 
It may also remove frames with bubbles and plot final intensity
Skipping bubbles is based on the sum of the first 10 points. 
It is experimental feature, so be careful when playing with it
Run command bellow to see what are the options
```
python average_and_substract.py --help
```
Example run with plot and 'bubbles skipping'
```
python average_and_substract.py -s 490 -e 495  -f 1 -b ls2863_saxs_00479_0001_var_ave.dat
```
-----------------------------------------------------------------------
### Extracts time points from stopped-flow measurements
Extracts elapsed times from the log file and substarcts 5ms (set a as a default for measurements)
To run the script simply type:
```
python extract_times.py saxs2_saxs_20181121.log > samples_times.txt
```
Returns frame and subframe and corresponding time point