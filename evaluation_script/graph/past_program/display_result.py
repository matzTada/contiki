#for PDR and Energy

import numpy as np
import matplotlib.pylab as plt

pdr_lf_avg = [0.0,0.0,0.0,0.00464252553389,0.0530103795459,0.271123491179,0.462395543175,0.711234911792,0.86165273909,1.0]
pdr_no_avg = [0.0,0.0,0.0,0.00278551532033,0.0362116991643,0.0622098421541,0.206128133705,0.396471680594,0.646239554318,1.0]
nrg_lf_avg = [347.738167084,115.266782332,35.8992743985,23.9001649798,20.0564148833,20.954644609,21.842908989,21.4174188515,22.4931829181,17.6214121678] #mA, energy consumed by a node
nrg_no_avg = [352.768620244,152.329659181,37.7232398925,22.4148193042,16.5936285894,15.4647291792,16.1488110749,15.2402507403,15.953706361,13.961260303] #mA

title_name = "PDR and Energy - Leapfrog vs Normal"

fig = plt.figure()
plt.title(title_name)
ax1 = fig.add_subplot(111)
t = np.arange(10, 101, 10)


ax1.set_xlabel('Rx ratio (%)')
ax1.set_ylabel('Packet Delivery Ratio')
ax1.plot(t, pdr_lf_avg, 'bx-', label='pdr_lf_avg')
ax1.plot(t, pdr_no_avg, 'gx-', label='pdr_no_avg')
ax1.legend(loc="upper left")

ax2 = ax1.twinx()

ax2.plot(t, nrg_lf_avg, 'ro--', label='nrg_lf_avg')
ax2.plot(t, nrg_no_avg, 'yo--', label='nrg_no_avg')
ax2.legend(loc="upper center")
ax2.set_ylabel('Energy (mA)')

fig.savefig(title_name + ".png")
plt.show()

