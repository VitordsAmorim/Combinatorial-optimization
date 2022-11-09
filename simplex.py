import numpy as np

def update_base_xn(prd1, prd2, base):
    minimum = []
    for j in range(len(prd1)):
        if prd2[j] > 0:  # Ratio test, in it the divisor must be greater than zero
            minimum = np.append(minimum, prd1[j] / prd2[j])
    if minimum:
        res = prd1 - prd2 * min(minimum)
    else:
        print("This is an unlimited problem, so there is no optimal solution.")
        return False, False, False

    for k in range(len(res)):
        if round(float(res[k]), 4) == 0:
            leave_the_base = base[k]
            return k, leave_the_base, True

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
        [-1,  1, 1, 0, 3],
        [ 2, -3, 0, 1, 3],
        # [-1, 1, 0, 0, 1, 4],
    ], dtype=np.float64)

    """
    Objetive function c
    """
    c = np.array([
        [-2], [-2], [0], [0], [0],
    ], dtype=np.float64)

    """
    Required to set the transposed 'p'
    """
    base = [3, 4]  # initial base
    xn   = [1, 2]
    b = a[:, -1:]  # In this case: [6, 4, 4]

    while True:
        """
        Assemble the transposed matrix c only with the values corresponding to those of the base.
        Then, following the same idea, assemble matrix B.
        """
        ct  = np.zeros((1, len(base)))
        Bn = np.zeros((len(base), len(base)))
        for i in range(len(base)):
            ct[:, i] = (c[base[i]-1:base[i]])
            Bn[:, i:] = a[0:, (base[i]-1):base[i]]

        """
        Given the null variables
        """
        xn1 = a[0:, (xn[0] - 1):xn[0]]
        xn2 = a[0:, (xn[1] - 1):xn[1]]

        """
        General Solution
        """
        Bn_inv = np.linalg.inv(Bn)
        prd1 = np.dot(Bn_inv, b)  # xb - Represents the basic feasible solution

        prd2 = np.dot(Bn_inv, xn1)
        prd3 = np.dot(Bn_inv, xn2)

        txt = np.array([  # it only serves to help print the answer
            ['x'+str(base[0])],
            ['x'+str(base[1])],
            # ['x'+str(base[2])],
            ['x' + str(xn[0])],
            ['x' + str(xn[1])],
        ], dtype=str)

        # print("The general solution is:")
        # print(txt, "\n=\n", prd1, "\n-\n", prd2, "x", xn[0], "\n-\n", prd3, "x", xn[1])

        # print_var(txt, prd1)
        pt = np.dot(ct, Bn_inv)
        prod4 = np.dot(pt, b)  # fx = np.dot(ct, prd1)
        prod5 = + c[xn[0]-1] - np.dot(pt, xn1)  # relative costs
        prod6 = + c[xn[1]-1] - np.dot(pt, xn2)  # relative costs

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
            ratio_test = True
            if float(prod5) < float(prod6):
                """helps to know who enters and leaves the base"""
                k, leave_the_base, ratio_test = update_base_xn(prd1, prd2, base)
                if ratio_test is False:
                    break
                base[k] = xn[0]  # enter_the_base
                xn[0] = leave_the_base
            else:
                k, leave_the_base, ratio_test = update_base_xn(prd1, prd3, base)
                if ratio_test is False:
                    break
                base[k] = xn[1]
                xn[1] = leave_the_base


if __name__ == "__main__":
    """
    The video explains well about how to perform the simplex algorithm using matrix notation
    https://www.youtube.com/watch?v=k3fF7r50Vc0
    """
    main()

