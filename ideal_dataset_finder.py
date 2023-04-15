'''
Created on 14.04.2023

@author: david
'''
import doctest
from exceptions.UnequalsLenghtException import UnequalLengthExcpetion

"""
The purpose of this class is to find the ideal function, which is the best fit out of the functions provided.
The criterion for choosing the ideal functions for the training function is how they minimize the sum of all ydeviations squared (Least-Square)
"""
class _FunctionComparer():
    f1 = None
    f2 = None
    
    def __init__(self, f1,f2):
        self.f1 = f1
        self.f2 = f2
            
    def __get_sum_of_y_deviations_squared(self, f1, f2):
        """
        Gets the sum of the deviations between the functions f1 and f2 sqaured
        """
        sum_squared = 0
        # check input
        if len(f1)!=len(f2):
            raise UnequalLengthExcpetion()
        i = 0
        while i < len(f1):
            i+=1
            if f1[i]:
                pass
            
        
    
class IdealDatasetFinder():
    all_datasets = None
    function = None
    
    def __init__(self, a, f):
        self.all_datasets = a
        self.function = f
    
    
    
    def get_func_with_least_y_squares(self):
        l = []
        for ds in self.all_datasets:
            fc = _FunctionComparer(self.function,ds)
            l.append(fc)
        return min(l);
    
if __name__ == '__main__':
    doctest.testmod()