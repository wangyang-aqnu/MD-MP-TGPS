# -*- coding: utf-8 -*-
"""
Created on Wed Dec 19 21:36:23 2018

@author: Administrator
"""
import pandas as pd
import numpy as np
import math

def deg_K_items(filename):
  pre_double1=pd.read_csv(filename+r'pre_double.dat',sep='\t',header=0,index_col=0)
  pre_triple1=pd.read_csv(filename+r'pre_triple.dat',sep='\t',header=0,index_col=0)
  cumsum_items=pd.read_csv(filename+r'cumsum_items.dat',sep='\t',header=0,index_col=0)
  pre_hwL1=pd.read_csv(filename+r'pre_hwL.dat',sep='\t',header=0,index_col=0)
  pre_hwA1=pd.read_csv(filename+r'pre_hwA.dat',sep='\t',header=0,index_col=0)  
  sum2_degree=pd.read_csv(filename+r'sum2_degree.dat',sep='\t',header=0,index_col=0)  
  #pre_arima1=pd.read_csv(filename+r'pre_arima.dat',sep='\t',header=0,index_col=0)  
  
  
  pre_double=pre_double1.T

  pre_triple=pre_triple1.T
  
  pre_hwL=pre_hwL1.T
  pre_hwA=pre_hwA1.T
  
  
  #pre_arima=pre_arima1.T
  

  
  columns_name=[]
  rows_name=[]
  for  i in np.arange(1,sum2_degree.columns.size+1,1):
    columns_name.append(str(i))
  pre_double.columns=columns_name
  pre_triple.columns=columns_name
  
  pre_hwL.columns=columns_name
  pre_hwA.columns=columns_name
  
  #pre_arima.columns=columns_name
  
  for i in np.arange(1,sum2_degree.index.size+1,1):
      rows_name.append(str(i))
  
  sum2_degree.index=rows_name
  cumsum_items.index=rows_name

  dic_pre_double=pre_double.to_dict()
  dic_pre_triple=pre_triple.to_dict()
  dic_cumsum_items=cumsum_items.to_dict()
  dic_pre_hwL=pre_hwL.to_dict()
  dic_pre_hwA=pre_hwA.to_dict()
  #dic_pre_arima=pre_arima.to_dict()
  dic_sum2_degree=sum2_degree.to_dict()
  
  #print(dic_pre_hwL)
  #print(dic_cumsum_items)
  #print(dic_cumsum_items['1']['2'])
  #print(dic_pre_double)
  #print(dic_pre_triple)
  #print(dic_pre_double['1']['2'])
  return dic_pre_double,dic_pre_triple,dic_pre_hwL,dic_pre_hwA,dic_cumsum_items,dic_sum2_degree
  

'''
if __name__ == '__main__':
  deg_K_items(r'./ml/24T/sam1/')
'''   
    
    
