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

toPlot = []
training_data_color = ["red","green","blue","purple","yellow"]
for i in range(1,5):
    num = i
    var_name = 'var_' + str(num)
    globals()[var_name] = figure(x_axis_label='X-Axis', y_axis_label='Y-Axis', title="Training data #" + str(i))
    
    globals()[var_name].line(x='x', y='y'+str(i), source=source, line_color=training_data_color[i-1])
    toPlot.append(globals()[var_name])
   
print(toPlot)
grid = gridplot([toPlot])

# Render the plot
show(grid)

if __name__ == '__main__':
    pass
