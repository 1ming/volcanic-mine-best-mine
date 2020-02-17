import numpy as np
import matplotlib.pyplot as plt

def plot_vm(results, show=True, filename=None, plot_title=None):

    # initialize dataset
    t = results['t']
    s = results['s']

    fig, axs = plt.subplots(2, 1)

    # plot the vents
    for vent_name in ["a", "b", "c"]:
        vent_data = results[vent_name]
        axs[0].plot(t, vent_data, label=vent_name)
        # axs[0].plot(t, vent_data, marker='.', label=vent_name)  # if we want to change the marker type
    # axs[0].axvline(48, ls="--", color='r', label="kdjfkdjfk")
    # axs[0].axvline(100, ls="--", color='r', label="kdjfkdjfk")
    axs[0].legend(bbox_to_anchor=(1.05, 1), loc='upper left', borderaxespad=0.)
    axs[0].set_xlabel('time')
    axs[0].set_ylabel('Vents')
    axs[0].grid(True)

    # plot the stability
    axs[1].plot(t, s)
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
