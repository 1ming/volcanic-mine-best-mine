# define various rule methods
def very_aggresive_scenario(*args):
    pass

def very_safe(*args):
    pass

def normal(*args):
    pass

class Rule(object):
    def __init__(self, execute_method, *args):
        self.timestamps = []
        self.execute_method = execute_method
        self.execute_method_args = args

    def check(self):
        # call at every tick
        return self.execute_method(*self.execute_method_args)

    def dump(self):
        pass
