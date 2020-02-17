from rules import Rule
from consts import RUN_TIME
# Rule to fix a vent when its value is a certain distance away from 50
class Rule_Distance(Rule):
    def __init__(self, name, vent, threshold, start_time):
        super(Rule_Distance, self).__init__(name)
        # Minimum time for the rule to take effect
        # Mostly needed so that the rule isn't triggered before the initial fix is done.
        self.start_time = start_time
        
        self.threshold = threshold
        
        self.start_timestamps = []
        self.end_timestamps = []
        self.vent = vent
        # When action was started.
        self.start_doing = 0
    
    def check_condition(self, data):
        # Are we currently running to a vent?
        if self.start_doing > 0:
            # Check if we've finally reached the vent.
            return data["time"] >= self.start_doing + RUN_TIME[self.vent]
        # Not running to a vent, check if the time is within bounds.
        if data["time"] < self.start_time:
            return False
        # Check if the vent is far enough from 50.
        vent = data["vents"][self.vent]
        return abs(vent.val - 50) > self.threshold
        
    def do_action(self, data):
        # If we aren't running to the vent, start running
        if self.start_doing <= 0:
            self.start_doing = data["time"] + RUN_TIME[self.vent]
            self.start_timestamps.append(data["time"])
        # We made it to the vent, fix it.
        else:
            self.start_doing = 0
            data["vents"][self.vent].fix()
            self.end_timestamps.append(data["time"])
            
    def dump(self):
        return_val = {};
        return_val[self.name + "_start"] = self.start_timestamps
        return_val[self.name + "_end"] = self.end_timestamps
        return return_val
        