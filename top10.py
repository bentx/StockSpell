import requests
import pandas as pd
import csv
from csv import writer
import dataUtility
import stockFormula
import os
import numpy as np

def getTop(res12,res6,res3,date):
    top50=res12.loc
def getRolling(df,n):
    return df.rolling(n).apply(np.prod)


def process(mtl,ret_12,ret_6,ret_3,Time):
    for date in mtl.index[:-1]:
            stock_list=stockFormula.get_top10(ret_12,ret_6,ret_3,date)
            for i in range(0,10):
                dataUtility.storeInFile("./Results/top10Analysis/top10"+Time+".csv",[date,stock_list[i],str(mtl.loc[date:,stock_list[i]][1:2].values[0])])

def processdaily(mtl,ret_12,ret_6,ret_3,Time):
    for date in mtl.index[:-11]:
            stock_list=stockFormula.get_top10(ret_12,ret_6,ret_3,date)
            for i in range(0,10):
                result="Fail"
                val=0
                for j in range(1,11):
                    if(float(mtl.loc[date:,stock_list[i]][j:j+1].values[0])>=1.01):
                        result="Pass"
                        val=mtl.loc[date:,stock_list[i]][j:j+1].values[0]
                        break
                dataUtility.storeInFile("./Results/top10Analysis/top10"+Time+".csv",[date,stock_list[i],result,val])

def processdailyWithStratagy(mtl,ret_12,ret_6,ret_3,stockList,stratagy):
    for date in mtl.index[:-11]:
            stock_list=stockFormula.get_top10_WithStratagy(ret_12,ret_6,ret_3,date,stockList)
            shape = stock_list.shape
            for i in range(0,shape[1]):
                result="Fail"
                val=0
                for j in range(1,11):
                    if(float(mtl.loc[date:,stock_list[i]][j:j+1].values[0])>=1.01):
                        result="Pass"
                        val=mtl.loc[date:,stock_list[i]][j:j+1].values[0]
                        break
                dataUtility.storeInFile("./Results/top10AnalysisStratagy/top10"+stratagy,[date,stock_list[i],result,val])


def getTopAmongStratagy(rootdf):
    path = "./Results/details/"
    file_list = os.listdir(path) 
    for file in file_list:
        overalldata={}
        with open(f'./Results/details/{file}') as csv_file:
            print(f'Top10Processing {file}')
            csv_reader = csv.reader(csv_file, delimiter=',')
            for result in csv_reader:
                if result[0] in overalldata:
                    overalldata[result[0]].append(result[2])
                else:
                    overalldata[result[0]]=[]
                    overalldata[result[0]].append(result[2])
        for date in overalldata:
            dtl=(rootdf.pct_change()+1)[1:]
            dret_12,dret_6,dret_3 = stockFormula.get_rolling_ret(dtl,12),stockFormula.get_rolling_ret(dtl,6),stockFormula.get_rolling_ret(dtl,3)
            processdailyWithStratagy(dtl,dret_12,dret_6,dret_3,overalldata[date],file)





def getTopScorers(rootdf):
    rootdf =rootdf.dropna(axis=1)
    mtl=(rootdf.pct_change()+1)[1:].resample('M').prod()
    ret_12,ret_6,ret_3 = stockFormula.get_rolling_ret(mtl,12),stockFormula.get_rolling_ret(mtl,6),stockFormula.get_rolling_ret(mtl,3)
    process(mtl,ret_12,ret_6,ret_3,"Month")

    dtl=(rootdf.pct_change()+1)[1:]
    dret_12,dret_6,dret_3 = stockFormula.get_rolling_ret(dtl,12),stockFormula.get_rolling_ret(dtl,6),stockFormula.get_rolling_ret(dtl,3)
    processdaily(dtl,dret_12,dret_6,dret_3,"Day")

    dtl3=(rootdf.pct_change()+1)[1:].resample('3D').prod()
    dret3_12,dret3_6,dret3_3 = stockFormula.get_rolling_ret(dtl3,12),stockFormula.get_rolling_ret(dtl3,6),stockFormula.get_rolling_ret(dtl3,3)
    processdaily(dtl3,dret3_12,dret3_6,dret3_3,"Day3")

    dtl5=(rootdf.pct_change()+1)[1:].resample('5D').prod()
    dret5_12,dret5_6,dret5_3 = stockFormula.get_rolling_ret(dtl5,12),stockFormula.get_rolling_ret(dtl5,6),stockFormula.get_rolling_ret(dtl5,3)
    processdaily(dtl5,dret5_12,dret5_6,dret5_3,"Day5")
