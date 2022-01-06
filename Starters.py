''' The code below is for calculating Number of Shares to Buy just on the basis of One-Year Price Return which not a very good indicator and is just calculated for starting with something very basic '''

'''my_columns= ['Ticker','Price','One-Year Price Return','Number of Shares to Buy']
final_dataframe=pd.DataFrame(columns=my_columns)

for symbol_string in symbol_strings:
    batch_api_url = f'https://sandbox.iexapis.com/stable/stock/market/batch/?types=stats,quote&symbols={symbol_string}&token={IEX_CLOUD_API_TOKEN}'
    data=requests.get(batch_api_url).json()
    for symbol in symbol_string.split(','):
        print(symbol)
        final_dataframe=final_dataframe.append(
                   pd.Series(
                   [
                       symbol,
                       data[symbol]['quote']['latestPrice'],
                       data[symbol]['stats']['year1ChangePercent'],
                     'N/A'
                   ],
                   index=my_columns),
                   ignore_index=True
               )

final_dataframe.sort_values('One-Year Price Return',ascending=False,inplace=True)
final_dataframe=final_dataframe[:51]
final_dataframe.reset_index(drop=True,inplace=True)
#print(final_dataframe)

portfolio_input()
print(portfolio_size)
position_size=float(portfolio_size)/len(final_dataframe.index)

for i in range(0,len(final_dataframe.index)):
    final_dataframe.loc[i,'Number of Shares to Buy']=math.floor(position_size/final_dataframe['Price'][i])'''


