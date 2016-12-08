# -*- coding: utf-8 -*-
"""
Created on Wed May 11 12:46:30 2016

@author: Matthew Holford
"""

import pandas as pd
from datetime import date
import dateutil.parser


#import the data
df = pd.read_csv('vol21dates.csv', names=['inqRef', 'county', 'writType', 'writDate', 'inqDate'])

#create a new column for the date interval
#cf http://chrisalbon.com/python/pandas_create_column_with_loop.html
#http://stackoverflow.com/questions/22132525/add-column-with-number-of-days-between-dates-in-dataframe-pandas

#note that these dates cannot be converted to "datetime64" using the to_datetime function
#for dealing with 'out of bounds' dates (before c.1677) see http://pandas.pydata.org/pandas-docs/stable/timeseries.html#timeseries-oob


intervals = []
for row in df.iterrows():

    if row[1].writDate == 'Not available' or row[1].inqDate == 'Not available':
        intervals.append('Not available')
    else:
        
    
        writDate = dateutil.parser.parse(row[1].writDate)
    
        inqDate = dateutil.parser.parse(row[1].inqDate)
        interval = inqDate - writDate
        interval = str(interval)
        
        #neccesary to give interval as integer number of days only
        intervals.append(interval.split()[0])

df['interval(days)'] = intervals
df.replace('0:00:00', 0)

#row 215 has 0 days between writ and inq. which gives a value of 0:00:00

#change data type of intervals to numeric
df['interval(days)'] = df['interval(days)'].astype('int64')



#now to plot the data ... 

