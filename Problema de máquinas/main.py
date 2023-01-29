import random
import time
import numpy as np
import csv
import os



def read_file(path):

    data = np.genfromtxt(path, dtype=int, skip_header=2, usecols=(0, 1),
                         delimiter='\t', invalid_raise=False)
    matrix = data.reshape(-1, 2)  # reshape data into matrix

    with open(path) as file:
        dim = [next(file) for x in range(1)]
        dim = int(dim[0])

    # Create a new matrix of zeros with the shape of the maximum values of the original matrix + 1
    cij_matrix = np.zeros((dim, dim), dtype=int)

    # Iterate through the original matrix
    for i in range(matrix.shape[0]):
        # Get the row and column index from the original matrix
        row, col = matrix[i]
        cij_matrix[row - 1][col - 1] = 1
        cij_matrix[col - 1][row - 1] = 1
    return cij_matrix

def queue_size(cij_matrix):
    """
        Determines the size of each of the queues, the first being
         half of the total edges +- 20% of the total size
        """
    random.seed(10)
    l1 = len(cij_matrix)
    porc = random.randint(-20, 21)
    first_l = int((l1 / 2) * (1 + porc / 100))
    second_l = l1 - first_l
    return first_l, second_l


def evaluated_line(line, cij_matrix):
    fo = 0
    for i in range(len(line)-1):
        a = line[i]
        for s in range(len(line) - i - 1):
            b = line[s+i+1]
            if cij_matrix[a][b] != 0:
                fo = fo + abs((s+1))
    return fo

def evaluate(line1, line2, cij_matrix):
    fo1 = evaluated_line(line1, cij_matrix)
    fo2 = evaluated_line(line2, cij_matrix)

    fo3 = 0
    for i in range(len(line1)):
        for j in range(len(line2)):
            a = line1[i]
            b = line2[j]
            if i == j or cij_matrix[a][b] == 0:
                continue
            else:
                fo3 = fo3 + abs((i-j))
    return fo1 + fo2 + fo3


def swap_positions(list, pos1, pos2):
    """ heuristica de melhoramento - busca na vizinhança"""
    list[pos1], list[pos2] = list[pos2], list[pos1]
    return list


def local_search(line1, line2, cij_matrix):
    fo_min = evaluate(line1.copy(), line2.copy(), cij_matrix)
    best_l1, best_l2 = line1, line2
    line_unique = np.concatenate((best_l1, best_l2))
    count = 0
    for m in range(50):
        for k in range(100):
            first_position  = random.randint(0, len(line_unique) - 1)
            second_position = random.randint(0, len(line_unique) - 1)
            if first_position != second_position:
                new_s = swap_positions(line_unique.copy(), first_position, second_position)
                new_fo = evaluate(new_s[:len(line1)], new_s[len(line1):], cij_matrix)
                if new_fo < fo_min:
                    count = count + 1
                    fo_min = new_fo
                    best_s = new_s
                    best_l1 = new_s[:len(line1)]
                    best_l2 = new_s[len(line1):]
        line_unique = np.concatenate((best_l1, best_l2))
    return best_l1, best_l2


def relatorio(typeproblem, best_fitness, rodadas, deltat):

    minimum_fitness = min(best_fitness)
    maximum_fitness = max(best_fitness)
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
    w.writerow([typeproblem, minimum_fitness, maximum_fitness, media, dp, delta_time])
    f.close()



def main():

    f = open('Output.csv', 'w', newline='', encoding='utf-8')
    w = csv.writer(f)
    w.writerow(
        ['Instancia', 'Menor resultado', ' Melhor Resultado', ' Media', ' Desvio padrao', 'Intervalo de tempo'])
    f.close()

    rodadas = 3  # numero de vezes que vai rodar para cada arquivo

    path = 'Instâncias-Problema-das-Máquinas/'
    for _, _, arquivo in os.walk('Instâncias-Problema-das-Máquinas/'):
        continue

    for typeproblem in arquivo:

        cij_matrix = read_file(path + typeproblem)

        best_fitness = []
        initial_time = time.time()
        for i in range(rodadas):

            dim1, dim2 = queue_size(cij_matrix)

            """line1 and line2 are the initial solutions"""
            chosen = random.sample(range(0, len(cij_matrix)), len(cij_matrix))
            line1 = chosen[0:dim1]
            line2 = chosen[dim1:]

            line1, line2 = local_search(line1.copy(), line2.copy(), cij_matrix)
            fo = evaluate(line1, line2, cij_matrix)
            best_fitness.append(fo)

        t_final = time.time()
        deltat = t_final - initial_time
        relatorio(typeproblem, best_fitness, rodadas, deltat)
        print(typeproblem, ": ", max(best_fitness))


if __name__ == "__main__":
    main()
