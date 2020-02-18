from vm import main, get_rules
from consts import VALVE_START_RANGE, VentDirection
from vm_plots import plot_histogram, debug_histogram, plot_vm
import numpy as np
import sys
from collections import OrderedDict

NUM_SAMPLES = 2
SAVE_DIR = "results"

def get_final_stability(results):
    pass

def _random_valve_start(num_samples, low=VALVE_START_RANGE[0], high=(VALVE_START_RANGE[1]+1)):
    return np.random.randint(low=low, high=high, size=num_samples)

def _random_valve_dir(num_samples):
    return np.random.choice([VentDirection.up, VentDirection.down], size=num_samples)

def get_vent_dir_stats(config_input_samples):
    vent_dir_input_stats = OrderedDict.fromkeys(["start_dir_a", "start_dir_b", "start_dir_c"])
    for k in vent_dir_input_stats.keys():
        vent_dir_input_stats[k] = OrderedDict()
        vent_dir_input_stats[k]["num_up"] = list(config_input_samples[k]).count(VentDirection.up)
        vent_dir_input_stats[k]["num_down"] = num_samples - vent_dir_input_stats[k]["num_up"]
        vent_dir_input_stats[k]["percent_up"] = round(float(vent_dir_input_stats[k]["num_up"])/num_samples, 2)
        vent_dir_input_stats[k]["percent_down"] = round(1.0 - vent_dir_input_stats[k]["percent_up"], 2)
    return vent_dir_input_stats

def plot_percentile(percentile, stability_dataset, all_iteration_results, all_iteration_events):
    index = stability_dataset.index(np.percentile(stability_dataset, percentile, interpolation='nearest'))
    results = all_iteration_results[index]
    events = all_iteration_events[index]
    plot_vm(results, events, plot_title="{}th".format(percentile), filename="results/{}th.png".format(percentile))

def monte_carlo(num_samples=NUM_SAMPLES):
    config_full_dataset = {
        "start_a": _random_valve_start(num_samples),
        "start_b": _random_valve_start(num_samples),
        "start_c": _random_valve_start(num_samples),
        "start_dir_a": _random_valve_dir(num_samples),
        "start_dir_b": _random_valve_dir(num_samples),
        "start_dir_c": _random_valve_dir(num_samples),
    }

    # print config_full_dataset
    # print

    # get statistics of the valve start directions
    vent_dir_input_stats = get_vent_dir_stats(config_full_dataset)
    # print vent_dir_input_stats

    # set up results (stability value at 5 min  mark)
    stability_dataset = []

    # store full data from every iteration
    all_iteration_results = []
    all_iteration_events = []

    for i in range(num_samples):
        # generate initial conditions
            # vent A, B, C values, directions
        config_dict = {k: config_full_dataset[k][i] for k in config_full_dataset.keys()}
        # print config_dict

        # config_dict = {num: num*num for num in range(1, 11)}
        # execute vm
        (iteration_results, iteration_events) = main(config_dict)

        # add resulting stability value to dataset
        stability_dataset.append(iteration_results["s"][-1])

        # store iteration results to all results so we can plot later if needed
        all_iteration_results.append(iteration_results)
        all_iteration_events.append(iteration_events)

    # print out the rules being used.
    print("Rules used:")
    for rule in get_rules():
        print(rule.name)

    # print some statistics of results
    print("")
    print("Stability dataset over {} games:".format(num_samples))
    # print stability_dataset
    print("Avg stability at 5min reset: {}".format(np.mean(stability_dataset)))
    print("Standard deviation: {}".format(np.std(stability_dataset)))
    print("5th percentile: {}".format(np.percentile(stability_dataset, 5, interpolation='nearest')))
    print("25th percentile: {}".format(np.percentile(stability_dataset, 25, interpolation='nearest')))
    print("50th percentile: {}".format(np.percentile(stability_dataset, 50, interpolation='nearest')))
    print("75th percentile: {}".format(np.percentile(stability_dataset, 75, interpolation='nearest')))
    print("95th percentile: {}".format(np.percentile(stability_dataset, 95, interpolation='nearest')))

    # get indices of different cases
    for i in [0, 100]:
        plot_percentile(i, stability_dataset, all_iteration_results, all_iteration_events)

    # plot results
    debug_histogram(stability_dataset, num_bins=50, filename="results/histogram.png")

if __name__ == "__main__":
    num_samples = NUM_SAMPLES
    if len(sys.argv) == 2:
        num_samples = int(sys.argv[1])
    monte_carlo(num_samples)
