import neat

import server
import sys
from my_client import Track, drive, initialize_car, set_T, cambia_config
from snakeoil import Client
import my_checkpointer
from neat.six_util import iteritems, iterkeys, itervalues
import matplotlib.pyplot as plt
import numpy as np
from neat.math_util import mean, stdev
from neat.species import GenomeDistanceCache
import gzip

import pickle
from xml.dom import minidom
import visualize

# media e dev std fitness popolazione all'avanzare delle iterazioni
# fitness del miglior genoma //
# struttura rete del miglior genoma //


config = neat.Config(neat.DefaultGenome, neat.DefaultReproduction,
                     neat.DefaultSpeciesSet, neat.DefaultStagnation,
                     'config-feedforward')
#
# file_name_prefix = "popolazioni\seed8\generazione-"
# generazione = 60
# generation_statistics = []
#
# for i in range(0,13):
#     species_stats = {}
#     pop = None
#     if i <20 :
#         pop = my_checkpointer.MyCheckPointer.restore_checkpoint(file_name_prefix + str(i * 5))
#     else:
#         pop = my_checkpointer.MyCheckPointer.restore_checkpoint(file_name_prefix + str(i * 5)+".gz")
#
#     if pop is None:
#         print("EEEEEEEEEEEE")
#
#     pop.species.speciate(pop.config, pop.population, pop.generation)
#
#     #species_cross_validation_stats = {}
#     for sid, s in iteritems(pop.species.species):
#         species_stats[sid] = dict((k, v.fitness) for k, v in iteritems(s.members))
#
#     generation_statistics.append(species_stats)
#
#
#     # distances = GenomeDistanceCache(config.genome_config)
#     # gdmean = mean(itervalues(distances.distances))
#     # gdstdev = stdev(itervalues(distances.distances))
#     # print("MEDIA: ", gdmean, "VARIANZA: ",gdstdev)
#
# all_species = set()
# for gen_data in generation_statistics:
#     all_species = all_species.union(gen_data.keys())
#
# max_species = max(all_species)
# species_counts = []
# for gen_data2 in generation_statistics:
#     species = [len(gen_data2.get(sid, [])) for sid in range(1, max_species + 1)]
#     species_counts.append(species)
#
#
# species_sizes = species_counts
# num_generations = len(species_sizes)
# curves = np.array(species_sizes).T
#
#
# fig, ax = plt.subplots()
# ax.stackplot([0,5,10,15,20,25,30,35,40,45,50,55,60], *curves)
#
# plt.title("Speciazione")
# plt.ylabel("Dimensione specie")
# plt.xlabel("Generazione")
#
#
# # plt.savefig(filename)
#
# plt.show()
# plt.close()




with gzip.open("migliori_genomi_multi_05addrem\seed1.gz") as f:
    genomi = []
    while True:
        try:
            genoma = pickle.load(f)
            genomi.append(genoma)
        except EOFError:
            break

print(len(genomi))
best = None
for gen in genomi:
    if best is None or best.fitness <= gen.fitness:
        best = gen

print(best)

#visualize.draw_net(config, best, filename="rete_grossa")


#Start the game
cambia_config(filename = "quickrace_Aalborg.xml")
server.Server_gui().start()

set_T(Track())
C = Client(p=3001)

initialize_car(C)
C.S.d['stucktimer']= 0
C.S.d['targetSpeed']= 0

array_danni_subiti = []
array_distanza_percorsa = []
array_velocita = []
array_tempo = []

for step in range(C.maxSteps,0,-1):
    C.get_servers_input()
    drive(C, step, best)
    C.respond_to_server()
    # array_tempo.append(C.maxSteps-step)
    # array_distanza_percorsa.append(C.S.d['distRaced'])
    # array_danni_subiti.append(C.S.d['damage'])
    # array_velocita.append(C.S.d['speedX'])

C.shutdown()

# print(array_tempo)
# print(array_distanza_percorsa)
# print(array_velocita)
# print(array_danni_subiti)




