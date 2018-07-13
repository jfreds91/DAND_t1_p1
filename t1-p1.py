# t1-p1
# Exploring weather trends
# Jesse Fredrickson

import pandas as pd
import matplotlib.pyplot as plt

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
# df_global.rename(index=str, columns={'year': 'year_global', 'avg_temp': 'avg_temp_global'}, inplace=True)

# join dataframes by year
df = df_boston.set_index('year').join(df_global.set_index('year'), rsuffix='_global',)

# get rolling mean columns for boston and global weather
df['boston_rolling_temp'] = df['avg_temp'].rolling(10, min_periods=10).mean()
df['global_rolling_temp'] = df['avg_temp_global'].rolling(10, min_periods=10).mean()

# Plot
ax = df.plot(y=['avg_temp', 'avg_temp_global'])
ax.legend(['Boston', 'Global'])
plt.show()

print('done')