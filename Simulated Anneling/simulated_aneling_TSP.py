import csv
import math
import random
import matplotlib.pyplot as plt
import os
import numpy as np


def plot_fit_evolution(xp, yp, filename, fo):
    x, y = np.asarray(xp), np.asarray(yp)
    sentence = "Last fo:"
    plt.title(sentence + str(fo))
    plt.xlabel('State Evaluation'), plt.ylabel('Objetive Function')
    plt.plot(x, y, 'k', color='tab:blue')
    name = filename[0:filename.find('.')]  # regular expression usage
    name = str(name) + "_" + sentence + "_tsp"
    try:
        plt.savefig("Image/" + name)
    except FileNotFoundError:
        os.mkdir('Image')
        plt.savefig("Image/" + name)
    plt.close()
    plt.clf()
    pass


def plot_circuit(path, filename):
    xp, yp = [], []
    best_i = path
    for k in range(0, len(best_i)):
        x_aux, y_aux = (best_i[k])
        xp.append(x_aux), yp.append(y_aux)
    x, y = np.asarray(xp), np.asarray(yp)

    fo = potential_energy(path)
    fo = round(fo, 2)
    sentence = "Fo: "
    plt.title(sentence + str(fo))
    plt.xlabel('x'), plt.ylabel('y')
    plt.plot(x, y, 'k', color='tab:blue')
    name = str(filename[0:filename.find('.')]) + "_" + sentence + "_tsp"
    try:
        plt.savefig("Image/route/" + name)
    except FileNotFoundError:
        os.mkdir('Image')
        os.mkdir('Image/route')
        plt.savefig("Image/route/" + name)
    plt.close()
    plt.clf()
    pass


def swap_positions(path, pos1, pos2):
    path[pos1], path[pos2] = path[pos2], path[pos1]
    return path


def random_neighbor(route):
    first_position  = random.randint(0, len(route) - 1)
    second_position = random.randint(0, len(route) - 1)
    new_s = swap_positions(route, first_position, second_position)
    return new_s


def perturbation(route):
    first_position  = random.randint(0, len(route)-1)
    cover = 30
    upper_limit = first_position + cover
    if upper_limit >= len(route):
        cover = len(route) - first_position - 1
        upper_limit = first_position + cover
    second_position = random.randint(first_position, upper_limit)
    new_s = swap_positions(route, first_position, second_position)
    return new_s


def potential_energy(so):
    dist = 0
    for i in range(0, len(so)-1):
        dist = dist + float(((so[i][0] - so[i + 1][0]) ** 2) + ((so[i][1] - so[i + 1][1]) ** 2)) ** 0.5
    return dist


def main():

    """
    Reading a good initial solution, generated from a constructive greedy heuristic.
    """
    path = 'data/'
    file_names = ['xqf131_initial_path.csv', 'xqg237_initial_path.csv', 'pma343_initial_path.csv']
    index = 2
    with open(path + file_names[index]) as csvfile:
        data = [(float(x), float(y)) for x, y in csv.reader(csvfile, delimiter=',')]

    """Initial conditions """
    s0 = data.copy()             # Initial solution, path
    best_path = data             # Best solution, path
    best = potential_energy(s0)  # Best activation function value
    print("Initial Solution: ", round(best, 2))

    """
    Initial parameters
    """
    temperature      = 10000     # Initial temperature
    alpha            = 0.80      # Temperature reduction factor. Alpha < 1, usually, 0.8 < alpha < 0.99
    max_iteration    = 120000     # Maximum number of iterations
    max_perturbation = 50000      # Maximum number of perturbation per iterations
    success_number   = 1000       # Maximum number of successes per iteration
    # beta        = 0.0001      # Temperature reduction factor

    X, y = [], []
    count, s_number = 0, 0
    random.seed(10)
    plot_circuit(s0, (str(count) + file_names[index]))
    while temperature > 1 and (max_iteration > count):
        for j in range(max_perturbation):
            s = perturbation(s0.copy())  # Select a random solution, neighbor of the initial
            # s = random_neighbor(s0.copy())

            delta = potential_energy(s) - potential_energy(s0)
            if (delta < 20) and ((delta < 0) or (random.uniform(0, 1) < math.exp(-delta/temperature))):
                s0 = s.copy()
                aux2 = potential_energy(s)
                X.append(count), y.append(round(aux2, 2))  # Stores the performance of the activation function
                #plot_circuit(s0, (str(count) + file_names[index]))
                """
                As you always want to remember/save the best solution found so far.
                Saves the best solutions found.
                """
                if best > aux2:
                    best, best_path = aux2, s0  # Potential energy, and best solution
                    print("Best solution update: ", round(best, 3))

                if s_number == success_number:
                    s_number = 0
                    break
                s_number = s_number + 1
            count += 1  # Helps to plot the solution
        temperature = alpha * temperature
        # t = t/(1 + beta * t)

    plot_fit_evolution(X, y, file_names[index], round(aux2, 2))
    plot_circuit(s0, (str(count) + file_names[index]))

    print("Best solution found was: ", round(best, 2))
    print("Last solution found was: ", round(aux2, 2))


if __name__ == "__main__":
    main()

