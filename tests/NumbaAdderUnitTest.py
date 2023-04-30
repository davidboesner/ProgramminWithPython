'''
Created on 15.04.2023

@author: david
'''
import unittest

from numba_adder import get_sum_of_deviations_squared
import numpy as np

class Test(unittest.TestCase):
    
    def testNumbaAdder(self):
        self.assertEqual(27.0, get_sum_of_deviations_squared(np.array([1,2,3]),np.array([4,5,6])))

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()