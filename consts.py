from collections import namedtuple

# Guesses for the time it takes to fix a vent.
RUN_TIME = {
	"A": 15
}

# Enum for directions.
VentDirection = namedtuple("VentDirection", "up down")(*[1, -1])

# Rough guess on when 3rd rock is reached.
THIRD_ROCK_TIME = 195


DEFAULT_VENT_UPDATE = 2
TOTAL_TIME = 300
TIME_VENT_UPDATE = 6
TIME_STAB_UPDATE = 15
SWEET_SPOT_RANGE = [41, 59]
VALVE_START_RANGE = [30, 70]