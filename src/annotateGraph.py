# # https://matplotlib.org/3.1.1/gallery/lines_bars_and_markers/barchart.html
# # https://stackoverflow.com/questions/28931224/adding-value-labels-on-a-matplotlib-bar-chart

import numpy as np
import matplotlib.pyplot as plt

company=['google','amazon','msft','fb']
revenue=[80,68,54,27]

fig=plt.figure()
ax=plt.subplot()

xpos=np.arange(len(company))

bars = plt.bar(xpos,revenue)


annot = ax.annotate("", xy=(0,0), xytext=(-20,20),textcoords="offset points",
                    bbox=dict(boxstyle="round", fc="black", ec="b", lw=2),
                    arrowprops=dict(arrowstyle="->"))
#TODO: Find correct values for (x,y) and xytext.
annot.set_visible(False)

def update_annot(bar):

    x = bar.get_x()+bar.get_width()/2.
    y = bar.get_y()+bar.get_height()
    #.get_x / y -> what value of x,y does the rectangle start at.
    # .get_widht/ height -> kitna mota/lamba it is..
    annot.xy = (x,y) #what does this do??
    text = "({} - {:.2g})".format(company[int(x)],y)
    annot.set_text(text)
    annot.get_bbox_patch().set_alpha(0.4)


def hover(event):
    vis = annot.get_visible()
    if event.inaxes == ax:
        for bar in bars:
            cont, ind = bar.contains(event)
            if cont:
                update_annot(bar)
                annot.set_visible(True)
                fig.canvas.draw_idle()
                return
    if vis:
        annot.set_visible(False)
        fig.canvas.draw_idle()

fig.canvas.mpl_connect("motion_notify_event", hover)

plt.show()