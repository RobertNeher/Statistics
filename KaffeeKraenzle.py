import calendar
from datetime import datetime
import dateutil
import json
import locale
from locale import atof
import pandas
from pandas import DataFrame
import pickle
import os.path
import gspread
from pprint import pprint
from oauth2client.service_account import ServiceAccountCredentials
# from googleapiclient.discovery import build
# from google_auth_oauthlib.flow import InstalledAppFlow
# from google.auth.transport.requests import Request

def main():
    GOOGLE_SHEET_NAME = 'Revenues'

    revenues = openGoogleDoc(GOOGLE_SHEET_NAME)
    data = extend_data(revenues)
    reporting(data)
    exit(0)

def openGoogleDoc(docName):
    SCOPES = ['https://spreadsheets.google.com/feeds',
              'https://www.googleapis.com/auth/spreadsheets',
              'https://www.googleapis.com/auth/drive.file',
              'https://www.googleapis.com/auth/drive']

    credentials = ServiceAccountCredentials.from_json_keyfile_name("KaffeeKraenzle.json", SCOPES)

    client = gspread.authorize(credentials)
    sheet = client.open(docName).sheet1  # Open the spreadhseet
    df = pandas.DataFrame(sheet.get_all_records())
    df.set_index('Date')
    df['Date'] = df['Date'].apply(dateutil.parser.parse, dayfirst=True)
    df['Amount'] = pandas.to_numeric(df['Amount'], errors='coerce')
    
    return df
    
def extend_data(data):
    locale.setlocale(category=locale.LC_ALL, locale="German")
    weekDay_col = []

    for i, row in data.iterrows():
        weekDay_col.append(row.Date.weekday())

    data['WeekDay'] = weekDay_col
    
    return data

def reporting(data):
    SEP_LENGTH = 33
    locale.setlocale(category=locale.LC_ALL, locale="German")

    print('Total amount of data:', data['Date'].count())
    
    yearData = data.groupby(pandas.Grouper(key='Date', freq='1Y')).sum()

    for year, row in yearData.iterrows():
        print('='*SEP_LENGTH)
        print('Year: {:4d} - {:>12s}'.format(year.year, locale.currency(row[0], grouping=True)))
        print('-'*SEP_LENGTH)

        monthData = data.groupby(pandas.Grouper(key='Date', freq='1M')).sum()

        for month, row in monthData.iterrows():
            if month.year == year.year:
                print('{:>12} {:4d}:{:>15}'.format(calendar.month_name[month.month], month.year, locale.currency(row[0], grouping=True)))
    
                print('-'*SEP_LENGTH)
                print('Per week: {:2d}'.format(datetime.date(month).isocalendar()[1]))
                print('-'*SEP_LENGTH)
                weekData = data.groupby(pandas.Grouper(key='Date', freq='1W')).sum()

                for week, row in weekData.iterrows():
                    if (week.year == month.year) & (week.month == month.month):
                        print('{:2} {:4d}:{:>15}'.format(datetime.date(week).isocalendar()[1], week.year, locale.currency(row[0], grouping=True)))

                print('-'*SEP_LENGTH)

    return

if __name__ == '__main__':
    main()