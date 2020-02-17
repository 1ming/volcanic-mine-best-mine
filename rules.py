# define various rule methods
def very_aggresive_scenario(*args):
    pass

def very_safe(*args):
    pass

def normal(*args):
    pass

class Rule(object):
    def __init__(self, name):
        self.name = name

	# A condition that the rule checks to determine whether to do an action.
    def check_condition(self, data):
        pass

	# Function to dump info on when action was done for the outupt graph.
    def dump(self):
        pass
		
	# Function to perform an action (like fix a vent)
	def do_action(self):
		pass
