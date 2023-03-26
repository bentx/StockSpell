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
from scipy import stats

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

def pivotePoints(data_ohlc):
    data_ohlc['pivote'] = (data_ohlc['preMonthHigh'] + data_ohlc['preMonthLow'] + data_ohlc['preMonthClose'])/3
    data_ohlc['R1'] = (2*data_ohlc['pivote']) - data_ohlc['preMonthLow']
    data_ohlc['S1'] = (2*data_ohlc['pivote']) - data_ohlc['preMonthHigh']
    data_ohlc['R2'] = (data_ohlc['pivote']) + (data_ohlc['preMonthHigh'] - data_ohlc['preMonthLow'])
    data_ohlc['S2'] = (data_ohlc['pivote']) - (data_ohlc['preMonthHigh'] - data_ohlc['preMonthLow'])
    data_ohlc['R3'] = (data_ohlc['R1']) + (data_ohlc['preMonthHigh'] - data_ohlc['preMonthLow'])
    data_ohlc['S3'] = (data_ohlc['S1']) - (data_ohlc['preMonthHigh'] - data_ohlc['preMonthLow'])
    data_ohlc['R4'] = (data_ohlc['R3']) + (data_ohlc['R2'] - data_ohlc['R1'])
    data_ohlc['S4'] = (data_ohlc['S3']) - (data_ohlc['S1'] - data_ohlc['S2'])
    return data_ohlc


def pivotePointsYearly(data_ohlc):
    data_ohlc['pivoteYear'] = (data_ohlc['preYearHigh'] + data_ohlc['preYearLow'] + data_ohlc['preYearClose'])/3
    data_ohlc['R1Year'] = (2*data_ohlc['pivoteYear']) - data_ohlc['preYearLow']
    data_ohlc['S1Year'] = (2*data_ohlc['pivoteYear']) - data_ohlc['preYearHigh']
    data_ohlc['R2Year'] = (data_ohlc['pivoteYear']) + (data_ohlc['preYearHigh'] - data_ohlc['preYearLow'])
    data_ohlc['S2Year'] = (data_ohlc['pivoteYear']) - (data_ohlc['preYearHigh'] - data_ohlc['preYearLow'])
    data_ohlc['R3Year'] = (data_ohlc['R1Year']) + (data_ohlc['preYearHigh'] - data_ohlc['preYearLow'])
    data_ohlc['S3Year'] = (data_ohlc['S1Year']) - (data_ohlc['preYearHigh'] - data_ohlc['preYearLow'])
    data_ohlc['R4Year'] = (data_ohlc['R3Year']) + (data_ohlc['R2Year'] - data_ohlc['R1Year'])
    data_ohlc['S4Year'] = (data_ohlc['S3Year']) - (data_ohlc['S1Year'] - data_ohlc['S2Year'])
    return data_ohlc

def unix_to_iso(unix_timestamp):
    return datetime.fromtimestamp(unix_timestamp).strftime("%d-%b-%Y")

def getValWithKey(year,month,df2,pos):
    try:
        key=0
        if(month==1):
            key=(year-1,12)
        else:
            key=(year,month-1)
        return df2.loc[key][pos]
    except KeyError as e:
           return 0

def getValWithKeyforweekly(year,week,df2,pos):
    try:
        key=(year,week)
        return df2.loc[key][pos]
    except KeyError as e:
           return 0

def getValWithKeyforYearly(year,df2,pos):
    try:
        return df2.loc[year-1][pos]
    except KeyError as e:
           return 0

def convertToMonthly(df):
    IST = pytz.timezone('Asia/Kolkata')
    df['Timestamp'] = df['date'].apply(unix_to_iso)
    # Converting date to pandas datetime format
    df['DateTime'] = pd.to_datetime(df['Timestamp'])
    #Getting Week number
    df['Week_Number'] = df['DateTime'].dt.isocalendar().week
    # Getting month number
    df['Month_Number'] = df['DateTime'].dt.month
    # Getting year. month is common across years (as if you dont know :) )to we need to create unique index by using year and month
    df['Year'] = df['DateTime'].dt.year
    # Grouping based on required values
    df2 = df.groupby(['Year','Month_Number']).agg({'open':'first', 'high':'max', 'low':'min', 'close':'last','volume':'sum'})
    df['preMonthOpen'] = df.apply(lambda x: getValWithKey(x['Year'], x['Month_Number'],df2,'open'),axis=1)
    df['preMonthClose'] = df.apply(lambda x: getValWithKey(x['Year'], x['Month_Number'],df2,'close'),axis=1)
    df['preMonthLow'] = df.apply(lambda x: getValWithKey(x['Year'], x['Month_Number'],df2,'low'),axis=1)
    df['preMonthHigh'] = df.apply(lambda x: getValWithKey(x['Year'], x['Month_Number'],df2,'high'),axis=1)
    return df

def convertToMonthly_ha(ha_df,df):
    IST = pytz.timezone('Asia/Kolkata')
    ha_df['Timestamp'] = ha_df['date'].apply(unix_to_iso)
    # Converting date to pandas datetime format
    ha_df['DateTime'] = pd.to_datetime(ha_df['Timestamp'])
    # Getting month number
    ha_df['Month_Number'] = ha_df['DateTime'].dt.month
    # Getting week number
    ha_df['Week_Number'] = ha_df['DateTime'].dt.isocalendar().week
    # Getting year. month is common across years (as if you dont know :) )to we need to create unique index by using year and month
    ha_df['Year'] = ha_df['DateTime'].dt.year
    # Grouping based on required values
    dfW = df.groupby(['Year','Week_Number']).agg({'open':'first', 'high':'max', 'low':'min', 'close':'last','volume':'sum'})
    dfW=heikin_ashi_for_MultiKey(dfW)
    ha_df['preWeekOpen'] = ha_df.apply(lambda x: getValWithKeyforweekly(x['Year'], x['Week_Number'],dfW,'open'),axis=1)
    ha_df['preWeekClose'] = ha_df.apply(lambda x: getValWithKeyforweekly(x['Year'], x['Week_Number'],dfW,'close'),axis=1)
    ha_df['preWeekLow'] = ha_df.apply(lambda x: getValWithKeyforweekly(x['Year'], x['Week_Number'],dfW,'low'),axis=1)
    ha_df['preWeekHigh'] = ha_df.apply(lambda x: getValWithKeyforweekly(x['Year'], x['Week_Number'],dfW,'high'),axis=1)
    dfM = df.groupby(['Year','Month_Number']).agg({'open':'first', 'high':'max', 'low':'min', 'close':'last','volume':'sum'})
    dfM=heikin_ashi_for_MultiKey(dfM)
    ha_df['preMonthOpen'] = ha_df.apply(lambda x: getValWithKey(x['Year'], x['Month_Number'],dfM,'open'),axis=1)
    ha_df['preMonthClose'] = ha_df.apply(lambda x: getValWithKey(x['Year'], x['Month_Number'],dfM,'close'),axis=1)
    ha_df['preMonthLow'] = ha_df.apply(lambda x: getValWithKey(x['Year'], x['Month_Number'],dfM,'low'),axis=1)
    ha_df['preMonthHigh'] = ha_df.apply(lambda x: getValWithKey(x['Year'], x['Month_Number'],dfM,'high'),axis=1)
    dfY = df.groupby(['Year']).agg({'open':'first', 'high':'max', 'low':'min', 'close':'last','volume':'sum'})
    dfY = dfY.tail(-1)
    dfY=heikin_ashi_for_MultiKey(dfY)
    ha_df['preYearOpen'] = ha_df.apply(lambda x: getValWithKeyforYearly(x['Year'],dfY,'open'),axis=1)
    ha_df['preYearClose'] = ha_df.apply(lambda x: getValWithKeyforYearly(x['Year'],dfY,'close'),axis=1)
    ha_df['preYearLow'] = ha_df.apply(lambda x: getValWithKeyforYearly(x['Year'],dfY,'low'),axis=1)
    ha_df['preYearHigh'] = ha_df.apply(lambda x: getValWithKeyforYearly(x['Year'],dfY,'high'),axis=1)

    return ha_df
    
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
    heikin_ashi_df['candle'] = heikin_ashi_df.apply(lambda row : candlefinder(row[0],row[3]), axis=1)

    return heikin_ashi_df

def heikin_ashi_for_MultiKey(df):
    heikin_ashi_df = pd.DataFrame(index=df.index, columns=['open', 'high', 'low', 'close'])
    
    heikin_ashi_df['close'] = (df['open'] + df['high'] + df['low'] + df['close']) / 4
    
    for i in range(len(df)):
        if i == 0:
            heikin_ashi_df.iat[0, 0] = df['open'].iloc[0]
        else:
            heikin_ashi_df.iat[i, 0] = (heikin_ashi_df.iat[i-1, 0] + heikin_ashi_df.iat[i-1, 3]) / 2
        
    heikin_ashi_df['high'] = heikin_ashi_df.loc[:, ['open', 'close']].join(df['high']).max(axis=1)
    
    heikin_ashi_df['low'] = heikin_ashi_df.loc[:, ['open', 'close']].join(df['low']).min(axis=1)
    heikin_ashi_df['volume']=df['volume']
    #heikin_ashi_df['date']=df['date']
    #heikin_ashi_df['candle'] = heikin_ashi_df.apply(lambda row : candlefinder(row[0],row[3]), axis=1)

    return heikin_ashi_df

def candlefinder(open,close):
    if float(close) > float(open):
        return "G"
    else:
        return "R"  



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



def get_rolling_ret(df,n):
    return df.rolling(n).apply(np.prod)

def get_top10(ret_12,ret_6,ret_3,date):
    top_50=ret_12.loc[date].nlargest(50).index
    top_30=ret_6.loc[date,top_50].nlargest(30).index
    top_10=ret_3.loc[date,top_30].nlargest(10).index
    return top_10

def get_top10_WithStratagy(ret_12,ret_6,ret_3,date,stockList):
    filter = ret_12.reindex(columns = stockList)
    top_50=filter.loc[date].nlargest(8).index
    top_30=ret_6.loc[date,top_50].nlargest(5).index
    top_10=ret_3.loc[date,top_30].nlargest(3).index
    return top_10

def pf_perfomance(mtl,date):
    portfolio = mtl.loc[date:,get_top10(date)][1:2]
    return portfolio.mean(axis=1).values[0]

def get_linear_equation(x1,y1,x2,y2):
    x = np.array([x1, x2])
    y = np.array([y1, y2])

    # find the slope and intercept of the line    
    slope, intercept, r_value, p_value, std_err = stats.linregress(x,y)
    return  slope, intercept


def check_breakout(x,y,m,c):
    print(x,y,m,c)
    print(y,m*x+c)
    if y > m*x+c:
        return True
    return False