#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue May  5 19:53:58 2020

@author: chaowu
"""


import pandas as pd
import numpy as np
import matplotlib.pylab as plt
import matplotlib.cbook as cbook
import matplotlib.dates as mdates

from scipy.signal import savgol_filter

def smooth_list(l, window=3, poly=1):
    return savgol_filter(l, window, poly)


df = pd.read_csv("data/us-counties.csv")

all_state = list(set(df['state']))
all_county = list(set(df['county']))

df['date'] = pd.to_datetime(df['date'])

def load_data_by_county(df=df, county="Howard", state="Maryland"):

    data = df[(df['county'] == county) & (df['state'] == state)]

    return data


data = load_data_by_county()

# print(data)

def plot_data(data=data):
    fig, ax = plt.subplots()
    ax.plot(data['date'], data['cases'], 'bo-')

    #ax.fmt_xdata = mdates.DateFormatter('%Y-%m-%d')

    myFmt = mdates.DateFormatter('%m-%d')
    ax.xaxis.set_major_formatter(myFmt)

    fig.autofmt_xdate()

    plt.grid(True)
    plt.title("County Level Change")
    plt.show()


case_threshold = 500

def plot_state_data(state="Maryland"):
    
    print("analyzing state: ", state)

    fig = plt.figure(figsize=(14,11))

    ax_1 = fig.add_subplot(211)

    legend_list = []

    df_by_state = df[df['state'] == state]

    for county in all_county:

        data = df_by_state[df_by_state['county'] == county]
        if not data.empty:
            #print(data.iloc[-1])

            if data.iloc[-1]['cases'] > case_threshold:

                ax_1.plot(data['date'], data['cases'], 'o-')

                myFmt = mdates.DateFormatter('%Y-%m-%d')
                ax_1.xaxis.set_major_formatter(myFmt)

                legend_list.append(data.iloc[-1]['county'])

                fig.autofmt_xdate()

    ax_1.legend(legend_list)
    ax_1.grid(True)
    ax_1.set_xlabel('date')
    ax_1.set_ylabel('case number')
    ax_1.set_title("cases by county over time")

    ax_2 = fig.add_subplot(212)
    legend_list = []

    df_by_state = df[df['state'] == state]

    for county in all_county:

        data = df_by_state[df_by_state['county'] == county]
        if not data.empty:
            #print(data.iloc[-1])

            if data.iloc[-1]['cases'] > case_threshold:

                case_number = data['cases']
                case_number = smooth_list(case_number)

                rate = np.diff(case_number)/(case_number[1:])*100

                ax_2.plot(data['date'][1:], rate, 'o-')

                #myFmt = mdates.DateFormatter('%Y-%m-%d')
                myFmt = mdates.DateFormatter('%m-%d')

                ax_2.xaxis.set_major_formatter(myFmt)

                legend_list.append(data.iloc[-1]['county'])

    # add the state level
    legend_list.append("state level")

    md_data = df[df['state'] == state]

    grouped_df = md_data.groupby(['state', 'date']).sum().reset_index()

    case_number = grouped_df['cases']
    case_number = smooth_list(case_number)

    rate = np.diff(case_number)/(case_number[1:])*100

    ax_2.plot(grouped_df['date'][1:], rate, '*-')

    myFmt = mdates.DateFormatter('%m-%d')
    ax_2.xaxis.set_major_formatter(myFmt)
    fig.autofmt_xdate()

    ax_2.legend(legend_list)
    ax_2.grid(True)
    ax_2.set_xlabel('date')
    ax_2.set_ylabel('smoothed increase rate')
    ax_2.set_ylim([0,50])
    ax_2.set_title('increase rate at state: ' + state)

    plt.tight_layout()
    plt.savefig("result/case_trend_in_" + state + ".png", dpi=300)
    #plt.show()
    plt.close()


if __name__ == "__main__":
    
    #plot_data()
        
    #plot_state_data()
    
    for state in all_state:
        plot_state_data(state)
