import pandas as pd
import pandas_ta as ta
import numpy as np
import talib


                    
def VWMA(df):
    df['vwma'] = df.ta.vwma(length = 20,fillna=True)
    return df

def calculate_supertrend(df_original, period=10, multiplier=3):
    df = df_original.copy(deep=True)
    df = df.set_index("time")
    df['High-Low']=abs(df['high']-df['low'])
    df['High-PreviousClose']=abs(df['high']-df['close'].shift(1))
    df['Low-PreviousClose']=abs(df['low']-df["close"].shift(1))
    df['TrueRange']=df[['High-Low','High-PreviousClose','Low-PreviousClose']].max(axis=1,skipna=False)
    df['ATR']=df['TrueRange'].rolling(window=period).mean()

    df["BASIC_UPPERBAND"]=((df['high']+df['low'])/2) + multiplier*df['ATR'] 
    df["BASIC_LOWERBAND"]=((df['high']+df['low'])/2) - multiplier*df['ATR']
    df["FINAL_UPPERBAND"]=df["BASIC_UPPERBAND"]
    df["FINAL_LOWERBAND"]=df["BASIC_LOWERBAND"]
    ind = df.index
    for i in range(period,len(df)):
        if df['close'][i-1]<=df['FINAL_UPPERBAND'][i-1]:
            df.loc[ind[i],'FINAL_UPPERBAND']=min(df['BASIC_UPPERBAND'][i],df['FINAL_UPPERBAND'][i-1])
        else:
            df.loc[ind[i],'FINAL_UPPERBAND']=df['BASIC_UPPERBAND'][i]    
    for i in range(period,len(df)):
        if df['close'][i-1]>=df['FINAL_LOWERBAND'][i-1]:
            df.loc[ind[i],'FINAL_LOWERBAND']=max(df['BASIC_LOWERBAND'][i],df['FINAL_LOWERBAND'][i-1])
        else:
            df.loc[ind[i],'FINAL_LOWERBAND']=df['BASIC_LOWERBAND'][i]  
    df['Strend']=np.nan
    for test in range(period,len(df)):
        if df['close'][test-1]<=df['FINAL_UPPERBAND'][test-1] and df['close'][test]>df['FINAL_UPPERBAND'][test]:
            df.loc[ind[test],'Strend']=df['FINAL_LOWERBAND'][test]
            break
        if df['close'][test-1]>=df['FINAL_LOWERBAND'][test-1] and df['close'][test]<df['FINAL_LOWERBAND'][test]:
            df.loc[ind[test],'Strend']=df['FINAL_UPPERBAND'][test]
            break
    for i in range(test+1,len(df)):
        if df['Strend'][i-1]==df['FINAL_UPPERBAND'][i-1] and df['close'][i]<=df['FINAL_UPPERBAND'][i]:
            df.loc[ind[i],'Strend']=df['FINAL_UPPERBAND'][i]
        elif  df['Strend'][i-1]==df['FINAL_UPPERBAND'][i-1] and df['close'][i]>=df['FINAL_UPPERBAND'][i]:
            df.loc[ind[i],'Strend']=df['FINAL_LOWERBAND'][i]
        elif df['Strend'][i-1]==df['FINAL_LOWERBAND'][i-1] and df['close'][i]>=df['FINAL_LOWERBAND'][i]:
            df.loc[ind[i],'Strend']=df['FINAL_LOWERBAND'][i]
        elif df['Strend'][i-1]==df['FINAL_LOWERBAND'][i-1] and df['close'][i]<=df['FINAL_LOWERBAND'][i]:
            df.loc[ind[i],'Strend']=df['FINAL_UPPERBAND'][i]

    df = df.reset_index(drop=True)
    df_original["SuperTrend"]=df['Strend']
  

    return df_original

def calculate_supertrend_EWM(df_original, period=10, multiplier=3):
    df = df_original.copy(deep=True)
    df = df.set_index("time")
    df['High-Low']=abs(df['high']-df['low'])
    df['High-PreviousClose']=abs(df['high']-df['close'].shift(1))
    df['Low-PreviousClose']=abs(df['low']-df["close"].shift(1))
    df['TrueRange']=df[['High-Low','High-PreviousClose','Low-PreviousClose']].max(axis=1,skipna=False)
    df['ATREWM']=df['TrueRange'].ewm(com=period,min_periods=period).mean()

    df["BASIC_UPPERBAND"]=((df['high']+df['low'])/2) + multiplier*df['ATREWM'] 
    df["BASIC_LOWERBAND"]=((df['high']+df['low'])/2) - multiplier*df['ATREWM']
    df["FINAL_UPPERBAND"]=df["BASIC_UPPERBAND"]
    df["FINAL_LOWERBAND"]=df["BASIC_LOWERBAND"]
    ind = df.index
    for i in range(period,len(df)):
        if df['close'][i-1]<=df['FINAL_UPPERBAND'][i-1]:
            df.loc[ind[i],'FINAL_UPPERBAND']=min(df['BASIC_UPPERBAND'][i],df['FINAL_UPPERBAND'][i-1])
        else:
            df.loc[ind[i],'FINAL_UPPERBAND']=df['BASIC_UPPERBAND'][i]    
    for i in range(period,len(df)):
        if df['close'][i-1]>=df['FINAL_LOWERBAND'][i-1]:
            df.loc[ind[i],'FINAL_LOWERBAND']=max(df['BASIC_LOWERBAND'][i],df['FINAL_LOWERBAND'][i-1])
        else:
            df.loc[ind[i],'FINAL_LOWERBAND']=df['BASIC_LOWERBAND'][i]  
    df['Strend']=np.nan
    for test in range(period,len(df)):
        if df['close'][test-1]<=df['FINAL_UPPERBAND'][test-1] and df['close'][test]>df['FINAL_UPPERBAND'][test]:
            df.loc[ind[test],'Strend']=df['FINAL_LOWERBAND'][test]
            break
        if df['close'][test-1]>=df['FINAL_LOWERBAND'][test-1] and df['close'][test]<df['FINAL_LOWERBAND'][test]:
            df.loc[ind[test],'Strend']=df['FINAL_UPPERBAND'][test]
            break
    for i in range(test+1,len(df)):
        if df['Strend'][i-1]==df['FINAL_UPPERBAND'][i-1] and df['close'][i]<=df['FINAL_UPPERBAND'][i]:
            df.loc[ind[i],'Strend']=df['FINAL_UPPERBAND'][i]
        elif  df['Strend'][i-1]==df['FINAL_UPPERBAND'][i-1] and df['close'][i]>=df['FINAL_UPPERBAND'][i]:
            df.loc[ind[i],'Strend']=df['FINAL_LOWERBAND'][i]
        elif df['Strend'][i-1]==df['FINAL_LOWERBAND'][i-1] and df['close'][i]>=df['FINAL_LOWERBAND'][i]:
            df.loc[ind[i],'Strend']=df['FINAL_LOWERBAND'][i]
        elif df['Strend'][i-1]==df['FINAL_LOWERBAND'][i-1] and df['close'][i]<=df['FINAL_LOWERBAND'][i]:
            df.loc[ind[i],'Strend']=df['FINAL_UPPERBAND'][i]

    df = df.reset_index(drop=True)
    df_original["SuperTrendEWM"]=df['Strend']

    return df_original