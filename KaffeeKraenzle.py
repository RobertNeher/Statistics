from datetime import datetime
import pandas
from pandas import DataFrame as df
# import time

def main():
    KK_REVENUES = '2019_org.csv'
    # KK_REVENUES = 'Revenue{}'.format((datetime.datetime.now()).year)

    revenues = pandas.read_csv(KK_REVENUES, sep=',', thousands='.', parse_dates=[0], dayfirst=True)
    extended_data = extend_data(revenues)
    print(revenues[:20])
    
def extend_data(data):
    weekNo_col = []
    weekDay_col = []

    for i, row in data.iterrows():
        dt = row.Date
        weekNo_col.append(dt.isocalendar()[1])
        weekDay_col.append(dt.weekday())

    data['WeekNo'] = weekNo_col
    data['WeekDay'] = weekDay_col

    return data

if __name__ == '__main__':
    main()