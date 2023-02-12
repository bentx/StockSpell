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
import dataUtility
import talib
import pandas_ta as ta

IST = pytz.timezone('Asia/Kolkata')

def movingAverageFormula(ha_df,currIndex,preHigh,preLow,high,low):
    if( float(preHigh)>=float(preLow) and float(high)<=float(low) ):
        
        return True      
    return False       

def OpenPercentageGap(prevclose,open,av):
    return float(prevclose)>float(open) and int(av)>50000 and stockFormula.percentageCalc(prevclose,open)>2 and  stockFormula.percentageCalc(prevclose,open)<8

def WA1Stratagy1(ha_df,currIndex):
    if ( "RRRG1"==dataUtility.findCandleType(ha_df,currIndex-3)+dataUtility.findCandleType(ha_df,currIndex-2)+dataUtility.findCandleType(ha_df,currIndex-1)+dataUtility.findCandleType(ha_df,currIndex) )and (dataUtility.isTouchLow(ha_df,currIndex-1) or (dataUtility.isTouchLow(ha_df,currIndex-2))):
        return [True,"see currentdate"]
    return [False,"see currentdate"]


def WA1Stratagy2(ha_df,currIndex):
    if ( "RRRR1"==dataUtility.findCandleType(ha_df,currIndex-3)+dataUtility.findCandleType(ha_df,currIndex-2)+dataUtility.findCandleType(ha_df,currIndex-1)+dataUtility.findCandleType(ha_df,currIndex) )and (dataUtility.isTouchLow(ha_df,currIndex-1) or (dataUtility.isTouchLow(ha_df,currIndex-2))) and not (dataUtility.isTouchLow(ha_df,currIndex) ):
        return [True,"see currentdate"]
    return [False,"see currentdate"]

def bodyTouch(ha_df,currIndex,ma):
     if (float(ha_df.at[currIndex, ma])>float(ha_df.at[currIndex, 'open']) and float(ha_df.at[currIndex, ma]) < float(ha_df.at[currIndex, 'close']) and "GGG"==dataUtility.findCandleType(ha_df,currIndex-2)+dataUtility.findCandleType(ha_df,currIndex-1)+dataUtility.findCandleType(ha_df,currIndex) ):
        return True 
     return False

def wigTouch(ha_df,currIndex,ma):
     if (float(ha_df.at[currIndex, ma])>float(ha_df.at[currIndex, 'low']) and float(ha_df.at[currIndex, ma]) < float(ha_df.at[currIndex, 'open']) and "R1G1"==dataUtility.findCandleType(ha_df,currIndex-1)+dataUtility.findCandleType(ha_df,currIndex) ):
        return True
     return False

def TopGainer(df,currIndex,percentage):
    if float(df.at[currIndex-1, 'close']) <float(df.at[currIndex, 'close']):
        percent=stockFormula.percentageCalc(float(df.at[currIndex-1, 'close']) ,float(df.at[currIndex, 'close']))
        if(percent>percentage and percent<percentage+1):
            return True     
    return False

def RSAADX(df,currentIndex):
    if int(df.at[currentIndex, 'rsi2']) <25 and int(df.at[currentIndex, 'adx'])>20  and not int(df.at[currentIndex-1, 'rsi2']) <25 and int(df.at[currentIndex-1, 'adx'])>20  :
        return [True,"see currentdate"]
    return [False,"nop"]

def findTrend(df , index , length ,correction):
    HH=df.at[index-length, 'close']
    CH=df.at[index-length, 'close']
    LL=df.at[index-length, 'close']
    CL=df.at[index-length, 'close']
    HI=0
    LI=0
    initialLow=False
    initialHigh=False
    PH=df.at[index-length, 'close']
    PHD=0
    PL=df.at[index-length, 'close']
    trend="UN"
    for i in range(index-length+1,index+1):
        if i==index:
            if df.at[index-length, 'close']>PH:
                print(datetime.fromtimestamp(int(df.at[index, 'date']),IST).strftime("%b %d %Y %I:%M%p"),datetime.fromtimestamp(int(PHD),IST).strftime("%b %d %Y %I:%M%p"),correction)
                return True
            return False
        if(LL>df.at[i, 'close']):
            trend="D"
            LL=df.at[i, 'close']
            CH=df.at[i, 'close']
        elif(HH<df.at[i, 'close']):
            trend="U"
            HH=df.at[i, 'close']
            CL=df.at[i, 'close']
        elif(CL>df.at[i, 'close']):
            if(LI==correction):
                if initialHigh:
                    PH=df.at[i-correction, 'close']
                    PHD=df.at[i-correction, 'date']
                initialHigh=False
                CL=df.at[i, 'close']
                CH=df.at[i, 'close']
                HI=0
            else:
                LI=LI+1
                initialHigh=True

        elif(CH<df.at[i, 'close']):
            if(HI==correction):
                if initialLow:
                    PL=df.at[i-correction, 'close']
                initialLow=False
                CH=df.at[i, 'close']
                CL=df.at[i, 'close']
                LI=0
            else:
                HI=HI+1
                initialLow=True
    return False

def trianglePattern(df,index,length,correction):
    PH=-1
    PHI=0
    Pattern="N"
    for i in range(index-length,index+1):
        if i==index:
            if PH!=-1 and  float(df.at[PH, 'high'])<float(df.at[index, 'close']) and  not float(df.at[PH, 'high'])<float(df.at[index-1, 'close']):
                #print(datetime.fromtimestamp(int(df.at[index, 'date']),IST).strftime("%b %d %Y %I:%M%p"),datetime.fromtimestamp(int(df.at[PH, 'date']),IST).strftime("%b %d %Y %I:%M%p"),Pattern)
                return [True,datetime.fromtimestamp(int(df.at[PH, 'date']),IST).strftime("%b %d %Y %I:%M%p")]
        if i<index-2:
            
            if df.at[i-2, 'candle']+df.at[i-1, 'candle']+df.at[i, 'candle']+df.at[i+1, 'candle']+df.at[i+2, 'candle']=="GGRRR" :
                PH= i-1
                Pattern=Pattern+"H"
            if df.at[i-2, 'candle']+df.at[i-1, 'candle']+df.at[i, 'candle']+df.at[i+1, 'candle']+df.at[i+2, 'candle']=="RRGGG" :
                Pattern=Pattern+"L"
    return [False,"nop"]

def PP(df,index):
    if df.at[index, 'low']>df.at[index, 'pivote'] and df.at[index, 'candle'] =="G" and df.at[index-1, 'low'] < df.at[index-1, 'pivote']:
        pattern=df.at[index, 'candle']+df.at[index-1, 'candle']+df.at[index-2, 'candle']+df.at[index-3, 'candle']
        #print(datetime.fromtimestamp(int(df.at[index, 'date']),IST).strftime("%b %d %Y %I:%M%p"),pattern)
        return [True,pattern]
    if df.at[index, 'low']>df.at[index, 'S1'] and df.at[index, 'candle'] =="G" and df.at[index-1, 'low'] < df.at[index-1, 'S1']:
        pattern=df.at[index, 'candle']+df.at[index-1, 'candle']+df.at[index-2, 'candle']+df.at[index-3, 'candle']
        #print(datetime.fromtimestamp(int(df.at[index, 'date']),IST).strftime("%b %d %Y %I:%M%p"),pattern)
        return [True,pattern]
    if df.at[index, 'low']>df.at[index, 'S2'] and df.at[index, 'candle'] =="G" and df.at[index-1, 'low'] < df.at[index-1, 'S2']:
        pattern=df.at[index, 'candle']+df.at[index-1, 'candle']+df.at[index-2, 'candle']+df.at[index-3, 'candle']
        #print(datetime.fromtimestamp(int(df.at[index, 'date']),IST).strftime("%b %d %Y %I:%M%p"),pattern)
        return [True,pattern]
    return [False,'nop']


def PDCB(df,index):
    date=datetime.fromtimestamp(int(df.at[index, 'date']),IST).strftime("%a")
    if date=="Mon":
        predate=datetime.fromtimestamp(int(df.at[index-5, 'date']),IST).strftime("%a")
        return checkPDCB(df,index-5,index)
    if date=="Tue":
        predate=datetime.fromtimestamp(int(df.at[index-6, 'date']),IST).strftime("%a")
        return checkPDCB(df,index-6,index)
    if date=="Wed":
        predate=datetime.fromtimestamp(int(df.at[index-7, 'date']),IST).strftime("%a")
        return checkPDCB(df,index-7,index)
    if date=="Thu":
        predate=datetime.fromtimestamp(int(df.at[index-8, 'date']),IST).strftime("%a")
        return checkPDCB(df,index-8,index)
    if date=="Fri":
        return checkPDCB(df,index-9,index)



def checkPDCB(df,index,orginalIndex):
    high=0.00
    predate=datetime.fromtimestamp(int(df.at[index, 'date']),IST).strftime("%b %d %Y %I:%M%p")
    predateend=datetime.fromtimestamp(int(df.at[index+4, 'date']),IST).strftime("%b %d %Y %I:%M%p")
    for i in range(index,index+5):
        if float(df.at[i, 'high'])>high:
            high=float(df.at[i, 'high'])
    if high<float(df.at[orginalIndex, 'close']) and not high<float(df.at[orginalIndex-1, 'close']):
        return [True,predate+" "+predateend]
    return [False,predate+" "+predateend]







    
