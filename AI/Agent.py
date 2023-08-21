import neat
from neat.nn import FeedForwardNetwork as FFN

class Agent:
    def __init__(self, net):
        self.net = net

    def make_move(self, game):
        # TODO:  decide what our inputs are
        # NOTE:  remember to update this in config file too
        self.net.activate(inputs)


def eval_genomes(genomes, config):
    print("Eval genomes has not been implemented completely")
    raise NotImplemented

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
