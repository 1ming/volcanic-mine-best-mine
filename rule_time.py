from rules import Rule
from consts import RUN_TIME
# Rule to fix a vent within a certain time window
class Rule_Time(Rule):
    def __init__(self, name, vent, start_time, end_time, only_falling_stability):
        super(Rule_Time, self).__init__(name)
        # Minimum/maximum times for the rule to take effect
        self.start_time = start_time
        self.end_time = end_time
        
        # Should this rule be done only if stability is falling?
        self.only_falling_stability = only_falling_stability
        
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
        if data["time"] > self.end_time or data["time"] < self.start_time:
            return False
        # Rule still being followed, check if stability is falling if we care.
        if self.only_falling_stability and data["stability_change"] >= 0:
            return False
        # Only fix if it needs fixing.
        return not data["vents"][self.vent].check_correct_dir()
        
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
        return_val[self.name + " -> start running"] = self.start_timestamps
        return_val[self.name + " -> fixed vent"] = self.end_timestamps
        return return_val
        