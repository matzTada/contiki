#for energy

import numpy as np
import matplotlib.pylab as plt

pdr_lf_avg = [0.0,0.0,0.0,0.00464252553389,0.0530103795459,0.271123491179,0.462395543175,0.711234911792,0.86165273909,1.0]
pdr_no_avg = [0.0,0.0,0.0,0.00278551532033,0.0362116991643,0.0622098421541,0.206128133705,0.396471680594,0.646239554318,1.0]
nrg_lf_avg = [347.738167084,115.266782332,35.8992743985,23.9001649798,20.0564148833,20.954644609,21.842908989,21.4174188515,22.4931829181,17.6214121678] #mA, energy consumed by a node
nrg_no_avg = [352.768620244,152.329659181,37.7232398925,22.4148193042,16.5936285894,15.4647291792,16.1488110749,15.2402507403,15.953706361,13.961260303] #mA

title_name = "Energy Consumption - Leapfrog vs Normal"

fig = plt.figure()
plt.title(title_name)
ax1 = fig.add_subplot(111) #axes for all
ax2 = fig.add_axes([0.45, 0.4, 0.4, 0.4]) #axes for small

x1 = np.arange(10, 101, 10)
ax1.set_xlabel('Rx ratio (%)')
ax1.set_ylabel('Energy Consumption (mA)')
ax1.plot(x1, nrg_lf_avg, 'ro--', label='nrg_lf_avg')
ax1.plot(x1, nrg_no_avg, 'yo--', label='nrg_no_avg')

x2 = np.arange(60, 101, 10)
zoom_lf = []
zoom_no = []
for i in range(5, 10):
	zoom_lf.append(nrg_lf_avg[i])
	zoom_no.append(nrg_no_avg[i])
ax2.set_xlabel('Rx ratio (%)')
ax2.set_ylabel('Energy Consumption (mA)')
ax2.plot(x2, zoom_lf, 'ro--', label='nrg_lf_avg')
ax2.plot(x2, zoom_no, 'yo--', label='nrg_no_avg')

h1, l1 = ax1.get_legend_handles_labels() #get ax1's artist(Line2D) and label
h2, l2 = ax2.get_legend_handles_labels() #get ax2's artist and label

ax1.legend(h1, l1, loc="upper left") #display as ax1's legend

fig.savefig(title_name + ".png")
plt.show()