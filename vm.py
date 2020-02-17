from collections import namedtuple, OrderedDict

import vm_plots

# volcanic mine modelling
Direction = namedtuple("Direction", "up down")(*[1, -1])

# constants
TOTAL_TIME = 300
TIME_VENT_UPDATE = 6
TIME_STAB_UPDATE = 15
DEFAULT_VENT_UPDATE = 2
SWEET_SPOT_RANGE = [41, 59]

# change these into variables later
START_A = 30
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
    def fix_dir(self):
        if self.val < 50:
            self.direction = Direction.up
        elif self.val > 50:
            self.direction = Direction.down

    def check_in_ss(self):
        return (SWEET_SPOT_RANGE[0] <= self.val <= SWEET_SPOT_RANGE[1])

def update_stability(a, b, c):
    return 25 - (abs(a - 50) + abs(b-50) + abs(c-50))/3



def main():
    # create vents A, B, C
    vent_a = Vent("A", START_A, START_DIR_A, [])
    vent_b = Vent("B", START_B, START_DIR_B, [vent_a,])
    vent_c = Vent("C", START_C, START_DIR_C, [vent_a, vent_b])
    vents = [vent_a, vent_b, vent_c]

    # initialize result datasets for time series plot
    results = OrderedDict([
        ("t", []),
        ("a", []),
        ("b", []),
        ("c", []),
        ("s", []),
    ])

    stability = 50

    for i in range(1,TOTAL_TIME):
        # update vent values
        if i % TIME_VENT_UPDATE == 0:
            print("Iteration {}: Updating vent values".format(i))
            for vent in vents:
                vent.update_val()

        # update stability value
        if i % TIME_STAB_UPDATE == 0:
            print("Iteration {}: Updating stability value".format(i))
            stability += update_stability(*[x.val for x in vents])
            # Don't go over cap
            if stability > 100:
                stability = 100
            elif stability < 0:
                stability = 0

        # add dataset to results
        for (dataset, vent) in zip([results[k] for k in ["a", "b", "c"]], vents):
            dataset.append(vent.val)
        results["t"].append(i)
        results["s"].append(stability)

    return results

if __name__ == "__main__":
    results = main()
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

    vm_plots.plot_vm(results, plot_title="A=30down, B=40down, C=50down, nofix")
    # vm_plots.plot_vm(results, plot_title="A=30down, B=40down, C=50down, nofix", filename="mingtest.png")
