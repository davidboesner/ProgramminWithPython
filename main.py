'''
Created on 14.04.2023

@author: david
'''


# load training data
import pandas as pd
import sqlalchemy as db
from bokeh.plotting import figure, show, gridplot
from bokeh.models import ColumnDataSource

from IdealDatasetFinder import IdealDatasetFinder

engine = db.create_engine('sqlite:///training_data.db')

# load training data
df = pd.read_csv('resources/train.csv')
table_name = 'training_data'
df.to_sql(table_name, engine, if_exists='replace', index=True)

# Create a ColumnDataSource from the data
pd_training_data = pd.read_sql_table('training_data', engine)
source = ColumnDataSource(pd_training_data)

# Create a Bokeh plot
training_data_to_plot = []
for i in range(1,5):
    num = i
    var_name = 'var_' + str(num)
    globals()[var_name] = figure(x_axis_label='X-Axis', y_axis_label='Y-Axis', title="Training data #" + str(i))
    
    globals()[var_name].line(x='x', y='y'+str(i), source=source)
    training_data_to_plot.append(globals()[var_name])


# load ideal data
df = pd.read_csv('resources/ideal.csv')
table_name = 'ideal_data'
df.to_sql(table_name, engine, if_exists='replace', index=False)
 
# Create a ColumnDataSource from the data
pd_ideal_data = pd.read_sql_table('ideal_data', engine)
source = ColumnDataSource(pd_ideal_data)

# Create a Bokeh plot
ideal_data_to_plot = []
for i in range(1,51):
    num = i
    var_name = 'var_ideal_' + str(num)
    globals()[var_name] = figure(x_axis_label='X-Axis', y_axis_label='Y-Axis', title="Ideal data #" + str(i))
    
    globals()[var_name].line(x='x', y='y'+str(i), source=source)
    ideal_data_to_plot.append(globals()[var_name])

grid = gridplot([training_data_to_plot, ideal_data_to_plot])

#get the ideal data for data set

# Render the plot
# show(grid)

# get each data set of training data
list_of_all_training_data = []
for i in range(1,5):
    dataset_x = list(pd_training_data["x"])
    dataset_y = list(pd_training_data["y"+str(i)])
    training_dataset={"dataset_x": dataset_x, "dataset_y": dataset_y}
    idf = IdealDatasetFinder(pd_ideal_data, training_dataset);
    idf.get_func_with_least_y_squares();
     
if __name__ == '__main__':
    pass
