"""
Simple script to average SAXS data from the time-resolved measurments
"""

import os
import sys
import numpy as np
import subprocess
import optparse


def make_intensity_plot(qvector, exp_intensities, exp_errors):
    """
    Produces plot given the data
    :param data:
    :param log:
    :return:
    """
    import matplotlib
    import matplotlib.pyplot as plt

    matplotlib.use("TkAgg")
    plt.plot(qvector, exp_intensities, 'ko', markersize=4, mfc="none")
    plt.errorbar(qvector, exp_intensities, yerr=exp_errors,
                 fmt="ko", markersize=6, mfc='none', alpha=0.6, zorder=0)

    plt.yscale('log')
    plt.xscale('log')

    plt.ylabel("$log(Intenisty)$")
    plt.xlabel("$q [\AA^{-1}]$")
    #plt.ylabel("RMSD")
    #plt.xlabel("Noise $(\sigma)$")
    #plt.figure(figsize=(8, 6))
    #plt.savefig("average_substraced.png", dpi=300, bbox_inches='tight')
    plt.show()


def read_file_safe(filename, dtype="float64"):
    """
    Simple check if file exists
    :param filename:
    :return:
    """
    try:
        results = np.genfromtxt(filename, dtype=dtype, skip_header=1)
    except IOError as err:
        print(os.strerror(err.errno))
    return results


if __name__ == "__main__":

    doc = """
            Simple script for averaging tr-SAXS data buffer substruction
            Outputs file named 'average_subtsracted_[start_frame]_[end_frame]_[sub_frame].dat
            Final output is in [1/A], which is done in naive way from [1/nm]
        """
    print(doc)
    usage = "usage: %prog [options] args"
    option_parser_class = optparse.OptionParser
    parser = option_parser_class(usage=usage, version='0.1')

    parser.add_option("-s", "--start_frame", dest="start_frame", default=None,
                      type='int',
                      help="Starting frame [OBLIGATORY]")
    parser.add_option("-e", "--end_frame", dest="end_frame", default=None,
                      type='int',
                      help="End frame [OBLIGATORY]")
    parser.add_option("-f", "--sub_frame", dest="sub_frame", default=None,
                      type='int',
                      help="Sub frame for time point to average over [OBLIGATORY]")
    parser.add_option("-b", "--buffer_file", dest="buffer_file", default=None,
                      help="Buffer file name to substarct[OBLIGATORY]")
    parser.add_option("-k", "--skip_bubbles", dest="skip_bubbles", action="store_true",
                      help="Wheteher to skip bubbles or not [Requires AutoRg from Atsas Package installed]")
    parser.add_option("-p", "--show_plot", dest="show_plot", action="store_true",
                      help="Plots intensity")
    options, args = parser.parse_args()

    experimental_files = os.listdir(".")

    # To check consitency in the qsapce - some files seem to differ
    #qvector_size = 342
    buffer_curve_name =  options.buffer_file
    start_frame = int(options.start_frame)
    end_franme = int(options.end_frame)
    sub_frame = int(options.sub_frame)
    skip_bubbles = False
    plot_intensity = False
    if (sys.argv[4]) == 'skip_bubbles':
        skip_bubbles = True


    combined_intensity = []
    combined_errors = []
    valid_samples = 0
    first_run = True

    buffer = read_file_safe(buffer_curve_name)
    buffer_errors = buffer[:, 2]
    buffer_intensity = buffer[:, 1]
    valid_curves = 0
    for experimental_file in experimental_files:

        if 'ave.dat' in experimental_file:
            continue

        if 'averaged_substracted' in experimental_file or  experimental_file == 'tmp.txt':
            continue

        frame_no = int(experimental_file.split("_")[2])
        sub_frame_no = int(experimental_file.split("_")[3])
        if frame_no < start_frame or frame_no > end_franme:
            continue
        if sub_frame != sub_frame_no:
            continue


        experimental = read_file_safe(experimental_file)
        qvector =  experimental[:,0]
        intensity = experimental[:,1]
        errors = experimental[:,2]
        if first_run:
            qvector_to_check = qvector
            first_run = False

        #Qvector inconsitency
        if qvector.all() != qvector_to_check.all():
            print("qvector inconsistent. Skipping " + experimental_file)
            continue
        # if np.shape(qvector)[0] != qvector_size:
        #     print("qvector inconsistent. Skipping " + experimental_file)
        #     continue

        if options.skip_bubbles:
            #Filter out bubbles with very simple criteria
            substracted_intensity = intensity - buffer_intensity
            substracted_errors = np.sqrt(buffer_errors ** 2 + errors ** 2)
            #if (substracted_intensity[2]-substracted_intensity[1])> cutoff_set:
            #    continue
            np.savetxt('tmp.txt', np.transpose([qvector, substracted_intensity,substracted_errors]))
            proc = subprocess.Popen(["autorg tmp.txt"], stdout=subprocess.PIPE, shell=True)
            (out, err) = proc.communicate()
            out_string = str(out)
            if out_string=="b\'\'":
                print("Skipping bubble file "+experimental_file)
                continue

        combined_intensity.append(intensity)
        combined_errors.append(errors)
        valid_curves+=1
    combined_intensity =np.average(combined_intensity, axis=0)
    combined_errors=np.average(combined_errors, axis=0)
    substracted_errors = np.sqrt(buffer_errors**2 + combined_errors**2)
    substracted = combined_intensity - buffer_intensity
    np.savetxt('averaged_substracted_'+str(start_frame)+"_"+str(end_franme)+"_"+str(sub_frame)+".dat",
               np.transpose([0.1*qvector, substracted, substracted_errors]))


    if options.show_plot:
        make_intensity_plot(0.1*qvector, substracted, combined_errors)

    #print('Number of valid curves used in averaging '+str(valid_curves))