from rules import Rule
from consts import RUN_TIME
# Rule to fix a vent at the start of the game
class Rule_Start(Rule):
    def __init__(self, name, vent, time):
        super(Rule_Start, self).__init__(name)
        # Approximately what time this is done by.
        self.time = time
        self.vent = vent
    
    def check_condition(self, data):
        return self.time == data["time"]
        
    def do_action(self, data):
        data["vents"][self.vent].fix()
            
    def dump(self):
        return_val = {};
        return_val[self.name] = self.time
        return return_val
        