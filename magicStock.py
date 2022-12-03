
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
import talib
import pandas_ta as ta
import dataUtility
import secretIngredient
import stockFormula
import os.path
import os



# logging.basicConfig(filename="application.log",
#                     format='%(message)s',
#                     filemode='w')
# logger = logging.getLogger()
# logger.setLevel(logging.INFO)
# handler = RotatingFileHandler('log/my_log.log', maxBytes=200000, backupCount=10)
# logger.addHandler(handler)


IST = pytz.timezone('Asia/Kolkata')

def getStatistics(stockCODE,stock,dfList,ha_dfList):
    ADX=[[0,25],[25,50],[50,75],[75,100]]
    RSI=[[0,25],[25,50],[50,75],[75,100]]
    WVA1=[[0,3000000],[3000000,8000000],[8000000,12000000],[14000000,80000000]]
    output={}
    for idx, df in enumerate(dfList):
     output[idx]= {}   
     overall={}
     for index, row in df.iterrows():
        if index > 200 :
                
                testResult=[]
                if( index<df.shape[0]-11 ):
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

                testResult.append(["MA200VS100",secretIngredient.movingAverageFormula(ha_dfList[idx],index,df.at[index-1, 'MA200'],df.at[index-1, 'MA100'],row['MA200'],row['MA100']),index+1])
                testResult.append(["MA100VS50",secretIngredient.movingAverageFormula(ha_dfList[idx],index,df.at[index-1, 'MA100'],df.at[index-1, 'MA50'],row['MA100'],row['MA50']),index+1])
                testResult.append(["MA50VS20",secretIngredient.movingAverageFormula(ha_dfList[idx],index,df.at[index-1, 'MA50'],df.at[index-1, 'MA20'],row['MA50'],row['MA20']),index+1])
                testResult.append(["MA100VS20",secretIngredient.movingAverageFormula(ha_dfList[idx],index,df.at[index-1, 'MA100'],df.at[index-1, 'MA20'],row['MA100'],row['MA20']),index+1])
                testResult.append(["MA200VS20",secretIngredient.movingAverageFormula(ha_dfList[idx],index,df.at[index-1, 'MA200'],df.at[index-1, 'MA20'],row['MA200'],row['MA20']),index+1])
                #testResult.append(["OPG",secretIngredient.OpenPercentageGap(df.at[index-1, 'close'],df.at[index, 'open'],df.at[index, 'av']),index])
                testResult.append(["1WA1",secretIngredient.WA1Stratagy1(ha_dfList[idx],index),index+1])
                testResult.append(["1WA2",secretIngredient.WA1Stratagy2(ha_dfList[idx],index),index+1])
                testResult.append(["bodyTouch200",secretIngredient.bodyTouch(ha_dfList[idx],index,'MA200'),index+1])
                testResult.append(["bodyTouch100",secretIngredient.bodyTouch(ha_dfList[idx],index,'MA100'),index+1])
                testResult.append(["wigTouch200",secretIngredient.wigTouch(ha_dfList[idx],index,'MA200'),index+1])
                testResult.append(["wigTouch100",secretIngredient.wigTouch(ha_dfList[idx],index,'MA100'),index+1])
                testResult.append(["TopGainer1",secretIngredient.TopGainer(df,index,1),index+1])
                testResult.append(["TopGainer2",secretIngredient.TopGainer(df,index,2),index+1])
                testResult.append(["RSAADX",secretIngredient.RSAADX(df,index),index+1])





                for result in testResult:
                    if result[1]:
                      if( index>df.shape[0]-2 ):
                            dataUtility.storeInFile("./Results/today/"+result[0]+str(idx)+"data.csv",[datetime.fromtimestamp(int(df.at[index, 'date']),IST).strftime("%b %d %Y %I:%M%p"),stock,stockCODE,dataUtility.findRange(WVA1,df.at[index, '1WVA']),dataUtility.findRange(ADX,df.at[index, 'adx']),dataUtility.findRange(RSI,df.at[index, 'rsi'])])

                      else:
                        close=df.at[result[2], "open"]
                        if result[0] =="OPG":
                            open=df.at[result[2], "open"]
                            high=df.at[result[2], "high"]
                            close=df.at[result[2], "close"]

                           # dataUtility.storeInFile("./Results/details/"+result[0]+str(idx)+"data.csv",[datetime.fromtimestamp(int(df.at[result[2], 'date']),IST).strftime("%b %d %Y %I:%M%p"),stock,stockCODE,float(close)-float(open),float(day1)-float(close),float(day2)-float(close),float(day3)-float(close),float(day4)-float(close),open])
                        else:
                             #logger.info(str(datetime.fromtimestamp(int(df.at[result[2], 'date']),IST).isoformat())+"|"+result[0]+"|"+stock+"|"+stockCODE+"|"+str(df.at[result[2], '1WVA'])+"|"+str(df.at[result[2], 'up'])+"|"+str(df.at[result[2], 'down'])+"|"+str(df.at[result[2], 'middle'])+"|"+str(df.at[result[2], 'adx'])+"|"+str(df.at[result[2], 'rsi'])+"|"+str(float(day1)-float(close))+"|"+str(float(day2)-float(close))+"|"+str(float(day3)-float(close))+"|"+str(float(day4)-float(close))+"|"+str(float(day5)-float(close))+"|"+str(float(day6)-float(close))+"|"+str(float(day7)-float(close))+"|"+str(float(day8)-float(close))+"|"+str(float(day9)-float(close))+"|"+str(float(day10)-float(close)))
                             dataUtility.storeInFile("./Results/details/"+result[0]+str(idx)+"data.csv",[datetime.fromtimestamp(int(df.at[result[2], 'date']),IST).strftime("%b %d %Y %I:%M%p"),stock,stockCODE,df.at[index, '1WVA'],df.at[index, 'adx'],df.at[index, 'rsi'],float(close),float(day1)-float(close),float(day2)-float(close),float(day3)-float(close),float(day4)-float(close),float(day5)-float(close),float(day6)-float(close),float(day7)-float(close),float(day8)-float(close),float(day9)-float(close),float(day10)-float(close)])

                        
                        #print([datetime.fromtimestamp(int(df.at[result[2], 'date']),IST).strftime("%b %d %Y %I:%M%p"),result[0],stock,stockCODE,idx,close,float(day1)-float(close),float(day2)-float(close),float(day3)-float(close),float(day4)-float(close),float(day5)-float(close),float(day6)-float(close),float(day7)-float(close),float(day8)-float(close),float(day9)-float(close),float(day10)-float(close)])
                        if overall.get(result[0]):
                            overall[result[0]].append([datetime.fromtimestamp(int(df.at[result[2], 'date']),IST).strftime("%b %d %Y %I:%M%p"),result[0],stock,stockCODE,idx,close,float(day1)-float(close),float(day2)-float(close),float(day3)-float(close),float(day4)-float(close),float(day5)-float(close),float(day6)-float(close),float(day7)-float(close),float(day8)-float(close),float(day9)-float(close),float(day10)-float(close)])
                        else:
                            overall[result[0]]=[]
                            overall[result[0]].append([datetime.fromtimestamp(int(df.at[result[2], 'date']),IST).strftime("%b %d %Y %I:%M%p"),result[0],stock,stockCODE,idx,close,float(day1)-float(close),float(day2)-float(close),float(day3)-float(close),float(day4)-float(close),float(day5)-float(close),float(day6)-float(close),float(day7)-float(close),float(day8)-float(close),float(day9)-float(close),float(day10)-float(close)])
     for stratagy in overall:
        [total,win,totalAmount,totalWin]=dataUtility.calcWinWithPercentage(stratagy,overall,1)
        dataUtility.storeInFile("./Results/"+str(idx)+stratagy+"overAll.csv",[stockCODE,stratagy,total,win])
        output[idx][stratagy]=[total,win,totalAmount,totalWin]
        
    return output

                

def process(stockCODE,stock,stockID):
    #use this if money control didnt work | responseday = requests.get("https://api.upstox.com/historical/NSE_EQ/"+stockID+"/day?timestamp=")
    #data =responseday.json()
    timeLine=[["1D",365]]
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
             
    line_count += 1
    print(f'Processed {line_count} lines.')
    
    
def analyzeResult():
    ADX=[[0,25],[25,50],[50,75],[75,100]]
    RSI=[[0,25],[25,50],[50,75],[75,100]]
    WVA1=[[0,3000000],[3000000,8000000],[8000000,12000000],[14000000,80000000]]
    path = "./Results/details/"
    file_list = os.listdir(path) 
    print("++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")

    for adx in ADX:
        for rsi in RSI:
            for wva1 in WVA1:
                for file in file_list:
                    with open(f'./Results/details/{file}') as csv_file:

                        csv_reader = csv.reader(csv_file, delimiter=',')
                        line_count = 0
                        visited=[]
                        total=0
                        active=0
                        win=0

                        stockVisited={}
                        total2=0
                        active2=0
                        win2=0
                        for result in csv_reader:
                            # total=total+1
                            # if result[0] not in visited and float(result[3])>wva1[0] and float(result[3])<wva1[1] and float(result[4])>adx[0] and float(result[4])<adx[1] and  float(result[5])>rsi[0] and float(result[5])<rsi[1]:
                            #     active=active+1
                            #     visited.append(result[0])
                            #     if dataUtility.calcRealProfit(result,visited):
                            #         win=win+1

    
                            total2=total2+1
                            if not stockVisited.get(result[2]):
                                stockVisited[result[2]]=[]
                            if result[0] not in stockVisited[result[2]] and float(result[3])>wva1[0] and float(result[3])<wva1[1] and float(result[4])>adx[0] and float(result[4])<adx[1] and  float(result[5])>rsi[0] and float(result[5])<rsi[1]:
                                active2=active2+1
                                stockVisited[result[2]].append(result[0])
                                if dataUtility.calcRealProfitInIsolation(result,stockVisited):
                                    win2=win2+1
                       # if active!=0:
                           # dataUtility.storeInFile("./Results/analysis/data.csv",[file,str(wva1[0])+"-"+str(wva1[1]),str(adx[0])+"-"+str(adx[1]),str(rsi[0])+"-"+str(rsi[1]),total,active,win])
                        
                        if active2!=0:
                            dataUtility.storeInFile("./Results/analysis/"+file,[file,str(wva1[0])+"-"+str(wva1[1]),str(adx[0])+"-"+str(adx[1]),str(rsi[0])+"-"+str(rsi[1]),total2,active2,win2])

                            print(f'file: {file}')
                            print(f'{wva1}|{adx}|{rsi}total: {total2} active: {active2} win: {win2}')
    print("++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")

def moniterResult():
    path = "./Results/today/"
    file_list = os.listdir(path) 
    for file in file_list:
             with open(f'./Results/today/{file}') as csv_file:
                    csv_reader = csv.reader(csv_file, delimiter=',')
                    for result in csv_reader:
                          key=result[3]+result[4]+result[5]
                          with open(f'./Results/analysis/{file}') as analysis_file:
                                analysis_reader = csv.reader(analysis_file, delimiter=',')
                                for analysisResult in analysis_reader:
                                    if stockFormula.findPercentage(analysisResult[6],analysisResult[5])>70 and key==analysisResult[1]+analysisResult[2]+analysisResult[3] :
                                        if os.path.exists(f'./Results/summory/{file}'):
                                            with open(f'./Results/summory/{file}') as summory_file:
                                                summory_reader = csv.reader(summory_file, delimiter=',')
                                                progressStatus=False
                                                for summory in summory_reader:
                                                   if result[2]==summory[2] and summory[8]=="PROGRESS":
                                                        print("noooooooooooooooooooooo")
                                                        progressStatus=True
                                                        break
                                                if not progressStatus:
                                                        dataUtility.storeInFile(f"./Results/summory/{file}",[result[0],result[0],result[2],file,key,analysisResult[4],analysisResult[5],analysisResult[6],"PROGRESS"])
                                        else:
                                           dataUtility.storeInFile(f"./Results/summory/{file}",[result[0],result[0],result[2],file,key,analysisResult[4],analysisResult[5],analysisResult[6],"PROGRESS"])





def updateResult():

    path = "./Results/summory/"
    file_list = os.listdir(path) 
    for file in file_list:
        sdf = pd.read_csv(f'./Results/summory/{file}',header = None)
        for rootindex, row in sdf.iterrows():
            try:
                if row[8]!="FAIL" and row[8]!="PASS":
                    fromdate = datetime.strptime(row[0], '%b %d %Y %I:%M%p')
                    todate = datetime.today()
                    diff=todate-fromdate
                    timeLine=[["1D",diff.days+1]]#becareful
                    dataList=dataUtility.getStockData(row[2],timeLine)
                    df=stockFormula.convertToDF(dataList[0][1])

                    open=df.at[1, 'open']
                    flag="PROGRESS"
                    for index, val in df.iterrows():
                        if index>1 :
                            if (10000/open)*(val['close']-open)>100: 
                                flag="PASS"
                                sdf.loc[rootindex, 1] = datetime.fromtimestamp(int(val['date']),IST).strftime("%b %d %Y %I:%M%p")
                                sdf.loc[rootindex, 9]= index 
                                break
                        if index==11:
                                sdf.loc[rootindex, 1] = datetime.fromtimestamp(int(val['date']),IST).strftime("%b %d %Y %I:%M%p")
                                sdf.loc[rootindex, 9]= index 
                                flag="FAIL"
                                break
                    if flag=="PROGRESS":
                        sdf.loc[rootindex, 1] = datetime.fromtimestamp(int(val['date']),IST).strftime("%b %d %Y %I:%M%p")
                        sdf.loc[rootindex, 9]= index 
                    
                    sdf.loc[rootindex, 8] = flag
                    sdf.to_csv(f'./Results/summory/{file}', header = None,index=False)

            except Exception as e:
                print("Oops!", e, "occurred.")

def resetDirectory():
    dirList=["./Results/analysis/","./Results/details/","./Results/StockWiseStratagy/","./Results/today/"]
    for dir in dirList:
        print(f'removing {dir}.......')
        if (os.path.exists(dir)):
            file_list = os.listdir(dir) 
            for file in file_list:
                os.remove(f'{dir}{file}')

resetDirectory()
WatchStockMarket()
analyzeResult()
updateResult()
moniterResult()
