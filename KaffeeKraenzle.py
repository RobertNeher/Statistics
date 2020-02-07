# from __future__ import print_function
from datetime import datetime
import json
import locale
import pandas
from pandas import DataFrame as df
import pickle
import os.path
import gspread
from oauth2client.service_account import ServiceAccountCredentials
# from googleapiclient.discovery import build
# from google_auth_oauthlib.flow import InstalledAppFlow
# from google.auth.transport.requests import Request

def main():
    KK_REVENUES = 'Revenues.csv'
    # KK_REVENUES = 'Revenue{}'.format((datetime.datetime.now()).year)

    revenues = openGoogleDoc('Revenues')
    data = extend_data(revenues)
    reporting(KK_REVENUES, data)

def prepare_data(csv_file):
    data = pandas.read_csv(csv_file, sep=',', thousands='.', parse_dates=[0], dayfirst=True)

    # normalize dates in Date column
    data.Date = pandas.to_datetime(data.Date)
    return data

def openGoogleDoc(docName):
    SCOPES = ['https://spreadsheets.google.com/feeds',
              'https://www.googleapis.com/auth/spreadsheets',
              'https://www.googleapis.com/auth/drive.file',
              'https://www.googleapis.com/auth/drive']
    DOCUMENT_ID = '11dGMkS97OFD53Lcd_T-zDAxt29EjWKOte-a2qc3MntA'
    SPREADSHEET = 'Revenues'

    credentials = ServiceAccountCredentials.from_json_keyfile_name("KaffeeKraenzle.json", SCOPES)

    client = gspread.authorize(credentials)
    sheet = client.open(SPREADSHEET).sheet1  # Open the spreadhseet
    data = sheet.get_all_records()  # Get a list of all records

    return pd.DataFrame(data,mindex=data[:,0])


def extend_data(data):
    weekDay_col = []

    for i, row in data.iterrows():
        dt = row.Date
        weekDay_col.append(dt.weekday())

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
    
    print('Revenue per year:')
    records = data.groupby(pandas.Grouper(key='Date', freq='1Y')).sum()
    
    for i, row in records.iterrows():
        print('{}\t{}'.format(i.year, locale.currency(row[0], grouping=True)))

    print('='*SEP_LENGTH)
    print('Revenue per month:')
    records = data.groupby(pandas.Grouper(key='Date', freq='1M')).sum()
    
    for i, row in records.iterrows():
        print('{:2d} {:4d}:{:>13}'.format(i.month, i.year, locale.currency(row[0], grouping=True)))

    print('='*SEP_LENGTH)
    # print('Revenue per week:')
    # print(data.groupby(pandas.Grouper(key='Date', freq='1W')).sum())

    return

if __name__ == '__main__':
    main()