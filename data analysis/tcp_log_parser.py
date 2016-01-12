from datetime import date
from datetime import datetime
from decimal import Decimal
from time import mktime
import decimal
import time
import sys
import os
import collections

UDP_PREFIX  = "udp_"
FTP_PREFIX  = "ftp_"

# the file sizes used in the tests, in ascending order, in key:value pairs. the 
# keys are the codes used in the file names for each size (e.g. 0_5 for 500 kB) 
# the values have the textual representation '500 kB' and the exact number of 
# bytes, separated by a ':'.
FILE_SIZES = {'0_5' : '"500 kB":512000', '5' : '"5 MB":5242880', '50' : '"50 MB":52428800'}
#FILE_SIZES = {'5' : '"5 MB":5242880', '50' : '"50 MB":52428800'}

THPT_SUFFIX = "thpt"
STAT_SUFFIX = "stat"
PCKT_SUFFIX = "pckt"
BYTE_SUFFIX = "byte"
SENT_SUFFIX = "sent"
RCVD_SUFFIX = "rcvd"
DAT_SUFFIX  = "dat"

TIMESTAMP   = "TIMESTAMP"
THROUGHPUT  = "THROUGHPUT"
ISENT       = "ISENT"
RECVD       = "RECV"
HOLES       = "HOLES"
CURWIN      = "CURWIN"
RTT         = "RTT"
RTTE        = "RTTE"

def main():

    if len(sys.argv) < 1:

        print "Incorrect usage: python tcp_log_parser.py"

        return

    today_date = datetime.now().strftime("%Y-%m-%d")

    # create a .dat file for each file size
    for file_size, tick in FILE_SIZES.iteritems():

        if file_size == "0_5":
            n = 1000
        else:
            n = 100

        initial_gnuplot_timestamp = 0
        is_initial_gnuplot_timestamp = True

        thpt_file_name = FTP_PREFIX + file_size + "." + THPT_SUFFIX

        if not os.path.isfile(thpt_file_name):
            print "throughput file '" + thpt_file_name + "' does not exist. Exiting."
            return

        thpt_file = open(thpt_file_name)
        thpt_file_lines = thpt_file.readlines()
        thpt_file.close()

        thpt_file_printList = []

        # initial line
        thpt_file_printList.append("# " + TIMESTAMP + "\t" + THROUGHPUT + "\n")

        for line in thpt_file_lines:

            # remove all '"'
            line = line.replace('"', '')

            # replace ',' by ' ' as delimiting character
            line = line.replace(',',' ')

            # work on the timestamp representation

            # extract the timestamp, as formated by wireshark (ignore the 
            # 1/100 second part, after the '.' for now)

            # FIXME: we attempt a trick here, give the script a 'fake' date to 
            # the wireshark time, so that the subsequent operations are 
            # performed on UNIX timestamps. this trick is bad and you should 
            # feel bad.
            wireshark_tmstmp_str = today_date + " " + line.split()[0].split('.')[0]

            # extract the time with format %H:%M:%S from the wireshark time 
            # representation, so that python knows how to work with it
            unix_timestamp = datetime.strptime(wireshark_tmstmp_str, "%Y-%m-%d %H:%M:%S")

            # create the gnuplot_timestamp, a timestamp format that gnuplot 
            # understands
            gnuplot_timestamp = Decimal(str(mktime(unix_timestamp.timetuple())).split('.')[0] + "." + line.split()[0].split('.')[1])

            # save the initial gnuplot_timestamp value
            if is_initial_gnuplot_timestamp:
                initial_gnuplot_timestamp = gnuplot_timestamp
                is_initial_gnuplot_timestamp = False

            # extract the throughput value, multiply it by 10^(-4) to convert 
            # it to Mbps
            thpt = Decimal(line.split()[1])
            thpt = thpt * n * decimal.Decimal('0.000001')

            # add the fabricated line to the list of lines of the future .dat 
            # file
            thpt_file_printList.append(str(gnuplot_timestamp - initial_gnuplot_timestamp) + "\t" + str(thpt) + "\n")

        # dump everything to the respective .thpt.dat file
        gnuplot_dat_file = open(str(FTP_PREFIX + file_size + "." + THPT_SUFFIX + "." + DAT_SUFFIX), "w");

        for item in thpt_file_printList:
            gnuplot_dat_file.write(item);

        gnuplot_dat_file.close();

        # delete the line array contents
        del thpt_file_printList[:]

if __name__ == "__main__":
    main()

