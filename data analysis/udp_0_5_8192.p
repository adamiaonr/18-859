# Gnuplot script file

set terminal postscript enhanced font "Helvetica,10"
set output '| ps2pdf - udp_0_5_8192.pdf'

set multiplot layout 3, 1 title "0.5 MB, 8192 B Chunk Size"
set tmargin 2
set lmargin 10
set rmargin 10

unset log                           # remove any log-scaling
unset label                         # remove any previous labels

set tmargin 2

set xlabel "Time (sec)"

set xtic auto                       # set xtics automatically
set ytic auto                       # set ytics automatically

set key outside horizontal
set key center bottom

plot "udp_0_5_8192.thpt.dat" using 1:2 title 'Throughput (Mbps)' with lines

set xrange [GPVAL_X_MIN:GPVAL_X_MAX] 

plot "udp_0_5_8192.dat" using 1:2 title 'Interests Sent' axes x1y1 with linespoints , \
        "udp_0_5_8192.dat" using 1:3 title 'Content Received' axes x1y1 with linespoints

set xrange [GPVAL_X_MIN:GPVAL_X_MAX] 

plot    "udp_0_5_8192.dat" using 1:4 title 'Holes' axes x1y1 with linespoints , \
        "udp_0_5_8192.dat" using 1:5 axes x1y1 title 'CCN Curwin' with linespoints

unset multiplot
