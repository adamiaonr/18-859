# Gnuplot script file

set terminal postscript enhanced font "Helvetica,16"
set terminal postscript landscape 16
set output '| ps2pdf - udp_5_4096.pdf'

set multiplot layout 3, 1
set tmargin 2
set lmargin 5
set rmargin 0

unset log                           # remove any log-scaling
unset label                         # remove any previous labels

set tmargin 2

set xtic auto                       # set xtics automatically
set ytic auto                       # set ytics automatically

set key outside horizontal
set key center bottom
set ytic 5

plot "udp_5_4096.thpt.dat" using 1:2 title 'Throughput (Mbps)' with lines

set xrange [GPVAL_X_MIN:GPVAL_X_MAX] 
set ytic 200

plot "udp_5_4096.dat" using 1:2 title 'Interests Sent' axes x1y1 with linespoints , \
        "udp_5_4096.dat" using 1:3 title 'Content Received' axes x1y1 with linespoints

set xlabel "Time (sec)"
set xrange [GPVAL_X_MIN:GPVAL_X_MAX] 
set ytic 10

plot    "udp_5_4096.dat" using 1:4 title 'Holes' axes x1y1 with linespoints , \
        "udp_5_4096.dat" using 1:5 axes x1y1 title 'CCN Curwin' with linespoints

unset multiplot
