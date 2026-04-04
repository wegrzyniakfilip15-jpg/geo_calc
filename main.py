from math import sqrt

h1 = float(input("Koło lewe: "))
h2 = float(input("Koło prawe: "))
measurments = []

def add_measurment(h1, h2):
    h1_h2 = (h1, h2)
    measurments.append(h1_h2)


def calc_c():
    c_result = []
    if len(measurments) <= 1:
        raise ValueError("No measurments")
    else:
        for h1, h2 in measurments:
            if h1 < 200:
                c = (h2 - (h1 + 200)) / 2
                c_result.append(c)
            else:
                c = (h2 - (h1 - 200)) / 2
                c_result.append(c)

    c_average = sum(c_result) / len(c_result)
    sum_v = 0
    for c in c_result:
        v = c - c_average
        v = pow(v, 2)
        sum_v += v

    c_error = sqrt(sum_v / (len(c_result)*(len(c_result) - 1)))

    return c_error, c_result