'''
Taking log file from stopped-flow experiment at ID02 and dumps frames and time to the file
'''
import sys
f = open(sys.argv[1])
counter = 0
lines = f.readlines()
times = []
for index, line in enumerate(lines):
	if 'ccdmcal' in line:
		times = []
	if 'Elapsed time' in line:
		time_elapsed = float(line.split('=')[1][:-9]) - 0.005
		times.append(round(time_elapsed,3))
	if 'ccdmvdc' in line:
		sample = ''
	if 'Writing dark file' in line:
		sample_name = line[-15:-10].strip('\n')
	for i,t in enumerate(times):
		print (sample_name+'_'+str(i+1), t)

