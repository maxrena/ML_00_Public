import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from numpy.polynomial.chebyshev import chebfit,chebval
import pandas as pd

import warnings
warnings.filterwarnings("ignore") 

# yfinance is used to fetch data 
import yfinance as yf

yf.pdr_override()
# input
symbol = 'AMD'
start = '2017-01-01'
end = '2020-01-01'

# Read data 
dataset = yf.download(symbol,start,end)

# View Columns
print(dataset.head())
print(dataset.tail())

y = np.array(dataset['Adj Close'])

x = np.arange(len(y))
c = chebfit(x, y, 30)

p = []
for i in np.arange(len(y)):
    p.append(chebval(i, c))
df = pd.DataFrame(data={'x': x, 'y': y, 'p': p})
df['diff'] = df['y'] - df['p']
sns.set(rc={'figure.figsize':(14,10)})
sns.pointplot(x = 'x', y = 'y', data=df, color='green')
sns.pointplot(x = 'x', y = 'p', data=df, color='red')
sns.pointplot(x = 'x', y = 'diff', data=df, color='blue')


