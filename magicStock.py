
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
import top10



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
        if index > 100 :
                
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
                if index > 500: 

                # testResult.append(["MA200VS100",secretIngredient.movingAverageFormula(ha_dfList[idx],index,df.at[index-1, 'MA200'],df.at[index-1, 'MA100'],row['MA200'],row['MA100']),index+1])
                # testResult.append(["MA100VS50",secretIngredient.movingAverageFormula(ha_dfList[idx],index,df.at[index-1, 'MA100'],df.at[index-1, 'MA50'],row['MA100'],row['MA50']),index+1])
                # testResult.append(["MA50VS20",secretIngredient.movingAverageFormula(ha_dfList[idx],index,df.at[index-1, 'MA50'],df.at[index-1, 'MA20'],row['MA50'],row['MA20']),index+1])
                # testResult.append(["MA100VS20",secretIngredient.movingAverageFormula(ha_dfList[idx],index,df.at[index-1, 'MA100'],df.at[index-1, 'MA20'],row['MA100'],row['MA20']),index+1])
                # testResult.append(["MA200VS20",secretIngredient.movingAverageFormula(ha_dfList[idx],index,df.at[index-1, 'MA200'],df.at[index-1, 'MA20'],row['MA200'],row['MA20']),index+1])
   
                #testResult.append(["OPG",secretIngredient.OpenPercentageGap(df.at[index-1, 'close'],df.at[index, 'open'],df.at[index, 'av']),index])
   
                    testResult.append(["1WA1",secretIngredient.WA1Stratagy1(ha_dfList[idx],index),index+1])
                    testResult.append(["1WA2",secretIngredient.WA1Stratagy2(ha_dfList[idx],index),index+1])
                    # testResult.append(["bodyTouch200",secretIngredient.bodyTouch(ha_dfList[idx],index,'MA200'),index+1])
                    # testResult.append(["bodyTouch100",secretIngredient.bodyTouch(ha_dfList[idx],index,'MA100'),index+1])
                    # testResult.append(["wigTouch200",secretIngredient.wigTouch(ha_dfList[idx],index,'MA200'),index+1])
                    # testResult.append(["wigTouch100",secretIngredient.wigTouch(ha_dfList[idx],index,'MA100'),index+1])
                    # testResult.append(["TopGainer1",secretIngredient.TopGainer(df,index,1),index+1])
                    # testResult.append(["TopGainer2",secretIngredient.TopGainer(df,index,2),index+1])
                    testResult.append(["RSAADX",secretIngredient.RSAADX(df,index),index+1])
                    # #testResult.append(["linebreak",secretIngredient.findTrend(df,index,120,3),index+1])
                    # testResult.append(["TrianglePattern",secretIngredient.trianglePattern(df,index,120,3),index+1])
                    testResult.append(["TrianglePatternWithHA",secretIngredient.trianglePattern(ha_dfList[idx],index,120,3),index+1])
                    testResult.append(["PDCB",secretIngredient.PDCB(df,index),index+1])
                    testResult.append(["PP",secretIngredient.PP(ha_dfList[idx],index,df),index+1])
                    testResult.append(["PPW",secretIngredient.PPW(ha_dfList[idx],index),index+1])
                else:
                    testResult.append(["TrianglePatternWithHA",secretIngredient.trianglePattern(ha_dfList[idx],index,99,3),index+1])
                    testResult.append(["PP",secretIngredient.PP(ha_dfList[idx],index,df),index+1])
                    testResult.append(["PPW",secretIngredient.PPW(ha_dfList[idx],index),index+1])









                pattern=""
                for result in testResult:
                    if result[1][0]:
                        pattern+=result[0]

                for result in testResult:
                    if result[1][0]:
                      if( index>df.shape[0]-2 ):
                            dataUtility.storeInFile("./Results/today/"+result[0]+str(idx)+"data.csv",[datetime.fromtimestamp(int(df.at[index, 'date']),IST).strftime("%b %d %Y %I:%M%p"),stock,stockCODE,dataUtility.findRange(WVA1,df.at[index, '1WVA']),dataUtility.findRange(ADX,df.at[index, 'adx']),dataUtility.findRange(RSI,df.at[index, 'rsi']),result[1][1],pattern])

                      else:
                        close=df.at[result[2], "open"]
                        if result[0] =="OPG":
                            open=df.at[result[2], "open"]
                            high=df.at[result[2], "high"]
                            close=df.at[result[2], "close"]

                           # dataUtility.storeInFile("./Results/details/"+result[0]+str(idx)+"data.csv",[datetime.fromtimestamp(int(df.at[result[2], 'date']),IST).strftime("%b %d %Y %I:%M%p"),stock,stockCODE,float(close)-float(open),float(day1)-float(close),float(day2)-float(close),float(day3)-float(close),float(day4)-float(close),open])
                        else:
                             #logger.info(str(datetime.fromtimestamp(int(df.at[result[2], 'date']),IST).isoformat())+"|"+result[0]+"|"+stock+"|"+stockCODE+"|"+str(df.at[result[2], '1WVA'])+"|"+str(df.at[result[2], 'up'])+"|"+str(df.at[result[2], 'down'])+"|"+str(df.at[result[2], 'middle'])+"|"+str(df.at[result[2], 'adx'])+"|"+str(df.at[result[2], 'rsi'])+"|"+str(float(day1)-float(close))+"|"+str(float(day2)-float(close))+"|"+str(float(day3)-float(close))+"|"+str(float(day4)-float(close))+"|"+str(float(day5)-float(close))+"|"+str(float(day6)-float(close))+"|"+str(float(day7)-float(close))+"|"+str(float(day8)-float(close))+"|"+str(float(day9)-float(close))+"|"+str(float(day10)-float(close)))
                             dataUtility.storeInFile("./Results/details/"+result[0]+str(idx)+"data.csv",[datetime.fromtimestamp(int(df.at[result[2], 'date']),IST).strftime("%b %d %Y %I:%M%p"),stock,stockCODE,df.at[index, '1WVA'],df.at[index, 'adx'],df.at[index, 'rsi'],float(close),float(day1)-float(close),float(day2)-float(close),float(day3)-float(close),float(day4)-float(close),float(day5)-float(close),float(day6)-float(close),float(day7)-float(close),float(day8)-float(close),float(day9)-float(close),float(day10)-float(close),result[1][1],pattern])

                        
                        #print([datetime.fromtimestamp(int(df.at[result[2], 'date']),IST).strftime("%b %d %Y %I:%M%p"),result[0],stock,stockCODE,idx,close,float(day1)-float(close),float(day2)-float(close),float(day3)-float(close),float(day4)-float(close),float(day5)-float(close),float(day6)-float(close),float(day7)-float(close),float(day8)-float(close),float(day9)-float(close),float(day10)-float(close)])
                        if overall.get(result[0]):
                            overall[result[0]].append([datetime.fromtimestamp(int(df.at[result[2], 'date']),IST).strftime("%b %d %Y %I:%M%p"),result[0],stock,stockCODE,idx,close,float(day1)-float(close),float(day2)-float(close),float(day3)-float(close),float(day4)-float(close),float(day5)-float(close),float(day6)-float(close),float(day7)-float(close),float(day8)-float(close),float(day9)-float(close),float(day10)-float(close)])
                        else:
                            overall[result[0]]=[]
                            overall[result[0]].append([datetime.fromtimestamp(int(df.at[result[2], 'date']),IST).strftime("%b %d %Y %I:%M%p"),result[0],stock,stockCODE,idx,close,float(day1)-float(close),float(day2)-float(close),float(day3)-float(close),float(day4)-float(close),float(day5)-float(close),float(day6)-float(close),float(day7)-float(close),float(day8)-float(close),float(day9)-float(close),float(day10)-float(close)])
     for stratagy in overall:
        [total,win,totalAmount,totalWin]=dataUtility.calcWinWithPercentage(stratagy,overall,1)
        dataUtility.storeInFile("./Results/overall/"+str(idx)+stratagy+"overAll.csv",[stockCODE,stratagy,total,win])
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
    rootdf = pd.DataFrame()
    swingStock=dataUtility.getSwingStock()

    
    for row in csv_reader:
        if row[1] in swingStock:
            try:
                print(row[1])
                stockCODE=row[0]
                stock=row[1]
                timeLine=[["1D",665],["60",665]]
                if not os.path.isfile("./DFState/data"+stockCODE+timeLine[0][0]+".pkl"):
                    dataList=dataUtility.getStockData(stockCODE,timeLine)
                    [dfList,ha_dfList]=dataUtility.preProcess(dataList,stockCODE)

                    if(int(dfList[0].at[0, 'date'])<1517410600):#To remove the unwanted 2000 dates
                        print(stockCODE)
                        dataUtility.storeInFile("./Results/scam.csv",[datetime.fromtimestamp(int(dfList[0].at[0, 'date']),IST).strftime("%b %d %Y %I:%M%p"),stock,stockCODE])
                        continue
                    getStatistics(stockCODE,stock,dfList,ha_dfList)

                    dfList[0]['date'] = pd.to_datetime(dfList[0]['date'],unit='s')
                    df=dfList[0][['date','close']]
                    df=df.set_index('date')
                    df.rename(columns = {'close':row[0]}, inplace = True)
                    rootdf=pd.concat([rootdf, df], axis=1) 
                else:
                    [dfList,ha_dfList]=dataUtility.getPreLoadedData(timeLine,stockCODE)
                    getStatistics(stockCODE,stock,dfList,ha_dfList) 

                    dfList[0]['date'] = pd.to_datetime(dfList[0]['date'],unit='s')
                    df=dfList[0][['date','close']]
                    df=df.set_index('date')
                    df.rename(columns = {'close':row[0]}, inplace = True)
                    rootdf=pd.concat([rootdf, df], axis=1)
                # for idx in output:
                #     for stratagies in output[idx]:
                #         dataUtility.storeInFile("./Results/StockWiseStratagy/OverALLdata.csv",[row[0],row[1],str(idx)+stratagies,output[idx][stratagies][0],output[idx][stratagies][1],output[idx][stratagies][2],output[idx][stratagies][3],str(output[idx][stratagies][3]-output[idx][stratagies][2])])

                #         if msg.get(str(idx)+stratagies):
                #             msg[str(idx)+stratagies].append([output[idx][stratagies][0],output[idx][stratagies][1],output[idx][stratagies][2],output[idx][stratagies][3]])
                #         else:
                #             msg[str(idx)+stratagies]=[]
                #             msg[str(idx)+stratagies].append([output[idx][stratagies][0],output[idx][stratagies][1],output[idx][stratagies][2],output[idx][stratagies][3]])
                line_count+= 1
            except Exception as e:
                print("Oops!", e, "occurred.")
    #top10.getTopScorers(rootdf)
    #top10.getTopAmongStratagy(rootdf)
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
                        print(f'Processing {file}')
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

                            #print(f'file: {file}')
                            #print(f'{wva1}|{adx}|{rsi}total: {total2} active: {active2} win: {win2}')
    print("++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")

def moniterResult():
    print(f'++++++++++++++++++++++++++++++++++++++++++++++++++++++++Monitoring Results')

    path = "./Results/today/"
    file_list = os.listdir(path) 
    for file in file_list:
             with open(f'./Results/today/{file}') as csv_file:
                    print(f'Processing {file}')

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
                                                        progressStatus=True
                                                        break
                                                if not progressStatus:
                                                        dataUtility.storeInFile(f"./Results/summory/{file}",[result[0],result[0],result[2],file,key,analysisResult[4],analysisResult[5],analysisResult[6],"PROGRESS",'0'])
                                        else:
                                           dataUtility.storeInFile(f"./Results/summory/{file}",[result[0],result[0],result[2],file,key,analysisResult[4],analysisResult[5],analysisResult[6],"PROGRESS",'0'])





def updateResult():
    print(f'+++++++++++++++++++++++++++++++++++++++++++++++++++updateResult')

    path = "./Results/summory/"
    file_list = os.listdir(path) 
    for file in file_list:
        sdf = pd.read_csv(f'./Results/summory/{file}',header = None)
        print(f'Processing {file}')

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


def moniter_breakout():
    print(f'+++++++++++++++++++++++++++++++++++++++++++++++++++moniter breakout')

    path = "./Results/breakout/"
    file_list = os.listdir(path) 
    for file in file_list:
        sdf = pd.read_csv(f'./Results/breakout/{file}',header = None)
        print(f'Processing {file}')

        for rootindex, row in sdf.iterrows():
                if row[6]!="DROP" and row[6]!="PASS":
                    todate = datetime.today()
                    fromdate = datetime.strptime(row[0], '%b %d %Y %I:%M%p')
                    tilldate = datetime.strptime(row[1], '%b %d %Y %I:%M%p')
                    if todate > tilldate:
                        sdf.loc[rootindex, 6]= "DROP"
                        sdf.to_csv(f'./Results/summory/{file}', header = None,index=False)
                    else:
                        diff=tilldate-fromdate
                        timeLine=[["1D",1]]#becareful
                        dataList=dataUtility.getStockData(row[3],timeLine)
                        df=stockFormula.convertToDF(dataList[0][1])
                        slope,intercept =stockFormula.get_linear_equation(float(0),float(row[4]),float(diff.days),float(row[5]))
                        currentdate = datetime.fromtimestamp(int( df.iloc[-1]['date']))
                        current_x=currentdate-fromdate
                        if stockFormula.check_breakout(current_x.days, df.iloc[-1]['close'], slope,intercept ):
                            sdf.loc[rootindex, 6]= "PASS" 
                        else:
                            sdf.loc[rootindex, 6]= "PROGRESS"
                        sdf.to_csv(f'./Results/breakout/{file}', header = None,index=False)

            

    

def resetDirectory():
    dirList=["./Results/analysis/","./Results/details/","./Results/today/","./Results/top10Analysis/","./Results/top10AnalysisStratagy/","./Results/overall/"]
    for dir in dirList:
        if (os.path.exists(dir)):
            print(f'removing {dir}.......')
            file_list = os.listdir(dir) 
            for file in file_list:
                os.remove(f'{dir}{file}')
        if(not os.path.exists(dir)):
            print(f'adding {dir}.......')
            os.mkdir(dir)
            
def monitor_top_gainer():
    print("monitor top gainer")
    #check top gainers part
    if(not os.path.exists("./Results/topGainers/")):
            print(f'adding ./Results/topGainers/.......')
            os.mkdir('./Results/topGainers/')
    tg = dataUtility.get_top_gainers()
    #tg={"legends":[["NIFTY","NIFTY 50"],["BANKNIFTY","BANK NIFTY"],["NIFTYNEXT50","NIFTY NEXT 50"],["SecGtr20","Securities > Rs 20"],["SecLwr20","Securities < Rs 20"],["FOSec","F&O Securities"],["allSec","All Securities"]],"NIFTY":{"data":[{"symbol":"ADANIPORTS","series":"EQ","open_price":664,"high_price":694.15,"low_price":659.5,"ltp":691,"prev_price":664.95,"net_price":3.92,"trade_quantity":6340270,"turnover":42969.911871000004,"market_type":"N","ca_ex_dt":"14-Jul-2022","ca_purpose":"Dividend - Rs 5 Per Share","perChange":3.92},{"symbol":"ADANIENT","series":"EQ","open_price":1888,"high_price":1983,"low_price":1872.1,"ltp":1955,"prev_price":1890,"net_price":3.44,"trade_quantity":7541150,"turnover":145819.446975,"market_type":"N","ca_ex_dt":"14-Jul-2022","ca_purpose":"Dividend - Re 1 Per Share","perChange":3.44},{"symbol":"TATAMOTORS","series":"EQ","open_price":509.8,"high_price":526.4,"low_price":504.75,"ltp":525,"prev_price":508.45,"net_price":3.25,"trade_quantity":19343560,"turnover":100143.54447600001,"market_type":"N","ca_ex_dt":"18-Jul-2016","ca_purpose":"Dividend - Re 0.20/- Per Share","perChange":3.25},{"symbol":"TECHM","series":"EQ","open_price":1056.55,"high_price":1078.75,"low_price":1049,"ltp":1072,"prev_price":1048.7,"net_price":2.22,"trade_quantity":2624323,"turnover":28065.0350266,"market_type":"N","ca_ex_dt":"09-Nov-2022","ca_purpose":"Special Dividend - Rs 18 Per Share","perChange":2.22},{"symbol":"INFY","series":"EQ","open_price":1256.05,"high_price":1273.3,"low_price":1252.8,"ltp":1269,"prev_price":1246,"net_price":1.85,"trade_quantity":11094136,"turnover":140655.8938624,"market_type":"N","ca_ex_dt":"02-Jun-2023","ca_purpose":"Annual General Meeting/Dividend - Rs 17.50 Per Share","perChange":1.85},{"symbol":"HCLTECH","series":"EQ","open_price":1088.6,"high_price":1104,"low_price":1082.45,"ltp":1094,"prev_price":1079.9,"net_price":1.31,"trade_quantity":1984436,"turnover":21769.0644764,"market_type":"N","ca_ex_dt":"28-Apr-2023","ca_purpose":"Interim Dividend - Rs 18 Per Share","perChange":1.31},{"symbol":"AXISBANK","series":"EQ","open_price":920.9,"high_price":927,"low_price":908.95,"ltp":926,"prev_price":914.7,"net_price":1.24,"trade_quantity":8393002,"turnover":76958.7925388,"market_type":"N","ca_ex_dt":"07-Jul-2022","ca_purpose":"Dividend - Rs 1 Per Share","perChange":1.24},{"symbol":"M&M","series":"EQ","open_price":1252.9,"high_price":1262.45,"low_price":1237.45,"ltp":1258,"prev_price":1245.5,"net_price":1,"trade_quantity":1588996,"turnover":19903.446096800002,"market_type":"N","ca_ex_dt":"14-Jul-2022","ca_purpose":"Annual General Meeting/Dividend - Rs 11.55 Per Share","perChange":1},{"symbol":"ULTRACEMCO","series":"EQ","open_price":7637,"high_price":7689.15,"low_price":7585.1,"ltp":7680,"prev_price":7604.15,"net_price":1,"trade_quantity":138709,"turnover":10605.412722000001,"market_type":"N","ca_ex_dt":"02-Aug-2022","ca_purpose":"Annual General Meeting/Dividend - Rs 38 Per Share","perChange":1},{"symbol":"GRASIM","series":"EQ","open_price":1710,"high_price":1723.95,"low_price":1685,"ltp":1720.55,"prev_price":1705.7,"net_price":0.87,"trade_quantity":241696,"turnover":4114.1734816,"market_type":"N","ca_ex_dt":"11-Aug-2022","ca_purpose":"Annual General Meeting/Dividend - Rs 5 Per Share/Special Dividend - Rs 5 Per Share","perChange":0.87},{"symbol":"WIPRO","series":"EQ","open_price":384.8,"high_price":388.2,"low_price":383.5,"ltp":385.9,"prev_price":382.6,"net_price":0.86,"trade_quantity":3640791,"turnover":14056.7299719,"market_type":"N","ca_ex_dt":"24-Jan-2023","ca_purpose":"Interim Dividend - Re  1 Per Share","perChange":0.86},{"symbol":"ICICIBANK","series":"EQ","open_price":951.45,"high_price":956,"low_price":941.6,"ltp":954,"prev_price":946.5,"net_price":0.79,"trade_quantity":15427412,"turnover":146313.575408,"market_type":"N","ca_ex_dt":"08-Aug-2022","ca_purpose":"Dividend - Rs 5 Per Share","perChange":0.79},{"symbol":"TCS","series":"EQ","open_price":3210,"high_price":3234.5,"low_price":3203.05,"ltp":3224.55,"prev_price":3199.85,"net_price":0.77,"trade_quantity":1152449,"turnover":37107.9358408,"market_type":"N","ca_ex_dt":"16-Jan-2023","ca_purpose":"Interim Dividend - Rs 8 Per Share Special Dividend - Rs 67 Per Share","perChange":0.77},{"symbol":"KOTAKBANK","series":"EQ","open_price":1930,"high_price":1946.85,"low_price":1923.5,"ltp":1942,"prev_price":1927.4,"net_price":0.76,"trade_quantity":3946927,"turnover":76300.0193005,"market_type":"N","ca_ex_dt":"11-Aug-2022","ca_purpose":"Dividend - Rs 1.10 Per Share","perChange":0.76},{"symbol":"INDUSINDBK","series":"EQ","open_price":1243,"high_price":1251,"low_price":1221.6,"ltp":1247.6,"prev_price":1238.9,"net_price":0.7,"trade_quantity":2366675,"turnover":29224.64957,"market_type":"N","ca_ex_dt":"11-Aug-2022","ca_purpose":"Annual General Meeting/Dividend - Rs 8.50 Per Share","perChange":0.7},{"symbol":"MARUTI","series":"EQ","open_price":9060,"high_price":9118.2,"low_price":8960.55,"ltp":9108,"prev_price":9053.3,"net_price":0.6,"trade_quantity":543472,"turnover":49029.0003968,"market_type":"N","ca_ex_dt":"03-Aug-2022","ca_purpose":"Dividend - Rs 60 Per Share","perChange":0.6},{"symbol":"BHARTIARTL","series":"EQ","open_price":799.35,"high_price":808.35,"low_price":793.25,"ltp":804.1,"prev_price":799.35,"net_price":0.59,"trade_quantity":3432240,"turnover":27484.005024000002,"market_type":"N","ca_ex_dt":"01-Aug-2022","ca_purpose":"Dividend - Rs 3 Per Share","perChange":0.59},{"symbol":"HINDUNILVR","series":"EQ","open_price":2628.65,"high_price":2649,"low_price":2600.65,"ltp":2641,"prev_price":2627.55,"net_price":0.51,"trade_quantity":1174757,"turnover":30819.6324193,"market_type":"N","ca_ex_dt":"01-Nov-2022","ca_purpose":"Interim Dividend - Rs 17 Per Share","perChange":0.51},{"symbol":"RELIANCE","series":"EQ","open_price":2434.05,"high_price":2445.95,"low_price":2418.85,"ltp":2444,"prev_price":2434.05,"net_price":0.41,"trade_quantity":3715280,"turnover":90381.988088,"market_type":"N","ca_ex_dt":"18-Aug-2022","ca_purpose":"Dividend - Rs 8 Per Share","perChange":0.41},{"symbol":"HINDALCO","series":"EQ","open_price":408,"high_price":408.4,"low_price":400.4,"ltp":407.75,"prev_price":406.5,"net_price":0.31,"trade_quantity":5523299,"turnover":22332.907176599998,"market_type":"N","ca_ex_dt":"11-Aug-2022","ca_purpose":"Annual General Meeting/Dividend - Rs 4 Per Share","perChange":0.31}],"timestamp":"19-May-2023 16:00:14"},"BANKNIFTY":{"data":[{"symbol":"PNB","series":"EQ","open_price":48.85,"high_price":49.6,"low_price":48.35,"ltp":49.45,"prev_price":48.45,"net_price":2.06,"trade_quantity":46965076,"turnover":23003.4942248,"market_type":"N","ca_ex_dt":"22-Jun-2022","ca_purpose":"Annual General Meeting/Dividend - Rs 0.64 Per Share","perChange":2.06},{"symbol":"AXISBANK","series":"EQ","open_price":920.9,"high_price":927,"low_price":908.95,"ltp":926,"prev_price":914.7,"net_price":1.24,"trade_quantity":8393002,"turnover":76958.7925388,"market_type":"N","ca_ex_dt":"07-Jul-2022","ca_purpose":"Dividend - Rs 1 Per Share","perChange":1.24},{"symbol":"AUBANK","series":"EQ","open_price":747.6,"high_price":756,"low_price":734,"ltp":755.5,"prev_price":747.6,"net_price":1.06,"trade_quantity":2181998,"turnover":16272.4682848,"market_type":"N","ca_ex_dt":"28-Jul-2022","ca_purpose":"Dividend - Rs 0.50 Per Share","perChange":1.06},{"symbol":"ICICIBANK","series":"EQ","open_price":951.45,"high_price":956,"low_price":941.6,"ltp":954,"prev_price":946.5,"net_price":0.79,"trade_quantity":15427412,"turnover":146313.575408,"market_type":"N","ca_ex_dt":"08-Aug-2022","ca_purpose":"Dividend - Rs 5 Per Share","perChange":0.79},{"symbol":"KOTAKBANK","series":"EQ","open_price":1930,"high_price":1946.85,"low_price":1923.5,"ltp":1942,"prev_price":1927.4,"net_price":0.76,"trade_quantity":3946927,"turnover":76300.0193005,"market_type":"N","ca_ex_dt":"11-Aug-2022","ca_purpose":"Dividend - Rs 1.10 Per Share","perChange":0.76},{"symbol":"BANKBARODA","series":"EQ","open_price":181,"high_price":182.35,"low_price":178,"ltp":181.7,"prev_price":180.35,"net_price":0.75,"trade_quantity":18643969,"turnover":33641.1776636,"market_type":"N","ca_ex_dt":"17-Jun-2022","ca_purpose":"Annual General Meeting/Dividend - Rs 2.85 Per Share","perChange":0.75},{"symbol":"INDUSINDBK","series":"EQ","open_price":1243,"high_price":1251,"low_price":1221.6,"ltp":1247.6,"prev_price":1238.9,"net_price":0.7,"trade_quantity":2366675,"turnover":29224.64957,"market_type":"N","ca_ex_dt":"11-Aug-2022","ca_purpose":"Annual General Meeting/Dividend - Rs 8.50 Per Share","perChange":0.7},{"symbol":"SBIN","series":"EQ","open_price":579,"high_price":586.25,"low_price":569.9,"ltp":575.65,"prev_price":574.2,"net_price":0.25,"trade_quantity":42293962,"turnover":243638.5974972,"market_type":"N","ca_ex_dt":"25-May-2022","ca_purpose":"Dividend - Rs 7.10 Per Share","perChange":0.25},{"symbol":"HDFCBANK","series":"EQ","open_price":1648,"high_price":1650,"low_price":1631.55,"ltp":1646.5,"prev_price":1645,"net_price":0.09,"trade_quantity":15230166,"turnover":250003.17489,"market_type":"N","ca_ex_dt":"16-May-2023","ca_purpose":"Dividend - Rs 19 Per Share","perChange":0.09},{"symbol":"IDFCFIRSTB","series":"EQ","open_price":66.95,"high_price":67.15,"low_price":65.65,"ltp":66.75,"prev_price":66.7,"net_price":0.07,"trade_quantity":19419804,"turnover":12894.749855999999,"market_type":"N","ca_ex_dt":"23-Jul-2018","ca_purpose":"Dividend Re 0.75 Per Share","perChange":0.07}],"timestamp":"19-May-2023 16:00:14"},"NIFTYNEXT50":{"data":[{"symbol":"AWL","series":"EQ","open_price":378.75,"high_price":412.2,"low_price":366,"ltp":403.95,"prev_price":378,"net_price":6.87,"trade_quantity":6990238,"turnover":27657.5756708,"market_type":"N","ca_ex_dt":"19-Aug-2022","ca_purpose":"Annual General Meeting","perChange":6.87},{"symbol":"ADANITRANS","series":"EQ","open_price":729.05,"high_price":789.15,"low_price":714.05,"ltp":789.15,"prev_price":751.6,"net_price":5,"trade_quantity":4723254,"turnover":35286.4859832,"market_type":"N","ca_ex_dt":"18-Jul-2022","ca_purpose":"Annual General Meeting","perChange":5},{"symbol":"ADANIGREEN","series":"EQ","open_price":839,"high_price":903.55,"low_price":818.6,"ltp":903.55,"prev_price":860.55,"net_price":5,"trade_quantity":2849747,"turnover":24868.887144899996,"market_type":"N","ca_ex_dt":"18-Jul-2022","ca_purpose":"Annual General Meeting","perChange":5},{"symbol":"ATGL","series":"EQ","open_price":633.35,"high_price":699.95,"low_price":633.35,"ltp":699.1,"prev_price":666.65,"net_price":4.87,"trade_quantity":11382817,"turnover":75266.6008491,"market_type":"N","ca_ex_dt":"14-Jul-2022","ca_purpose":"Dividend - Rs 0.25 Per Share","perChange":4.87},{"symbol":"DLF","series":"EQ","open_price":460.9,"high_price":473,"low_price":453.5,"ltp":472.85,"prev_price":459.95,"net_price":2.8,"trade_quantity":8398165,"turnover":39060.705231500004,"market_type":"N","ca_ex_dt":"02-Aug-2022","ca_purpose":"Dividend - Rs 3 Per Share","perChange":2.8},{"symbol":"MCDOWELL-N","series":"EQ","open_price":790,"high_price":821.2,"low_price":781,"ltp":817,"prev_price":797,"net_price":2.51,"trade_quantity":3025568,"turnover":24428.436031999998,"market_type":"N","ca_ex_dt":"13-Aug-2019","ca_purpose":"Annual General Meeting","perChange":2.51},{"symbol":"NAUKRI","series":"EQ","open_price":3773.05,"high_price":3857.4,"low_price":3732.7,"ltp":3827,"prev_price":3743.15,"net_price":2.24,"trade_quantity":393715,"turnover":15026.841662,"market_type":"N","ca_ex_dt":"18-Nov-2022","ca_purpose":"Interim Dividend - Rs 10 Per Share","perChange":2.24},{"symbol":"MOTHERSON","series":"EQ","open_price":78.95,"high_price":81.3,"low_price":77.3,"ltp":80.2,"prev_price":78.65,"net_price":1.97,"trade_quantity":19457711,"turnover":15544.765317899999,"market_type":"N","ca_ex_dt":"03-Oct-2022","ca_purpose":"Bonus 1:2","perChange":1.97},{"symbol":"LTIM","series":"EQ","open_price":4751.65,"high_price":4843.25,"low_price":4730.15,"ltp":4797,"prev_price":4712.8,"net_price":1.79,"trade_quantity":527489,"turnover":25346.8486791,"market_type":"N","ca_ex_dt":"31-Jan-2023","ca_purpose":"Interim Dividend - Rs 20 Per Share","perChange":1.79},{"symbol":"NYKAA","series":"EQ","open_price":126,"high_price":128.85,"low_price":123.8,"ltp":127.8,"prev_price":125.75,"net_price":1.63,"trade_quantity":4845666,"turnover":6148.6655874,"market_type":"N","ca_ex_dt":"10-Nov-2022","ca_purpose":"Bonus 5:1","perChange":1.63},{"symbol":"SHREECEM","series":"EQ","open_price":24075.55,"high_price":24498,"low_price":23727.6,"ltp":24327.2,"prev_price":23984.3,"net_price":1.43,"trade_quantity":29803,"turnover":7188.492540900001,"market_type":"N","ca_ex_dt":"16-Feb-2023","ca_purpose":"Interim Dividend - Rs   45 Per Share","perChange":1.43},{"symbol":"ZOMATO","series":"EQ","open_price":63.95,"high_price":65,"low_price":63.2,"ltp":64.35,"prev_price":63.5,"net_price":1.34,"trade_quantity":73620039,"turnover":47175.720991199996,"market_type":"N","ca_ex_dt":"-","ca_purpose":"-","perChange":1.34},{"symbol":"VEDL","series":"EQ","open_price":281,"high_price":282.3,"low_price":277.2,"ltp":282.1,"prev_price":278.55,"net_price":1.27,"trade_quantity":6918149,"turnover":19387.4207576,"market_type":"N","ca_ex_dt":"06-Apr-2023","ca_purpose":"Interim Dividend - Rs 20.50 Per Share","perChange":1.27},{"symbol":"AMBUJACEM","series":"EQ","open_price":399.05,"high_price":406,"low_price":395.65,"ltp":404,"prev_price":399.05,"net_price":1.24,"trade_quantity":4401094,"turnover":17673.0330664,"market_type":"N","ca_ex_dt":"30-Mar-2022","ca_purpose":"Dividend - Rs 6.30 Per Share","perChange":1.24},{"symbol":"CANBK","series":"EQ","open_price":297,"high_price":298.9,"low_price":291.35,"ltp":298.3,"prev_price":295.15,"net_price":1.07,"trade_quantity":6343566,"turnover":18752.2154526,"market_type":"N","ca_ex_dt":"15-Jun-2022","ca_purpose":"Dividend - Rs 6.5 Per Share","perChange":1.07},{"symbol":"ACC","series":"EQ","open_price":1719.95,"high_price":1741.35,"low_price":1705,"ltp":1729,"prev_price":1712.45,"net_price":0.97,"trade_quantity":492673,"turnover":8483.7305254,"market_type":"N","ca_ex_dt":"04-Apr-2022","ca_purpose":"Dividend - Rs 58 Per Share","perChange":0.97},{"symbol":"DMART","series":"EQ","open_price":3390,"high_price":3434,"low_price":3375.6,"ltp":3399.85,"prev_price":3368.55,"net_price":0.93,"trade_quantity":265437,"turnover":9046.7034651,"market_type":"N","ca_ex_dt":"09-Aug-2021","ca_purpose":"Annual General Meeting","perChange":0.93},{"symbol":"VBL","series":"EQ","open_price":1581.8,"high_price":1607,"low_price":1580,"ltp":1588,"prev_price":1576.15,"net_price":0.75,"trade_quantity":665121,"turnover":10582.6072068,"market_type":"N","ca_ex_dt":"12-Apr-2023","ca_purpose":"Dividend - Re 1 Per Share","perChange":0.75},{"symbol":"BANKBARODA","series":"EQ","open_price":181,"high_price":182.35,"low_price":178,"ltp":181.7,"prev_price":180.35,"net_price":0.75,"trade_quantity":18643969,"turnover":33641.1776636,"market_type":"N","ca_ex_dt":"17-Jun-2022","ca_purpose":"Annual General Meeting/Dividend - Rs 2.85 Per Share","perChange":0.75},{"symbol":"PIDILITIND","series":"EQ","open_price":2552.25,"high_price":2575.7,"low_price":2545.3,"ltp":2570,"prev_price":2552.25,"net_price":0.7,"trade_quantity":313001,"turnover":8022.9981325,"market_type":"N","ca_ex_dt":"26-Jul-2022","ca_purpose":"Dividend - Rs 10  Per Share","perChange":0.7}],"timestamp":"19-May-2023 16:00:14"},"SecGtr20":{"data":[{"symbol":"REFEX","series":"EQ","open_price":426.65,"high_price":426.65,"low_price":415.05,"ltp":426.65,"prev_price":355.55,"net_price":20,"trade_quantity":714413,"turnover":3036.8267804,"market_type":"N","ca_ex_dt":"15-Sep-2022","ca_purpose":"Annual General Meeting","perChange":20},{"symbol":"SHANTI","series":"EQ","open_price":19.45,"high_price":21.95,"low_price":19.45,"ltp":21.65,"prev_price":18.3,"net_price":18.31,"trade_quantity":1099702,"turnover":229.837718,"market_type":"N","ca_ex_dt":"29-Dec-2022","ca_purpose":"Extra Ordinary General Meeting","perChange":18.31},{"symbol":"KSOLVES","series":"EQ","open_price":800,"high_price":960,"low_price":790.7,"ltp":926.3,"prev_price":800.9,"net_price":15.66,"trade_quantity":330995,"turnover":2873.69859,"market_type":"N","ca_ex_dt":"03-Mar-2023","ca_purpose":"Interim Dividend - Rs 3 Per Share","perChange":15.66},{"symbol":"CORDSCABLE","series":"EQ","open_price":83.05,"high_price":95,"low_price":81.25,"ltp":93,"prev_price":80.9,"net_price":14.96,"trade_quantity":3239404,"turnover":2932.6324412,"market_type":"N","ca_ex_dt":"15-Sep-2022","ca_purpose":"Annual General Meeting","perChange":14.96},{"symbol":"BALAXI","series":"EQ","open_price":605,"high_price":649.85,"low_price":605,"ltp":609,"prev_price":547.65,"net_price":11.2,"trade_quantity":62706,"turnover":386.0118654,"market_type":"N","ca_ex_dt":"01-Jul-2022","ca_purpose":"Annual General Meeting/Dividend - Rs 0.50 Per Share","perChange":11.2},{"symbol":"FOSECOIND","series":"EQ","open_price":2498,"high_price":2740,"low_price":2475,"ltp":2733,"prev_price":2471.15,"net_price":10.6,"trade_quantity":42951,"turnover":1123.2287814000001,"market_type":"N","ca_ex_dt":"17-May-2023","ca_purpose":"Annual General Meeting/Dividend - Rs 25 Per Share/ Special Dividend - Rs 15 Per Share","perChange":10.6},{"symbol":"MINDTECK","series":"EQ","open_price":122,"high_price":141,"low_price":120.35,"ltp":133,"prev_price":120.4,"net_price":10.47,"trade_quantity":447222,"turnover":601.289979,"market_type":"N","ca_ex_dt":"04-Aug-2022","ca_purpose":"Annual General Meeting/Dividend - Re 1 Per Share","perChange":10.47},{"symbol":"CHEMFAB","series":"EQ","open_price":288.15,"high_price":314.7,"low_price":288.15,"ltp":314.7,"prev_price":286.1,"net_price":10,"trade_quantity":363102,"turnover":1127.7585018,"market_type":"N","ca_ex_dt":"07-Sep-2022","ca_purpose":"Annual General Meeting/Dividend - Rs 1.25 Per Share","perChange":10},{"symbol":"AURIONPRO","series":"EQ","open_price":595.35,"high_price":653.05,"low_price":595.3,"ltp":653.05,"prev_price":593.7,"net_price":10,"trade_quantity":188597,"turnover":1206.3041314,"market_type":"N","ca_ex_dt":"16-Sep-2022","ca_purpose":"Annual General Meeting/Dividend - Rs 2.50 Per Share","perChange":10},{"symbol":"KHAITANLTD","series":"EQ","open_price":42.95,"high_price":45.9,"low_price":42.95,"ltp":45.9,"prev_price":41.75,"net_price":9.94,"trade_quantity":45837,"turnover":20.9200068,"market_type":"N","ca_ex_dt":"16-Sep-2022","ca_purpose":"Annual General Meeting","perChange":9.94},{"symbol":"HECPROJECT","series":"EQ","open_price":34,"high_price":37.8,"low_price":34,"ltp":37.8,"prev_price":34.4,"net_price":9.88,"trade_quantity":44366,"turnover":16.6727428,"market_type":"N","ca_ex_dt":"22-Sep-2022","ca_purpose":"Annual General Meeting","perChange":9.88},{"symbol":"PAR","series":"EQ","open_price":195,"high_price":222.45,"low_price":189.8,"ltp":210,"prev_price":191.2,"net_price":9.83,"trade_quantity":343289,"turnover":718.2979036,"market_type":"N","ca_ex_dt":"01-Sep-2022","ca_purpose":"Annual General Meeting","perChange":9.83},{"symbol":"KEC","series":"EQ","open_price":484,"high_price":547,"low_price":482.75,"ltp":527,"prev_price":480.3,"net_price":9.72,"trade_quantity":10679394,"turnover":56381.860623,"market_type":"N","ca_ex_dt":"15-Jun-2022","ca_purpose":"Dividend - Rs 4 Per Share","perChange":9.72},{"symbol":"MARINE","series":"EQ","open_price":50.8,"high_price":53.45,"low_price":50,"ltp":53.3,"prev_price":49.05,"net_price":8.66,"trade_quantity":4168859,"turnover":2161.9702774,"market_type":"N","ca_ex_dt":"09-Sep-2022","ca_purpose":"Annual General Meeting","perChange":8.66},{"symbol":"BRNL","series":"EQ","open_price":29.55,"high_price":33.55,"low_price":29.2,"ltp":31.8,"prev_price":29.3,"net_price":8.53,"trade_quantity":358281,"turnover":115.2231696,"market_type":"N","ca_ex_dt":"05-Dec-2019","ca_purpose":"Dividend - Rs 0.50 Per Share","perChange":8.53},{"symbol":"RAMCOCEM","series":"EQ","open_price":798.9,"high_price":850,"low_price":798,"ltp":841.95,"prev_price":781.6,"net_price":7.72,"trade_quantity":6819595,"turnover":56229.606653500006,"market_type":"N","ca_ex_dt":"02-Aug-2022","ca_purpose":"Annual General Meeting/Dividend - Rs 3 Per Share","perChange":7.72},{"symbol":"AWL","series":"EQ","open_price":378.75,"high_price":412.2,"low_price":366,"ltp":403.95,"prev_price":378,"net_price":6.87,"trade_quantity":6990238,"turnover":27657.5756708,"market_type":"N","ca_ex_dt":"19-Aug-2022","ca_purpose":"Annual General Meeting","perChange":6.87},{"symbol":"KOKUYOCMLN","series":"EQ","open_price":90.35,"high_price":99.45,"low_price":89.6,"ltp":97.4,"prev_price":91.2,"net_price":6.8,"trade_quantity":985512,"turnover":944.1204959999999,"market_type":"N","ca_ex_dt":"23-Jun-2022","ca_purpose":"Annual General Meeting","perChange":6.8},{"symbol":"UGROCAP","series":"EQ","open_price":205,"high_price":227.25,"low_price":205,"ltp":212.75,"prev_price":199.55,"net_price":6.61,"trade_quantity":2908154,"turnover":6341.811427799999,"market_type":"N","ca_ex_dt":"04-Aug-2022","ca_purpose":"Annual General Meeting","perChange":6.61},{"symbol":"JPOLYINVST","series":"EQ","open_price":532,"high_price":588.8,"low_price":510,"ltp":564.95,"prev_price":529.9,"net_price":6.61,"trade_quantity":57287,"turnover":324.5136689,"market_type":"N","ca_ex_dt":"21-Sep-2022","ca_purpose":"Annual General Meeting","perChange":6.61}],"timestamp":"19-May-2023 16:00:14"},"SecLwr20":{"data":[{"symbol":"VISHWARAJ","series":"EQ","open_price":15.65,"high_price":18.6,"low_price":15.4,"ltp":17.85,"prev_price":15.7,"net_price":13.69,"trade_quantity":12987997,"turnover":2258.6126783,"market_type":"N","ca_ex_dt":"21-Feb-2023","ca_purpose":"Interim Dividend - Rs 0.10 Per Share","perChange":13.69},{"symbol":"EXCEL","series":"EQ","open_price":0.4,"high_price":0.45,"low_price":0.35,"ltp":0.45,"prev_price":0.4,"net_price":12.5,"trade_quantity":8357572,"turnover":33.430288,"market_type":"N","ca_ex_dt":"28-Sep-2022","ca_purpose":"Bonus 1:2","perChange":12.5},{"symbol":"SRPL","series":"EQ","open_price":4.95,"high_price":5.2,"low_price":4.8,"ltp":5.2,"prev_price":47.7,"net_price":9.47,"trade_quantity":2654192,"turnover":137.2217264,"market_type":"N","ca_ex_dt":"19-May-2023","ca_purpose":"Face Value Split (Sub-Division) - From Rs 10/- Per Share To Re 1/- Per Share","perChange":-89.1},{"symbol":"NEXTMEDIA","series":"EQ","open_price":6.45,"high_price":6.45,"low_price":6.1,"ltp":6.45,"prev_price":5.9,"net_price":9.32,"trade_quantity":114021,"turnover":7.320148199999999,"market_type":"N","ca_ex_dt":"22-Aug-2017","ca_purpose":"Annual General Meeting","perChange":9.32},{"symbol":"HCC","series":"EQ","open_price":16.4,"high_price":17.65,"low_price":16.25,"ltp":17.35,"prev_price":15.95,"net_price":8.78,"trade_quantity":80994297,"turnover":13882.4225058,"market_type":"N","ca_ex_dt":"21-Sep-2022","ca_purpose":"Annual General Meeting","perChange":8.78},{"symbol":"GODHA","series":"EQ","open_price":1.15,"high_price":1.25,"low_price":1.15,"ltp":1.25,"prev_price":1.15,"net_price":8.7,"trade_quantity":3046418,"turnover":37.1662996,"market_type":"N","ca_ex_dt":"12-May-2023","ca_purpose":"Rights 2:1 @ Premium Rs 0/-","perChange":8.7},{"symbol":"GAYAHWS","series":"BE","open_price":0.65,"high_price":0.7,"low_price":0.65,"ltp":0.7,"prev_price":0.65,"net_price":7.69,"trade_quantity":56448,"turnover":0.3838464,"market_type":"N","ca_ex_dt":"21-Sep-2022","ca_purpose":"Annual General Meeting","perChange":7.69},{"symbol":"ANTGRAPHIC","series":"BE","open_price":0.65,"high_price":0.7,"low_price":0.65,"ltp":0.7,"prev_price":0.65,"net_price":7.69,"trade_quantity":184851,"turnover":1.2200166000000001,"market_type":"N","ca_ex_dt":"26-Sep-2022","ca_purpose":"Annual General Meeting","perChange":7.69},{"symbol":"GTLINFRA","series":"EQ","open_price":0.8,"high_price":0.85,"low_price":0.8,"ltp":0.85,"prev_price":0.8,"net_price":6.25,"trade_quantity":13432037,"turnover":107.456296,"market_type":"N","ca_ex_dt":"21-Sep-2015","ca_purpose":"Annual General Meeting","perChange":6.25},{"symbol":"VISHAL","series":"EQ","open_price":18.3,"high_price":19.5,"low_price":18.3,"ltp":19.4,"prev_price":18.4,"net_price":5.43,"trade_quantity":184915,"turnover":35.0783755,"market_type":"N","ca_ex_dt":"22-Sep-2022","ca_purpose":"Annual General Meeting","perChange":5.43},{"symbol":"TREEHOUSE","series":"EQ","open_price":16.5,"high_price":17.3,"low_price":16.5,"ltp":17.3,"prev_price":16.5,"net_price":4.85,"trade_quantity":39034,"turnover":6.7099446,"market_type":"N","ca_ex_dt":"22-Sep-2022","ca_purpose":"Annual General Meeting","perChange":4.85},{"symbol":"SILLYMONKS","series":"EQ","open_price":17.55,"high_price":17.55,"low_price":17.1,"ltp":17.55,"prev_price":16.75,"net_price":4.78,"trade_quantity":11990,"turnover":2.100648,"market_type":"N","ca_ex_dt":"15-Feb-2021","ca_purpose":"Interim Dividend - Rs 0.50 Per Share","perChange":4.78},{"symbol":"SHRENIK","series":"EQ","open_price":1.05,"high_price":1.1,"low_price":1.05,"ltp":1.1,"prev_price":1.05,"net_price":4.76,"trade_quantity":443667,"turnover":4.7472369,"market_type":"N","ca_ex_dt":"14-Sep-2021","ca_purpose":"Annual General Meeting","perChange":4.76},{"symbol":"SILGO","series":"EQ","open_price":17.5,"high_price":18.95,"low_price":17.5,"ltp":18.75,"prev_price":17.9,"net_price":4.75,"trade_quantity":22485,"turnover":4.155228,"market_type":"N","ca_ex_dt":"16-Sep-2022","ca_purpose":"Annual General Meeting","perChange":4.75},{"symbol":"DUCON","series":"BE","open_price":7.45,"high_price":7.8,"low_price":7.3,"ltp":7.8,"prev_price":7.45,"net_price":4.7,"trade_quantity":384800,"turnover":29.47568,"market_type":"N","ca_ex_dt":"22-Sep-2022","ca_purpose":"Annual General Meeting","perChange":4.7},{"symbol":"VCL","series":"EQ","open_price":2.45,"high_price":2.55,"low_price":2.4,"ltp":2.5,"prev_price":2.4,"net_price":4.17,"trade_quantity":247922,"turnover":6.074089,"market_type":"N","ca_ex_dt":"15-Feb-2023","ca_purpose":"Face Value Split (Sub-Division) - From Rs 2/- Per Share To Re 1/- Per Share","perChange":4.17},{"symbol":"CCCL","series":"BE","open_price":1.35,"high_price":1.35,"low_price":1.25,"ltp":1.35,"prev_price":1.3,"net_price":3.85,"trade_quantity":386649,"turnover":5.0264370000000005,"market_type":"N","ca_ex_dt":"21-Dec-2022","ca_purpose":"Annual General Meeting","perChange":3.85},{"symbol":"TIJARIA","series":"EQ","open_price":5.3,"high_price":5.5,"low_price":5.15,"ltp":5.5,"prev_price":5.3,"net_price":3.77,"trade_quantity":2072,"turnover":0.109816,"market_type":"N","ca_ex_dt":"02-Jan-2023","ca_purpose":"Extra Ordinary General Meeting","perChange":3.77},{"symbol":"KBCGLOBAL","series":"BE","open_price":2.85,"high_price":2.85,"low_price":2.65,"ltp":2.85,"prev_price":2.75,"net_price":3.64,"trade_quantity":6763572,"turnover":188.7036588,"market_type":"N","ca_ex_dt":"21-Sep-2022","ca_purpose":"Annual General Meeting","perChange":3.64},{"symbol":"PARSVNATH","series":"EQ","open_price":7,"high_price":7.45,"low_price":7,"ltp":7.25,"prev_price":7,"net_price":3.57,"trade_quantity":611764,"turnover":44.1693608,"market_type":"N","ca_ex_dt":"22-Sep-2022","ca_purpose":"Annual General Meeting","perChange":3.57}],"timestamp":"19-May-2023 16:00:14"},"FOSec":{"data":[{"symbol":"RAMCOCEM","series":"EQ","open_price":798.9,"high_price":850,"low_price":798,"ltp":841.95,"prev_price":781.6,"net_price":7.72,"trade_quantity":6819595,"turnover":56229.606653500006,"market_type":"N","ca_ex_dt":"02-Aug-2022","ca_purpose":"Annual General Meeting/Dividend - Rs 3 Per Share","perChange":7.72},{"symbol":"BSOFT","series":"EQ","open_price":321,"high_price":337.35,"low_price":320.1,"ltp":333.8,"prev_price":319,"net_price":4.64,"trade_quantity":10244689,"turnover":33970.3642551,"market_type":"N","ca_ex_dt":"01-Nov-2022","ca_purpose":"Interim Dividend - Rs 1.50 Per Share","perChange":4.64},{"symbol":"ADANIPORTS","series":"EQ","open_price":664,"high_price":694.15,"low_price":659.5,"ltp":691,"prev_price":664.95,"net_price":3.92,"trade_quantity":6340270,"turnover":42969.911871000004,"market_type":"N","ca_ex_dt":"14-Jul-2022","ca_purpose":"Dividend - Rs 5 Per Share","perChange":3.92},{"symbol":"GLENMARK","series":"EQ","open_price":605,"high_price":629.85,"low_price":602,"ltp":626,"prev_price":604.1,"net_price":3.63,"trade_quantity":3771939,"turnover":23111.0474469,"market_type":"N","ca_ex_dt":"12-Sep-2022","ca_purpose":"Annual General Meeting/Dividend - Rs 2.50 Per Share","perChange":3.63},{"symbol":"ADANIENT","series":"EQ","open_price":1888,"high_price":1983,"low_price":1872.1,"ltp":1955,"prev_price":1890,"net_price":3.44,"trade_quantity":7541150,"turnover":145819.446975,"market_type":"N","ca_ex_dt":"14-Jul-2022","ca_purpose":"Dividend - Re 1 Per Share","perChange":3.44},{"symbol":"TATAMOTORS","series":"EQ","open_price":509.8,"high_price":526.4,"low_price":504.75,"ltp":525,"prev_price":508.45,"net_price":3.25,"trade_quantity":19343560,"turnover":100143.54447600001,"market_type":"N","ca_ex_dt":"18-Jul-2016","ca_purpose":"Dividend - Re 0.20/- Per Share","perChange":3.25},{"symbol":"OBEROIRLTY","series":"EQ","open_price":894.05,"high_price":924.1,"low_price":884.75,"ltp":915,"prev_price":890.05,"net_price":2.8,"trade_quantity":1276153,"turnover":11569.3478674,"market_type":"N","ca_ex_dt":"07-Jul-2022","ca_purpose":"Dividend - Rs 3 Per Share","perChange":2.8},{"symbol":"DLF","series":"EQ","open_price":460.9,"high_price":473,"low_price":453.5,"ltp":472.85,"prev_price":459.95,"net_price":2.8,"trade_quantity":8398165,"turnover":39060.705231500004,"market_type":"N","ca_ex_dt":"02-Aug-2022","ca_purpose":"Dividend - Rs 3 Per Share","perChange":2.8},{"symbol":"PERSISTENT","series":"EQ","open_price":4785,"high_price":4896,"low_price":4765.4,"ltp":4880,"prev_price":4748.25,"net_price":2.77,"trade_quantity":508919,"turnover":24704.3023413,"market_type":"N","ca_ex_dt":"25-Jan-2023","ca_purpose":"Interim Dividend - Rs 28 Per Share","perChange":2.77},{"symbol":"MPHASIS","series":"EQ","open_price":1862.2,"high_price":1927.75,"low_price":1848.55,"ltp":1912,"prev_price":1862.2,"net_price":2.67,"trade_quantity":737768,"turnover":14034.1180032,"market_type":"N","ca_ex_dt":"05-Jul-2022","ca_purpose":"Annual General Meeting/Dividend - Rs 46 Per Share","perChange":2.67},{"symbol":"MCDOWELL-N","series":"EQ","open_price":790,"high_price":821.2,"low_price":781,"ltp":817,"prev_price":797,"net_price":2.51,"trade_quantity":3025568,"turnover":24428.436031999998,"market_type":"N","ca_ex_dt":"13-Aug-2019","ca_purpose":"Annual General Meeting","perChange":2.51},{"symbol":"NAUKRI","series":"EQ","open_price":3773.05,"high_price":3857.4,"low_price":3732.7,"ltp":3827,"prev_price":3743.15,"net_price":2.24,"trade_quantity":393715,"turnover":15026.841662,"market_type":"N","ca_ex_dt":"18-Nov-2022","ca_purpose":"Interim Dividend - Rs 10 Per Share","perChange":2.24},{"symbol":"TECHM","series":"EQ","open_price":1056.55,"high_price":1078.75,"low_price":1049,"ltp":1072,"prev_price":1048.7,"net_price":2.22,"trade_quantity":2624323,"turnover":28065.0350266,"market_type":"N","ca_ex_dt":"09-Nov-2022","ca_purpose":"Special Dividend - Rs 18 Per Share","perChange":2.22},{"symbol":"PNB","series":"EQ","open_price":48.85,"high_price":49.6,"low_price":48.35,"ltp":49.45,"prev_price":48.45,"net_price":2.06,"trade_quantity":46965076,"turnover":23003.4942248,"market_type":"N","ca_ex_dt":"22-Jun-2022","ca_purpose":"Annual General Meeting/Dividend - Rs 0.64 Per Share","perChange":2.06},{"symbol":"LICHSGFIN","series":"EQ","open_price":366,"high_price":374.55,"low_price":364.5,"ltp":373.05,"prev_price":365.8,"net_price":1.98,"trade_quantity":2809030,"turnover":10397.343642,"market_type":"N","ca_ex_dt":"19-Sep-2022","ca_purpose":"Annual General Meeting/Dividend - Rs 8.50 Per Share","perChange":1.98},{"symbol":"MOTHERSON","series":"EQ","open_price":78.95,"high_price":81.3,"low_price":77.3,"ltp":80.2,"prev_price":78.65,"net_price":1.97,"trade_quantity":19457711,"turnover":15544.765317899999,"market_type":"N","ca_ex_dt":"03-Oct-2022","ca_purpose":"Bonus 1:2","perChange":1.97},{"symbol":"DIXON","series":"EQ","open_price":3005.3,"high_price":3043,"low_price":2992,"ltp":3042,"prev_price":2983.7,"net_price":1.95,"trade_quantity":467483,"turnover":14131.1228723,"market_type":"N","ca_ex_dt":"11-Aug-2022","ca_purpose":"Annual General Meeting/Dividend - Rs 2 Per Share","perChange":1.95},{"symbol":"INFY","series":"EQ","open_price":1256.05,"high_price":1273.3,"low_price":1252.8,"ltp":1269,"prev_price":1246,"net_price":1.85,"trade_quantity":11094136,"turnover":140655.8938624,"market_type":"N","ca_ex_dt":"02-Jun-2023","ca_purpose":"Annual General Meeting/Dividend - Rs 17.50 Per Share","perChange":1.85},{"symbol":"LTIM","series":"EQ","open_price":4751.65,"high_price":4843.25,"low_price":4730.15,"ltp":4797,"prev_price":4712.8,"net_price":1.79,"trade_quantity":527489,"turnover":25346.8486791,"market_type":"N","ca_ex_dt":"31-Jan-2023","ca_purpose":"Interim Dividend - Rs 20 Per Share","perChange":1.79},{"symbol":"COFORGE","series":"EQ","open_price":4228,"high_price":4303.45,"low_price":4206.05,"ltp":4278,"prev_price":4206.15,"net_price":1.71,"trade_quantity":343809,"turnover":14673.8712627,"market_type":"N","ca_ex_dt":"10-May-2023","ca_purpose":"Interim Dividend - Rs 19 Per Share","perChange":1.71}],"timestamp":"19-May-2023 16:00:14"},"allSec":{"data":[{"symbol":"REFEX","series":"EQ","open_price":426.65,"high_price":426.65,"low_price":415.05,"ltp":426.65,"prev_price":355.55,"net_price":20,"trade_quantity":714413,"turnover":3036.8267804,"market_type":"N","ca_ex_dt":"15-Sep-2022","ca_purpose":"Annual General Meeting","perChange":20},{"symbol":"SHANTI","series":"EQ","open_price":19.45,"high_price":21.95,"low_price":19.45,"ltp":21.65,"prev_price":18.3,"net_price":18.31,"trade_quantity":1099702,"turnover":229.837718,"market_type":"N","ca_ex_dt":"29-Dec-2022","ca_purpose":"Extra Ordinary General Meeting","perChange":18.31},{"symbol":"KSOLVES","series":"EQ","open_price":800,"high_price":960,"low_price":790.7,"ltp":926.3,"prev_price":800.9,"net_price":15.66,"trade_quantity":330995,"turnover":2873.69859,"market_type":"N","ca_ex_dt":"03-Mar-2023","ca_purpose":"Interim Dividend - Rs 3 Per Share","perChange":15.66},{"symbol":"CORDSCABLE","series":"EQ","open_price":83.05,"high_price":95,"low_price":81.25,"ltp":93,"prev_price":80.9,"net_price":14.96,"trade_quantity":3239404,"turnover":2932.6324412,"market_type":"N","ca_ex_dt":"15-Sep-2022","ca_purpose":"Annual General Meeting","perChange":14.96},{"symbol":"VISHWARAJ","series":"EQ","open_price":15.65,"high_price":18.6,"low_price":15.4,"ltp":17.85,"prev_price":15.7,"net_price":13.69,"trade_quantity":12987997,"turnover":2258.6126783,"market_type":"N","ca_ex_dt":"21-Feb-2023","ca_purpose":"Interim Dividend - Rs 0.10 Per Share","perChange":13.69},{"symbol":"EXCEL","series":"EQ","open_price":0.4,"high_price":0.45,"low_price":0.35,"ltp":0.45,"prev_price":0.4,"net_price":12.5,"trade_quantity":8357572,"turnover":33.430288,"market_type":"N","ca_ex_dt":"28-Sep-2022","ca_purpose":"Bonus 1:2","perChange":12.5},{"symbol":"BALAXI","series":"EQ","open_price":605,"high_price":649.85,"low_price":605,"ltp":609,"prev_price":547.65,"net_price":11.2,"trade_quantity":62706,"turnover":386.0118654,"market_type":"N","ca_ex_dt":"01-Jul-2022","ca_purpose":"Annual General Meeting/Dividend - Rs 0.50 Per Share","perChange":11.2},{"symbol":"FOSECOIND","series":"EQ","open_price":2498,"high_price":2740,"low_price":2475,"ltp":2733,"prev_price":2471.15,"net_price":10.6,"trade_quantity":42951,"turnover":1123.2287814000001,"market_type":"N","ca_ex_dt":"17-May-2023","ca_purpose":"Annual General Meeting/Dividend - Rs 25 Per Share/ Special Dividend - Rs 15 Per Share","perChange":10.6},{"symbol":"MINDTECK","series":"EQ","open_price":122,"high_price":141,"low_price":120.35,"ltp":133,"prev_price":120.4,"net_price":10.47,"trade_quantity":447222,"turnover":601.289979,"market_type":"N","ca_ex_dt":"04-Aug-2022","ca_purpose":"Annual General Meeting/Dividend - Re 1 Per Share","perChange":10.47},{"symbol":"CHEMFAB","series":"EQ","open_price":288.15,"high_price":314.7,"low_price":288.15,"ltp":314.7,"prev_price":286.1,"net_price":10,"trade_quantity":363102,"turnover":1127.7585018,"market_type":"N","ca_ex_dt":"07-Sep-2022","ca_purpose":"Annual General Meeting/Dividend - Rs 1.25 Per Share","perChange":10},{"symbol":"AURIONPRO","series":"EQ","open_price":595.35,"high_price":653.05,"low_price":595.3,"ltp":653.05,"prev_price":593.7,"net_price":10,"trade_quantity":188597,"turnover":1206.3041314,"market_type":"N","ca_ex_dt":"16-Sep-2022","ca_purpose":"Annual General Meeting/Dividend - Rs 2.50 Per Share","perChange":10},{"symbol":"KHAITANLTD","series":"EQ","open_price":42.95,"high_price":45.9,"low_price":42.95,"ltp":45.9,"prev_price":41.75,"net_price":9.94,"trade_quantity":45837,"turnover":20.9200068,"market_type":"N","ca_ex_dt":"16-Sep-2022","ca_purpose":"Annual General Meeting","perChange":9.94},{"symbol":"HECPROJECT","series":"EQ","open_price":34,"high_price":37.8,"low_price":34,"ltp":37.8,"prev_price":34.4,"net_price":9.88,"trade_quantity":44366,"turnover":16.6727428,"market_type":"N","ca_ex_dt":"22-Sep-2022","ca_purpose":"Annual General Meeting","perChange":9.88},{"symbol":"PAR","series":"EQ","open_price":195,"high_price":222.45,"low_price":189.8,"ltp":210,"prev_price":191.2,"net_price":9.83,"trade_quantity":343289,"turnover":718.2979036,"market_type":"N","ca_ex_dt":"01-Sep-2022","ca_purpose":"Annual General Meeting","perChange":9.83},{"symbol":"KEC","series":"EQ","open_price":484,"high_price":547,"low_price":482.75,"ltp":527,"prev_price":480.3,"net_price":9.72,"trade_quantity":10679394,"turnover":56381.860623,"market_type":"N","ca_ex_dt":"15-Jun-2022","ca_purpose":"Dividend - Rs 4 Per Share","perChange":9.72},{"symbol":"SRPL","series":"EQ","open_price":4.95,"high_price":5.2,"low_price":4.8,"ltp":5.2,"prev_price":47.7,"net_price":9.47,"trade_quantity":2654192,"turnover":137.2217264,"market_type":"N","ca_ex_dt":"19-May-2023","ca_purpose":"Face Value Split (Sub-Division) - From Rs 10/- Per Share To Re 1/- Per Share","perChange":-89.1},{"symbol":"NEXTMEDIA","series":"EQ","open_price":6.45,"high_price":6.45,"low_price":6.1,"ltp":6.45,"prev_price":5.9,"net_price":9.32,"trade_quantity":114021,"turnover":7.320148199999999,"market_type":"N","ca_ex_dt":"22-Aug-2017","ca_purpose":"Annual General Meeting","perChange":9.32},{"symbol":"HCC","series":"EQ","open_price":16.4,"high_price":17.65,"low_price":16.25,"ltp":17.35,"prev_price":15.95,"net_price":8.78,"trade_quantity":80994297,"turnover":13882.4225058,"market_type":"N","ca_ex_dt":"21-Sep-2022","ca_purpose":"Annual General Meeting","perChange":8.78},{"symbol":"GODHA","series":"EQ","open_price":1.15,"high_price":1.25,"low_price":1.15,"ltp":1.25,"prev_price":1.15,"net_price":8.7,"trade_quantity":3046418,"turnover":37.1662996,"market_type":"N","ca_ex_dt":"12-May-2023","ca_purpose":"Rights 2:1 @ Premium Rs 0/-","perChange":8.7},{"symbol":"MARINE","series":"EQ","open_price":50.8,"high_price":53.45,"low_price":50,"ltp":53.3,"prev_price":49.05,"net_price":8.66,"trade_quantity":4168859,"turnover":2161.9702774,"market_type":"N","ca_ex_dt":"09-Sep-2022","ca_purpose":"Annual General Meeting","perChange":8.66}],"timestamp":"19-May-2023 16:00:14"}}
    for stock in tg["BANKNIFTY"]["data"]:
        if not dataUtility.checkStockExist(stock['symbol'],"BANKNIFTY.csv"):
            dataUtility.storeInFile("./Results/topGainers/BANKNIFTY.csv",[datetime.now().strftime("%b %d %Y %I:%M%p"),datetime.now().strftime("%b %d %Y %I:%M%p"),stock['symbol'],"process",stock["perChange"]])
    for stock in tg["NIFTY"]["data"]:
        if not dataUtility.checkStockExist(stock['symbol'],"NIFTY.csv"):
            dataUtility.storeInFile("./Results/topGainers/NIFTY.csv",[datetime.now().strftime("%b %d %Y %I:%M%p"),datetime.now().strftime("%b %d %Y %I:%M%p"),stock['symbol'],"process",stock["perChange"]])
    for stock in tg["NIFTYNEXT50"]["data"]:
        if not dataUtility.checkStockExist(stock['symbol'],"NIFTYNEXT50.csv"):
            dataUtility.storeInFile("./Results/topGainers/NIFTYNEXT50.csv",[datetime.now().strftime("%b %d %Y %I:%M%p"),datetime.now().strftime("%b %d %Y %I:%M%p"),stock['symbol'],"process",stock["perChange"]])
   
    #update top gainers data
    path = "./Results/topGainers/"
    file_list = os.listdir(path) 
    for file in file_list:
        sdf = pd.read_csv(f'./Results/topGainers/{file}',header = None)
        print(f'Processing {file}')

        for rootindex, row in sdf.iterrows():
            try:
                if row[3]!="Done":
                    lastProcessdate = datetime.strptime(row[1], '%b %d %Y %I:%M%p')
                    todate = datetime.today()

                    if lastProcessdate.day != todate.day and lastProcessdate.month == todate.month and row.size < 15:
                        timeLine=[["1D",1]]#becareful
                        dataList=dataUtility.getStockData(row[2],timeLine)
                        df=stockFormula.convertToDF(dataList[0][1])
                        diff=stockFormula.percentage_without_abs_Calc(float(df.at[1, 'close']),float(df.at[0, 'close']))
                        sdf.loc[rootindex, 1]=todate.strftime("%b %d %Y %I:%M%p")
                        sdf.loc[rootindex, row.size]= diff
                        sdf.to_csv(f'./Results/topGainers/{file}', header = None,index=False)
                    elif row.size == 15: 
                        sdf.loc[rootindex, 3]= "done"
                        sdf.to_csv(f'./Results/topGainers/{file}', header = None,index=False)
            except Exception as e:
                print("Oops!", e, "occurred.")

#calculation part
    path = "./Results/topGainers/"
    file_list = os.listdir(path) 
    for file in file_list:
        sdf = pd.read_csv(f'./Results/topGainers/{file}',header = None)
        print(f'Processing {file}')
        result={}
        for rootindex, row in sdf.iterrows():
            try:
                total_size=row.size
                startBuffer=4
                indexbuffer=5
                for index in range(indexbuffer,total_size):
                    if total_size>index:
                        if result.get(index - startBuffer):
                            if result[index - startBuffer].get(int(row[startBuffer])):
                                result[index - startBuffer][int(row[startBuffer])].append(row[index])
                            else:
                                result[index - startBuffer][int(row[startBuffer])]=[]
                                result[index - startBuffer][int(row[startBuffer])].append(row[index])
                        else:
                            result[index - startBuffer]={}
                            result[index - startBuffer][int(row[startBuffer])]=[]
                            result[index - startBuffer][int(row[startBuffer])].append(row[index])
            except Exception as e:
                print("Oops!", e, "occurred.")
        output=[datetime.now().strftime("%b %d %Y %I:%M%p"),"-","-","-","-","-","-","-","-","-","-",]
        for day in result:
            for percentage in result[day]:
                output[percentage+1]=sum(result[day][percentage])/len(result[day][percentage])
        dataUtility.storeInFile("./Results/today/"+file+"RESULT.csv",output)
                
        
    


resetDirectory()
WatchStockMarket()
analyzeResult()
updateResult()
moniterResult()
moniter_breakout()
#monitor_top_gainer()
