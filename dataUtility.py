
import csv
import random
from datetime import datetime, timedelta
import time
import pytz
from pytz import timezone
from pydantic import BaseModel
import pymongo
from pymongo import MongoClient
import requests
from pushbullet import Pushbullet
import pandas as pd
from csv import writer
import stockFormula
import talib
import pandas_ta as ta
import os.path
def getStockData(stockCode,timeList):
    data=[]
    for timeLine in timeList:
        #todate = datetime.today()-timedelta(days=365)
        todate = datetime.today()
        fromdate = todate - timedelta(days=timeLine[1])
        #response = requests.get("https://priceapi.moneycontrol.com/techCharts/indianMarket/stock/history?symbol="+stockCode+"&resolution="+timeLine[0]+"&from="+str(int (time.mktime(fromdate.timetuple())))+"&to=1673827200&countback=365&currencyCode=INR",headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.76 Safari/537.36', "Upgrade-Insecure-Requests": "1","DNT": "1","Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8","Accept-Language": "en-US,en;q=0.5","Accept-Encoding": "gzip, deflate"}
#)      

        response = requests.get("https://priceapi.moneycontrol.com/techCharts/indianMarket/stock/history?symbol="+stockCode+"&resolution="+timeLine[0]+"&from="+str(int (time.mktime(fromdate.timetuple())))+"&to="+str(int (time.mktime(todate.timetuple())))+"&countback="+str(timeLine[1])+"&currencyCode=INR",headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.76 Safari/537.36', "Upgrade-Insecure-Requests": "1","DNT": "1","Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8","Accept-Language": "en-US,en;q=0.5","Accept-Encoding": "gzip, deflate"})
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
        df=stockFormula.RSI(df)
        df=stockFormula.VA(df,"1WVA")
        df=stockFormula.bollinger_bands(df)
        df=stockFormula.ADX(df)
        df=stockFormula.MovingAverage(df)
        df=stockFormula.AverageVolume(df)
        df['candle'] = df.apply(lambda row : stockFormula.candlefinder(row[1],row[4]), axis=1)

        #df.to_pickle("./DFState/data"+stockCode+data[0]+".pkl")

        #hiken
        ha_df=stockFormula.heikin_ashi(df.copy())
        ha_df=stockFormula.MACD(ha_df)
        ha_df=stockFormula.VWMA(ha_df)
        ha_df=stockFormula.RSI(ha_df)
        ha_df=stockFormula.VA(ha_df,"1WVA")
        ha_df=stockFormula.bollinger_bands(ha_df)
        ha_df=stockFormula.ADX(ha_df)
        ha_df=stockFormula.MovingAverage(ha_df)
        ha_df=stockFormula.AverageVolume(ha_df)

        #df.to_pickle("./DFState/HAdata"+stockCode+data[0]+".pkl")
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
            currentAmount=10000+((10000/result[5])*result[i])
            #print("initial"+str(result[i]))
            if result[i]>0 and proceed:           
                if i==14:
                    #print(result[0]+"finalLoop"+str(result[i]))
                    winAmount=winAmount+currentAmount
                    #print(result[0]+"finalLoop@#################################"+str(winAmount))

                else:
                    current=stockFormula.percentageCalc(result[5],result[i]+result[5])             
                    if currentAmount-10000>100:
                        win=win+1
                        #print(result[0]+"possitive_Win"+str(result[i]))
                        winAmount=winAmount+currentAmount
                        #print(result[0]+"win_current_End@#################################"+str(winAmount))

                        proceed=False
                    elif previous>current:
                        #print(result[0]+"negative_current"+str(result[i]))
                        winAmount=winAmount+currentAmount
                        #print(result[0]+"negative_current_End@#################################"+str(winAmount))
                        proceed=False
                    previous=current
            else:
                if i==14 and  proceed:
                    #print(result[0]+"finalLoop_"+str(result[i]))
                    winAmount=winAmount+currentAmount
                    #print(result[0]+"finalLoop_@#################################"+str(winAmount))

                elif  proceed:
                    #print(result[0]+"negative_val"+str(result[i]))
                    winAmount=winAmount+currentAmount
                    #print(result[0]+"negative_val@#################################"+str(winAmount))

                break
    return [total,win,totalAmount,winAmount]

def findCandleType(df,index):
    if ((df.loc[:, 'open'][index]<df.loc[:, 'close'][index])and(df.loc[:, 'open'][index]==df.loc[:, 'low'][index]) ):
        return "G"
    elif ((df.loc[:, 'open'][index]>df.loc[:, 'close'][index])and(df.loc[:, 'open'][index]==df.loc[:, 'high'][index]) ):
        return "R"
    elif ((df.loc[:, 'open'][index]<df.loc[:, 'close'][index]) ):
        return "G1"
    else:
        return "R1"  

def isTouchLow(df,index):
    if((df.loc[:, 'close'][index]<df.loc[:, 'down'][index])):
        return True
    else:
        return False

def calcRealProfit(result,visited):
     count =(10000/float(result[6]))
     for i in range(7,16):
        if(float(result[i])*count>100):
            return True
        else:
            date=datetime.strptime(result[0], '%b %d %Y %I:%M%p')
            date=date+timedelta(days=i-5)
            visited.append(date.strftime("%b %d %Y %I:%M%p"))
     return False

def calcRealProfitInIsolation(result,stockVisited):
     count =(10000/float(result[6]))
     for i in range(7,16):
        if(float(result[i])*count>100):
            for j in range(1,31):
                date=datetime.strptime(result[0], '%b %d %Y %I:%M%p')
                date=date+timedelta(days=j)
                stockVisited[result[2]].append(date.strftime("%b %d %Y %I:%M%p"))

            return True
        else:
            date=datetime.strptime(result[0], '%b %d %Y %I:%M%p')
            date=date+timedelta(days=i-5)
            stockVisited[result[2]].append(date.strftime("%b %d %Y %I:%M%p"))
     return False

def findRange(rangeList,val):
    for i in rangeList:
        if float(val)>float(i[0]) and float(val)<float(i[1]):
            return str(i[0])+"-"+str(i[1])
    return "null"    

def FCTP(df,index):
    if float(df.at[index, 'close']) > float(df.at[index, 'open']):
        return "G"
    else:
        return "R"  