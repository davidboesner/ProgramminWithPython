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

list_of_ideal_data = pd2ListOfFunctionsXY(pd_training_data)
max_y = list_of_ideal_data.get_max_y()
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
df.to_sql(table_name, engine, if_exists='replace', index=True)
 
# Create a ColumnDataSource from the data
pd_ideal_data = pd.read_sql_table('ideal_data', engine)
source = ColumnDataSource(pd_ideal_data)

list_of_ideal_data = pd2ListOfFunctionsXY(pd_ideal_data)
max_y = list_of_ideal_data.get_max_y()

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
list_of_ideal_candidates = []
i=1
for element in list_of_training_data:
    fig = figure(title='Example Plot', x_axis_label='X', y_axis_label='Y')
    var_name = 'var_ideal_my_func' + str(num)

    idf = IdealDatasetFinder(list_of_ideal_data.getListOfFunctionsXY(), element);
    #get the ideal data for data set
    fwls = idf.get_func_with_least_y_squares();
    globals()[var_name] = figure(x_axis_label='X-Axis', y_axis_label='Y-Axis', title="Found candidate from list of ideal #" + str(i) + " index of ideal data: " + str(fwls.get_index_of_compared_function()))
    x_values= fwls.get_f2().get_x_values()
    y_values = fwls.get_f2().get_y_values()
    globals()[var_name].line(x='x', y='y'+str(i), source=(ColumnDataSource(data={"x": x_values, "y"+str(i): np.array(y_values)})))
    list_of_figures.append(globals()[var_name])
    list_of_ideal_candidates.append(fwls)
    i+=1
    
# the test data (B) must be loaded line-by-line from another CSV-file and – if it complies with the compiling criterion – matched to one of the four functions chosen under i (subsection above)

# Afterwards, the results need to be saved into another fourcolumn-table in the SQLite database
grid = gridplot([training_data_to_plot, ideal_data_to_plot, list_of_figures])




# Render the plot
show(grid)    
     
if __name__ == '__main__':
    pass
