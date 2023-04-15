'''
Created on 15.04.2023

@author: david
'''
from exceptions.UnequalsLenghtException import UnequalLengthExcpetion

class FunctionXY():
    '''
    classdocs
    '''
    
    x_values = None
    y_values = None
    
    def __init__(self, x_values, y_values):
        if not isinstance(x_values, list):
            raise TypeError("Parameter must be a list.")
        if not isinstance(y_values, list):
            raise TypeError("Parameter must be a list.")
        if len(x_values) != len(y_values):
            raise UnequalLengthExcpetion("Every x value must be mapped to a y value")
        
        self.x_values = x_values
        self.y_values = y_values
        
    def get_x_values(self):
        return self.x_values
        
    def get_y_values(self):
        return self.y_values