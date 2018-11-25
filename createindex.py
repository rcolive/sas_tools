'''''This script will write an index.txt file in tab-delimited format for parsing .dat files in the specified data_folder. Each line will contain the filename followed by information from the header (first line) of the associated datafile.'''''
import os


data_folder = 'D:/ESRFdata/'
f = open('index.txt', 'a+')


for filename in os.listdir(data_folder):
    if filename.endswith('.dat'):
        #print filename

        with open(data_folder+filename) as openfile:
            for line in openfile:
                line_edit = line.replace('|','\t')
                table1 = [filename, line_edit]
                print '\t'.join(table1)
                f.write('\t'.join(table1))
                break

f.close()
print 'done'
