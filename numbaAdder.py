'''
Created on 15.04.2023

@author: david
'''
from numba import jit

@jit(nopython=True)
def get_sum_of_deviations_squared(l_1, l_2):    
    sum_squared = 0.0
    i = 0
    while i < len(l_1):
        sum_squared += (l_1[i] - l_2[i])**2
        i+=1
    return  sum_squared
    