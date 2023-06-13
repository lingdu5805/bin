#!/share/home/chem-lij/xuhb/apps/Python3.9/bin/python3
###Author: Xuhongbin 2022-12-13 in SUSTech-TCCL
###Version: 0.2.2.H.g
###Latest update: 2023-03-01
###Work in HuaXueXi
# !!pip install PyGnuplot==0.11.16
# !!change Python3.9/lib/python3.9/site-packages/PyGnuplot.py line30：gnuplot_address
import os
import time

import PyGnuplot as gp

totalwidth: max(os.get_terminal_size().columns, 80) = max(os.get_terminal_size().columns, 80)
totalhigth = max(os.get_terminal_size().lines - 5, 20)
K = []
tim = []
T = []
POT = []
au2ev = float(27.21132457027)

#######↓↓↓↓↓↓↓↓---[read file]---↓↓↓↓↓↓↓↓#######
os.system('cp cp2k.out cp2k.out0')
fo = open("cp2k.out0", "r")
for line in fo.readlines():
    if "TIME [fs]" in line:
        tim.append(line.split()[3])
    if "KINETIC ENERGY [hartree]" in line:
        K.append(line.split()[4])
    if "TEMPERATURE [K]" in line:
        T.append(line.split()[3])
    if "POTENTIAL ENERGY[hartree]" in line:
        POT.append(line.split()[3])
POT.remove("=")
fo.close()
#######↑↑↑↑↑↑↑↑---[read file]---↑↑↑↑↑↑↑↑#######
tim = list(map(float, tim))
K = list(map(float, K))
T = list(map(float, T))
POT = list(map(float, POT))
print("run time: {:.0f} → {:.0f} fs".format(tim[0], tim[-1]))
startime = input("start time[fs](default:{:.0f}):".format(tim[0])) or tim[0]
endtime = input("end time[fs](default:{:.0f}):".format(tim[-1])) or tim[-1]

#######↓↓↓↓↓↓↓↓---[au2ev]---↓↓↓↓↓↓↓↓#######
maxpot = max(POT)
POTEV = []
for i in POT:
    potau = float(i)
    POTEV.append((potau - maxpot) * 27.21132457027)
#######↑↑↑↑↑↑↑↑---[au2ev]---↑↑↑↑↑↑↑↑#######

#######↓↓↓↓↓↓↓↓---[print]---↓↓↓↓↓↓↓↓#######
# print("  TIME[fs]         KINETIC[eV]        TEMP[K]            POTENTIAL[eV]        ")
# print("---------------------------------------------------------------------------------")
# for i in range(0,len(tim)):
#    print('{0:>10.0f}{1:>20.6f}{2:>15}{3:>25.6f}'.format(float(tim[i]),float(K[i])*au2ev,T[i],float(POT[i])*autoev))
#######↑↑↑↑↑↑↑↑---[print]---↑↑↑↑↑↑↑↑#######

#######↓↓↓↓↓↓↓↓---[draw]---↓↓↓↓↓↓↓↓#######
gp.s([tim, K, T, POTEV], ".md")
gp.c('set term dumb size ' + str(totalwidth/2) + ',' + str(totalhigth/2) + ';set size 1,1;set yrange [' + str(
    min(POTEV)) + ':' + str(max(POTEV)) + '];set xrange [' + str(startime) + ':' + str(
    endtime) + '];set xlabel "Time[fs]";set ylabel "POTENTIAL[eV]";plot ".md" u 1:4 w l lc 3 axis x1y1 t "POTENTIAL['
               'eV]" ')
gp.c('set term dumb size ' + str(totalwidth/2) + ',' + str(totalhigth/2) + ';set size 1,1;set yrange [' + str(
    min(T)) + ':' + str(max(T)) + '];set xrange [' + str(startime) + ':' + str(
    endtime) + '];set xlabel "Time[fs]";set ylabel "TEMPERATURE[K]";plot ".md" u 1:3 w l lc 6 axis x1y1 t '
               '"TEMPERATURE[K]" ')
'''gp.c('set term dumb size '+str(totalwidth)+','+str(totalhigth)+';set size 1,1;set yrange ['+str(min(
POTEV))+':'+str(max(POTEV))+'];set xrange ['+str(startime)+':'+str(endtime)+'];set xlabel "Time[fs]";set y2tics;set 
y2range ['+str(min(T))+':'+str(max(T))+'];set ylabel "POTENTIAL[eV]";set y2label "TEMPERATURE[K]";plot ".md" u 1:4 w 
l lc 3 axis x1y1 t "POTENTIAL[eV]" , ".md" u 1:3  w l lc 6 axis x1y2 t "TEMPERATURE[K]"')'''
#######↑↑↑↑↑↑↑↑---[draw]---↑↑↑↑↑↑↑↑#######
time.sleep(0.1)
print("AIMD RUN: {:.0f} → {:.0f} fs".format(startime, endtime))

