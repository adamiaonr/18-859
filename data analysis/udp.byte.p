# Gnuplot script file

set terminal postscript enhanced font "Helvetica,12"
set output '| ps2pdf - udp.pdf'

set multiplot layout 2, 1 title "CCNx Packet and Byte Count vs. File and Chunk Size"

# margins for the chart box
set tmargin 2
set lmargin 10
set rmargin 10

unset log                           # remove any log-scaling
unset label                         # remove any previous labels

set style data histogram
set style histogram cluster gap 1
set style fill solid border -1

set tmargin 2

a = 'black'
b = '#555555'
c = '#999999'
w = 'white'

set title "500 kB"

set ylabel "Num. of Packets"

unset key

plot 'udp_0_5.stat.pckt.dat' using 2:xtic(1) ti col fc rgb w, '' u 3 ti col fc rgb c, '' u 4 ti col fc rgb a

unset title

set ylabel "Bytes"
set xlabel "Chunk Size (Bytes)"

set key outside horizontal
set key bottom center

plot 'udp_0_5.stat.byte.dat' using 2:xtic(1) ti col fc rgb w, '' u 3 ti col fc rgb c, '' u 4 ti col fc rgb a

unset multiplot
