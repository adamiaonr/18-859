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

CHUNK_SIZES = []

CHUNK_SIZES.append("1024")
CHUNK_SIZES.append("4096")
CHUNK_SIZES.append("8192")

STAT_SUFFIX = "stat"
PCKT_SUFFIX = "pckt"
BYTE_SUFFIX = "byte"
SENT_SUFFIX = "sent"
RCVD_SUFFIX = "rcvd"
DAT_SUFFIX  = "dat"

def main():

    if len(sys.argv) < 2:

        print "Incorrect usage: python stat_parser.py [OPTION]"
        print "\tudp\nCreate .dat files for CCNx (UDP) transfers"
        print "\ttcp\nCreate .dat files for TCP transfers"

        return

    # save the transfer option (UDP from CCNx or TCP), which determines wich 
    # files to parse and .dat files to generate.
    transfer_option = sys.argv[1]

    # string lists for populating the .pckt and .byte .dat files.
    pckt_dat_file_printList = []
    byte_dat_file_printList = []

    # based on the transfer_option, create UDP or TCP .dat files.
    if transfer_option == "udp":

        # create a .dat file line for each file size
        for file_size, tick in FILE_SIZES.iteritems():

            # create a line for the group of different CHUNK_SIZES for 
            # file_size.
            #pckt_dat_file_printList.append(tick)
            #byte_dat_file_printList.append(tick)

            # The idea is to have a line in the following way.
            #
            # file_size 3 x (INTEREST_PACKETS/BYTES    CONTENT_PACKETS/BYTES   TOTAL_PACKETS/BYES), 
            # for each chunk_size.

            # Add the column titles for the .dat files.
            # Also add a column marking the file size, in bytes (will be used for 
            # comparison in the charts, to directly visualize overhead).
            pckt_dat_file_printList.append('"Chunk Size"' + "\t " + '"Interests"' + "\t" + '"Content Obj."' + "\t" + '"Total"' + "\t" + '"File Size"' + "\n")
            byte_dat_file_printList.append('"Chunk Size"' + "\t " + '"Interests"' + "\t" + '"Content Obj."' + "\t" + '"Total"' + "\t" + '"File Size"' + "\n")

            # extract the file size in bytes
            file_size_bytes = tick.split(':')[1]

            for chunk_size in CHUNK_SIZES:

                pckt_dat_file_printList.append(chunk_size)
                byte_dat_file_printList.append(chunk_size)

                stat_file_name = UDP_PREFIX + file_size + "_" + chunk_size + "." + STAT_SUFFIX

                if not os.path.isfile(stat_file_name):
                    print "wireshark stat file '" + stat_file_name + "' does not exist. Exiting."
                    return

                stat_file = open(stat_file_name)
                stat_file_lines = stat_file.readlines()
                stat_file.close()

                for line in stat_file_lines:

                    # remove all '"'
                    line = line.replace('"', '')

                    # replace ',' by ' ' as delimiting character
                    line = line.replace(',',' ')

                    # retrieve the necessary variables and build part of the 
                    # .dat file string for the current file_size.
                    pckt_dat_file_printList.append("\t" + line.split()[6] + "\t" + line.split()[8] + "\t" + line.split()[4] + "\t" + file_size_bytes + "\n")

                    # the byte values require a special treatment.
                    interest_bytes = long(line.split()[7])
                    content_bytes = long(line.split()[9])
                    total_bytes = interest_bytes + content_bytes

                    byte_dat_file_printList.append("\t" + line.split()[7] + "\t" + line.split()[9] + "\t" + str(total_bytes) + "\t" + file_size_bytes + "\n")

            # dump everything to the respective files.
            pckt_dat_file = open(str(UDP_PREFIX + file_size + "." + STAT_SUFFIX + "." + PCKT_SUFFIX + "." + DAT_SUFFIX), "w")
            byte_dat_file = open(str(UDP_PREFIX + file_size + "." + STAT_SUFFIX + "." + BYTE_SUFFIX + "." + DAT_SUFFIX), "w")

            for item in pckt_dat_file_printList:
                pckt_dat_file.write(item)

            pckt_dat_file.close()

            for item in byte_dat_file_printList:
                byte_dat_file.write(item)

            byte_dat_file.close()

            # delete the line array contents.
            del pckt_dat_file_printList[:]
            del byte_dat_file_printList[:]

    elif transfer_option == "tcp":

        # create a .dat file line for each file size
        for file_size, tick in FILE_SIZES.iteritems():

            # Add the column titles for the .dat files
            pckt_dat_file_printList.append('"File Size"' + "\t " + '"Sent"' + "\t" + '"Received"' + "\t" + '"Total"' + "\t" + '"File Size"' + "\n")
            byte_dat_file_printList.append('"File Size"' + "\t " + '"Sent"' + "\t" + '"Received"' + "\t" + '"Total"' + "\t" + '"File Size"' + "\n")

            # extract the file size in str representation and bytes
            file_size_str = tick.split(':')[0]
            file_size_bytes = tick.split(':')[1]

            # create a line for the group of different CHUNK_SIZES for 
            # file_size.
            pckt_dat_file_printList.append(file_size_str)
            byte_dat_file_printList.append(file_size_str)

            # The idea is to have a line in the following way.
            #
            # file_size 3 x (INTEREST_PACKETS/BYTES    CONTENT_PACKETS/BYTES   TOTAL_PACKETS/BYES).

            stat_file_name = FTP_PREFIX + file_size + "." + STAT_SUFFIX

            if not os.path.isfile(stat_file_name):
                print "wireshark stat file '" + stat_file_name + "' does not exist. Exiting."
                return

            stat_file = open(stat_file_name)
            stat_file_lines = stat_file.readlines()
            stat_file.close()

            for line in stat_file_lines:

                # remove all '"'
                line = line.replace('"', '')

                # replace ',' by ' ' as delimiting character
                line = line.replace(',',' ')

                # retrieve the necessary variables and build part of the 
                # .dat file string for the current file_size.

                # wireshark is inconsistent when retrieving the order of 
                # sender/receiver. based on the indication of receiver's IP, 
                # choose the appropriate way of retrieving the log values.

                if line.split()[0] == "192.168.1.100":
                    pckt_dat_file_printList.append("\t" + line.split()[6] + "\t" + line.split()[8] + "\t" + line.split()[4] + "\t" + file_size_bytes)
                    byte_dat_file_printList.append("\t" + line.split()[7] + "\t" + line.split()[9] + "\t" + line.split()[5] + "\t" + file_size_bytes)
                else:   
                    pckt_dat_file_printList.append("\t" + line.split()[8] + "\t" + line.split()[6] + "\t" + line.split()[4] + "\t" + file_size_bytes)
                    byte_dat_file_printList.append("\t" + line.split()[9] + "\t" + line.split()[7] + "\t" + line.split()[5] + "\t" + file_size_bytes)

            pckt_dat_file_printList.append("\n")
            byte_dat_file_printList.append("\n")

            # dump everything to the respective files.
            pckt_dat_file = open(str(FTP_PREFIX + file_size + "." + STAT_SUFFIX + "." + PCKT_SUFFIX + "." + DAT_SUFFIX), "w")
            byte_dat_file = open(str(FTP_PREFIX + file_size + "." + STAT_SUFFIX + "." + BYTE_SUFFIX + "." + DAT_SUFFIX), "w")

            for item in pckt_dat_file_printList:
                pckt_dat_file.write(item)

            pckt_dat_file.close()

            for item in byte_dat_file_printList:
                byte_dat_file.write(item)

            byte_dat_file.close()

            # delete the line array contents.
            del pckt_dat_file_printList[:]
            del byte_dat_file_printList[:]

    else:

        print "Unrecognized option: " + transfer_option

if __name__ == "__main__":
    main()

