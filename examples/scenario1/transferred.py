import matplotlib.pyplot as plt
import numpy as np


# labels = ['G1', 'G2', 'G3', 'G4', 'G5']
ipfs_std= [4.2282121254470875, 6.077280093375106,4.881939505292269,8.534895690308373,6.880729935438859,
        6.095535707019979,28.122746823325933,11.292081788187291,20.754919095642524]
wedav_std=[9.16515138991168, 9.437513796899408,14.576998624164334,0.6324555320336759,16.778292854492413, 
        0.8755950357709131, 18.945535973767893,20.36445705416943,16.069640112128628]
IPFS_means = [18.1, 24.6, 31.5, 42.2, 50.3, 63.6, 81, 206.8, 763.1]
WebDAV_means = [25, 26.2, 31.4, 27.2, 39.8, 45.9, 105.6, 305.4, 1091.3]

x = np.arange(9)  # the label locations
width = 0.35  # the width of the bars

fig, ax = plt.subplots()
rects1 = ax.bar(x - width/2, IPFS_means, width, yerr=ipfs_std, label='IPFS')
rects2 = ax.bar(x + width/2, WebDAV_means, width, yerr=wedav_std, label='WebDAV')

# Add some text for labels, title and custom x-axis tick labels, etc.
ax.set_ylabel('Time')
ax.set_title('Comparison of average download time between IPFS and WebDAV')
ax.set_xticks(x)
ax.legend(loc="upper left")

ax.bar_label(rects1, padding=3)
ax.bar_label(rects2, padding=3)

fig.tight_layout()

plt.show()