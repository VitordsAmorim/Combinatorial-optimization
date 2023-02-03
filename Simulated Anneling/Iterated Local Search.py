import csv
import random
import matplotlib.pyplot as plt
import os
import numpy as np
import math



def reading_file(path, file_name):
    """
    Reading a good initial solution, generated from a constructive greedy heuristic.
    """
    with open(path + file_name) as csvfile:
        data = [(float(x), float(y)) for x, y in csv.reader(csvfile, delimiter=',')]
    return data


def plot_fit_evolution(xp, yp, filename, fo_v):
    x, y = np.asarray(xp), np.asarray(yp)
    sentence = "Best solution: "
    plt.title(sentence + str(fo_v))
    plt.xlabel('Iteration'), plt.ylabel('Objetive Function')
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

    fob = fo(path)
    fob = round(fob, 2)
    sentence = "Fo: "
    plt.title(sentence + str(fob))
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


def local_search(route, max_visited):
    values = 0
    min_fo = fo(route)
    best_route = route.copy()
    while values < max_visited:
        first_position  = random.randint(1, len(route) - 2)
        second_position = random.randint(1, len(route) - 2)
        if first_position != second_position:
            new_s = swap_positions(route.copy(), first_position, second_position)
            nf = fo(new_s)
            values = values + 1
            if nf < min_fo:
                min_fo = nf
                best_route = new_s.copy()
                print(round(nf, 2), "   iteracao: ", values)
    return best_route


def fo(so):
    dist = 0
    for i in range(0, len(so)-1):
        dist = dist + float(((so[i][0] - so[i + 1][0]) ** 2) + ((so[i][1] - so[i + 1][1]) ** 2)) ** 0.5
    return dist


def perturbation(route):


    rota = route.copy()
    for k in range(10):
        best_route = 1000000
        for i in range(80000):
            first_position  = random.randint(1, len(rota) - 2)
            second_position = random.randint(1, len(rota) - 2)
            if first_position != second_position:
                new_s = swap_positions(rota.copy(), first_position, second_position)
                nf = fo(new_s)
                if nf < best_route:
                    best_route = nf
                    best_rota = new_s.copy()
        rota = best_rota.copy()
        print('teste ', k, ":", fo(rota))
        # plot_circuit(rota, ("Teste: " + str(k)))
    return rota



def main():

    file_names = ['xqf131_initial_path.csv', 'xqg237_initial_path.csv', 'pma343_initial_path.csv']
    index = 2
    data = reading_file('data/', file_names[index])

    """Initial conditions """
    s0 = data.copy()             # Initial solution, path
    best_path = data.copy()      # Incumbent solution, path
    best_value = fo(s0)          # Best function value
    random.seed(10)

    """Initial parameters """
    tabu_list = np.zeros([len(data), len(data)], dtype=int)
    max_visited   = 5000        # Maximum number of neighborhood solutions visited
    time_limit    = 2000        # Maximum number of iterations
    max_iteration = 10        # Maximum number of iterations

    X, y = [], []
    count, s_number = 0, 0
    plot_circuit(s0, (str(count) + file_names[index]))
    print("Initial Solution: ", round(best_value, 2))


    for i in range(max_iteration):
        new_s = local_search(s0, max_visited)
        s0 = new_s.copy()
        print(fo(s0))
        pert_s = perturbation(s0)

        print(fo(pert_s))
        s0 = pert_s.copy()

        X.append(i), y.append(round(fo(new_s), 3))

    print("Best solution: ", round(fo(new_s), 3))
    plot_fit_evolution(X, y, file_names[index], (round(fo(new_s), 3)))
    plot_circuit(new_s, file_names[index])


if __name__ == "__main__":
    main()