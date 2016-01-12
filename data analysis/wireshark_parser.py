from datetime import date
from datetime import datetime
from decimal import Decimal
from time import mktime
import sys
import os
import collections
import dateutil.parser

TIMESTAMP   = "TIMESTAMP"
THROUGHPUT  = "THROUGHPUT"

def main():

    if len(sys.argv) < 2:
        print "Incorrect usage: python wireshark_parser.py [LOG_ABS_PATH]"

        return

    if not os.path.isfile(sys.argv[1]):
        print "wireshark log file '" + sys.argv[1] + "' does not exist. Exiting."
        return

    FILE = open(sys.argv[1])
    log_file = FILE.readlines()
    FILE.close()

    printList = []

    is_initial_timestamp = True

    # initial line
    printList.append("# " + TIMESTAMP + "\t" + THROUGHPUT + "\n")

    for line in log_file:

        # remove all '"'
        line = line.replace('"', '')

        # replace ',' by ' ' as delimiting character
        line = line.replace(',',' ')

        # work on the timestamp representation, pass it to a UNIX timestamp
        timestamp_str = line.split()[0]
        timestamp_str = timestamp_str.split('.')[0]
        t = datetime.strptime(timestamp_str, "%H:%M:%S")

        print mktime(t.timetuple())+1e-6*t.microsecond

            isent       = line.split()[2]
            recvd       = line.split()[4]
            holes       = line.split()[8]
            curwin      = line.split()[14]
            rtt         = line.split()[16]
            rtte        = line.split()[18]

            printList.append(str(timestamp - initial_timestamp) + "\t" + isent + "\t" + recvd + "\t" + holes + "\t" + curwin + "\t" + rtt + "\t" + rtte + "\n")

    gnuplot_dat_file = open("udp_0_5_1024.dat", "w");

    for item in printList:
        gnuplot_dat_file.write(item);

    gnuplot_dat_file.close();

    # initial line
    printList.append("# " + TIMESTAMP + "\t" + ISENT + "\t" + RECVD + "\t" + HOLES + "\t" + CURWIN + "\t" + RTT + "\t" + RTTE + "\n")

if __name__ == "__main__":
    main()

