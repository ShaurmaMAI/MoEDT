# -*- coding: utf-8 -*-

from requests import get
import re
import numpy as np
import math
import scipy
import matplotlib.pyplot as plt
import os
import json as js

def jn(n0, kr0):
    return scipy.special.spherical_jn(n0, kr0)


def yn(n1, kr1):
    return scipy.special.spherical_yn(n1, kr1)


def hn(n2, kr2):
    return jn(n2, kr2) + yn(n2, kr2) * 1j


def an(n3, kr3):
    return jn(n3, kr3) / hn(n3, kr3)


def bn(n4, kr4):
    return (kr4 * jn(n4 - 1, kr4) - n4 * jn(n4, kr4)) / (kr4 * hn(n4 - 1, kr4) - n4 * hn(n, kr4))


if __name__ == '__main__':
    url = 'https://jenyay.net/uploads/Student/Modelling/task_02_01.txt'
    name = 'file.txt'
    with open(name, 'wb') as file:
        response = get(url)
        file.write(response.content)
    with open(name, 'r') as file:
        file_lines = file.readlines()
    Var1 = re.split('. D=|; fmin=|; fmax=|\\n', file_lines[0])
    D = float(Var1[1])
    f_min = float(Var1[2])
    f_max = float(Var1[3])

    print(f_min, f_max, D)

    count = 1000
    r = D / 2
    df = np.linspace(f_min, f_max, count)
    c = 3 * 10 ** 8
    lmb = c / df
    k = 2 * math.pi / lmb

    summa = 0
    for n in range(1, 80):
        summa += ((-1) ** n * (n + 0.5) * (bn(n, k * r) - an(n, k * r)))
    sigma = (2 * lmb ** 2 / math.pi) * abs(summa) ** 2

    plt.plot(df, sigma)
    plt.xlabel('f, Гц')
    plt.ylabel(u'\u03C3, м^2')
    plt.show()

    if not os.path.exists('results'):
        os.mkdir('results')
    os.chdir(os.path.join(os.getcwd(), 'results'))

    str_f = '   "freq": [' + '{:.4f}'.format(df[0])
    str_lmb = ' "lambda": [' + '{:.4f}'.format(lmb[0]) 
    str_sigma = '   "sigma": [' + '{:.4f}'.format(sigma[0])
    for i in range(1, count):
        str_f += ', {:.4f}'.format(df[i])
        str_lmb += ', {:.4f}'.format(lmb[i])
        str_sigma += ', {:E}'.format(sigma[i])
    str_f += '],\n'
    str_lmb += '],\n'
    str_sigma += ']\n'
    with open('result.json', 'w', encoding='utf8') as file:
        file.write('{\n')
        file.write(str_f)
        file.write(str_lmb)
        file.write(str_sigma)
        file.write('}')
        
