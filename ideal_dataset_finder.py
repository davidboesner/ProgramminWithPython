'''
Created on 14.04.2023

@author: david
'''

"""
The purpose of this class is to find the ideal function, which is the best fit out of the functions provided.
The criterion for choosing the ideal functions for the training function is how they minimize the sum of all ydeviations squared (Least-Square)
"""

import sys
sys.path.append('types')

from exceptions.IllegalTypeException import IllegalTypeException
from exceptions.UnequalsLenghtException import UnequalLengthExcpetion
from function_xy import FunctionXY
from numba_adder import get_sum_of_deviations_squared
import numpy as np

class Function2Compare():
    ideal_data = None
    training_data = None
    index_of_compared_function = None
    
    def __init__(self, training_data,ideal_data, index_of_compared_function):
        if not isinstance(ideal_data, FunctionXY) or not isinstance(training_data, FunctionXY):
            raise IllegalTypeException();
        
        self.ideal_data = ideal_data
        self.training_data = training_data
        self.index_of_compared_function = index_of_compared_function
        
    def __get_sum_of_y_deviations_squared(self):
        """
        Gets the sum of the deviations between the functions ideal_data and training_data squared
        """

        # check input
        if len(self.ideal_data.get_x_values())!=len(self.training_data.get_x_values()):
            raise UnequalLengthExcpetion()
        
        # sum y values
        y1 = np.array(self.ideal_data.get_y_values())
        y2 = np.array(self.training_data.get_y_values())

        return get_sum_of_deviations_squared(y1, y2)
    
    def __eq__(self, other):        
        return self.__get_sum_of_y_deviations_squared() == other.__get_sum_of_y_deviations_squared()
    
    def __lt__(self, other):        
        return self.__get_sum_of_y_deviations_squared() < other.__get_sum_of_y_deviations_squared()
    
    def __gt__(self, other):
        return self.__get_sum_of_y_deviations_squared() > other.__get_sum_of_y_deviations_squared()
    
    def get_ideal_data(self):
        return self.ideal_data
    
    def get_training_data(self):
        return self.training_data
    
    def get_index_of_compared_function(self):
        return self.index_of_compared_function
    
class IdealDatasetFinder():
    ideal_datasets = None
    function = None
    
    def __init__(self, a, f):
        self.ideal_datasets = a
        self.function = f
    
    def get_func_with_least_y_squares(self):
        """
        Gets the function with the least squares y distance
        """
        l = []
        for ds in self.ideal_datasets:
            fc = Function2Compare(self.function,ds,ds.get_n())
            l.append(fc)
        return min(l)