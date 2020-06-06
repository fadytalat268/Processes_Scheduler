import matplotlib.pyplot as plt


def get_cmap(n, name='hsv'):
    '''Returns a function that maps each index in 0, 1, ..., n-1 to a distinct
    RGB color; the keyword argument name must be a standard mpl colormap name.'''
    return plt.cm.get_cmap(name, n)


def Draw_GanttChart(jobs, total_time):
    fig, gnt = plt.subplots()

    # Setting Y-axis limits
    gnt.set_ylim(0, 4 * len(jobs) + 1)

    # Setting X-axis limits
    gnt.set_xlim(0, float(total_time))
    #gnt.set_xticks(range(0, int(total_time) + 2), 0.1)
    xticks = []
    for i in range(0, len(jobs)):
        for slots in jobs[i]['Time_Slots']:
            xticks.append(slots[0])
            xticks.append(slots[0] + slots[1])

    gnt.set_xticks(xticks)

    # Setting labels for x-axis and y-axis
    gnt.set_xlabel('Unit Time')
    gnt.set_ylabel('Processes')

    # Setting ticks on y-axis
    # Labelling tickes of y-axis
    yticks = []
    ylabels = []
    for i in range(0, len(jobs)):
        yticks.append(3 + (4 * i))
        ylabels.append(str(jobs[i]['Task']))
    gnt.set_yticks(yticks)
    gnt.set_yticklabels(ylabels)

    # Setting graph attribute
    gnt.grid(True)
    cmap = get_cmap(len(jobs) + 1)

    for i in range(0, len(jobs)):
        gnt.broken_barh(jobs[i]['Time_Slots'], ((2 + (4 * i)), 2), facecolors=cmap(i))

    fig.set_size_inches(14, 6)
    fig.savefig("fig1.png")
    return
