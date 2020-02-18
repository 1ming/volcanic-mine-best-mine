from collections import namedtuple, OrderedDict

import vm_plots
from rule_time import Rule_Time
from rule_start import Rule_Start
from rule_distance import Rule_Distance

# volcanic mine modelling
Direction = namedtuple("Direction", "up down")(*[1, -1])

# constants
TOTAL_TIME = 300
TIME_VENT_UPDATE = 6
TIME_STAB_UPDATE = 15
DEFAULT_VENT_UPDATE = 2
SWEET_SPOT_RANGE = [41, 59]

# change these into variables later
START_A = 50
START_B = 40
START_C = 50
START_DIR_A = Direction.down
START_DIR_B = Direction.down
START_DIR_C = Direction.down
# START_DIR_A = Direction.up
# START_DIR_B = Direction.up
# START_DIR_C = Direction.up

class Vent():
    def __init__(self, name, start_val, direction, parents):
        self.val = start_val
        self.name = name
        self.direction = direction
        self.parents = parents

    def update_val(self):
        update_amount = DEFAULT_VENT_UPDATE
        # Check if parents are in sweet spot.
        for parent in self.parents:
            if parent.check_in_ss():
                update_amount -= 1
        # Check own sweet spot.
        if self.check_in_ss():
            update_amount -= 1
        # Don't go negative
        if update_amount < 0:
            update_amount = 0
        self.val = self.val + update_amount * self.direction
        # Don't go over cap
        if self.val > 100:
            self.val = 100
        elif self.val < 0:
            self.val = 0

    # Change direction so that value goes towards 50
    def fix(self):
        if self.val < 50:
            self.direction = Direction.up
        elif self.val > 50:
            self.direction = Direction.down

    def check_in_ss(self):
        return (SWEET_SPOT_RANGE[0] <= self.val <= SWEET_SPOT_RANGE[1])

def get_stability_change(a, b, c):
    return 25 - (abs(a - 50) + abs(b-50) + abs(c-50))/3

def get_rules():
    return [
    Rule_Distance("Hey Jase Safe Rule", "A", 25, 60),
    # Rule_Time("Discord Fix A", "A", 30, 240, True),
    # Rule_Start("Discord Fix A at start", "A", 40),
    Rule_Start("Discord Fix B at start", "B", 20),
    ]


def main():
    # Create data object.
    data = {}
    # create vents A, B, C
    vent_a = Vent("A", START_A, START_DIR_A, [])
    vent_b = Vent("B", START_B, START_DIR_B, [vent_a,])
    vent_c = Vent("C", START_C, START_DIR_C, [vent_a, vent_b])
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
