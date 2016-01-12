from datetime import date
from datetime import datetime
from decimal import Decimal
from time import mktime
import decimal
import time
import sys
import os
import collections

TIMESTAMP   = "TIMESTAMP"
THROUGHPUT  = "THROUGHPUT"
ISENT       = "ISENT"
RECVD       = "RECV"
HOLES       = "HOLES"
CURWIN      = "CURWIN"
RTT         = "RTT"
RTTE        = "RTTE"

def main():

    if len(sys.argv) < 4:
        print "Incorrect usage: python log_parser.py [FILE_NAME] [CCN_LOG_ABS_PATH] [WIRESHARK_LOG_ABS_PATH]"

        return

    if not os.path.isfile(sys.argv[2]):
        print "ccncatchunks log file '" + sys.argv[2] + "' does not exist. Exiting."
        return

    if not os.path.isfile(sys.argv[3]):
        print "wireshark log file '" + sys.argv[3] + "' does not exist. Exiting."
        return

    # let's handle the ccncatchunks file first, well just for a little bit... 
    # to get the date and time out of it, which wireshark doesn't give us.
    if not os.stat(sys.argv[2]).st_size > 0:
        print "ccncatchunks log file is empty. ABORTING."
        return

    filename = sys.argv[1]

    CCN_FILE = open(sys.argv[2])
    ccn_log_file = CCN_FILE.readlines()
    CCN_FILE.close()

    ccn_printList = []

    initial_timestamp = 0
    is_initial_timestamp = True
    date_str = ""

    for line in ccn_log_file:

        # check if it is a '*** Hole at' line.
        if "*" not in line[1]:

            timestamp   = Decimal(line.split()[0])

            # timestamp transformations. objective: transform it to the format 
            # 2013-09-16 09:56:53.405
            timestamp_str = datetime.fromtimestamp(timestamp).strftime("%Y-%m-%d %H:%M:%S") + "." + line.split()[0].split('.')[1]
            date_str = timestamp_str.split()[0]

            break

    # let's leave the ccncatchunks log file for a moment, let's handle 
    # wireshark.
    WIRESHARK_FILE = open(sys.argv[3])
    wireshark_log_file = WIRESHARK_FILE.readlines()
    WIRESHARK_FILE.close()

    wireshark_printList = []

    # initial line
    wireshark_printList.append("# " + TIMESTAMP + "\t" + THROUGHPUT + "\n")

    for line in wireshark_log_file:

        # remove all '"'
        line = line.replace('"', '')

        # replace ',' by ' ' as delimiting character
        line = line.replace(',',' ')

        # work on the timestamp representation, pass it to a UNIX timestamp
        tmstmp_str = date_str + " " + line.split()[0].split('.')[0]
        unix_timestamp = datetime.strptime(tmstmp_str, "%Y-%m-%d %H:%M:%S")
        timestamp = Decimal(str(mktime(unix_timestamp.timetuple())).split('.')[0] + "." + line.split()[0].split('.')[1])

        if is_initial_timestamp:
            initial_timestamp = timestamp
            is_initial_timestamp = False

        thpt = Decimal(line.split()[1])
        thpt = thpt * 100 * decimal.Decimal('0.000001')

        wireshark_printList.append(str(timestamp - initial_timestamp) + "\t" + str(thpt) + "\n")

    gnuplot_dat_file = open(str(filename + ".thpt.dat"), "w");

    for item in wireshark_printList:
        gnuplot_dat_file.write(item);

    gnuplot_dat_file.close();

    isent       = 0
    recvd       = 0
    holes       = 0
    curwin      = 0
    rtt         = 0
    rtte        = 0

    for line in ccn_log_file:

        # check if it is a '*** Hole at' line.
        if "*" not in line[0]:

            timestamp   = Decimal(line.split()[0])

            isent       = line.split()[2]
            recvd       = line.split()[4]
            holes       = line.split()[8]
            curwin      = line.split()[14]
            rtt         = line.split()[16]
            rtte        = line.split()[18]

            ccn_printList.append(str(timestamp - initial_timestamp) + "\t" + isent + "\t" + recvd + "\t" + holes + "\t" + curwin + "\t" + rtt + "\t" + rtte + "\n")

    gnuplot_dat_file = open(str(filename + ".dat"), "w");

    for item in ccn_printList:
        gnuplot_dat_file.write(item);

    gnuplot_dat_file.close();

if __name__ == "__main__":
    main()

