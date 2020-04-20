import matplotlib.pyplot as plt
import numpy as np

fig = plt.figure()
fig.subplots_adjust(hspace=0.8, wspace = 0.5)
fig.suptitle("BREXIT REAL TIME CLASSIFICATION - Comparing models:", fontsize=16)
my_colors = ['brown','pink', 'red', 'limegreen', 'blue', 'cyan',
    'orange', 'dodgerblue','purple', 'turquoise', 'darkorchid', 'gold']

kmeans = [0,24,3,0,2,0,1,0,0]
gmm = [20,0,0,7,2,1,0]

ax = fig.add_subplot(1,2,1)
x = np.arange(1,len(kmeans)+1)
bars = ax.bar(x, kmeans, align='center', color = my_colors, edgecolor='k', linewidth=2)
for bar in bars:
    yval = bar.get_height()
    plt.text(bar.get_x(), yval + .5, str(int(yval)))

ax.set_xticks(x)
ax.set_yticks(np.array(range(0,30,5)))
plt.title('#tweets per cluster: kmeans - allD')  



ax = fig.add_subplot(1,2,2)
x = np.arange(1,len(gmm)+1)
bars = ax.bar(x, gmm, align='center', color = my_colors, edgecolor='k', linewidth=2)
for bar in bars:
    yval = bar.get_height()
    plt.text(bar.get_x(), yval + 1., str(int(yval)))

ax.set_xticks(x)
ax.set_yticks(np.array(range(0,30,5)))
plt.title('#tweets per cluster: gmm - 2d')   

plt.show()
