'''
Created on 14.04.2023

@author: david
'''


# load training data
import pandas as pd
import sqlalchemy as db
from bokeh.plotting import figure, show, gridplot
from bokeh.models import ColumnDataSource

import random 
from docutils.nodes import title

engine = db.create_engine('sqlite:///training_data.db')

# load training data
df = pd.read_csv('resources/train.csv')
table_name = 'training_data'
df.to_sql(table_name, engine, if_exists='replace', index=False)

# Create a ColumnDataSource from the data
source = ColumnDataSource(pd.read_sql_table('training_data', engine))

# Create a Bokeh plot
training_data_to_plot = []
training_data_color = ["red","green","blue","purple","yellow"]
for i in range(1,5):
    num = i
    var_name = 'var_' + str(num)
    globals()[var_name] = figure(x_axis_label='X-Axis', y_axis_label='Y-Axis', title="Training data #" + str(i))
    
    globals()[var_name].line(x='x', y='y'+str(i), source=source, line_color=training_data_color[i-1])
    training_data_to_plot.append(globals()[var_name])


# load training data
df = pd.read_csv('resources/ideal.csv')
table_name = 'ideal_data'
df.to_sql(table_name, engine, if_exists='replace', index=False)

print (df) 
# Create a ColumnDataSource from the data
source = ColumnDataSource(pd.read_sql_table('ideal_data', engine))

# Create a Bokeh plot
ideal_data_to_plot = []
for i in range(1,51):
    num = i
    var_name = 'var_ideal_' + str(num)
    globals()[var_name] = figure(x_axis_label='X-Axis', y_axis_label='Y-Axis', title="Ideal data #" + str(i))
    
    globals()[var_name].line(x='x', y='y'+str(i), source=source)
    ideal_data_to_plot.append(globals()[var_name])
   
print(training_data_to_plot)

grid = gridplot([training_data_to_plot, ideal_data_to_plot])

# Render the plot
show(grid)

if __name__ == '__main__':
    pass
