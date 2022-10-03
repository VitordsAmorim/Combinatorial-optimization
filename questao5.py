

# coding: utf8
import csv
import numpy as np

def question_five( ):
    f = open('exercicio5.csv', 'w+', newline='\n', encoding='utf-8')
    writeFile = csv.writer(f)

    writeFile.writerow(['u', 'v', 'w', 'F(u,v,w)'])
    count, w = 0, 5
    for u in range(1, 4, 1):
        for x in range((3+1), (25+1), 1):
            w = (30 - x - u)
            if w == 4:
                count = count + 1
                print(count, ":  ", 'u =', u, 'v =', x, ',w = ', w, ',F(u,v,w)=', function)
                writeFile.writerow([int(u), int(x), int(w), int(function)])

                break
            if not x == (30-x-u):
                w = (30 - x - u)
                function = (u + x + 2 * (30 - x - u))
                count = count + 1
                print(count, ":  ", 'u =', u, 'v =', x, ',w = ', w, ',F(u,v,w)=', function)
                writeFile.writerow([int(u), int(x), int(w), int(function)])

                continue
                # print('Combinação inválida por conta da restrição.\n
                # u != v != w')
        print("")
    f.close()
    print('*************************')
    print('Total de combinações:', count)


    f = open("exercicio5.csv")
    arquivocsv = csv.reader(f)
    next(arquivocsv)
    X, y = [], []
    for linha in arquivocsv:
        y.append(linha.pop(-1))
        X.append(linha)
    f.close()

    X = np.array(X, dtype=int)  # data
    y = np.array(y, dtype=int)    # target
    print('Maior valor da F(u,v,w):', max(y))
    pos = np.argmax(y)
    print('Parâmetros das variáveis: u =', int(X[pos:pos+1, 0]),
          ', v =', int(X[pos:pos+1, 1]), ', w =', int(X[pos:pos+1, 2]))


if __name__ == '__main__':
    question_five()