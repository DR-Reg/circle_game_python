import neat
from neat.nn import FeedForwardNetwork as FFN
import sys
from Vector import V2
import random

class Agent:
    def __init__(self, net):
        self.net = net

    def make_move(self, game):
        # TODO:  decide what our inputs are
        # NOTE:  remember to update this in config file too
        self.net.activate(inputs)
    
class Random(Agent):
    def __init__(self, pyg, radius, dradius):
        self.pyg = pyg
        self.radius = radius
        self.dradius = dradius
    
    def make_move(self,game):
        game.add_line(random.random(), random.random())
        game.add_line(random.random(), random.random())

class Human(Agent):
    def __init__(self, pyg, radius, dradius):
        self.pyg = pyg
        self.screen = self.pyg.display.get_surface()
        self.width, self.height = self.screen.get_size()
        self.radius = radius
        self.dradius = dradius
        self.center = V2(self.width/2, self.height/2)
    
    # run in loop until human clicks
    def make_move(self, game):
        no_move = True
        while no_move:
            for event in self.pyg.event.get():
                if event.type == self.pyg.QUIT:
                    sys.exit(0)

                mousevec = V2(*self.pyg.mouse.get_pos()) - self.center
                end = mousevec.normalise() * self.dradius + self.center
                game.blit(self.screen)
                # cursor line
                self.pyg.draw.line(self.screen, (255,0,0), self.center.tuple, end.tuple)
                self.pyg.draw.circle(self.screen, (255,0,0), end.tuple, 5)

                if event.type == self.pyg.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        no_move = game.add_line(*end.tuple)
            self.pyg.display.flip()
                

def eval_genomes(genomes, config):
    print("Eval genomes has not been implemented completely")
    raise NotImplementedError

    # options:
    # - play all vs all
    # - play a shuffled 1v1, winner fitness = 1, loser = 0
    # - play 3 shuffled matches, avg. fitness
    i = 0
    for gen_id, gen in genomes:
        # define new agent for this genome
        curr_net = FFN.create(gen, config)
        curr_agent = Agent(curr_net)
        # Ex: play against all other genomes
        # we haven't already played against
        for gen_id_2, gen2 in genomes[i:]:
            if gen_id == gen_id_2: continue

            enemy_net = FFN.create(gen2, config)
            enemy_agent = Agent(enemy_net)

            game = CircleGame([curr_net, enemy_net])

            # life span determines number of moves
            # may want to increase this over time
            life_span = 10
            curr_span = 0
            someone_won = False
            while curr_span < life_span:
                ended, who = game.make_move()
                if ended:
                    # TODO: update fitness of both genomes
                    # accordingly
                    someone_won = True
                    break
            if not someone_won:
                # TODO: handle the case where nobody won in the given lifespan
                # assess who has the most points for example
                pass
        i += 1
