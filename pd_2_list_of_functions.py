'''
Created on 15.04.2023

@author: david
'''

from function_xy import FunctionXY
class pd2ListOfFunctionsXY:
    pd = None
    def __init__(self, pd):
        self.pd = pd
        
    def get_max_y(self):
        """
        Gets the element with the maximum y
        """
        i = 1
        while True:
            try:
                self.pd["y"+str(i)]
                i+=1
            except KeyError:
                return i            
            
    def getListOfFunctionsXY(self):
        r = []
        max_y = self.get_max_y()
        for i in range(1,max_y):
            dataset_x = list(self.pd["x"])
            dataset_y = list(self.pd["y"+str(i)])            
            r.append(FunctionXY(dataset_x, dataset_y))
        return r
          
if __name__ == '__main__':
    pass