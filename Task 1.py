# -*- coding: utf-8 -*-

import math
import matplotlib.pyplot as plt
import numpy as np
import xml.etree.ElementTree as ET
import os


def func(x):
    return 10 + x * x - 10 * math.cos(2 * math.pi * x)


if __name__ == '__main__':
    xmin = -5.12
    xmax = 5.12
    count = 500
    xlist = np.linspace(xmin, xmax, count)
    ylist = [func(x) for x in xlist]
    if not os.path.exists('results'):
        os.mkdir('results')
    os.chdir(os.path.join(os.getcwd(), 'results'))
    with open('result.txt', 'w') as f:
        for i in range(count):
            f.write('{:.4f}'.format(xlist[i]))
            f.write('    ')
            f.write('{:.4f}'.format(ylist[i]))
            f.write('\n')
    plt.plot(xlist, ylist)
    plt.show()
    
    

    
