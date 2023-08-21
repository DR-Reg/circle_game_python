class CircleGame:
    def __init__(self, agents):
        self.agents = agents
        # index keeping the index of the next agent's move
        self.move = 0
        self.points = [0,0]
    def make_move(self):
        self.agents[self.move].make_move(self)
        self.add_points()
        if self.check_win():
            return True, self.move
        self.move = not self.move
        return False, self.move

    def add_points(self):
        raise NotImplemented
    def check_win(self):
        raise NotImplemented 
