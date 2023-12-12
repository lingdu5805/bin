#!/share/home/chem-lij/xuhb/apps/deepmd-kit/bin/python
###Author: Xuhongbin 2022-12-13 in SUSTech-TCCL
###Version: 0.2.2.H.m
###Latest update: 2023-03-01
###Work in HuaXueXi
import os
import time
import matplotlib.pyplot as plt
#d1 = time.time()
totalwidth = max(os.get_terminal_size().columns, 80)
totalhigth = max(os.get_terminal_size().lines - 5, 20)
K = []
tim = []
T = []
POT = []
au2ev = float(27.21132457027)

#######↓↓↓↓↓↓↓↓---[read file]---↓↓↓↓↓↓↓↓#######
os.system('cp cp2k.out cp2k.out0')
#with open("cp2k.out", "r") as fo:
#    line = fo.readline()
#    while line :
#        if "TIME [fs]" in line:
#            tim.append(line.split()[3])
#        elif "KINETIC ENERGY [hartree]" in line:
#            K.append(line.split()[4])
#        elif "TEMPERATURE [K]" in line:
#            T.append(line.split()[3])
#        elif "POTENTIAL ENERGY[hartree]" in line:
#            POT.append(line.split()[3])
#        else :
#           pass
#        line = fo.readline()
#POT.remove("=")
fo=open("cp2k.out0","r")
for line in fo.readlines():
    if "TIME [fs]" in line:
            tim.append(line.split()[3])
    elif "KINETIC ENERGY [hartree]" in line:
            K.append(line.split()[4])
    elif "TEMPERATURE [K]" in line:
            T.append(line.split()[3])
    elif "POTENTIAL ENERGY[hartree]" in line:
            POT.append(line.split()[3])
    else :
        pass
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

###############↓↓↓↓↓↓↓↓---[draw]---↓↓↓↓↓↓↓↓#######
fig, (ax1, ax2) = plt.subplots(2)
fig.suptitle('AIMD RUN: {:.0f} → {:.0f} fs'.format(startime, endtime))

ax1.plot(tim, POTEV)
ax1.set(ylabel='POTENTIAL[eV]')
ax1.set_xlim([startime, endtime])

ax2.plot(tim, T)
ax2.set(xlabel='Time[fs]', ylabel='TEMPERATURE[K]')
ax2.set_xlim([startime, endtime])


plt.savefig('output.png')
plt.show()
#######↑↑↑↑↑↑↑↑---[draw]---↑↑↑↑↑↑↑↑#######

time.sleep(0.1)
print("AIMD RUN: {:.0f} → {:.0f} fs".format(startime, endtime))
#d2 = time.time()
#print(str(d2-d1))
