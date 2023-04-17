'''
Created on 14.04.2023

@author: david
'''


# load training data
import sys

from bokeh.models import ColumnDataSource
from bokeh.plotting import figure, show, gridplot

from ideal_dataset_finder import IdealDatasetFinder
import pandas as pd
from pd_2_list_of_functions import pd2ListOfFunctionsXY
import sqlalchemy as db
import numpy as np

engine = db.create_engine('sqlite:///db.db')

# load training data
filename = 'resources/train.csv'
try:
    df = pd.read_csv(filename)
except FileNotFoundError:    
    sys.exit("File: " + filename + " not found")
    
table_name = 'training_data'
df.to_sql(table_name, engine, if_exists='replace', index=True)

# Create a ColumnDataSource from the data
pd_training_data = pd.read_sql_table('training_data', engine)
source = ColumnDataSource(pd_training_data)

pd2dict = pd2ListOfFunctionsXY(pd_training_data)
max_y = pd2dict.get_max_y()
# Create a Bokeh plot
training_data_to_plot = []
for i in range(1,max_y):
    num = i
    var_name = 'var_' + str(num)
    globals()[var_name] = figure(x_axis_label='X-Axis', y_axis_label='Y-Axis', title="Training data #" + str(i))
    
    globals()[var_name].line(x='x', y='y'+str(i), source=source)
    training_data_to_plot.append(globals()[var_name])


# load ideal data
filename = 'resources/ideal.csv'
try:
    df = pd.read_csv(filename)
except FileNotFoundError:    
    sys.exit("File: " + filename + " not found")

table_name = 'ideal_data'
df.to_sql(table_name, engine, if_exists='replace', index=False)
 
# Create a ColumnDataSource from the data
pd_ideal_data = pd.read_sql_table('ideal_data', engine)
source = ColumnDataSource(pd_ideal_data)

pd2dict = pd2ListOfFunctionsXY(pd_ideal_data)
max_y = pd2dict.get_max_y()

# Create a Bokeh plot
ideal_data_to_plot = []
for i in range(1,max_y):
    num = i
    var_name = 'var_ideal_' + str(num)
    globals()[var_name] = figure(x_axis_label='X-Axis', y_axis_label='Y-Axis', title="Ideal data #" + str(i))
    
    globals()[var_name].line(x='x', y='y'+str(i), source=source)
    ideal_data_to_plot.append(globals()[var_name])

# get each data set of training data
list_of_training_data = pd2ListOfFunctionsXY(pd_training_data).getListOfFunctionsXY()
list_of_figures = []
i=1
for element in list_of_training_data:
    fig = figure(title='Example Plot', x_axis_label='X', y_axis_label='Y')
    var_name = 'var_ideal_my_func' + str(num)
    # Add a line glyph to the figure    

    idf = IdealDatasetFinder(pd2ListOfFunctionsXY(pd_ideal_data).getListOfFunctionsXY(), element);
    fwls = idf.get_func_with_least_y_squares();
    globals()[var_name] = figure(x_axis_label='X-Axis', y_axis_label='Y-Axis', title="Found candidate for from list of ideal #" + str(i))
    x_values= fwls.get_f2().get_x_values()
    y_values = fwls.get_f2().get_y_values()
    globals()[var_name].line(x='x', y='y'+str(i), source=(ColumnDataSource(data={"x": x_values, "y"+str(i): np.array(y_values)})))
    list_of_figures.append(globals()[var_name])
    i+=1
grid = gridplot([training_data_to_plot, ideal_data_to_plot, list_of_figures])

#get the ideal data for data set

# Render the plot
show(grid)    
     
if __name__ == '__main__':
    pass
