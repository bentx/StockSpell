import requests
import pandas as pd
from datetime import datetime, timedelta
import StockIndicators


def enrich_data(df):
    df = StockIndicators.rsi(df)
    df = StockIndicators.rsi_trend(df)
    df=StockIndicators.calculate_supertrend(df)
    df=StockIndicators.calculate_supertrend_EWM(df)
    df=StockIndicators.VWMA(df)
    return df

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
    heikin_ashi_df['time']=df['time']
    heikin_ashi_df['candle'] = heikin_ashi_df.apply(lambda row : candlefinder(row[0],row[3]), axis=1)
    return heikin_ashi_df

def get_swing_stock():
    API_ENDPOINT = "https://api.tickertape.in/screener/query"
    response =requests.post(url = API_ENDPOINT, json={"match":{"mrktCapf":{"g":1000,"l":1647964.1},"lastPrice":{"g":200,"l":89070.9},"acVol":{"g":50000,"l":176950201},"4wpctN":{"g":5,"l":20}},"sortBy":"mrktCapf","sortOrder":-1,"project":["subindustry","mrktCapf","lastPrice","acVol","4wpctN"],"offset":0,"count":200,"sids":[]}
    ,headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.76 Safari/537.36', "Upgrade-Insecure-Requests": "1","DNT": "1","Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8","Accept-Language": "en-US,en;q=0.5","Accept-Encoding": "gzip, deflate"})
    response = response.json()
    data=[]
    for stockdetail in response["data"]["results"]:
        data.append(stockdetail["stock"]["info"]["ticker"])
    print(data)
    return data

def getSwingStockId():
     data = []
     try:
        swingStock = get_swing_stock()
        colNames=['StockCode', 'Name', 'NSECode'] 
        NSEColNames=['instrument_key','exchange_token','tradingsymbol','name','last_price','expiry','strike','tick_size','lot_size','instrument_type','option_type','exchange'] 
        NSEDatafile = pd.read_csv('./Stocks/NSE_EQ.csv',names=NSEColNames, header = None)
        for stockCode in swingStock:
            stockDetail=NSEDatafile.loc[NSEDatafile['tradingsymbol'] == stockCode]
            data.append([stockDetail['instrument_key'].values[:1][0],stockDetail['name'].values[:1][0]])
     except IndexError as e:
         print(e)
     return data

         
def get_stock_data(instrumentKey,timeList):
    data=[]
    for timeLine in timeList:
        interval = timeLine[0]
        toDate = datetime.today()
        fromDate = toDate - timedelta(days=timeLine[1])
        to_Date=toDate.strftime("%Y-%m-%d")
        from_Date = fromDate.strftime("%Y-%m-%d")
        response = requests.get(f"https://api-v2.upstox.com/historical-candle/{instrumentKey}/{interval}/{to_Date}/{from_Date}",headers = {"Api-Version":"2.0"})
        response = response.json()
        df = pd.DataFrame(response['data']['candles'], columns =['date', 'open', 'high', 'low', 'close', 'volume', 'random'])
        df['time'] = pd.to_datetime(df['date'], format ='%Y-%m-%dT%H:%M:%S%z')
        df = df.iloc[::-1]
        df = df.reset_index()
        df = df.drop('index', axis =1)
        if interval == '30minute':
             H1_df ,H4_df = extract_1H_and_4H_data(df)
             data.append(['1H',H1_df])
             data.append(['4H',H4_df])
        data.append([interval,df])
    return data

def extract_1H_and_4H_data(M30_df):
    H1_df = M30_df.copy(deep=True)
    H1_df = H1_df.set_index('time').resample('1H').agg({
                    'date':'first',
                    'open': 'first',
                    'high': 'max',
                    'low': 'min',
                    'close': 'last',
                    'volume': 'sum'
                })
    H1_df = H1_df.dropna() 
    H1_df = H1_df.reset_index()
    H4_df = H1_df.set_index('time').resample('4H').agg({
                    'date':'first',
                    'open': 'first',
                    'high': 'max',
                    'low': 'min',
                    'close': 'last',
                    'volume': 'sum'
                })
    H4_df = H4_df.dropna() 
    H4_df = H4_df.reset_index()
    return H1_df ,H4_df

def candlefinder(open,close):
    if float(close) > float(open):
        return "G"
    else:
        return "R"  