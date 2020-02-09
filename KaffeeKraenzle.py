import calendar
import json
import locale
import os.path
from datetime import datetime
from pprint import pprint

import dateutil
import gspread
import matplotlib
import matplotlib.pyplot as plt
import numpy
import pandas
from oauth2client.service_account import ServiceAccountCredentials
from pandas import DataFrame


###################################################################
def main():
    GOOGLE_SHEET_NAME = 'Revenues'

    revenues = openGoogleDoc(GOOGLE_SHEET_NAME)
    data = extend_data(revenues)
    # reportingBYText(data)
    reportingByPlots(data)
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

def reportingByText(data):
    SEP_LENGTH = 33
    locale.setlocale(category=locale.LC_ALL, locale="German")

    print('Total amount of data:', data['Date'].count())
    
    annualData = data.groupby(pandas.Grouper(key='Date', freq='1Y', sort=True)).sum()

    for year, row in annualData.iterrows():
        print('='*SEP_LENGTH)
        print('Year: {:4d} - {:>12s}'.format(year.year, locale.currency(row[0], grouping=True)))
        print('-'*SEP_LENGTH)

        monthlyData = data.groupby(pandas.Grouper(key='Date', freq='1M'), sort=True).sum()

        for month, row in monthlyData.iterrows():
            if month.year == year.year:
                print('{:>12} {:4d}:{:>15}'.format(calendar.month_name[month.month], month.year, locale.currency(row[0], grouping=True)))
    
                print('-'*SEP_LENGTH)
                print('Per week: {:2d}'.format(datetime.date(month).isocalendar()[1]))
                print('-'*SEP_LENGTH)
                weeklyData = data.groupby(pandas.Grouper(key='Date', freq='1W'), sort=True).sum()

                for week, row in weeklyData.iterrows():
                    if (week.year == month.year) & (week.month == month.month):
                        print('{:2} {:4d}:{:>15}'.format(datetime.date(week).isocalendar()[1], week.year, locale.currency(row[0], grouping=True)))

                print('-'*SEP_LENGTH)

    return

def reportingByPlots(data):
    # barChart_AnnualRevuene(aata).show()
    barChart_MonthlyRevenue(data)
#
# Plot:
# Gegenüberstellung der Monate gebündlte auf Jahr
#
def barChart_MonthlyRevenue(data):
    BAR_WIDTH = 0.35
    OPACITYy = 0.8

    labels1 = []
    labels2 = []
    dataSet = []
    monthSet = []
    old_year = 0
    monthlyData = data.groupby(pandas.Grouper(key='Date', freq='1M'), sort=True).sum()

    for month, row in monthlyData.iterrows():
        labels1.append(month.year)
        labels2.append(month.month)

        if month.year == old_year:
            monthSet.append(int(row.Amount))
        else:
            if len(monthSet) > 0:
                dataSet.append([month.year, monthSet])
                monthSet = []

        old_year = month.year

    yearLabels = numpy.unique(labels1)
    monthLabels = numpy.unique(labels2)

    barPos = numpy.arange(len(monthLabels))
    colors=numpy.random.rand(len(yearLabels),3)

    for year, row in dataSet:
        plt.bar(barPos, row[1], color=colors, width=BAR_WIDTH, edgeColor='white', label=year)
        barPos = [x + BAR_WIDTH for x in barPos]

    plt.xlabel('Month over year', fontweight='bold')
    plt.xticks([r + BAR_WIDTH for r in range(len(monthLabels))], monthLabels)
    plt.legend()
    plt.show()
    return

def barChart_AnnualRevuene(data):
    annualData = data.groupby(pandas.Grouper(key='Date', freq='1Y', sort=True)).sum()

    labels = []
    yearData = []
    for year, row in data.iterrows():
        labels.append(year.year)
        yearData.append(int(row.Amount))

    x = numpy.arange(len(labels))
    BAR_WIDTH = 0.3
    
    fig, ax = plt.subplots()
    rects = ax.bar(x, yearData, BAR_WIDTH, label = 'Year')
    ax.set_ylabel('Revenue')
    # 
    ax.set_title('Revenue per year')
    ax.set_xticks(x)
    ax.set_xticklabels(labels)
    autolabel(ax, rects)
    fig.tight_layout()
    return plt
    
def autolabel(ax, rects):
    """Attach a text label above each bar in *rects*, displaying its height."""
    for rect in rects:
        height = rect.get_height()
        ax.annotate('{}'.format(height),
                    xy=(rect.get_x() + rect.get_width() / 2, height),
                    xytext=(0, 3),  # 3 points vertical offset
                    textcoords="offset points",
                    ha='center', va='bottom')

if __name__ == '__main__':
    main()
