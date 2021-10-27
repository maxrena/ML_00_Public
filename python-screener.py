import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import math
from datetime import datetime
from dateutil import relativedelta
import warnings
warnings.filterwarnings("ignore")

# yfinance is used to fetch data 
import yfinance as yf
yf.pdr_override()

# input
# A.I. Stock
symbols = ['NVDA','MSFT','TWLO','AMZN','GOOGL','NFLX','CRM','DE','SPLK','VERI','SNPS','QUIK','BRN.AX']
start = '2010-01-01'
end = '2020-12-20'
df = pd.DataFrame()
for s in symbols:
    df[s] = yf.download(s,start,end)['Adj Close']
    
d1 = datetime.strptime(start, "%Y-%m-%d")
d2 = datetime.strptime(end, "%Y-%m-%d")
delta = relativedelta.relativedelta(d2,d1)
print('How many years of investing?')
print('%s years' % delta.years)

number_of_years = delta.years
days = (df.index[-1] - df.index[0]).days
days
# show 5 result đầu tiên
df.head()
# show 5 result sau cùng
df.tail()

plt.figure(figsize=(12,8))
plt.plot(df)
plt.title('Artificial Intelligence Stocks Closing Price')
plt.legend(labels=df.columns)

# Normalize the data/Chuẩn hóa dữ liệu
normalize = (df - df.min())/ (df.max() - df.min())

plt.figure(figsize=(18,12))
plt.plot(normalize)
plt.title('Artificial Intelligence Stocks Normalize')
plt.legend(labels=normalize.columns)

# Xét giao thoa profit
stock_rets = df.pct_change().dropna()

plt.figure(figsize=(12,8))
plt.plot(stock_rets)
plt.title('Artificial Intelligence Stocks Returns')
plt.legend(labels=stock_rets.columns)

# Xuất tổng tích lũy 
plt.figure(figsize=(12,8))
plt.plot(stock_rets.cumsum())
plt.title('Artificial Intelligence Stocks Returns Cumulative Sum')
plt.legend(labels=stock_rets.columns)

# Sắp xếp thuật toán K-means
sns.set(style='ticks')
ax = sns.pairplot(stock_rets, diag_kind='hist')

nplot = len(stock_rets.columns)
for i in range(nplot) :
    for j in range(nplot) :
        ax.axes[i, j].locator_params(axis='x', nbins=6, tight=True)
        
ax = sns.PairGrid(stock_rets)
ax.map_upper(plt.scatter, color='purple')
ax.map_lower(sns.kdeplot, color='blue')
ax.map_diag(plt.hist, bins=30)
for i in range(nplot) :
    for j in range(nplot) :
        ax.axes[i, j].locator_params(axis='x', nbins=6, tight=True)

# mô hình dự đoán compare prof between comp
plt.figure(figsize=(7,7))
corr = stock_rets.corr()

# plot the heatmap
sns.heatmap(corr, 
        xticklabels=corr.columns,
        yticklabels=corr.columns,
            cmap="Blues")

# Box plot
stock_rets.plot(kind='box',figsize=(12,8))

rets = stock_rets.dropna()

plt.figure(figsize=(12,8))
plt.scatter(rets.mean(), rets.std(),alpha = 0.5)

plt.title('Stocks Risk & Returns')
plt.xlabel('Expected returns')
plt.ylabel('Risk')
plt.grid(which='major')

for label, x, y in zip(rets.columns, rets.mean(), rets.std()):
    plt.annotate(
        label, 
        xy = (x, y), xytext = (50, 50),
        textcoords = 'offset points', ha = 'right', va = 'bottom',
        arrowprops = dict(arrowstyle = '-', connectionstyle = 'arc3,rad=-0.3'))

# Chuẩn hóa giá trị trả về
Normalized_Value = ((rets[:] - rets[:].min()) /(rets[:].max() - rets[:].min()))
Normalized_Value.head()