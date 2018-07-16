# t1-p1
# Exploring weather trends
# Jesse Fredrickson

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# SQL: search through available cities in city_list
# SELECT *
# FROM city_list
# WHERE country = 'United States'
# ORDER BY city

# SQL: query city_data to get temperatures for Boston
# SELECT *
# FROM city_data
# WHERE city = 'Boston' OR city = 'boston'
# ORDER BY year

# SQL: query global_data to get global temperatures
# SELECT *
# FROM global_data
# ORDER BY year

# read boston and global data as dataframes
pth = 'C:/Users/Jesse/Documents/PyData/DAND_t1_p1/'

df_boston = pd.read_csv(pth + 'boston_weather.csv')
df_global = pd.read_csv(pth + 'global_weather.csv')

# join dataframes by year
df = df_boston.set_index('year').join(df_global.set_index('year'), rsuffix='_global', )

# get rolling mean columns for boston and global weather
df['boston_rolling_temp'] = df['avg_temp'].rolling(10, min_periods=10).mean()
df['global_rolling_temp'] = df['avg_temp_global'].rolling(10, min_periods=10).mean()

# clean missing data
df_clean = df.dropna(subset=['boston_rolling_temp', 'global_rolling_temp'], how='any')

# form linear regression trendlines
trend_bos = np.polyfit(df_clean.index, df_clean['boston_rolling_temp'], 3)
bos_trend_p = np.poly1d(trend_bos)
df_clean['trend_bos'] = bos_trend_p(df_clean.index)

trend_global = np.polyfit(df_clean.index, df_clean['global_rolling_temp'], 3)
global_trend_p = np.poly1d(trend_global)
df_clean['trend_global'] = global_trend_p(df_clean.index)


def r_squared(y, y_fit):
    # returns the coefficient of determination for y and y_fit
    ybar = np.sum(y) / len(y)
    ssreg = np.sum((y_fit - ybar) ** 2)
    sstot = np.sum((y - ybar) ** 2)
    determination = ssreg / sstot

    return determination


# get R^2 values for the fit lines
boston_r2 = r_squared(df_clean['boston_rolling_temp'], df_clean['trend_bos'])
global_r2 = r_squared(df_clean['global_rolling_temp'], df_clean['trend_global'])

# Plot
df_clean.plot(y=['boston_rolling_temp', 'global_rolling_temp', 'trend_bos', 'trend_global'])
plt.legend(['Boston', 'Global', 'Boston Trend' + ' (R2 {:.3f})'.format(boston_r2),
            'Global Trend' + ' (R2 {:.3f})'.format(global_r2)])
plt.title('Local and Global Temperatures')
plt.ylabel('Temperature (C)')
plt.xlabel('Year')
plt.ylim((5, 10))
plt.show()
