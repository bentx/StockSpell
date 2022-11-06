
import csv
import random
from datetime import datetime, timedelta
import time
import pytz
from pytz import timezone
from pydantic import BaseModel
from fastapi import FastAPI
import uvicorn
import pymongo
from pymongo import MongoClient
import requests
from pushbullet import Pushbullet
from fastapi.middleware.cors import CORSMiddleware
import pandas as pd
from csv import writer
import stockFormula
import talib
import pandas_ta as ta
import os.path
def getStockData(stockCode,timeList):
    data=[]
    for timeLine in timeList:
        todate = datetime.today()
        fromdate = todate - timedelta(days=timeLine[1])
        response = requests.get("https://priceapi.moneycontrol.com/techCharts/indianMarket/stock/history?symbol="+stockCode+"&resolution="+timeLine[0]+"&from="+str(int (time.mktime(fromdate.timetuple())))+"&to="+str(int (time.mktime(todate.timetuple()))))
        data.append([timeLine[0],response.json()])
    return data
def getPreLoadedData(timeLine,stockCode):
    print(" processing from state")
    dfList=[]
    ha_dfList=[]
    for t in timeLine:
        df = pd.read_pickle("./DFState/data"+stockCode+t[0]+".pkl")
        ha_df=pd.read_pickle("./DFState/HAdata"+stockCode+t[0]+".pkl")
        dfList.append(df.copy())
        ha_dfList.append(ha_df.copy())
    return [dfList,ha_dfList]


def preProcess(dataList,stockCode):
    dfList=[]
    ha_dfList=[]
    for data in dataList:
        df=stockFormula.convertToDF(data[1])
        df=stockFormula.MACD(df)
        df=stockFormula.VWMA(df)
        df=stockFormula.bollinger_bands(df)
        df=stockFormula.ADX(df)
        df=stockFormula.MovingAverage(df)
        df.to_pickle("./DFState/data"+stockCode+data[0]+".pkl")

        #hiken
        ha_df=stockFormula.heikin_ashi(df.copy())
        ha_df=stockFormula.MACD(ha_df)
        ha_df=stockFormula.VWMA(ha_df)
        ha_df=stockFormula.bollinger_bands(ha_df)
        ha_df=stockFormula.ADX(ha_df)
        ha_df=stockFormula.MovingAverage(ha_df)
        df.to_pickle("./DFState/HAdata"+stockCode+data[0]+".pkl")
        dfList.append(df.copy())
        ha_dfList.append(ha_df.copy())
        
    return [dfList,ha_dfList]

def storeInFile(fileName,data):
    with open( fileName, 'a',newline='', encoding='utf-8') as object:
                                writer_object = writer(object)
                                writer_object.writerow(data)
                                object.close()

def calcWinWithPercentage(stratagy,overall,percentage):
    total=0
    win=0
    totalAmount=0
    winAmount=0
    for result in overall[stratagy]:
        total=total+1
        previous =0
        proceed=True
        totalAmount=totalAmount+10000
        #print("######################################")
        for i in range(6,15):
            #print("initial"+str(result[i]))
            if result[i]>0 and proceed:           
                if i==14:
                    #print(result[0]+"finalLoop"+str(result[i]))
                    winAmount=winAmount+10000+((10000/result[5])*result[i])
                    #print(result[0]+"finalLoop@#################################"+str(winAmount))

                else:
                    current=stockFormula.percentageCalc(result[5],result[i]+result[5])             
                    if current>percentage:
                        win=win+1
                        #print(result[0]+"possitive_Win"+str(result[i]))
                        winAmount=winAmount+10000+((10000/result[5])*result[i])
                        #print(result[0]+"win_current_End@#################################"+str(winAmount))

                        proceed=False
                    elif previous>current:
                        #print(result[0]+"negative_current"+str(result[i]))
                        winAmount=winAmount+10000+((10000/result[5])*result[i])
                        #print(result[0]+"negative_current_End@#################################"+str(winAmount))
                        proceed=False
                    previous=current
            else:
                if i==14 and  proceed:
                    #print(result[0]+"finalLoop_"+str(result[i]))
                    winAmount=winAmount+10000+((10000/result[5])*result[i-1])
                    #print(result[0]+"finalLoop_@#################################"+str(winAmount))

                elif  proceed:
                    #print(result[0]+"negative_val"+str(result[i]))
                    winAmount=winAmount+10000+((10000/result[5])*result[i])
                    #print(result[0]+"negative_val@#################################"+str(winAmount))

                break
    return [total,win,totalAmount,winAmount]