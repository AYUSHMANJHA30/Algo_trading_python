import numpy as np
import pandas as pd
import requests
import math
from scipy import stats
import xlsxwriter
from statistics import mean
from secrets import IEX_CLOUD_API_TOKEN

'''For batch api calls which are faster we use this function to divide our bigger list into chunks of equal size'''
def chunks(lst,n):
    for i in range(0,len(lst),n):
        yield lst[i:i+n]

'''Function for taking valid input'''
def portfolio_input():
    global  portfolio_size
    portfolio_size=input('Enter the size of your portfolio')
    try:
        val=float(portfolio_size)
    except ValueError:
        input('That is not a number !!!!  \n Try Again')
        portfolio_size=input('Enter the size of your portfolio')


stocks=pd.read_csv('../sp_500_stocks.csv')
symbol='AAPL'
api_url=f'https://sandbox.iexapis.com/stable/stock/{symbol}/stats?token={IEX_CLOUD_API_TOKEN}'
data=requests.get(api_url).json()
symbol_groups=list(chunks(stocks['Ticker'],100))
symbol_strings=[]

for i in range(0,len(symbol_groups)):
    symbol_strings.append(','.join(symbol_groups[i]))
    #print(symbol_strings[i])

hqm_columns = [
                'Ticker',
                'Price',
                'Number of Shares to Buy',
                'One-Year Price Return',
                'One-Year Return Percentile',
                'Six-Month Price Return',
                'Six-Month Return Percentile',
                'Three-Month Price Return',
                'Three-Month Return Percentile',
                'One-Month Price Return',
                'One-Month Return Percentile',
                'HQM Score'
                ]

hqm_dataframe = pd.DataFrame(columns = hqm_columns)

for symbol_string in symbol_strings:
    #print(symbol_strings)
    batch_api_call_url = f'https://sandbox.iexapis.com/stable/stock/market/batch/?types=stats,quote&symbols={symbol_string}&token={IEX_CLOUD_API_TOKEN}'
    data = requests.get(batch_api_call_url).json()
    for symbol in symbol_string.split(','):
        hqm_dataframe = hqm_dataframe.append(
            pd.Series([symbol,
                       data[symbol]['quote']['latestPrice'],
                       'N/A',
                       data[symbol]['stats']['year1ChangePercent'],
                       'N/A',
                       data[symbol]['stats']['month6ChangePercent'],
                       'N/A',
                       data[symbol]['stats']['month3ChangePercent'],
                       'N/A',
                       data[symbol]['stats']['month1ChangePercent'],
                       'N/A',
                       'N/A'
                       ],
                      index = hqm_columns),
            ignore_index = True)

hqm_dataframe.fillna(0,inplace=True)
time_periods = [
                'One-Year',
                'Six-Month',
                'Three-Month',
                'One-Month'
                ]

for row in hqm_dataframe.index:
    for time_period in time_periods:
        hqm_dataframe.loc[row, f'{time_period} Return Percentile'] = stats.percentileofscore(hqm_dataframe[f'{time_period} Price Return'], hqm_dataframe.loc[row, f'{time_period} Price Return'])/100

for row in hqm_dataframe.index:
    momentum_percentiles=[]
    for time_period in time_periods:
        momentum_percentiles.append(hqm_dataframe.loc[row,f'{time_period} Return Percentile'])
    hqm_dataframe.loc[row,'HQM Score']    =mean(momentum_percentiles)

hqm_dataframe.sort_values('HQM Score',ascending=False,inplace=True)
hqm_dataframe=hqm_dataframe[:51]
hqm_dataframe.reset_index(drop=True,inplace=True)
portfolio_input()
print(portfolio_size)
position_size=float(portfolio_size)/len(hqm_dataframe.index)

for row in hqm_dataframe.index:
    hqm_dataframe.loc[row,'Number of Shares to Buy']=math.floor(position_size/hqm_dataframe.loc[row,'Price'])

print(hqm_dataframe)
hqm_dataframe.to_csv('final2.csv')

