import csv
import random
import matplotlib.pyplot as plt
import os
import numpy as np


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


def neighboring_solutions(route, max_visited):
    swap_list = []
    values = []
    while len(values) < max_visited:
        first_position  = random.randint(0, len(route) - 1)
        second_position = random.randint(0, len(route) - 1)
        if first_position != second_position:
            new_s = swap_positions(route.copy(), first_position, second_position)
            swap_list.append((first_position, second_position))
            values.append(round(fo(new_s), 3))
    return swap_list, values


def fo(so):
    dist = 0
    for i in range(0, len(so)-1):
        dist = dist + float(((so[i][0] - so[i + 1][0]) ** 2) + ((so[i][1] - so[i + 1][1]) ** 2)) ** 0.5
    return dist

def check_tabu_list(movement, tabu, max_tabu):
    i, j = movement

    """Updates the tabu list according to the number of iterations"""
    dim = len(tabu)
    for row in range(dim):
        for column in range(dim):
            if tabu[row, column] != 0:
                tabu[row, column] = tabu[row, column] - 1

    if tabu[i, j] == 0:
        tabu[i, j] = max_tabu
        tabu[j, i] = max_tabu
        return True
    else:
        return False


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
    max_tabu      = 100          # Maximum number of forbidden iterations
    max_visited   = 5000         # Maximum number of neighborhood solutions visited
    time_limit    = 2000         # Maximum number of iterations
    max_iteration = 1000         # Maximum number of iterations

    X, y = [], []
    count, s_number = 0, 0
    plot_circuit(s0, (str(count) + file_names[index]))
    print("Initial Solution: ", round(best_value, 2))


    for i in range(max_iteration):
        swap_list, fo_list = neighboring_solutions(s0, max_visited)
        sorted_list = np.sort(fo_list)[:5]
        for k in sorted_list:
            swap_index = fo_list.index(k)
            permission = check_tabu_list(swap_list[swap_index], tabu_list, max_tabu)

            """If the value is not in the tabu list, the exchange takes place"""
            if permission is True:
                pos1, pos2 = swap_list[swap_index]
                s0 = swap_positions(s0, pos1, pos2)
                if fo(s0) < fo(best_path):
                    best_path = s0.copy()  # Update the incumbent solution
                break
            else:
                """Aspiration criteria"""
                if fo(s0) < fo(best_path):
                    best_path = s0.copy()  # Update the incumbent solution
        # print("Incumbent solution: ", round(fo(s0), 3))
        X.append(i), y.append(round(fo(s0), 3))

    print("Best solution: ", round(fo(best_path), 3))
    plot_fit_evolution(X, y, file_names[index], (round(fo(best_path), 3)))
    plot_circuit(best_path, file_names[index])


if __name__ == "__main__":
    main()
