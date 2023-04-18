'''
Created on 18.04.2023

@author: david
'''
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine, Column, Integer, String, Float

Base = declarative_base()

class CandiateFunctionAndMapping(Base):
    __tablename__ = 'CandiateFunctionAndMapping'
    
    id = Column(Integer, primary_key=True)
    #X (test func)
    x = Column(Float)
     
    #Y (test func)
    y = Column(Float) 
    #Delta Y (test func)
    dy = Column(Float)
     
    #Number of ideal func
    n = Column(Integer)
    
if __name__ == '__main__':
    pass