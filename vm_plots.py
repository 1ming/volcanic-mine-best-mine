import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as colors
import matplotlib.cm as mplcm

DEFAULT_COLOURS = ['b', 'g', 'r', 'c', 'm', 'y']
EVENTS_LINE_WIDTH = 0.75
PLOTS_LINE_WIDTH = 0.8

def colour_cycler(colour_list = DEFAULT_COLOURS):
    while True:
        for colour in colour_list:
            yield colour

def debug_histogram(dataset, num_bins=20, filename=None):
    fig, axs = plt.subplots(figsize=(10,6))

    axs.hist(dataset, bins=num_bins)

    if filename is not None:
        plt.savefig(filename, bbox_inches='tight')

    plt.show()


def plot_mc_histograms():
    np.random.seed(19680801)

    N_points = 100000
    n_bins = 20

    # Generate a normal distribution, center at x=0 and y=5
    x = np.random.randn(N_points)
    y = .4 * x + np.random.randn(100000) + 5

    fig, axs = plt.subplots(1, 2, sharey=True, tight_layout=True)

    # We can set the number of bins with the `bins` kwarg
    axs[0].hist(x, bins=n_bins)
    axs[1].hist(y, bins=n_bins)

    plt.show()

def plot_histogram(dataset, num_bins=20, show_percentiles=False):
    pass

def plot_vm(results, events, show=True, filename=None, plot_title=None):
    # initialize colour cycler
    cc = colour_cycler()

    # initialize time series dataset
    t = results['t']
    s = results['s']

    fig, axs = plt.subplots(2,1,figsize=(10,6))

    # plot the vents timeseries
    for vent_name in ["A", "B", "C"]:
        vent_data = results[vent_name]
        axs[0].plot(t, vent_data, label=vent_name, lw=PLOTS_LINE_WIDTH, color=cc.next())

    # add annotations for events (when rules were applied)
    for (event_name, timestamps) in events.iteritems():
        event_label = "{}\n({})".format(event_name, ", ".join([str(a) for a in timestamps]))
        label_clr = cc.next()
        for (index, timestamp) in enumerate(timestamps):
            if index == 0:
                # only create a label if it's the first event of this type
                # otherwise it will create multiple labels in the legend for the same event
                axs[0].axvline(timestamp, ls="--", linewidth=EVENTS_LINE_WIDTH, label=event_label, color=label_clr)
            else:
                axs[0].axvline(timestamp, ls="--", linewidth=EVENTS_LINE_WIDTH, color=label_clr)


    axs[0].legend(bbox_to_anchor=(1.05, 1), loc='upper left', borderaxespad=0.)
    axs[0].set_xlabel('time')
    axs[0].set_ylabel('Vents')
    axs[0].grid(True)

    # plot the stability time series
    axs[1].plot(t, s, lw=PLOTS_LINE_WIDTH, color=cc.next())
    axs[1].set_xlabel('time')
    axs[1].set_ylabel('Stability')
    axs[1].grid(True)

    if plot_title is not None:
        plt.suptitle(plot_title)

    # adjust subplot area so title can fit above
    fig.tight_layout(rect=[0, 0.03, 1, 0.95])

    if filename is not None:
        plt.savefig(filename, bbox_inches='tight')

    if show:
        plt.show()
