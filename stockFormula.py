##
from re import L
import requests
from datetime import datetime, timedelta
import time
import pytz
from pytz import timezone
import pandas as pd
import pandas_ta as ta
import numpy as np
import talib
import pandas_ta as ta


def RSI(df):
    close = df['close']
    rsi = talib.RSI(close, timeperiod=14)
    rsi2 = talib.RSI(close, timeperiod=14)
    df['rsi'] = rsi
    df['rsi2'] = rsi2
    return df

     
def RSIMovingAverage(list,index,divident):
    data = list[:index+1]
    data = data[-divident:]
    sum=0.00
    for i in data:
        sum=sum+ RSI(list,list.index(i),divident)
    return(sum/divident)

def MovingAverage(df):
    df['MA200'] = df['close'].rolling(200).mean()
    df['MA100'] = df['close'].rolling(100).mean()
    df['MA50'] = df['close'].rolling(50).mean()
    df['MA20'] = df['close'].rolling(20).mean()
    df['MA14'] = df['close'].rolling(14).mean()
    df['MA5'] = df['close'].rolling(5).mean()
    return df

def AverageVolume(df) :
    df['av']  = df['volume'].rolling(30).mean()
    return df
       
def hikendataconvertion(data):
    hikendata =  data.copy()
    for i in data[1:] :
         prevdata=hikendata[data.index(i)-1].split(",")
         arrdata=data[data.index(i)].split(",")
         HAopen=round(((float(prevdata[1]) + float(prevdata[4]))/2),2)
         HAclose=round(((float(arrdata[1])+float(arrdata[4])+float(arrdata[2])+float(arrdata[3]))/4),2)
         testdata=arrdata[0]+","+str(round(((float(prevdata[1]) + float(prevdata[4]))/2),2))+","+str(max(HAopen,HAclose,float(arrdata[2])))+","+str(min(HAopen,HAclose,float(arrdata[3])))+","+str(round(((float(arrdata[1])+float(arrdata[4])+float(arrdata[2])+float(arrdata[3]))/4),2))+","+arrdata[5]
         hikendata[data.index(i)]=testdata
    return hikendata

def convertToDF(data):
    return  pd.DataFrame({
                    'date':data["t"],
                    'open': data["o"],
                    'high': data["h"],
                    'low':data["l"],
                    'close':data["c"],
                    'volume':data["v"]})
                    
def VWMA(df):
    df['vwma'] = df.ta.vwma(length = 20,fillna=True)
    return df

def VA(df,type):
    if type=="1WVA":
         df['1WVA'] = df['volume'].rolling(5).mean()
    return df
        

    
def MACD(df):
    # Get the 26-day EMA of the closing price
    k = df['close'].ewm(span=12, adjust=False, min_periods=12).mean()
    # Get the 12-day EMA of the closing price
    d = df['close'].ewm(span=26, adjust=False, min_periods=26).mean()
    # Subtract the 26-day EMA from the 12-Day EMA to get the MACD
    macd = k - d
    # Get the 9-Day EMA of the MACD for the Trigger line
    macd_s = macd.ewm(span=9, adjust=False, min_periods=9).mean()
    # Calculate the difference between the MACD - Trigger for the Convergence/Divergence value
    macd_h = macd - macd_s
    # Add all of our new values for the MACD to the dataframe
    df['macd'] = df.index.map(macd)
    df['macd_h'] = df.index.map(macd_h)
    df['macd_s'] = df.index.map(macd_s)

    return df

# responseday = requests.get("https://api.upstox.com/historical/NSE_EQ/1660/day?timestamp=")
# data=responseday.json()['data']
# print(data.index(data[-1]))
# index=data.index(data[-4])
# print (data[index])
# hikendata=hikendataconvertion(data)
# MovingAverage(hikendata,index,50)todate = datetime.today()
def heikin_ashi(df):
    heikin_ashi_df = pd.DataFrame(index=df.index.values, columns=['open', 'high', 'low', 'close'])
    
    heikin_ashi_df['close'] = (df['open'] + df['high'] + df['low'] + df['close']) / 4
    
    for i in range(len(df)):
        if i == 0:
            heikin_ashi_df.iat[0, 0] = df['open'].iloc[0]
        else:
            heikin_ashi_df.iat[i, 0] = (heikin_ashi_df.iat[i-1, 0] + heikin_ashi_df.iat[i-1, 3]) / 2
        
    heikin_ashi_df['high'] = heikin_ashi_df.loc[:, ['open', 'close']].join(df['high']).max(axis=1)
    
    heikin_ashi_df['low'] = heikin_ashi_df.loc[:, ['open', 'close']].join(df['low']).min(axis=1)
    heikin_ashi_df['volume']=df['volume']
    heikin_ashi_df['date']=df['date']

    return heikin_ashi_df


def bollinger_bands(df):
    currunt_upper_bollinger_band = ta.bbands(df["close"], length=20, std=2)
    df['up']=currunt_upper_bollinger_band["BBU_20_2.0"]
    df['down']=currunt_upper_bollinger_band["BBL_20_2.0"]
    df['middle']=currunt_upper_bollinger_band["BBM_20_2.0"]
    return df
   
def ADX(df):
    df['adx']  = talib.ADX(df['high'], df['low'], df['close'], timeperiod=14)
    return df
    
def percentageCalc(num1,num2):
    x=abs(num1-num2)
    y=num1+num2
    z=x/y
    return z*100

def findPercentage(num1,num2):
    return int(num1)/int(num2)*100

