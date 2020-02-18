from collections import namedtuple, OrderedDict
from consts import VentDirection, TOTAL_TIME, TIME_VENT_UPDATE, TIME_STAB_UPDATE, VALVE_START_RANGE

import vm_plots
from rule_time import Rule_Time
from rule_start import Rule_Start
from rule_distance import Rule_Distance
from vent import Vent

# volcanic mine modelling

# change these into variables later
DEFAULT_KWARGS = {
    "start_a": 50,
    "start_b": 40,
    "start_c": 30,
    "start_dir_a": VentDirection.down,
    "start_dir_b": VentDirection.down,
    "start_dir_c": VentDirection.down,
}

def validate_kwargs(input_config_dict):
    output_config_dict = input_config_dict
    # TODO implement validation of config dictionary and output a valid one
    # warn user if input config was not valid
    return output_config_dict

START_A = 50
START_B = 40
START_C = 50
START_DIR_A = VentDirection.down
START_DIR_B = VentDirection.down
START_DIR_C = VentDirection.down
# START_DIR_A = VentDirection.up
# START_DIR_B = VentDirection.up
# START_DIR_C = VentDirection.up

def get_stability_change(a, b, c):
    return 25 - (abs(a - 50) + abs(b-50) + abs(c-50))/3

def get_rules():
    return [
    Rule_Distance("Hey Jase Safe Rule", "A", 25, 60),
    # Rule_Time("Discord Fix A", "A", 30, 240, True),
    # Rule_Start("Discord Fix A at start", "A", 40),
    Rule_Start("Discord Fix B at start", "B", 20),
    ]


def main(config_dict=None):
    # handle default argument overrides
    if config_dict is None:
        config_dict = {}
    for (k, v) in DEFAULT_KWARGS.iteritems():
        if config_dict.get(k) is None:
            config_dict[k] = v
    config_dict = validate_kwargs(config_dict)

    # Create data object.
    data = {}
    # create vents A, B, C
    vent_a = Vent("A", config_dict["start_a"], config_dict["start_dir_a"], [])
    vent_b = Vent("B", config_dict["start_b"], config_dict["start_dir_b"], [vent_a,])
    vent_c = Vent("C", config_dict["start_c"], config_dict["start_dir_b"], [vent_a, vent_b])
    data["vents"] = {
    "A": vent_a,
    "B": vent_b,
    "C": vent_c
    }

    # initialize result datasets for time series plot
    results = OrderedDict([
        ("t", []),
        ("A", []),
        ("B", []),
        ("C", []),
        ("s", []),
    ])

    # Initialize stability.
    data["stability"] = 50
    data["stability_change"] = 0

    # Get rules
    rules = get_rules()

    for i in range(1,TOTAL_TIME):
        data["time"] = i;

        # update vent values
        if i % TIME_VENT_UPDATE == 0:
            print("Iteration {}: Updating vent values".format(i))
            for vent in data["vents"].values():
                vent.update_val()

        # update stability value
        if i % TIME_STAB_UPDATE == 0:
            print("Iteration {}: Updating stability value".format(i))
            data["stability_change"] = get_stability_change(*[x.val for x in data["vents"].values()])
            data["stability"] += data["stability_change"]
            # Don't go over cap
            if data["stability"] > 100:
                data["stability"] = 100
            elif data["stability"] < 0:
                data["stability"] = 0

        # Run player action rules.
        for rule in rules:
            if rule.check_condition(data):
                print("Iteration {}: Doing rule action {}".format(i, rule.name))
                rule.do_action(data)

        # add dataset to results
        for ventName, vent in data["vents"].items():
            results[ventName].append(vent.val)
        results["t"].append(i)
        results["s"].append(data["stability"])

    # populate events dictionary
    events = OrderedDict()
    for rule in rules:
        events.update(rule.dump())

    return (results, events)

if __name__ == "__main__":
    (results, events) = main()
    for (k, v) in results.iteritems():
        print("{}: {}".format(k, v))
        print

    # save to csv
    f = "test.csv"
    with open(f, "w") as fh:
        # write headers
        fh.write("{}\n".format(",".join(results.keys())))

        # write rows
        # assume all rows are the same length
        num_rows = len(results.values()[0])
        for i in range(num_rows):
            vals = [results[k][i] for k in results.keys()]
            fh.write("{}\n".format(",".join([str(a) for a in vals])))

    # vm_plots.plot_vm(results, plot_title="A=30down, B=40down, C=50down, nofix")
    vm_plots.plot_vm(results, events, plot_title="A=50down, B=40down, C=50down, nofix", filename="mingtest.png")
