'''
Created on 15.04.2023

@author: david
'''

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
        
        self.x_values = x_values
        self.y_values = y_values
        
        