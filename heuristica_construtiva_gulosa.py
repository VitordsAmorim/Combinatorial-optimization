import numpy as np
import random
import networkx as nx
import re
import matplotlib.pyplot as plt
import time


def plot_bestfit(best_individual, rnd, k):
    xp, yp = [], []
    best_i = best_individual

    for k in range(0, len(best_i)):
        x_aux, y_aux = (best_i[k])
        xp.append(x_aux)
        yp.append(y_aux)

    x = np.asarray(xp)
    y = np.asarray(yp)

    plt.title("Problema do caixeiro-viajante")
    plt.xlabel('x')
    plt.ylabel('y')
    plt.plot(x, y, marker="o", markerfacecolor="r")

    name = str(k) + "_" + str(rnd) + "_tsp"
    plt.savefig("Image/" + name)
    plt.clf()
    pass

def ler_arquivo(filename):
    # filename =
    instance = open(filename, 'r')
    coord_section = False
    points = {}

    G = nx.Graph()
    for line in instance.readlines():
        if re.match('NODE_COORD_SECTION.*', line):
            coord_section = True
            continue
        elif re.match('EOF.*', line):
            break
        if coord_section:
            coord = line.split(' ')
            index = int(coord[0])
            cx = float(coord[1])
            cy = float(coord[2])
            points[index] = (cx, cy)
            G.add_node(index, pos=(cx, cy))
    instance.close()
    return points


def main(r, seed, filename):

    points = ler_arquivo(filename)
    random.seed(seed)
    initial_point = random.randint(1, len(points))

    order_tsp = []
    x, y = points[initial_point]
    order_tsp.append(points[initial_point])
    points.pop(initial_point)

    menor_delta = 1000000
    custo_fo = 0
    while len(points) > 1:
        for i in points:
            x1, y1 = points[i]
            delta = np.sqrt((x1 - x)**2 + (y1 - y)**2)
            if delta < menor_delta:
                menor_delta = delta
                pos = i
        x, y = points[pos]
        custo_fo = custo_fo + menor_delta
        order_tsp.append(points[pos])
        points.pop(pos)
        menor_delta = 1000000
    plot_bestfit(order_tsp, r, filename)
    return custo_fo


if __name__ == "__main__":
    file_names = ['pbl395.tsp', 'uy734.tsp']
    for k in file_names:
        t_inicial = time.time()
        seed = [10, 20, 30, 40, 50, 60, 70, 80, 90, 100]
        best_solution = []
        for r in range(len(seed)):
            best = main(r, seed[r], k)
            best_solution.append(round(float(best), 2))
        print("Melhor valor obtido em cada uma das 10 rodadas: ", best_solution)
        print("Menor valor obtido entre todas as 10 rodadas: ", min(best_solution))
        t_final = time.time()
        deltat = t_final - t_inicial
        print("Intervalor de tempo para executar o algoritmo: ", round(deltat, 3), '\n')

        xp, yp = [2.385, 5.374], [395, 734]
        x, y = np.asarray(xp), np.asarray(yp)


        plt.title("Tempo de processamento x dimensão")
        plt.xlabel('t(s)'), plt.ylabel('dimensão')
        plt.plot(x, y, marker="o", markerfacecolor="r")
        name = "tempo_dimensão_tsp"
        plt.savefig("Image/" + name)
        plt.clf()






