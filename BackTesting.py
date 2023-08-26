import DataMinner
import Stratagy
import pandas as pd
import matplotlib.pyplot as plt



plt.style.use('fivethirtyeight')
plt.rcParams['figure.figsize'] = (10,5)

def update_amount(buy, sell, amount):
    quantity = amount / buy
    diff = abs(buy - sell)
    if buy < sell:
        amount += quantity * diff
    else:
        amount -= quantity * diff
    return amount

timeLine = [["day",665],["30minute",665]]
stockId = DataMinner.getSwingStockId()
#stockId = [['NSE_EQ|INE205B01023','ELECON ENG. CO. LTD']]
for id in stockId:
    stockId = id[0]
    stockName = id[1]
    print(stockName)
    dataList = DataMinner.get_stock_data(stockId,timeLine)
    for data in dataList:
        interval = data[0]
        candleData = data[1]
        hikenData = DataMinner.heikin_ashi(candleData.copy(deep=True))
        candleData = DataMinner.enrich_data(candleData)
        hikenData = DataMinner.enrich_data(hikenData)
        amount = 10000
        amountData = {'date':[],'amount':[]}
        isBuyStatus = False
        buyPrice = 0
        sellPrice = 0
        initial = -1
        final = len(candleData) - 1
        for index, row in candleData.iterrows():
            if index > initial and index < final :
                if not isBuyStatus:
                    if Stratagy.isBuy(candleData, hikenData, index):
                        isBuyStatus = True
                        buyPrice = (abs(candleData['open'][index+1] - candleData['close'][index+1])/2) + candleData['open'][index+1] 
                if isBuyStatus:
                    if Stratagy.isSell(candleData, hikenData, index):
                        isBuyStatus = False
                        sellPrice = (abs(candleData['open'][index+1] - candleData['close'][index+1])/2) + candleData['open'][index+1]
                        amount = update_amount(buyPrice, sellPrice, amount)
                        amountData['date'].append(candleData['date'][index])
                        amountData['amount'].append(amount)
            if index == final:
                if isBuyStatus:
                    sellPrice = (abs(candleData['open'][index] - candleData['close'][index])/2) + candleData['open'][index]
                    amount = update_amount(buyPrice, sellPrice, amount)
                amountData['date'].append(candleData['date'][index])
                amountData['amount'].append(amount)
        
        # amountDf = pd.DataFrame(amountData)
        # print(amountDf)
        # candleData=candleData.set_index('date')
        # plt.plot(candleData['close'],linewidth = 2)
        # plt.legend(loc = 'upper left')
        # plt.title('TSLA ST TRADING SIGNALS'+interval)
        # plt.show()

        # amountDf=amountDf.set_index('date')
        # plt.plot(amountDf['amount'],linewidth = 2)
        # plt.legend(loc = 'upper left')
        # plt.title('TSLA ST TRADING SIGNALS'+interval)
        # plt.show()

        data = {'name':[stockName],'amount':[amount]}
        df = pd.DataFrame(data)
        df.to_csv(f'./BackTestingResults/test{interval}.csv', mode='a', index=False, header=False)







