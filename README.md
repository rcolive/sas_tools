# sas_tools
Simple SAXS/SANS utilities for data processing and visualisation 
with minimum maintanace effort.
Scripts will be mantained as requsted. 
##Instalation
For the basic functionality requires python and numpy package

##Scripts
###Average and substract
Averaging frames from the given range and substracts buffer. 
It may also remove frames with bubbles and plot final intensity
Skipping bubbles requires however installing AutoRg from Atsas 
package in 
Run command bellow to see what are the options
```
python average_and_substract.py --help
```
Example run with plot and 'bubbles skipping'
```
average_and_substract.py -s 490 -e 495  -f 1 -b ls2863_saxs_00479_0001_var_ave.dat
```

