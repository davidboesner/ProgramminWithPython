'''
Created on 15.04.2023

@author: david
'''
from numba import jit

@jit(nopython=True)
def get_sum_of_deviations_squared(l_1, l_2): 
    """
    Gets the sum of the deviations squared of each element in the list
    
    >>> get_sum_of_deviations_squared(np.array([1,2,3]),np.array([4,5,6]))
    27.0
    """
    sum_squared = 0.0
    i = 0
    while i < len(l_1):
        sum_squared += (l_1[i] - l_2[i])**2
        i+=1
    return  sum_squared

if __name__ == "__main__":
    import doctest
    import numpy as np
    doctest.testmod()
    