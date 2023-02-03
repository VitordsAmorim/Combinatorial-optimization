
def genetic_algorithm(problem, population_size, n_generations, round, mutation_rate):

    """
    best_fit: valor da fitnes do melhor indivíduo
    best_pos: posicao dentro da população, em que está o melhor indivíduo
    path: os valores, dos parametros, do melhor indivíduo
    fitn: o valor da fitnes de toda a população
    """
    old_population = problem.initial_population(population_size)  # Create a initial population
    best_fit, best_pos, best_individual, fitn = problem.fitness(old_population)

    best_solutions, ngeracoes = [], []  # Armazena o melhor indivíduo de cada uma das gerações
    for k in range(0, n_generations):
        new_population = []  # 'zerar' os valores da nova população
        for m in range(0, (population_size//2)):

            # seleciona dois pais dentro da população
            # retorna a posição de onde os pais estão dentro da lista da população
            # fitn contain all the fitness of the population
            pai1, pai2 = problem.selection_process(fitn)

            # Realiza o Crossover - Order 1
            # Retorna 2 indivíduos da próxima geração
            # individual one and two (i1, i2)
            i1, i2 = problem.crossover(old_population[pai1], old_population[pai2])

            f1 = problem.mutation(i1, mutation_rate)
            f2 = problem.mutation(i2, mutation_rate)
            new_population.append(f1)
            new_population.append(f2)

        """
        ELITISM
        
        Makes the best individual of the past generation survive into the new.
        Generation, replacing the worst individual of the current generation
        """
        # print("Round:", round, "Iterations:", k, "best fitness:", best_fit)
        best_solutions.append(best_fit)
        best_individual_old = best_individual
        old_population = problem.elitism(new_population, best_individual_old, fitn)
        best_fit, best_pos, best_individual, fitn = problem.fitness(new_population)
        ngeracoes.append(k)
    print("Round:", round, "best fitness:", best_fit)
    # problem.plot(best_solutions, ngeracoes, round)
    problem.plot_bestfit(best_individual, round)
    return [best_solutions, ngeracoes]
