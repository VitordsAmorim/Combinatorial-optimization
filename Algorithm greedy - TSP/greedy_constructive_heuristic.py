import numpy as np
import random
import re
import matplotlib.pyplot as plt
import time
import os


def plot_bestfit(best_individual, rnd, filename):
    xp, yp = [], []
    best_i = best_individual

    for k in range(0, len(best_i)):
        x_aux, y_aux = (best_i[k])
        xp.append(x_aux)
        yp.append(y_aux)

    x = np.asarray(xp)
    y = np.asarray(yp)

    plt.title("Problema do caixeiro-viajante")
    plt.xlabel('x'), plt.ylabel('y')
    plt.plot(x, y, marker="o", markerfacecolor="r")

    # regular expression usage
    fname = filename[0:filename.find('.')]
    name = str(fname) + "-" + str(rnd) + "_tsp"
    try:
        plt.savefig("Image/" + name)
    except FileNotFoundError:
        os.mkdir('Image')
        plt.savefig("Image/" + name)
    plt.clf()
    pass


def ler_arquivo(filename):
    instance = open(filename, 'r')
    coord_section = False
    points = {}
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
    instance.close()
    return points


def problem(r, seed, filename):
    points = ler_arquivo(filename)
    random.seed(seed)
    initial_point = random.randint(1, len(points))

    order_tsp = []
    x, y = points[initial_point]
    order_tsp.append(points[initial_point])
    points.pop(initial_point)

    menor_delta = 1000000
    pos = 0

    # só atende aos 3 primeiros valores,
    # para gerar o primeiro circuito
    limit = len(points)-2
    while len(points) > limit:
        for i in points:
            x1, y1 = points[i]
            d = np.sqrt((x1 - x) ** 2 + (y1 - y) ** 2)
            if d < menor_delta:
                menor_delta = d
                pos = i
        x, y = points[pos]
        order_tsp.append(points[pos])
        points.pop(pos)
        menor_delta = 1000000

    initial_circuit = order_tsp  # Composed of 3 points
    order_tsp = insert_to_circuit(initial_circuit, points)
    plot_bestfit(order_tsp, r, filename)
    fo_cost = fo(order_tsp)
    return fo_cost

def insert_to_circuit(initial_circuit, points):
    _, d_old0 = delta(initial_circuit, points[1])
    while len(points) > 0:
        d_old = d_old0
        insertion_position, deltas = [], []
        for i in points:
            ins_point, d = delta(initial_circuit, points[i])
            insertion_position.append(ins_point)
            deltas.append(d)
            """
            saber a posição no dic points, onde foi encontrado o melhor ponto
            porque logo depois, vou remover esse ponto da lista.
            """
            if d < d_old:
                pos = i
                d_old = d
        """
        Encontrar o elemento de referencia, e depois dele será inserido o novo ponto.
        Logo, o circuito inicial é atualizado
        p : encontra um elemento do circuito já estabelecido, utiliza a posição dele como referencia
            para depois, adicionar na posição seguinte o novo ponto ao circuito
        """
        p = insertion_position[deltas.index(min(deltas))][0]
        new_to_circuit = insertion_position[deltas.index(min(deltas))][2]
        initial_circuit.insert(initial_circuit.index(p) + 1, new_to_circuit)
        points.pop(pos)
    return initial_circuit

def delta(initial_circuit, ponto_k):
    """
    Dado um ponto e o circuito, retorna o melhor local para inserir o ponto
    """
    dt, insertion_point = [], []
    for p in range(len(initial_circuit)-1):
        cik = cost(initial_circuit[p], ponto_k)
        cjk = cost(initial_circuit[p+1], ponto_k)
        cij = cost(initial_circuit[p], initial_circuit[p+1])
        d = cik + cjk - cij
        insertion_point.append([initial_circuit[p], initial_circuit[p+1], ponto_k])
        dt.append(d)
    return insertion_point[dt.index(min(dt))], min(dt)


def cost(ponto0, ponto1):
    xk, yk = ponto0
    x, y = ponto1
    c = np.sqrt((xk - x) ** 2 + (yk - y) ** 2)
    return c

def fo(order_tsp):
    tc = 0
    for i in range(len(order_tsp)-1):
        c = cost(order_tsp[i], order_tsp[i + 1])
        tc = tc + c
    return tc

def plot_time_dim(t1, t2):
    xp, yp = [t1, t2], [395, 734]
    x, y = np.asarray(xp), np.asarray(yp)
    plt.title("Tempo de processamento x dimensão")
    plt.xlabel('t(s)'), plt.ylabel('dimensão')
    plt.plot(x, y, marker="o", markerfacecolor="r")
    name = "tempo_dimensão_tsp"
    plt.savefig("Image/" + name)
    plt.clf()

def main():
    file_names = ['pbl395.tsp', 'uy734.tsp']
    dtime = []
    for k in file_names:
        t_inicial = time.time()
        seed = [10, 20, 30, 40, 50, 60, 70, 80, 90, 100]
        best_solution = []
        for r in range(10):  # range(len(seed)):
            best = problem(r, seed[r], k)
            best_solution.append(round(float(best), 2))
        print("Melhor valor obtido em cada uma das 10 rodadas: ", best_solution)
        print("Média dos valores: ", sum(best_solution)/len(best_solution))
        print("Desvio Padrão: ", np.std(best_solution))
        print("Menor valor obtido entre todas as 10 rodadas: ", min(best_solution))
        t_final = time.time()
        deltat = t_final - t_inicial
        dtime.append(deltat)
        print("Intervalor de tempo para executar o algoritmo: ", round(deltat, 3), '\n')
    plot_time_dim(dtime[0], dtime[1])


if __name__ == "__main__":
    main()

