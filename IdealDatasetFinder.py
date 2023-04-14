'''
Created on 14.04.2023

@author: david
'''
import doctest

"""
The purpose of this class is to find the ideal function, which is the best fit out of the functions provided.
The criterion for choosing the ideal functions for the training function is how they minimize the sum of all ydeviations squared (Least-Square)
"""

class IdealDatasetFinder():
    all_datasets = None
    function = None
    
    def __init__(self, a, f):
        self.all_datasets = a
        self.function = f
    
    def __get_sum_of_y_deviations(self, f1, f2):
        """
        Gets the sum of the deviations between the functions f1 and f2
        """
        pass
    
    def get_func_with_least_y_squares(self):
        print(self.all_datasets[['x','y1']])
    
if __name__ == '__main__':
    doctest.testmod()