def isBuy(df, ha, index):
    if df['close'][index] > df['SuperTrendEWM'][index] and df['close'][index - 1] <= df['SuperTrendEWM'][index - 1] :   
        return True
    
def isSell(df, ha, index):
    if (df['close'][index] < df['SuperTrendEWM'][index] and df['close'][index - 1] >= df['SuperTrendEWM'][index - 1]) :               
        return True
   