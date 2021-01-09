import neat

import my_client
import server
from snakeoil import Client, clip

PI= 3.14159265359

# Load configuration.
config = neat.Config(neat.DefaultGenome, neat.DefaultReproduction,
                     neat.DefaultSpeciesSet, neat.DefaultStagnation,
                     'config-feedforward')

# Create the population, which is the top-level object for a NEAT run.
population = neat.Population(config)

# Add a stdout reporter to show progress in the terminal.
population.add_reporter(neat.StdOutReporter(False))

with open("winner.txt",'r') as f:
    w = f.read()


def eval_genomes(genomes, config):
    for genome_id, genome in genomes:
        server.Server().start()
        C = Client()
        for step in range(C.maxSteps, 0, -1):
            C.get_servers_input()
            drive(C, genome)
            C.respond_to_server()
        S = C.S.d
        C.shutdown()
        if S['lastLapTime'] == 0:
            genome.fitness = S['distRaced']/S['curLapTime']
        else:
            genome.fitness = (S['distRaced'] + 2050)/(S['curLapTime'] + S['lastLapTime'])




def drive(c, genoma = None):

    S= c.S.d
    R= c.R.d

    # S: {'angle': 0.0467207, 'curLapTime': 2.468, 'damage': 0.0, 'distFromStart': 2047.54, 'distRaced': 14.9774,
    #     'fuel': 94.0, 'gear': 1.0, 'lastLapTime': 0.0,
    #     'opponents': [200.0, 200.0, 200.0, 200.0, 200.0, 200.0, 200.0, 200.0, 200.0, 200.0, 200.0, 200.0, 200.0, 200.0,
    #                   200.0, 200.0, 200.0, 200.0, 200.0, 200.0, 200.0, 200.0, 200.0, 200.0, 200.0, 200.0, 200.0, 200.0,
    #                   4.85916, 200.0, 200.0, 200.0, 200.0, 200.0, 200.0, 10.4405], 'racePos': 1.0, 'rpm': 5792.73,
    #     'speedX': 48.7787, 'speedY': 0.743483, 'speedZ': 0.0274631,
    #     'track': [5.37889, 5.66359, 6.49984, 8.44336, 14.2813, 29.5085, 65.08, 200.0, 100.793, 54.695, 37.7275, 28.963,
    #               23.649, 20.1121, 15.7716, 12.4104, 10.6624, 9.82549, 9.63669], 'trackPos': 0.283664,
    #     'wheelSpinVel': [41.4835, 40.4579, 43.3378, 42.535], 'z': 0.344934, 'focus': [-1.0, -1.0, -1.0, -1.0, -1.0]}

    # R: {'accel': 0.5600000000000006, 'brake': 0, 'clutch': 0, 'gear': 1, 'steer': 0.12010916050557581,
    #     'focus': [-90, -45, 0, 45, 90], 'meta': 0}


    # # Damage Control
    # target_speed-= S['damage'] * .05
    # if target_speed < 25: target_speed= 25
    #
    # # Steer To Corner
    # R['steer']= S['angle']*10 / PI
    # # Steer To Center
    # R['steer']-= S['trackPos']*.10
    # R['steer']= clip(R['steer'],-1,1)

    # # Throttle Control
    # if S['speedX'] < target_speed - (R['steer']*50):
    #     R['accel']+= .01
    # else:
    #     R['accel']-= .01
    # if S['speedX']<10:
    #    R['accel']+= 1/(S['speedX']+.1)

    target_speed = 100

    # Steer To Corner
    R['steer'] = S['angle'] * 10 / PI
    # Steer To Center
    R['steer'] -= S['trackPos'] * .10

    # Throttle Control
    if S['speedX'] < target_speed - (R['steer'] * 50):
        R['accel'] += .01
    else:
        R['accel'] -= .01
    if S['speedX'] < 10:
        R['accel'] += 1 / (S['speedX'] + .1)


    winner_net = neat.nn.FeedForwardNetwork.create(genoma, config)

    improved_frontal = max(S['track'][8], S['track'][9], S['track'][10])
    inputs = [S['angle'], S['speedX'], S['speedY'], S['speedZ'], S['trackPos'], S['track'][0], S['track'][3], S['track'][6], improved_frontal, S['track'][12], S['track'][15], S['track'][18]]


    delta_accel, delta_brake, delta_steer = winner_net.activate(inputs)

    R['accel'] += delta_accel
    R['brake'] += delta_brake
    R['steer'] += delta_steer


    # Traction Control System
    if ((S['wheelSpinVel'][2]+S['wheelSpinVel'][3]) -
       (S['wheelSpinVel'][0]+S['wheelSpinVel'][1]) > 5):
       R['accel']-= .2
    R['accel']= clip(R['accel'],0,1)

    # Automatic Transmission
    R['gear']=1
    if S['speedX']>50:
        R['gear']=2
    if S['speedX']>80:
        R['gear']=3
    if S['speedX']>110:
        R['gear']=4
    if S['speedX']>140:
        R['gear']=5
    if S['speedX']>170:
        R['gear']=6

    #print("R: ", R)

    return


if __name__ == "__main__":

    # Run until a solution is found.
    winner = population.run(eval_genomes,n=2)

    # Display the winning genome.
    print('\nBest genome:\n{!s}'.format(winner))

    # Start the game
    server.Server_gui().start()
    C = Client()


    for step in range(C.maxSteps, 0, -1):
        C.get_servers_input()
        drive(C, winner)
        C.respond_to_server()
    C.shutdown()


    with open("winner.txt", 'w') as f:
        f.write(str(winner))

