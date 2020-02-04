from datetime import datetime
import pandas
from pandas import DataFrame as df
# import time

def main():
    KK_REVENUES = '2019'
    # KK_REVENUES = 'Revenue{}'.format((datetime.datetime.now()).year)

    revenues = prepareData(KK_REVENUES)
    extended_data = extend_data(revenues)
    print(revenues[:10])
    
def extend_data(data):
    weekNo_col = []
    weekDay_col = []

    for i, row in data.iterrows():
        dt = datetime.strptime(row.Date, '%Y-%m-%d')
        weekNo_col.append(dt.isocalendar()[1])
        weekDay_col.append(dt.weekday())

    data['WeekNo'] = weekNo_col
    data['WeekDay'] = weekDay_col
      
    # fn = lambda row: data['Date'].dt.week # define a function for the new column
    # col = data.apply(fn, axis=1) # get column data with an index
    # data  = data.assign(WeekNo=col.values) # assign values to column 'c'
    return data

def prepareData(csvFile):
    df =  pandas.read_csv(csvFile + '.csv', sep=',')

    for i, row in df.iterrows():
        date = datetime(int((df.at[i,'Date'])[6:10]), int((df.at[i,'Date'])[3:5]), int((df.at[i,'Date'])[0:2]))
        df.at[i,'Date'] = date.strftime('%Y-%m-%d')

    return df

if __name__ == '__main__':
    main()