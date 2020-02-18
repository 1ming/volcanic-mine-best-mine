from consts import VentDirection, DEFAULT_VENT_UPDATE, SWEET_SPOT_RANGE

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
            self.direction = VentDirection.up
        elif self.val > 50:
            self.direction = VentDirection.down

    def check_in_ss(self):
        return (SWEET_SPOT_RANGE[0] <= self.val <= SWEET_SPOT_RANGE[1])
        
    # Check if the direction needs fixing.
    def check_correct_dir(self):
        if self.val >= 50:
            return self.direction == VentDirection.down
        return self.direction == VentDirection.up
            