import matplotlib.pyplot as plt
import numpy as np


# labels = ['G1', 'G2', 'G3', 'G4', 'G5']
ipfs_std=[0,0,0,0,0,0,0,0,0]
# ipfs_std= [12.720079397176516,12.900469666017125,12.881717445868288,12.82756227443913,12.745004418889131,
        # 12.559116616986616,12.770307666886163,12.767287342936482,8.515212218591717]
wedav_std=[0.0338673541129338,0.023147290366496775,0.03363363200476123,0.05440992830521473,0.038180646980186944,
        0.04262282891422877,0.039902551129576476,0.11052098205062763,0.2364613579323825]
IPFS_means = [4.55993618965149,4.565255427360535,4.605974817276001,4.5554465532302855,4.608577990531922,
        5.371003890037537,5.884150433540344,9.674112248420716,25.33629479408264]
WebDAV_means = [0.47037158012390134,0.4848583698272705,0.4883012056350708,0.5207067728042603,0.5628653287887573,
        0.7051048040390014,1.2055161237716674,3.0324445962905884,10.024100065231323]

x = np.arange(9)  # the label locations
width = 0.35  # the width of the bars

fig, ax = plt.subplots()
rects1 = ax.bar(x - width/2, IPFS_means, width, yerr=ipfs_std, label='IPFS')
rects2 = ax.bar(x + width/2, WebDAV_means, width, yerr=wedav_std, label='WebDAV')

# Add some text for labels, title and custom x-axis tick labels, etc.
ax.set_ylabel('Time')
ax.set_title('Comparison of average makespan between IPFS and WebDAV')
ax.set_xticks(x)
ax.legend(loc="upper left")

ax.bar_label(rects1, padding=3)
ax.bar_label(rects2, padding=3)

fig.tight_layout()

plt.show()