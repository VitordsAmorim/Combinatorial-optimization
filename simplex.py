import numpy as np

def update_base_xn(prd1, prd2, base):
    minimum = []
    for j in range(len(prd1)):
        minimum = np.append(minimum, prd1[j] / prd2[j])
    res = prd1 - prd2 * min(minimum)
    for k in range(len(res)):
        if round(float(res[k]), 4) == 0:
            leave_the_base = base[k]
            return k, leave_the_base

def print_var(txt, prd1):
    print("\nThe basic solution is:")
    for j in range(len(txt)):
        if j < 3:
            print("%s = %0.2f" % (txt[j], prd1[j]))
        elif j == 3:
            print("\nNon-basic variables - xn:")
            print("%s = %0.2f" % (txt[j], 0))
        else:
            print("%s = %0.2f" % (txt[j], 0))

def print_objetive_function(prod4, prod5, prod6, xn):
    print("\nThe objective function written in terms of Xn is:")
    print("f(x) = %0.2f  +  %0.2fx%d  +  %0.2fx%d" % (float(prod4), float(prod5), xn[0], float(prod6), xn[1]))
    print("The minimum value for f(x) = %0.2f\n" % (float(prod4)))


def main():
    """
                Ax = b
    min f(x_1, x_2) = -3x_1 -2x_2 + 0x_3 + 0x_4 + 0x_5
    s.t.
    0.5 x_1 + 0.3 x_2 +   1x_3 + 0x_4 + 0x_5 = 3
    0.1 x_1 + 0.2 x_2 +   0x_3 + 1x_4 + 0x_5 = 1
    0.4 x_1 + 0.5 x_2 +   0x_3 + 0x_4 + 1x_5 = 3
    """
    a = np.array([
        [0.5, 0.3, 1, 0, 0, 3],
        [0.1, 0.2, 0, 1, 0, 1],
        [0.4, 0.5, 0, 0, 1, 3],
    ], dtype=np.float64)

    """
    Objetive function c
    """
    c = np.array([
        [-3], [-2], [0], [0], [0],
    ], dtype=np.float64)

    """
    Required to set the transposed 'p'
    """
    base = [3, 4, 5]  # initial base
    xn   = [1, 2]
    b = a[0:, 5:6]  # In this case: [3, 1, 3]

    while True:

        """There is a better way to write this step of the algorithm."""
        c1 = c[base[0]-1:base[0]]
        c2 = c[base[1]-1:base[1]]
        c3 = c[base[2]-1:base[2]]
        ct = np.concatenate((c1, c2, c3), axis=1)

        column1 = a[0:, (base[0]-1):base[0]]
        column2 = a[0:, (base[1]-1):base[1]]
        column3 = a[0:, (base[2]-1):base[2]]
        Bn = np.concatenate((column1, column2, column3), axis=1)

        """
        Given the null variables
        """
        xn1 = a[0:, (xn[0] - 1):xn[0]]
        xn2 = a[0:, (xn[1] - 1):xn[1]]

        """
        General Solution
        """
        Bn_inv = np.linalg.inv(Bn)
        prd1 = np.dot(Bn_inv, b)

        prd2 = np.dot(Bn_inv, xn1)
        prd3 = np.dot(Bn_inv, xn2)

        txt = np.array([  # it only serves to help print the answer
            ['x'+str(base[0])],
            ['x'+str(base[1])],
            ['x'+str(base[2])],
            ['x' + str(xn[0])],
            ['x' + str(xn[1])],
        ], dtype=str)

        # print("The general solution is:")
        # print(txt, "\n=\n", prd1, "\n-\n", prd2, "x", xn[0], "\n-\n", prd3, "x", xn[1])

        # print_var(txt, prd1)
        pt = np.dot(ct, Bn_inv)
        prod4 = np.dot(pt, b)
        prod5 = -np.dot(pt, xn1) + c[xn[0]-1]
        prod6 = -np.dot(pt, xn2) + c[xn[1]-1]

        """
        The objective function written as a function of xn
        writing in terms of non-basic variables
        """
        # print_objetive_function(prod4, prod5, prod6, xn)

        """At this point, there are no more parameters to change"""
        if float(prod5) >= 0 and float(prod6) >= 0:
            print("Found the optimal value of the function")
            print_objetive_function(prod4, prod5, prod6, xn)
            print_var(txt, prd1)
            break
        else:
            if float(prod5) < float(prod6):
                """helps to know who enters and leaves the base"""
                k, leave_the_base = update_base_xn(prd1, prd2, base)
                base[k] = xn[0]  # enter_the_base
                xn[0] = leave_the_base
            else:
                k, leave_the_base = update_base_xn(prd1, prd3, base)
                base[k] = xn[1]
                xn[1] = leave_the_base


if __name__ == "__main__":
    """
    The video explains well about how to perform the simplex algorithm using matrix notation
    https://www.youtube.com/watch?v=0qaAG8wdGHQ
    https://www.youtube.com/watch?v=k3fF7r50Vc0
    """
    main()
