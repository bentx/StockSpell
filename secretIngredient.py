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

def movingAverageFormula(ha_df,currIndex,preHigh,preLow,high,low):
    if(int(ha_df.at[currIndex, '1WVA'])>8000000 and float(preHigh)>=float(preLow) and float(high)<=float(low) ):
        
        return True      
    return False       

def OpenPercentageGap(prevclose,open,av):
    return float(prevclose)>float(open) and int(av)>50000 and stockFormula.percentageCalc(prevclose,open)>2 and  stockFormula.percentageCalc(prevclose,open)<8

def WA1Stratagy1(ha_df,currIndex):
    if (int(ha_df.at[currIndex, '1WVA'])>8000000 and  "RRRG1"==dataUtility.findCandleType(ha_df,currIndex-3)+dataUtility.findCandleType(ha_df,currIndex-2)+dataUtility.findCandleType(ha_df,currIndex-1)+dataUtility.findCandleType(ha_df,currIndex) )and (dataUtility.isTouchLow(ha_df,currIndex-1) or (dataUtility.isTouchLow(ha_df,currIndex-2))):
        return True
    return False


def WA1Stratagy2(ha_df,currIndex):
    if (int(ha_df.at[currIndex, '1WVA'])>8000000 and  "RRRR1"==dataUtility.findCandleType(ha_df,currIndex-3)+dataUtility.findCandleType(ha_df,currIndex-2)+dataUtility.findCandleType(ha_df,currIndex-1)+dataUtility.findCandleType(ha_df,currIndex) )and (dataUtility.isTouchLow(ha_df,currIndex-1) or (dataUtility.isTouchLow(ha_df,currIndex-2))) and not (dataUtility.isTouchLow(ha_df,currIndex) ):
        return True
    return False

def bodyTouch(ha_df,currIndex,ma):
     if (int(ha_df.at[currIndex, '1WVA'])<4000000 and float(ha_df.at[currIndex, ma])>float(ha_df.at[currIndex, 'open']) and float(ha_df.at[currIndex, ma]) < float(ha_df.at[currIndex, 'close']) and "GGG"==dataUtility.findCandleType(ha_df,currIndex-2)+dataUtility.findCandleType(ha_df,currIndex-1)+dataUtility.findCandleType(ha_df,currIndex) ):
        return True 
     return False

def wigTouch(ha_df,currIndex,ma):
     if (int(ha_df.at[currIndex, '1WVA'])<4000000 and float(ha_df.at[currIndex, ma])>float(ha_df.at[currIndex, 'low']) and float(ha_df.at[currIndex, ma]) < float(ha_df.at[currIndex, 'open']) and "R1G1"==dataUtility.findCandleType(ha_df,currIndex-1)+dataUtility.findCandleType(ha_df,currIndex) ):
        return True
     return False

def TopGainer(df,currIndex,percentage):
    if float(df.at[currIndex-1, 'close']) <float(df.at[currIndex, 'close']):
        percent=stockFormula.percentageCalc(float(df.at[currIndex-1, 'close']) ,float(df.at[currIndex, 'close']))
        if(percent>percentage and percent<percentage+1):
            return True     
    return False

def RSAADX(df,currentIndex):
    if int(df.at[currentIndex, 'rsi2']) <25 and int(df.at[currentIndex, 'adx'])>20 :
        return True
    return False
    
