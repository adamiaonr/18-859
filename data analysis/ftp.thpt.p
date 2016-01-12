# Gnuplot script file

set terminal postscript enhanced font "Helvetica,10"
set output '| ps2pdf - ftp.thpt.pdf'

#set multiplot layout 2, 1 title "0.5 MB, 1024 B Chunk Size"
set multiplot layout 3, 1
set tmargin 3
set bmargin 3
set lmargin 10
set rmargin 10

unset log                           # remove any log-scaling
unset label                         # remove any previous labels

set ylabel "Throughput (Mbps)"

set xtic auto                       # set xtics automatically
set ytic auto                       # set ytics automatically

#set key outside horizontal
#set key center bottom
unset key

set title "500 kB"
plot "ftp_0_5.thpt.dat" using 1:2 title 'Throughput (Mbps)' with lines

set title "5 MB"
plot "ftp_5.thpt.dat" using 1:2 title 'Throughput (Mbps)' with lines

set title "50 MB"
set xlabel "Time (sec)"

plot "ftp_50.thpt.dat" using 1:2 title 'Throughput (Mbps)' with lines

unset multiplot
