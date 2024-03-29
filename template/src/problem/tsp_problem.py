import numpy as np
from template.src.problem.problem_interface import ProblemInterface
import random
import matplotlib.pyplot as plt


class TSPProblem(ProblemInterface):

    def __init__(self, fname):
        self.filename = fname  # load dataset
        with open(fname, "r") as f:
            lines = f.readlines()
        lines = [l.rstrip().rsplit() for l in lines]

        """Convert the list of list into a numpy matrix of integers"""
        lines = np.array(lines).astype(np.float32)
        self.x = lines[:, :-1]
        self.y = lines[:, -1:]
        pass

    def initial_population(self, population_size):

        """
        Write the list with the for 1 to the size of the population(the number of cities)
        """
        lista = []
        for i in range(1, len(self.x)):
            lista.append(i)

        population = []  # The initial population
        for j in range(0, population_size):
            population.append(random.sample(lista, len(self.x) - 1))
        return population

    def fitness(self, population):
        fitn = []
        for k in range(0, len(population)):  # Compute the fitness function for the entire population
            ind = 0
            total_distance = 0

            for i in range(0, len(self.x) - 1):   # Compute the fitness function for an individual
                n = population[k][i]
                distance = np.sqrt((self.x[ind] - self.x[n]) ** 2 + (self.y[ind] - self.y[n]) ** 2)
                total_distance = float(total_distance) + float(distance)
                ind = n
            distance = np.sqrt((self.x[ind] - self.x[0]) ** 2 + (self.y[ind] - self.y[0]) ** 2)
            total_distance = total_distance + float(distance)
            fitn.append(float(total_distance))
        best_fit = min(fitn)
        best_pos = fitn.index(best_fit)
        path = population[best_pos]
        return best_fit, best_pos, path, fitn

    def elitism(self, newpopulation, bestindividualold, fitn):
        """
        Finds the worst individual of the current generation and replaces it with the best individual of the previous.

        :param newpopulation:
        :param bestindividualold:
        :param fitn:
        :return:
        """
        bigger_fitness = max(fitn)
        pos = fitn.index(bigger_fitness)
        newpopulation[pos] = bestindividualold
        return newpopulation

    def mutation(self, individual, mutation_rate):
        lista = []
        prob = np.random.random_sample()
        if prob < mutation_rate:

            # print("Individual before the mutation: ")
            # print("    ", individual)

            for i in range(0, len(individual)):
                lista.append(i)

            rand_pos1, rand_pos2 = random.sample(lista, 2)  # Randomly select two positions
            aux = individual[rand_pos1]  # Swap the position of two cities
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
        for i in range(1, len(p1)):
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
        son1 = self.subcrossover(start_point, end_point, p1, p2, son1)
        # print("filho ",son1)
        son2 = self.subcrossover(start_point, end_point, p2, p1, son2)
        # print("filho ",son2)
        return son1, son2

    def subcrossover(self, start_point, end_point, p1, p2, son1):

        # Write the gene of pai2 in the son1
        for i in range(start_point, end_point):
            son1[i] = p2[i]

        # Write the gene of pai1 in the son1 - Part 1
        j = end_point
        end_list = len(p1)
        for i in range(end_point, end_list):

            if p1[i] not in son1:
                son1[j] = p1[i]
                j = j + 1

            if j == len(p1):
                j = 0

        # Write the gene of pai1 in the son1 - Part 2
        for i in range(0, end_list):
            if p1[i] not in son1:
                son1[j] = p1[i]
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
        """
        Randomly choose two individuals to compete,
        and the one with the lowest fitness value wins,
        becoming parent 1.
        """
        i1, i2 = random.sample(lista, 2)
        if fitn[i1] > fitn[i2]:  # Selection process - It want to minimize
            pai1 = i2
        elif fitn[i1] < fitn[i2]:
            pai1 = i1
        else:
            pai1 = i1  # Then put a random choice in case something goes wrong

        """
        It randomly chooses two other individuals to compete,
         and the one with the lowest fitness value wins,
         becoming parent 2.
        """
        i1, i2 = random.sample(lista, 2)
        if fitn[i1] > fitn[i2]:
            pai2 = i2
        elif fitn[i1] < fitn[i2]:
            pai2 = i1
        else:
            pai2 = i1
        return pai1, pai2

    def plot(self, best_fitness, ngeracoes):

        best_f, generation = best_fitness, ngeracoes
        ngeracoes = np.asarray(ngeracoes)
        xi = ngeracoes

        y0 = np.asarray(best_f[0])
        y1 = np.asarray(best_f[1])
        y2 = np.asarray(best_f[2])
        #y3 = np.asarray(best_f[3])
        #y4 = np.asarray(best_f[4])
        media = (y0 + y1 + y2)/3
        fig, ax = plt.subplots()
        # ax.plot(xi, yi)
        ax.plot(xi, y0, 'b-',
                xi, y1, 'b-',
                xi, y2, 'b-',
                xi, media, 'r-',
                )
        ax.set(xlabel='gerações', ylabel='fitness',
               title='Problema do caixeiro-viajante')
        ax.grid()

        plt.savefig("Image/tsp_fitness")
        plt.clf()
        pass

    def plot_bestfit(self, best_individual, rnd):
        xp, yp = [], []
        best_i = best_individual
        best_i.insert(0, 0)
        best_i.insert(len(best_i), 0)
        for k in range(0, len(best_i)):
            indice = best_i[k]
            xp.append(float(self.x[indice]))
            yp.append(float(self.y[indice]))

        x = np.asarray(xp)
        y = np.asarray(yp)

        plt.title("Problema do caixeiro-viajante")
        plt.xlabel('x')
        plt.ylabel('y')
        plt.plot(x, y, marker="o", markerfacecolor="r")

        name = str(rnd) + "_tsp"
        plt.savefig("Image/" + name)
        plt.clf()
        pass