
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
import talib
import pandas_ta as ta
import dataUtility
import secretIngredient
import os.path

IST = pytz.timezone('Asia/Kolkata')

def getStatistics(stockCODE,stock,dfList,ha_dfList):
    output={}
    for idx, df in enumerate(dfList):
     output[idx]= {}   
     overall={}
     for index, row in df.iterrows():
        if index > 200 :
            if(index<df.shape[0]-11 ):
                testResult=[]
                day1=df.at[index+1, 'close']
                day2=df.at[index+2, 'close']
                day3=df.at[index+3, 'close']
                day4=df.at[index+4, 'close']
                day5=df.at[index+5, 'close']
                day6=df.at[index+6, 'close']
                day7=df.at[index+7, 'close']
                day8=df.at[index+8, 'close']
                day9=df.at[index+9, 'close']
                day10=df.at[index+10, 'close']

                testResult.append(["MA200VS100",secretIngredient.movingAverageFormula(df.at[index-1, 'MA200'],df.at[index-1, 'MA100'],row['MA200'],row['MA100']),index+1])
                testResult.append(["MA100VS50",secretIngredient.movingAverageFormula(df.at[index-1, 'MA100'],df.at[index-1, 'MA50'],row['MA100'],row['MA50']),index+1])
                testResult.append(["MA50VS20",secretIngredient.movingAverageFormula(df.at[index-1, 'MA50'],df.at[index-1, 'MA20'],row['MA50'],row['MA20']),index+1])

                for result in testResult:
                    if result[1]:
                        close=df.at[result[2], "open"]
                        dataUtility.storeInFile("./Results/details/"+result[0]+str(idx)+"data.csv",[datetime.fromtimestamp(int(df.at[result[2], 'date']),IST).strftime("%d/%m/%Y"),stock,stockCODE,float(day1)-float(close),float(day2)-float(close),float(day3)-float(close),float(day4)-float(close),float(day5)-float(close),float(day6)-float(close),float(day7)-float(close),float(day8)-float(close),float(day9)-float(close),float(day10)-float(close)])
                        #print([datetime.fromtimestamp(int(df.at[result[2], 'date']),IST).strftime("%d/%m/%Y"),result[0],stock,stockCODE,idx,close,float(day1)-float(close),float(day2)-float(close),float(day3)-float(close),float(day4)-float(close),float(day5)-float(close),float(day6)-float(close),float(day7)-float(close),float(day8)-float(close),float(day9)-float(close),float(day10)-float(close)])
                        if overall.get(result[0]):
                            overall[result[0]].append([datetime.fromtimestamp(int(df.at[result[2], 'date']),IST).strftime("%d/%m/%Y"),result[0],stock,stockCODE,idx,close,float(day1)-float(close),float(day2)-float(close),float(day3)-float(close),float(day4)-float(close),float(day5)-float(close),float(day6)-float(close),float(day7)-float(close),float(day8)-float(close),float(day9)-float(close),float(day10)-float(close)])
                        else:
                            overall[result[0]]=[]
                            overall[result[0]].append([datetime.fromtimestamp(int(df.at[result[2], 'date']),IST).strftime("%d/%m/%Y"),result[0],stock,stockCODE,idx,close,float(day1)-float(close),float(day2)-float(close),float(day3)-float(close),float(day4)-float(close),float(day5)-float(close),float(day6)-float(close),float(day7)-float(close),float(day8)-float(close),float(day9)-float(close),float(day10)-float(close)])
     for stratagy in overall:
        [total,win,totalAmount,totalWin]=dataUtility.calcWinWithPercentage(stratagy,overall,1)
        dataUtility.storeInFile("./Results/"+str(idx)+stratagy+"overAll.csv",[stockCODE,stratagy,total,win])
        output[idx][stratagy]=[total,win,totalAmount,totalWin]
        
    return output

                

def process(stockCODE,stock,stockID):
    #use this if money control didnt work | responseday = requests.get("https://api.upstox.com/historical/NSE_EQ/"+stockID+"/day?timestamp=")
    #data =responseday.json()
    timeLine=[["15",23],["30",45],["60",90],["1D",365]]
    if not os.path.isfile("./DFState/data"+stockCODE+timeLine[0][0]+".pkl"):
        dataList=dataUtility.getStockData(stockCODE,timeLine)
        [dfList,ha_dfList]=dataUtility.preProcess(dataList,stockCODE)
        return getStatistics(stockCODE,stock,dfList,ha_dfList) 
    else:
        [dfList,ha_dfList]=dataUtility.getPreLoadedData(timeLine,stockCODE)
        return getStatistics(stockCODE,stock,dfList,ha_dfList) 

    



def WatchStockMarket():
 with open('./Stocks/NSE_Script_code.csv') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    line_count = 0
    msg={}
    
    for row in csv_reader:
       try:
            print(row[1])
            output=process(row[0],row[1],row[2])
            for idx in output:
                for stratagies in output[idx]:
                    dataUtility.storeInFile("./Results/StockWiseStratagy/OverALLdata.csv",[row[0],row[1],str(idx)+stratagies,output[idx][stratagies][0],output[idx][stratagies][1],output[idx][stratagies][2],output[idx][stratagies][3],str(output[idx][stratagies][3]-output[idx][stratagies][2])])

                    if msg.get(str(idx)+stratagies):
                        msg[str(idx)+stratagies].append([output[idx][stratagies][0],output[idx][stratagies][1],output[idx][stratagies][2],output[idx][stratagies][3]])
                    else:
                        msg[str(idx)+stratagies]=[]
                        msg[str(idx)+stratagies].append([output[idx][stratagies][0],output[idx][stratagies][1],output[idx][stratagies][2],output[idx][stratagies][3]])
            line_count+= 1
       except Exception as e:
             print("Oops!", e, "occurred.")

    for x in msg:
                total=0
                sum=0
                totalAmount=0
                winAmount=0
                for i in msg[x]:
                    totalAmount=totalAmount+i[2]
                    winAmount=winAmount+i[3]
                    total=total+i[0]
                    sum=sum+i[1]
                print(x+"==============> "+str(sum)+"/"+str(total)+"====>"+str(totalAmount)+"/"+str(winAmount))
                print("\n")
    print(f'Processed {line_count} Stock.')

WatchStockMarket()