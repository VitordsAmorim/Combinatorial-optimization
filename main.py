import csv
from template.src.problem.tsp_problem import TSPProblem
from template.src.algorithm.genetic_algorithm import genetic_algorithm
import time
import numpy as np


def generate_report(output, problem, n_generations, best_fitness, deltat, typeproblem, rodadas):

    problem.plot(output, n_generations)
    menorfit = min(best_fitness)
    maiorfit = max(best_fitness)
    media = sum(best_fitness)
    media = media/rodadas
    delta_time = deltat/rodadas

    dp = 0.0
    for k in range(0, rodadas):
        dp = dp + (best_fitness[k] - media)**2
    dp = dp/rodadas
    dp = np.sqrt(dp)

    f = open('Output.csv', 'a', newline='', encoding='utf-8')
    w = csv.writer(f)
    w.writerow([typeproblem, menorfit, maiorfit, media, dp, delta_time])
    f.close()
    pass


def build_problem(problem_name):
    if problem_name == "tsp":
        return TSPProblem("template/data/tsp/pma343_initial_path.txt")  # xqg237_initial_path.txt   xqf131.txt
    else:
        raise NotImplementedError()


def main():

    f = open('Output.csv', 'w', newline='', encoding='utf-8')
    w = csv.writer(f)
    w.writerow(['Tipo do Problema', ' Menor fitness', ' Maior fitness', ' Media', ' Desvio padrao', 'Intervalo de tempo'])
    f.close()

    """ Hyperparameters for the TSP"""
    typeproblem = ["tsp"]
    population_s = [5000]
    ngeracoes = [4000]
    rodadas = 3

    """"
    The way it is implemented, it is possible to use this same heuristic, Genetic Algorithm, for other problems.
    """
    for t in range(0, 1):
        problem = build_problem(typeproblem[t])
        graph, best_fitness = [], []
        t_initial = time.time()
        """
        Run the algorithm 3 times to compare the results of each of the rounds.
        """
        for i in range(0, rodadas):
            output, n = genetic_algorithm(
                problem,
                population_size=population_s[t],
                n_generations=ngeracoes[t],
                round=i,
                mutation_rate=0.1)
            graph.append(output)
            best_fitness.append(output[ngeracoes[t] - 1])
        t_final = time.time()
        deltat = t_final - t_initial
        generate_report(graph, problem, n, best_fitness, deltat, typeproblem[t], rodadas)
    print("END")


if __name__ == "__main__":
    main()
