'''
Created on 14.04.2023

@author: david
'''


# load training data
import math
import os
import sys

from bokeh.models import ColumnDataSource, HoverTool
from bokeh.plotting import figure, show, gridplot
from sqlalchemy import Column, Integer, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from ideal_dataset_finder import IdealDatasetFinder
from line import Line
import numpy as np
import pandas as pd
from pd_2_list_of_functions import pd2ListOfFunctionsXY
import sqlalchemy as db
from bokeh.models import Span
import logging

db_name = "db.db"
try:
    os.remove(db_name)
except Exception:
    pass
logging.basicConfig(filename="app.log", filemode="w", format="%(name)s- %(levelname)s - %(message)s")

# drop old database
engine = db.create_engine('sqlite:///' + db_name)

filename = 'resources/train.csv'

# load training data

try:
    df = pd.read_csv(filename)
except FileNotFoundError:    
    sys.exit("File: " + filename + " not found")
    logging.error("CSV file not found")

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
list_of_ideal_candiate_figures = []
list_of_ideal_candidates = []

for i, element in enumerate(list_of_training_data):
    i = i+1    
    var_name = 'var_ideal_my_func' + str(i)

    idf = IdealDatasetFinder(list_of_ideal_data.getListOfFunctionsXY(), element);
    #get the ideal data for data set
    try:
        fwls = idf.get_func_with_least_y_squares();
    except:
        sys.exit("Could not parse input")
    globals()[var_name] = figure(x_axis_label='X-Axis', y_axis_label='Y-Axis', title="Found candidate from list of ideal #" + str(i) + " index of ideal data: " + str(fwls.get_index_of_compared_function()))
    x_values= fwls.get_ideal_data().get_x_values()
    y_values = fwls.get_ideal_data().get_y_values()
    globals()[var_name].line(x='x', y='y'+str(i), source=(ColumnDataSource(data={"x": x_values, "y"+str(i): np.array(y_values)})))
    list_of_ideal_candiate_figures.append(globals()[var_name])
    list_of_ideal_candidates.append(fwls)
    
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


# create a session factory
Session = sessionmaker(bind=engine)

# create a base class for declarative models

Base = declarative_base()

class TestFunctionAndMapping(Base):
    __tablename__ = 'TestFunctionAndMapping'
    
    id = Column(Integer, primary_key=True)
    #X (test func)
    x_test = Column(Float)
     
    #Y (test func)
    y_test = Column(Float) 
    
    #Delta Y (test func)
    dy_test = Column(Float)
     
    #Number of ideal func
    n_ideal = Column(Integer)

# create the table in the database
Base.metadata.create_all(engine)

# create a session
session = Session()

# match to one of the four functions chosen under i (subsection above)
for l in list_all_lines_sorted:
    f_x = l.x
    f_y = l.y
    
    min_distance_x = None
    min_distance_y_ideal = None
    min_distance_delta = None
    ideal_index = None
    
    for f in list_of_ideal_candidates:
        ideal_function = f.get_ideal_data()
        n_ideal_function = f.get_ideal_data().get_n()
        ideal_function_x_y_dict = dict(zip(ideal_function.get_x_values(), ideal_function.get_y_values()))
        if f_x in ideal_function_x_y_dict:
            ideal_data_y = ideal_function_x_y_dict[f_x]
            dist = abs((ideal_data_y - f_y))
            if dist < math.sqrt(2) and (min_distance_delta == None or (dist < min_distance_delta)):
                min_distance_y_ideal = ideal_data_y
                min_distance_x = f_x
                ideal_index = n_ideal_function
                min_distance_delta =  f_y - ideal_data_y
    
    # create a user object and add it to the session
    tfam = TestFunctionAndMapping(x_test=f_x, y_test=f_y, dy_test=min_distance_delta, n_ideal=ideal_index)
    session.add(tfam)

# commit the transaction to the database
session.commit()

# close the session
session.close()

# display data
test_function_and_mapping = pd.read_sql_table('TestFunctionAndMapping', engine)
print(test_function_and_mapping)
list_of_figures_changed = []


for i, element in enumerate(list_of_ideal_candidates):
    i = i+1    
    var_name = 'var_ideal_my_func_changed' + str(i)
    
    globals()[var_name] = figure(x_axis_label='X-Axis', y_axis_label='Y-Axis', title="Found candidate from list of ideal #" + str(i) + " with diffs")
    x_values= element.get_training_data().get_x_values()
    y_values = element.get_training_data().get_y_values()
    n_ideal = element.get_ideal_data().get_n()
    x_values_diff = []
    y_values_diff = []
    p = globals()[var_name]
    all_diffs = []
    for j,tfam_n_ideal in enumerate(test_function_and_mapping.n_ideal):
        if tfam_n_ideal == n_ideal:
            x_values_diff.append(test_function_and_mapping.x_test[j]) 
            y_values_diff.append(test_function_and_mapping.y_test[j])
            vline = Span(location=test_function_and_mapping.x_test[j], dimension='height', line_color='red', line_width=0.5, line_dash=[6, 3])
            p.add_layout(vline)
            all_diffs.append(test_function_and_mapping.dy_test[j])
    TOOLTIPS = [        
        ("diff", "@diff"),
        ("(x,y)", "(@x, @y"+str(i)+")"),
    ]
    source=(ColumnDataSource(data={"x": x_values, "y"+str(i): np.array(y_values), "diff":[0] * len(x_values)}))    
    p.line(x='x', y='y'+str(i),source=source)
    p.dot(x='x', y='y'+str(i), color="green", size=20, source=(ColumnDataSource(data={"x": x_values_diff, "y"+str(i): np.array(y_values_diff), "diff": all_diffs})))
    p.add_tools(HoverTool(tooltips=TOOLTIPS))
    
    list_of_figures_changed.append(p)
    

# Afterwards, the results need to be saved into another fourcolumn-table in the SQLite database
grid = gridplot([training_data_to_plot, ideal_data_to_plot, list_of_ideal_candiate_figures, list_of_figures_changed])

# Render the plot
show(grid)    
