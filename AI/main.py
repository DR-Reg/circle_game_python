import neat
from neat.nn import FeedForwardNetwork as FFN


#TODO: adapt to codebase FROM NEAT-PYTHON DOCS
def run(config_file, generations):
    config = neat.Config(neat.DefaultGenome, neat.DefaultReproduction,
                         neat.DefaultSpeciesSet, neat.DefaultStagnation,
                         config_file)
    p = neat.Population(config)

    # p.add_reporter(neat.StdOutReporter(True))
    # stats = neat.StatisticsReporter()
    # p.add_reporter(stats)
    # p.add_reporter(neat.Checkpointer(5))

    winner = p.run(eval_genomes, generations)
    print('\nBest genome:\n{!s}'.format(winner))

    # run winner against some training data
    print('\nOutput:')
    winner_net = FFN.create(winner, config)
    # TODO: run winner against training data/human using winner_net.activate
    # NOTE: may want to create a derived class from Agent called HumanAgent
    # which when called "make_move" runs a game loop in pygame and waits for the
    # human to make a move


    # node_names = {-1: 'A', -2: 'B', 0: 'A XOR B'}
    # visualize.draw_net(config, winner, True, node_names=node_names)
    # visualize.draw_net(config, winner, True, node_names=node_names, prune_unused=True)
    # visualize.plot_stats(stats, ylog=False, view=True)
    # visualize.plot_species(stats, view=True)

    # p = neat.Checkpointer.restore_checkpoint('neat-checkpoint-4')
    # p.run(eval_genomes, 10)


if __name__ == '__main__':
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, 'neat.cfg')
    run(config_path)
