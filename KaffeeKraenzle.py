from datetime import datetime
import locale
import pandas
from pandas import DataFrame as df
# import time

def main():
    KK_REVENUES = '2019_org.csv'
    # KK_REVENUES = 'Revenue{}'.format((datetime.datetime.now()).year)

    revenues = prepare_data(KK_REVENUES)
    data = extend_data(revenues)
    reporting(KK_REVENUES, data)

def prepare_data(csv_file):
    data = pandas.read_csv(csv_file, sep=',', thousands='.', parse_dates=[0], dayfirst=True)

    # normalize dates in Date column
    data.Date = pandas.to_datetime(data.Date)
    return data

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

def reporting(dataset, data):
    locale.setlocale(locale.LC_ALL, 'de_DE')
    SEP_LENGTH = 40
    print('File processed: ', dataset)
    print('Total amount of data:', data['Date'].count())
    print('='*SEP_LENGTH)
    print('Total revenue: ', locale.currency(data['Amount'].sum(), grouping=True))
    print('='*SEP_LENGTH)
    print('Revenue per month:')
    print(data.groupby(pandas.Grouper(key='Date', freq='1M')).sum())
    print('='*SEP_LENGTH)
    # print('='*SEP_LENGTH)
    # print('Revenue per week:')
    # print(data['WeekNo'].value_counts())
    # print('='*20)

    return

if __name__ == '__main__':
    main()