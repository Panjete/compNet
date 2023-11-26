import matplotlib.pyplot as plt
import numpy as np
import csv


part1files = ["part1/newreno.dat", "part1/vegas.dat", "part1/veno.dat", "part1/westwood.dat"]
part2afiles = ["part2a/c3.txt", "part2a/c5.txt", "part2a/c10.txt", "part2a/c15.txt", "part2a/c30.txt"]
part2bfiles = ["part2b/a1.txt", "part2b/a2.txt", "part2b/a4.txt", "part2b/a8.txt", "part2b/a12.txt"]
part3file = ["part3/part3.txt"]

part1titles = ["TCP Congestion Control: TCP NewReno", "TCP Congestion Control: TCP Vegas", "TCP Congestion Control: TCP Veno", "TCP Congestion Control: TCP WestWood"]
part2atitles = ["Channel Rate = 3Mbps", "Channel Rate = 5Mbps", "Channel Rate = 10Mbps", "Channel Rate = 15Mbps", "Channel Rate = 30Mbps"]
part2btitles = ["Application Data Rate= 1Mbps", "Application Data Rate= 2Mbps", "Application Data Rate= 4Mbps","Application Data Rate= 8Mbps","Application Data Rate= 12Mbps"]
part3title = ["Congestion Window vs time in Simulation, Part3"]

outputs1 = ["part1/newreno", "part1/vegas", "part1/veno", "part1/westwood"]
outputs2a = ["part2a/c3", "part2a/c5", "part2a/c10", "part2a/c15", "part2a/c30"]
outputs2b = ["part2b/a1", "part2b/a2", "part2b/a4", "part2b/a8", "part2b/a12"]
outputs3 = ["part3/cwind"]

files = [part1files, part2afiles, part2bfiles, part3file]
titles = [part1titles, part2atitles, part2btitles, part3title]
outs = [outputs1, outputs2a, outputs2b, outputs3]

for i in range(0,4):
    for j in range(len(files[i])):

        drops=0
        maxcwind=0
        f= open(files[i][j], 'r')
        X = []
        Y = []
        for line in f:
            b = line.split("\t")
            #print(b)
            if ((b[-1][:-1]).isdigit()):
                X += [float(b[0])]
                Y += [int(b[-1])]
                if(int(b[-1])>maxcwind):
                     maxcwind=int(b[-1])
                
            elif(b[0][:6]=="RxDrop"):
                drops +=1
        if(i==0):
        
        	print(part1titles[j])
        	print("Number of Packets Dropped = ", drops)
        	print("Maximum Congestion Window Size = ", maxcwind)
        plt.plot(X, Y)
        plt.title(titles[i][j])
        plt.xlabel('Time')
        plt.ylabel('Congestion Window')
        if(i==3):
            plt.axvspan(1, 19.9, color='red', alpha=0.5)
        if(i==3):
      	    plt.axvspan(20, 29.9, color='green', alpha=0.5)
        if(i==3):
            plt.axvspan(30, 100, color='yellow', alpha=0.5)
      
        plt.savefig("{}.png".format(outs[i][j]), bbox_inches='tight')
        #callbacks.process('close_event', CloseEvent())
        plt.close()


