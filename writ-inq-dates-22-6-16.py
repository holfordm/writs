# -*- coding: utf-8 -*-
"""
Created on Wed May 11 12:46:30 2016

@author: Matthew Holford
"""

import pandas as pd




#import the data

#note that all dates need to be in the form YYYY-MM-DD

df = pd.read_csv('vol21dates.csv', names=['inqRef', 'county', 'writType', 'writDate', 'inqDate'])

#create a new column for the date interval
#cf http://chrisalbon.com/python/pandas_create_column_with_loop.html
#http://stackoverflow.com/questions/22132525/add-column-with-number-of-days-between-dates-in-dataframe-pandas

#note that these dates cannot be converted to "datetime64" using the to_datetime function
#for dealing with 'out of bounds' dates (before c.1677) see http://pandas.pydata.org/pandas-docs/stable/timeseries.html#timeseries-oob


intervals = []
writYear = []
writMonth = []
for row in df.iterrows():

    if row[1].writDate == 'Not available' or row[1].inqDate == 'Not available':
        intervals.append('Not available')
    else:
        
        dateSplit = row[1].writDate.split('-')
        writDate = pd.Period(row[1].writDate)
       
        inqDate = pd.Period(row[1].inqDate)
        
        #row[1].writDate = writDate
        #row[1].inqDate = inqDate
        
        
        
        try:
            interval = inqDate - writDate
        except:
            interval = 'NaN'
        
        
        #neccesary to give interval as integer number of days only
        intervals.append(interval)
        writYear.append(dateSplit[0])
        writMonth.append(dateSplit[1])
        
        
        
#debug        
        print(row[1].inqRef, writDate, inqDate, interval)

df['interval(days)'] = intervals
df['writYear'] = writYear
df['writMonth'] = writMonth






#change data type of intervals to numeric
df['interval(days)'] = df['interval(days)'].astype('int64')


#?index by writ period -need to look into this more
#df.index = df['writPeriod']

#sort on writDate

sorted = df.sort('writDate')
 #sorted.plot(x='writDate', y='interval(days)')
#sorted[sorted['county'] == 'Norfolk'].plot(x='writDate', y='interval(days)')

#cannot convert to a time series or period index because data is not of regular frequency
#ts = pd.PeriodIndex(df['interval(days)'], index=df['writPeriod']) #turns all values to NaN
#ts = pd.Series(df['interval(days)']
 

#dateRange = pd.Period('1419-01-01', '1422-12-31')
#but if you try and turn it into a dataFrame it becomes integers
#dR = pd.DataFrame(data=dateRange)

dates = []
means = []
data = []
for year in range(1419, 1422):
    for month in range(1, 13):
        ymdf = df[(df['writYear'] == str(year)) & (df['writMonth'] == str(month).zfill(2))]
        mean = ymdf['interval(days)'].mean()
        datum = [str(year)+'-'+str(month), mean]        
        
        data.append(datum)
        means.append(mean)
        dates.append(str(year)+'-'+str(month).zfill(2))
        
ts=pd.DataFrame(data=[dates, means])
ts = ts.transpose()
#ts.plot()
