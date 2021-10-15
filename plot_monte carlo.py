import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# plt.rcParams["figure.autolayout"] = True

Directory = 'C:/Users/sasha/Documents/0Lunar 2021/sashankredo2/Monte carlo.csv'
df = pd.read_csv(Directory)

fig, ax1 = plt.subplots()
ax1.set_ylim([0,2.0])
# plt.scatter(df['Age']/1000, 100*df['MedianRA'], linewidths=2, s=2)
# plt.scatter(df['Age']/1000, 100*df['5thPercentileRA'], linewidths=2, s=2)
# plt.scatter(df['Age']/1000, 100*df['95thPercentileRA'], linewidths=2, s=2)
# plt.scatter(df['Age']/1000, 100*df['MeanRA'], linewidths=2, s=2)
ax1.plot(df['Age']/1000, 100*df['MedianRA'], marker='o', linewidth=1, markersize=2)
ax1.plot(df['Age']/1000, 100*df['5thPercentileRA'], marker='o', linewidth=1, markersize=2)
ax1.plot(df['Age']/1000, 100*df['95thPercentileRA'], marker='o', linewidth=1, markersize=2)
ax1.plot(df['Age']/1000, 100*df['MeanRA'], marker='o', linewidth=1, markersize=2)
plt.title('Rock Abundance Evolution (Monte Carlo Simulation)')
plt.xlabel('Age (Ga)')
plt.ylabel('Fractional Rock Abundance (%)')
plt.legend(['Median RA','5th Percentile','95th Percentile','Mean RA'], loc='upper right')

ax2 = ax1.twinx()
ax2.set_ylim([0,15.0])
# plt.scatter(df['Age']/1000, 100*df['MedianRA'], linewidths=2, s=2)
ax2.plot(df['Age']/1000, df['regthick'],'--', c='blue', linewidth=1, markersize=2)
plt.ylabel('Regolith Thickness (m)', c='blue')
plt.legend(['Regolith Thickness'], loc='upper left')


fig.tight_layout()
plt.savefig("Fig3.png", dpi=600)
plt.show()