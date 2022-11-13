from docplex.mp.model import Model


def isfractional(variables, i):
    """test condition to know if there is number with fractional value"""
    n1 = int(round(variables[i].solution_value, 3))
    n2 = round(variables[i].solution_value, 3)
    return not n1 == n2

def chosse_variable(m, variables):
    pivo_variable = []
    var = None
    melhor_valor = 100000
    for i in range(m.number_of_variables):
        if isfractional(variables, i):
            pivo_variable.append(variables[i].solution_value)
            if abs(variables[i].solution_value - 0.5) < abs(melhor_valor - 0.5):
                var = variables[i]
                melhor_valor = variables[i].solution_value
    return var

def new_nodel(m, variables, bound):
    z = m
    b = z.add_constraint(bound == variables)

    z.solve()
    print(variables, "=", round(variables.solution_value, 3))
    z.print_solution()
    print("")
    # z.remove_constraint(b)




def main():

    m = Model(name='exercicio_limitantes')  # create one model instance

    x1 = m.continuous_var(name='x1')
    x2 = m.continuous_var(name='x2')
    x3 = m.continuous_var(name='x3')
    x4 = m.continuous_var(name='x4')
    variables = [x1, x2, x3, x4]

    # constraints
    m.add_constraint( 3 * x1 - 2 * x2 + 1*x3        <= 3)
    m.add_constraint( 1 * x1 - 2 * x2 + 3*x3 + 4*x4 >= 1)
    m.add_constraint( 1 * x1 + 3 * x2 + 2*x3 + 4*x4 <= 5)
    m.add_constraint( 3 * x1 + 4 * x2 + 2*x3 + 5*x4 <= 7)

    m.add_constraint( x1 <= 1)
    m.add_constraint( x2 <= 1)
    m.add_constraint( x3 <= 1)
    m.add_constraint( x4 <= 1)

    m.maximize(x1 + 2*x2 + 3*x3 + 4*x4)  # objetive function
    # m.print_information()

    solutions = []

    s0 = m.solve()
    solutions.append(s0)
    m.print_solution(solutions[0])
    print("")

    teste = 0
    while teste != 4:
        var = chosse_variable(m, variables)
        if var is None:
            print("Valor otimo encontrado")
            break
        new_nodel(m, var, 0)
        # new_nodel(m, var, 1)
        teste = teste + 1


if __name__ == "__main__":
    main()

