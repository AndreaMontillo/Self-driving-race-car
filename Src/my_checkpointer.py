
import neat
import gzip
import pickle
import random
from neat.six_util import itervalues, iterkeys
from neat.population import Population
from neat.math_util import mean, stdev


class MyCheckPointer(neat.Checkpointer, neat.StdOutReporter):

    seed = 0
    show_species_detail = True

    def post_evaluate(self, config, population, species, best_genome):
        # pylint: disable=no-self-use
        fitnesses = [c.fitness for c in itervalues(population)]
        fit_mean = mean(fitnesses)
        fit_std = stdev(fitnesses)
        best_species_id = species.get_species_id(best_genome.key)
        best = None
        with open("risultati\seed" +str(self.seed)+ ".csv", 'a') as f:
            for key in population:
                if best is None:
                    best = population[key]

                if population[key].fitness > best.fitness:
                    best = population[key]

            f.write(str(fit_mean) + "," + str(fit_std) + "," + str(best.fitness))
            f.write("\n")

        with gzip.open("migliori_genomi\seed" + str(self.seed), 'a', compresslevel=5) as f:
            pickle.dump(best, f, protocol=pickle.HIGHEST_PROTOCOL)
            #pickle.dump("\n;\n", f, protocol=pickle.HIGHEST_PROTOCOL)

        print('Population\'s average fitness: {0:3.5f} stdev: {1:3.5f}'.format(fit_mean, fit_std))
        print(
            'Best fitness: {0:3.5f} - size: {1!r} - species {2} - id {3}'.format(best_genome.fitness,
                                                                                 best_genome.size(),
                                                                                 best_species_id,
                                                                                 best_genome.key))


    def save_checkpoint(self, config, population, species_set, generation):
        """ Save the current simulation state. """
        if generation % 5 == 0:
            filename = '{0}{1}'.format(self.filename_prefix,generation)
            print("Saving checkpoint to {0}".format(filename))

            with gzip.open(filename, 'w', compresslevel=5) as f:
                data = (generation, config, population, species_set, random.getstate())
                pickle.dump(data, f, protocol=pickle.HIGHEST_PROTOCOL)


    def restore_checkpoint(filename):
        """Resumes the simulation from a previous saved point."""
        with gzip.open(filename) as f:
            generation, config, population, species_set, rndstate = pickle.load(f)
            random.setstate(rndstate)
            return Population(config, (population, species_set, generation))
