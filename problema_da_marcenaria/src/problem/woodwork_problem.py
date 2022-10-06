import numpy as np
from template.problema_da_marcenaria.src.problem.problem_interface import ProblemInterface
import random
import matplotlib.pyplot as plt


class WoodworkProblem(ProblemInterface):

    def __init__(self, fname):
        # load dataset
        self.filename = fname
        with open(fname, "r") as f:
            lines = f.readlines()

        lines = [l.rstrip().rsplit() for l in lines]

        # Convert the list of list into a numpy matrix of integers.
        lines = np.array(lines).astype(np.int)
        self.x = lines[:, :-1]
        self.y = lines[:, -1:]
        pass

    def initial_population(self, population_size):

        # Represents the quantity to be produced of each type of part
        lista = [1, 1, 1, 1, 2, 2, 3, 4]
        population = []
        for k in range(0, population_size):
            population.append(random.sample(lista, len(lista)))

        return population

    def fitness(self, population):

        # Stores the fitness value of each individual in the population
        fitn = []

        # dim1 and dim2 represent the dimensions of the wooden sheet that is in the warehouse
        dim1, dim2 = 15, 13
        for k in range(0, len(population)):
            chapa_madeira = np.zeros((dim1, dim2), dtype=int)
            out = False
            placas = []
            for und in range(len(population[k])):
                first_stuck = population[k][und]
                x, y = int(self.x[(first_stuck-1)]), int(self.y[(first_stuck-1)])
                free_area = 0

                """ It goes through the two dimensions checking if there are any zeros
                    available in the row needed to allocate the wooden board with the specified
                    dimensions. According to the order of the individual in the population."""
                for z in range(dim1):
                    for w in range(dim2):
                        zero_n = np.count_nonzero(chapa_madeira[z, w:w+y] == 0)

                        '''As soon as you find a line that could possibly allocate the part,
                         the column dimension is analyzed'''
                        if zero_n == y:
                            free_area = free_area + zero_n
                            for h in range(z+1, dim1):
                                zero_n = np.count_nonzero(chapa_madeira[h, w:w + y] == 0)
                                if zero_n == y:
                                    free_area = free_area + zero_n
                                else:
                                    free_area = 0
                                    break

                                ''' Checks if there is free area on the wooden sheet to be able
                                    to produce the part with the specified dimensions'''
                                if free_area == (x * y):
                                    og_x = z
                                    og_y = w
                                    placas.append(first_stuck)

                                    ''' It fills in the matrix, in order to allow visualization
                                        of the cuts and allocation of the pieces'''
                                    for line in range(x):
                                        for column in range(y):
                                            chapa_madeira[line + og_x, og_y:(og_y + column + 1)] = first_stuck
                                    out = True
                                    break

                                # Upon reaching an edge point, exit all loops
                                elif h == (dim1 - 1):
                                    free_area = 0
                                    break
                            if out is True:
                                break
                    if out is True:
                        out = False
                        break

            '''Calculation of the objective function, information obtained
               according to the problem analyzed.'''
            objective_function = sum([placas.count(1) * 100, placas.count(2) * 350,
                                       placas.count(3) * 200, placas.count(4) * 400])
            fitn.append(int(objective_function))

        best_fit = max(fitn)
        best_pos = fitn.index(best_fit)
        path = population[best_pos]

        return best_fit, best_pos, path, fitn

    def elitism(self, newpopulation, bestindividualold, fitn):

        """ Find the worst individual of the current generation
         and replace it with the best individual of the previous generation """
        bigger_fitn = max(fitn)
        pos = fitn.index(bigger_fitn)
        newpopulation[pos] = bestindividualold
        return newpopulation

    def mutation(self, individual, mutation_rate):
        # Function not used in this case!

        lista = []
        prob = np.random.random_sample()
        if prob < mutation_rate:

            # print("Individual before the mutation: ")
            # print("    ", individual)

            for i in range(0, len(individual)):
                lista.append(i)

            # Randomly select two positions
            rand_pos1, rand_pos2 = random.sample(lista, 2)

            # Swap the position of two cities
            aux = individual[rand_pos1]
            individual[rand_pos1] = individual[rand_pos2]
            individual[rand_pos2] = aux

            # print("Individual after the mutation: ")
            # print("    ",individual)
        return individual

    def crossover(self, p1, p2):
        # print("pai1  ", p1)
        # print("pai2  ", p2, "\n")

        son1 = [0] * len(p1)
        son2 = [0] * len(p1)

        # Randomly choose two points to slice a solution
        lista = []
        for i in range(0, len(p1)):
            lista.append(i)
        corte1, corte2 = random.sample(lista, 2)

        if corte1 > corte2:
            start_point = corte2
            end_point = corte1
        else:
            start_point = corte1
            end_point = corte2

        # Return 1 son per function, then it's only necessary to flip p1 and p2
        # to generate the second son
        #print("Pai1:", p1, '- pai2:', p2)
        son1 = self.subcrossover(start_point, end_point, p1, p2, son1)
        son2 = self.subcrossover(start_point, end_point, p2, p1, son2)
        #print("Son1:", son1, '- Son2:', son2)
        return son1, son2

    def subcrossover(self, start_point, end_point, p1, p2, son1):

        # Write the gene of pai2 in the son1
        for i in range(start_point, end_point):
            son1[i] = p2[i]

        #  Part 1 - Write the gene of pai1 in the son1
        j = end_point
        end_list = len(p1)
        for i in range(end_point, end_list):

            if son1.count(p1[i]) < p1.count(p1[i]):
                son1[j] = p1[i]
                #print(son1)
                j = j + 1

            if j == len(p1):
                j = 0
        # Part 2 - Write the gene of pai1 in the son1
        for i in range(0, end_list):

            if son1.count(p1[i]) < p1.count(p1[i]):
                son1[j] = p1[i]
                #print(son1)
                j = j + 1

            if j == start_point:
                break
            elif j == len(p1):
                j = 0
        return son1

    def selection_process(self, fitn):

        lista = []
        for i in range(0, len(fitn)):
            lista.append(i)

        """ Randomly chooses two individuals to compete and
            the one with the HIGHEST fitness value wins, becoming parent 1"""
        i1, i2 = random.sample(lista, 2)

        # Selection process - It want to max
        if fitn[i1] < fitn[i2]:
            pai1 = i2
        elif fitn[i1] > fitn[i2]:
            pai1 = i1

        # In case of tie
        else:
            pai1 = i1  # depois colocar uma escolha aleatória caso algo de errado

        """ Randomly chooses two individuals to compete and
                    the one with the HIGHEST fitness value wins, becoming parent 2"""
        i3, i4 = random.sample(lista, 2)
        if fitn[i3] < fitn[i4]:
            pai2 = i2
        elif fitn[i1] > fitn[i4]:
            pai2 = i3
        else:
            pai2 = i3
        return pai1, pai2

    def plot(self, best_fitness, ngeracoes):

        best_f, generation = best_fitness, ngeracoes
        ngeracoes = np.asarray(ngeracoes)
        xi = ngeracoes

        y0 = np.asarray(best_f[0])
        y1 = np.asarray(best_f[1])
        y2 = np.asarray(best_f[2])
        y3 = np.asarray(best_f[3])
        y4 = np.asarray(best_f[4])

        media = (y0 + y1 + y2 + y3 + y4)/5

        fig, ax = plt.subplots()
        # ax.plot(xi, yi)
        ax.plot(xi, y0, 'b-',
                xi, y1, 'b-',
                xi, y2, 'b-',
                xi, y3, 'b-',
                xi, y4, 'b-',
                xi, media, 'r-',
                )
        ax.set(xlabel='Generations', ylabel='Fitness',
               title='Woodwork problem - 4 pieces')
        # ax.grid()
        plt.savefig("Image/marcenaria_fitness")
        plt.clf()
        pass

    def plot_bestfit(self, best_individual, rnd):
        xp, yp = [], []
        best_i = best_individual
        # Insere um zero na primeira e última posição da lista
        # não interessante no caso do problema de corte-bidimensional
        #best_i.insert(0, 0)
        #best_i.insert(len(best_i), 0)
        for k in range(0, len(best_i)):
            indice = best_i[k]
            xp.append(float(self.x[indice]))
            yp.append(float(self.y[indice]))

        x = np.asarray(xp)
        y = np.asarray(yp)

        plt.title("Otimização na Marcenaria")
        plt.xlabel('x')
        plt.ylabel('y')
        plt.plot(x, y, marker="o", markerfacecolor="r")

        name = str(rnd) + "_marcenaria"
        plt.savefig("Image/" + name)
        plt.clf()
        pass
