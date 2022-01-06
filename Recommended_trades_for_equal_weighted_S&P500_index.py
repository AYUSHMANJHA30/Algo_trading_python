import numpy as np
import pandas as pd
import requests
import xlsxwriter
import math
from secrets import IEX_CLOUD_API_TOKEN

'''Yield equal sized chunks from a list'''
def chunks(lst, n):
    for i in range(0, len(lst), n):
        yield lst[i:i + n]

'''For Taking Input in valid format'''
def portfolio_input():
    global portfolio_size
    portfolio_size = input("Enter the value of your portfolio:")

    try:
        val = float(portfolio_size)
    except ValueError:
        print("That's not a number! \n Try again:")
        portfolio_size = input("Enter the value of your portfolio:")


# reading the stock data
stocks = pd.read_csv('../sp_500_stocks.csv')
symbol_groups = list(chunks(stocks['Ticker'], 100))
symbol_strings = []

'''Converting all the list chunks into comma separated values'''
for i in range(0, len(symbol_groups)):
    symbol_strings.append(','.join(symbol_groups[i]))
    #print(symbol_strings[i])


# Our final data frame
my_columns = ['Ticker', 'Stock Price', 'Market Capitilization', 'Number of shares to buy']
final_dataframe = pd.DataFrame(columns=my_columns)

for symbol_string in symbol_strings:
    batch_api_call_url = f'https://sandbox.iexapis.com/stable/stock/market/batch?symbols={symbol_string}&types=quote&token={IEX_CLOUD_API_TOKEN}'
    #print(batch_api_call_url)
    data = requests.get(batch_api_call_url).json()
    for symbol in symbol_string.split(','):
        final_dataframe = final_dataframe.append(
            pd.Series(
                [
                    symbol,
                    data[symbol]['quote']['latestPrice'],
                    data[symbol]['quote']['marketCap'],
                    'N/A'
                ],
                index=my_columns,
            ),
            ignore_index=True
        )

'''Value to invest in each stock'''
portfolio_input()
position_size=float(portfolio_size)/len(final_dataframe.index)
print(position_size)

'''Iterating through all stocks'''
for i in range(0,len(final_dataframe.index)):
    final_dataframe.loc[i,'Number of shares to buy']=math.floor(position_size/final_dataframe.loc[i,'Stock Price'])

print(final_dataframe)
final_dataframe.to_csv('final_trades.csv')

