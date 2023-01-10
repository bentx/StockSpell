import requests
import pandas as pd
import csv
from csv import writer
import dataUtility
import stockFormula
import numpy as np

def getTop(res12,res6,res3,date):
    top50=res12.loc
def getRolling(df,n):
    return df.rolling(n).apply(np.prod)

def getTopScorers(rootdf):
    rootdf =rootdf.dropna(axis=1)
    mtl=(rootdf.pct_change()+1)[1:].resample('M').prod()
    ret_12,ret_6,ret_3 = stockFormula.get_rolling_ret(mtl,12),stockFormula.get_rolling_ret(mtl,6),stockFormula.get_rolling_ret(mtl,3)
    for date in mtl.index[:-1]:
            stock_list=stockFormula.get_top10(ret_12,ret_6,ret_3,date)
            for i in range(0,10):
                row=[]           
                row.append(date)
                row.append(stock_list[i])
                row.append(mtl.loc[date:,stock_list[i]][1:2])
                dataUtility.storeInFile("./Results/analysis/top10.csv",[date,stock_list[i],str(mtl.loc[date:,stock_list[i]][1:2])])

