'''
Created on 15.04.2023

@author: david
'''
class pd2ListOfDict:
    pd = None
    def __init__(self, pd):
        self.pd = pd
        
    def get_max_y(self):
        i = 1
        while True:
            try:
                self.pd["y"+str(i)]
                i+=1
            except KeyError:
                return i            
            
    def getDict(self):
        max_y = self.get_max_y()
        for i in range(1,max_y):
            dataset_x = list(self.pd["x"])
            dataset_y = list(self.pd["y"+str(i)])
            # training_dataset={"dataset_x": dataset_x, "dataset_y": dataset_y}
          
if __name__ == '__main__':
    pass