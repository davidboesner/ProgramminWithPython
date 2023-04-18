'''
Created on 14.04.2023

@author: david
'''


# load training data
import math
import sys

from bokeh.models import ColumnDataSource
from bokeh.plotting import figure, show, gridplot
from future.backports.http.client import FOUND

from ideal_dataset_finder import IdealDatasetFinder
from line import Line
import numpy as np
import pandas as pd
from pd_2_list_of_functions import pd2ListOfFunctionsXY
import sqlalchemy as db


engine = db.create_engine('sqlite:///db.db')

# load training data
filename = 'resources/train.csv'
try:
    df = pd.read_csv(filename)
except FileNotFoundError:    
    sys.exit("File: " + filename + " not found")
    
table_name = 'ideal_function_x_y_dict'
df.to_sql(table_name, engine, if_exists='replace', index=True)

# Create a ColumnDataSource from the data
pd_training_data = pd.read_sql_table('ideal_function_x_y_dict', engine)
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

table_name = 'ideal_function'
df.to_sql(table_name, engine, if_exists='replace', index=True)
 
# Create a ColumnDataSource from the data
pd_ideal_data = pd.read_sql_table('ideal_function', engine)
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
    x_values= fwls.get_training_data().get_x_values()
    y_values = fwls.get_training_data().get_y_values()
    globals()[var_name].line(x='x', y='y'+str(i), source=(ColumnDataSource(data={"x": x_values, "y"+str(i): np.array(y_values)})))
    list_of_figures.append(globals()[var_name])
    list_of_ideal_candidates.append(fwls)
    i+=1
    
# the test data (B) must be loaded line-by-line from another CSV-file and – if it complies with the compiling criterion – matched to one of the four functions chosen under i (subsection above)
list_all_lines = []
with open("resources/test.csv") as f:
    for l in f.readlines(): 
        x = l.split(",")[0].strip()
        y = l.split(",")[1].strip()
        try:
            x = float(x)
            y = float(y)
        except:
            continue
        line = Line(x,y)
        list_all_lines.append(line)
list_all_lines_sorted = sorted(list_all_lines, key=lambda line: line.x)

# match to one of the four functions chosen under i (subsection above)
for l in list_all_lines_sorted:
    f_x = l.x
    f_y = l.y
    
    min_distance_x = None
    min_distance_y = None
    min_distance_delta = None
    min_distance_index = None
    
    for f in list_of_ideal_candidates:
        ideal_function = f.get_ideal_function()
        n_ideal_function = f.get_ideal_function().get_n()
        ideal_function_x_y_dict = dict(zip(ideal_function.get_x_values(), ideal_function.get_y_values()))
        if f_x in ideal_function_x_y_dict:
            ideal_data_y = ideal_function_x_y_dict[f_x]
            dist = abs((ideal_data_y - f_y))
            if min_distance_delta == None or (dist < min_distance_delta and dist > math.sqrt(2)):
                min_distance_y = ideal_data_y
                min_distance_x = f_x
                min_distance_index = n_ideal_function
                min_distance_delta = ideal_data_y - f_y
            
    
# Afterwards, the results need to be saved into another fourcolumn-table in the SQLite database
grid = gridplot([training_data_to_plot, ideal_data_to_plot, list_of_figures])




# Render the plot
show(grid)    
     
if __name__ == '__main__':
    pass
