# Gnuplot script file

set terminal postscript enhanced font "Helvetica,12"
set output '| ps2pdf - tcp.pdf'

#set multiplot layout 2, 1 title "TCP Packet and Byte Count vs. File Size"
set multiplot layout 2, 3

# margins for the chart box
set tmargin 2
set bmargin 2
set lmargin 5
set rmargin 5

unset log                           # remove any log-scaling
unset label                         # remove any previous labels

set style data histogram
set style histogram cluster gap 1
set style fill solid border -1

a = 'black'
b = '#555555'
c = '#999999'
w = 'white'

set ylabel "Num. of Packets"
set xlabel "File Size"

unset key

plot 'ftp_0_5.stat.pckt.dat' using 2:xtic(1) ti col fc rgb w, '' u 3 ti col fc rgb c, '' u 4 ti col fc rgb a

unset ylabel
unset xlabel

plot 'ftp_5.stat.pckt.dat' using 2:xtic(1) ti col fc rgb w, '' u 3 ti col fc rgb c, '' u 4 ti col fc rgb a
plot 'ftp_50.stat.pckt.dat' using 2:xtic(1) ti col fc rgb w, '' u 3 ti col fc rgb c, '' u 4 ti col fc rgb a

unset title

set ylabel "Bytes (kB)"
set xlabel "File Size"

n = 1024

plot 'ftp_0_5.stat.byte.dat' using ($2/n):xtic(1) ti col fc rgb w, '' u ($3/n) ti col fc rgb c, '' u ($4/n) ti col fc rgb a, (512000/n) ti 'File Size' with lines

set ylabel "Bytes (MB)"
unset xlabel

n = 1024*1024

plot 'ftp_5.stat.byte.dat' using ($2/n):xtic(1) ti col fc rgb w, '' u ($3/n) ti col fc rgb c, '' u ($4/n) ti col fc rgb a, (5242880/n) ti 'File Size' with lines

#set key horizontal
#set key at 0,0

plot 'ftp_50.stat.byte.dat' using ($2/n):xtic(1) ti col fc rgb w, '' u ($3/n) ti col fc rgb c, '' u ($4/n) ti col fc rgb a, (52428800/n) ti 'File Size' with lines

unset multiplot
