#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Apr 15 16:40:00 2023

@author: fattabby
"""
#%Programs
#reference1: https://hackmd.io/@s02260441/HJcMcnds8
#reference2: https://hackmd.io/@s02260441/Hki9NN5jL
#reference3: https://hackmd.io/v7m8LMfzQHu1y_dQNuXwbQ

#import twstock
#target_stock = '0050'
#stock = twstock.Stock(target_stock)
#target_price = stock.fetch_from(2020, 5)

#貌似twstock掛了。如果是這樣就改用其他來源
#安裝套件請用pip install $套件名稱
import os
#import getpass
#from contextlib import chdir
import time
import yfinance as yf
import matplotlib.pyplot as plt
import pandas as pd
import mplfinance as mpf
from datetime import datetime
from datetime import timedelta
from datetime import date
from dateutil.relativedelta import relativedelta
import csv
#from talib import abstract
#import yfinance_timeframe_converter as converter
#https://github.com/LucasRocha-Png/yfinance-timeframe-converter
#from pandas_datareader import data as pdr
#import stock_pandas

#pip install ta-lib
#import talib
#指定從今天起回推多久，如4年
#感覺現階段還做不到**kwargs
binance_dark_day = {
    "base_mpl_style": "dark_background",
    "marketcolors": {
        "candle": {"up": "red", "down": "green"},  
        "edge": {"up": "red", "down": "green"},  
        "wick": {"up": "red", "down": "green"},  
        "ohlc": {"up": "red", "down": "green"},
        "volume": {"up": "red", "down": "green"},  
        "vcedge": {"up": "red", "down": "green"},  
        "vcdopcod": False,
        "alpha": 1,
    },
    "mavcolors": ("yellow", "#87CEFA", "#7CFC00","orange","white","magenta","#8A2BE2","#008080"),
    "facecolor": "#1b1f24",
    "gridcolor": "#2c2e31",
    "gridstyle": "--",
    "y_on_right": True,
    "rc": {
        "axes.grid": True,
        "axes.grid.axis": "y",
        "axes.edgecolor": "#474d56",
        "axes.titlecolor": "red",
        "figure.facecolor": "#161a1e",
        "figure.titlesize": "x-large",
        "figure.titleweight": "semibold",
    },
    "base_mpf_style": "dark_background",
}
binance_dark = {
    "base_mpl_style": "dark_background",
    "marketcolors": {
        "candle": {"up": "red", "down": "green"},  
        "edge": {"up": "red", "down": "green"},  
        "wick": {"up": "red", "down": "green"},  
        "ohlc": {"up": "red", "down": "green"},
        "volume": {"up": "red", "down": "green"},  
        "vcedge": {"up": "red", "down": "green"},  
        "vcdopcod": False,
        "alpha": 1,
    },
    "mavcolors": ("yellow", "#87CEFA", "#7CFC00","orange","white","#8A2BE2","#008080"),
    "facecolor": "#1b1f24",
    "gridcolor": "#2c2e31",
    "gridstyle": "--",
    "y_on_right": True,
    "rc": {
        "axes.grid": True,
        "axes.grid.axis": "y",
        "axes.edgecolor": "#474d56",
        "axes.titlecolor": "red",
        "figure.facecolor": "#161a1e",
        "figure.titlesize": "x-large",
        "figure.titleweight": "semibold",
    },
    "base_mpf_style": "dark_background",
}
binance_dark_month = {
    "base_mpl_style": "dark_background",
    "marketcolors": {
        "candle": {"up": "red", "down": "green"},  
        "edge": {"up": "red", "down": "green"},  
        "wick": {"up": "red", "down": "green"},  
        "ohlc": {"up": "red", "down": "green"},
        "volume": {"up": "red", "down": "green"},  
        "vcedge": {"up": "red", "down": "green"},  
        "vcdopcod": False,
        "alpha": 1,
    },
    "mavcolors": ("#87CEFA", "#7CFC00","orange","white","#8A2BE2"),
    "facecolor": "#1b1f24",
    "gridcolor": "#2c2e31",
    "gridstyle": "--",
    "y_on_right": True,
    "rc": {
        "axes.grid": True,
        "axes.grid.axis": "y",
        "axes.edgecolor": "#474d56",
        "axes.titlecolor": "red",
        "figure.facecolor": "#161a1e",
        "figure.titlesize": "x-large",
        "figure.titleweight": "semibold",
    },
    "base_mpf_style": "dark_background",
}
binance_dark_30min = {
    "base_mpl_style": "dark_background",
    "marketcolors": {
        "candle": {"up": "red", "down": "green"},  
        "edge": {"up": "red", "down": "green"},  
        "wick": {"up": "red", "down": "green"},  
        "ohlc": {"up": "red", "down": "green"},
        "volume": {"up": "red", "down": "green"},  
        "vcedge": {"up": "red", "down": "green"},  
        "vcdopcod": False,
        "alpha": 1,
    },
    "mavcolors": ("lime", "orange"),
    "facecolor": "#1b1f24",
    "gridcolor": "#2c2e31",
    "gridstyle": "--",
    "y_on_right": True,
    "rc": {
        "axes.grid": True,
        "axes.grid.axis": "y",
        "axes.edgecolor": "#474d56",
        "axes.titlecolor": "red",
        "figure.facecolor": "#161a1e",
        "figure.titlesize": "x-large",
        "figure.titleweight": "semibold",
    },
    "base_mpf_style": "dark_background",
}
mc = mpf.make_marketcolors(up='r',down='g',
                            edge='inherit',
                            wick='black',
                            volume='in',
                            ohlc='i')
s    = mpf.make_mpf_style(marketcolors=mc)
def stock_analysis_in_period(target_stock,period,interval):
    try:
    
        target_stock=target_stock
        price_history = yf.Ticker(target_stock).history(period=period, # valid periods: 1d,5d,1mo,3mo,6mo,1y,2y,5y,10y,ytd,max
                                                  #start='2016-01-01',end='2021-01-01' #若你想自訂區間
                                           interval=interval, # valid intervals: 1m,2m,5m,15m,30m,60m,90m,1h,1d,5d,1wk,1mo,3mo
                                           actions=False)       
        name_attribute = ['Open', 'High', 'Low', 'Close', 'Volume']
        df = pd.DataFrame(columns = name_attribute, data = price_history)   
        if interval=="1d":        
            df["SMA5"] = df['Close'].rolling(window = 5).mean()
            df["SMA10"] = df['Close'].rolling(window = 10).mean()
            df["SMA20"] = df['Close'].rolling(window = 20).mean()
            df["SMA60"] = df['Close'].rolling(window = 60).mean()
            df["SMA100"] = df['Close'].rolling(window = 100).mean()
            df["SMA120"] = df['Close'].rolling(window = 120).mean()
            df["SMA200"] = df['Close'].rolling(window = 200).mean()
            df["SMA1000"] = df['Close'].rolling(window = 1000).mean()
            df["VMA5"]=df["Volume"].rolling(window = 5).mean()
            df["VMA10"]=df["Volume"].rolling(window = 10).mean()
            df["VMA20"]=df["Volume"].rolling(window = 20).mean()                    
        elif interval == '1wk':
            df["SMA3"] = df['Close'].rolling(window = 3).mean()
            df["SMA8"] = df['Close'].rolling(window = 8).mean()
            df["SMA13"] = df['Close'].rolling(window = 13).mean()
            df["SMA21"] = df['Close'].rolling(window = 21).mean()
            df["SMA34"] = df['Close'].rolling(window = 34).mean()
            df["SMA55"] = df['Close'].rolling(window = 55).mean()            
        elif interval == "1mo":
            df["SMA1"] = df["Close"]
            df["SMA2"] = df['Close'].rolling(window = 2).mean()
            df["SMA3"] = df['Close'].rolling(window = 3).mean()
            df["SMA6"] = df['Close'].rolling(window = 6).mean()
            df["SMA12"] = df['Close'].rolling(window = 12).mean()
            df["SMA120"] = df['Close'].rolling(window = 120).mean()        
        elif interval =="30m":
            df["SMA20"] = df['Close'].rolling(window = 20).mean()
            df["SMA60"] = df['Close'].rolling(window = 60).mean()
        return df                         
    except Exception as e:
            print("錯誤訊息:", e)              

def stock_analysis(ticker_name,start_date, end_date, interval):
    try:        
        price_history = yf.Ticker(ticker_name).history(start=start_date,end=end_date, # valid periods: 1d,5d,1mo,3mo,6mo,1y,2y,5y,10y,ytd,max
                                                  #start='2016-01-01',end='2021-01-01'
                                           interval=interval, # valid intervals: 1m,2m,5m,15m,30m,60m,90m,1h,1d,5d,1wk,1mo,3mo
                                           actions=False)        
        name_attribute = ['Open', 'High', 'Low', 'Close', 'Volume']
        df = pd.DataFrame(columns = name_attribute, data = price_history)    
        if interval=="1d":
            df["SMA5"] = df['Close'].rolling(window = 5).mean()
            df["SMA10"] = df['Close'].rolling(window = 10).mean()
            df["SMA20"] = df['Close'].rolling(window = 20).mean()
            df["SMA60"] = df['Close'].rolling(window = 60).mean()
            df["SMA100"] = df['Close'].rolling(window = 100).mean()
            df["SMA120"] = df['Close'].rolling(window = 120).mean()
            df["SMA200"] = df['Close'].rolling(window = 200).mean()
            df["SMA1000"] = df['Close'].rolling(window = 1000).mean()
            df["VMA5"]=df["Volume"].rolling(window = 5).mean()
            df["VMA10"]=df["Volume"].rolling(window = 10).mean()
            df["VMA20"]=df["Volume"].rolling(window = 20).mean()
            subtitle2=("當日各均量為：",
                      "5MA: "+ str(df["VMA5"].iloc[-1].round(4)),
                      "10MA: "+ str(df["VMA10"].iloc[-1].round(4)),
                      "20MA: "+ str(df["VMA20"].iloc[-1].round(4)),
                      )               
            subtitle=("當日各均線為：", 
                  "5MA: "+ str(df["SMA5"].iloc[-1].round(4)),
                  "10MA: "+ str(df["SMA10"].iloc[-1].round(4)),
                  "20MA: "+ str(df["SMA20"].iloc[-1].round(4)),
                  "60MA: "+ str(df["SMA60"].iloc[-1].round(4)),
                  "100MA: "+ str(df["SMA100"].iloc[-1].round(4)),
                  "200MA: "+ str(df["SMA200"].iloc[-1].round(4)),
                  "1000MA: "+ str(df["SMA1000"].iloc[-1].round(4)),# sep="\n"
                  )                    
            print(subtitle2)
            print(subtitle)
        elif interval == '1wk':
            df["SMA3"] = df['Close'].rolling(window = 3).mean()
            df["SMA8"] = df['Close'].rolling(window = 8).mean()
            df["SMA13"] = df['Close'].rolling(window = 13).mean()
            df["SMA21"] = df['Close'].rolling(window = 21).mean()
            df["SMA34"] = df['Close'].rolling(window = 34).mean()
            df["SMA55"] = df['Close'].rolling(window = 55).mean()
            subtitle=("當週各均線為：",
            "3MA: "+ str(df["SMA3"].iloc[-1].round(4)),
            "8MA: "+ str(df["SMA8"].iloc[-1].round(4)),
            "13MA: "+ str(df["SMA13"].iloc[-1].round(4)),
            "21MA: "+ str(df["SMA21"].iloc[-1].round(4)),
            "34MA: "+ str(df["SMA34"].iloc[-1].round(4)),
            "55MA: "+ str(df["SMA55"].iloc[-1].round(4)),# sep="\n")
            )        
            print(subtitle)
        elif interval == "1mo":
            df["SMA1"] = df["Close"]
            df["SMA2"] = df['Close'].rolling(window = 2).mean()
            df["SMA3"] = df['Close'].rolling(window = 3).mean()
            df["SMA6"] = df['Close'].rolling(window = 6).mean()
            df["SMA12"] = df['Close'].rolling(window = 12).mean()
            df["SMA120"] = df['Close'].rolling(window = 120).mean()
            subtitle=("當月各均線為：",
            "1MA: "+ str(df["SMA1"].iloc[-1].round(4)),      
            "2MA: "+ str(df["SMA2"].iloc[-1].round(4)),
            "3MA: "+ str(df["SMA3"].iloc[-1].round(4)),
            "6MA: "+ str(df["SMA6"].iloc[-1].round(4)),
            "12MA: "+ str(df["SMA12"].iloc[-1].round(4)),
            "120MA: "+ str(df["SMA120"].iloc[-1].round(4)), #sep="\n"
            )        
            print(subtitle)
        elif interval =="30m":
            df["SMA20"] = df['Close'].rolling(window = 20).mean()
            df["SMA60"] = df['Close'].rolling(window = 60).mean()
            subtitle=("當30分各均線為：",
            "20MA: "+ str(df["SMA20"].iloc[-1].round(4)),      
            "60MA: "+ str(df["SMA60"].iloc[-1].round(4)) ,# sep="\n"
            )            
            print(subtitle)
        return df
    except Exception as e:
            print("錯誤訊息:", e)
    # https://stackoverflow.com/questions/60599812/how-can-i-customize-mplfinance-plot
    #ref https://github.com/matplotlib/mplfinance/issues/216
    #xmin = 0
    #xmax = len(price_history)
    #ref https://stackoverflow.com/questions/66623006/mplfinance-plot-tight-layout-cuts-information-off
    #apc=mpf.make_addplot(df['Volume'].iloc[4:],type = 'line',linestyle=' ',panel =1, mav = 10) #從算圖結果看來，這裡的MA應該是指量均線

#https://medium.com/%E9%87%8F%E5%8C%96%E4%BA%A4%E6%98%93%E7%9A%84%E8%B5%B7%E9%BB%9E-%E9%82%81%E5%90%91%E9%87%8F%E5%8C%96%E4%BA%A4%E6%98%93%E7%85%89%E9%87%91%E8%A1%93%E5%B8%AB%E4%B9%8B%E8%B7%AF/%E9%87%8F%E5%8C%96%E4%BA%A4%E6%98%93-%E5%B9%BE%E5%80%8B%E5%B8%B8%E8%A6%8B%E7%9A%84%E6%8C%87%E6%A8%99-ta-lib%E7%9A%84%E6%87%89%E7%94%A8-32560c136c79
##ChiuGuan Section
def stock_analysis_chiu_guan(ticker_name,start_date,end_date):  
    try:
        target_stock=ticker_name #台灣股票是「台灣股票代碼.TW」
        price_history = yf.Ticker(target_stock).history(start=start_date,end=end_date, # valid periods: 1d,5d,1mo,3mo,6mo,1y,2y,5y,10y,ytd,max
                                              #start='2016-01-01',end='2021-01-01'
                        interval="1d", # valid intervals: 1m,2m,5m,15m,30m,60m,90m,1h,1d,5d,1wk,1mo,3mo
                        actions=False)
        name_attribute = ['Open', 'High', 'Low', 'Close', 'Volume']
        df = pd.DataFrame(columns = name_attribute, data = price_history)
        #filename = f'~/data/TSLA.csv'
        #df.to_csv(filename)
        #stock = stock_pandas.StockDataFrame(price_history)
        #stock=stock.rename(columns={"Close":"close"})
        #df["close"]=df["Close"]
        #df["bbi"]=stock["bbi:3,6,12,24"]
        #https://stackoverflow.com/questions/11346283/renaming-column-names-in-pandas
        #ma5=stock['ma:5']
        #ma5_2=stock.exec('ma:5', create_column=True) # returns a numpy ndarray
        #https://github.com/kaelzhang/stock-pandas/blob/master/docs/README.md
        
    
        df["SMA3"] = df['Close'].rolling(window = 3).mean()
        df["SMA5"] = df['Close'].rolling(window = 5).mean()
        df["SMA8"] = df['Close'].rolling(window = 8).mean()
        df["SMA13"] = df['Close'].rolling(window = 13).mean()
        df["midbound"] = (df["SMA3"] + df["SMA5"] + df["SMA8"] +df["SMA13"]) / 4
        #on internet are 3,6,12,24
        #midbound=midbound.dropna()
        midbound=pd.DataFrame(df["midbound"])
        chiu_guan=midbound.iloc[-1,-1].round(4)    
        today_close=df["Close"].iloc[-1]
        print(ticker_name,"截至", df.index[-1].strftime('%Y-%m-%d'),"丘關為：",chiu_guan, " 點/元")
        if today_close>=chiu_guan:
            subtitle="今日收盤價 "+str(today_close.round(4))+" 站上或高於丘關 "+str(chiu_guan)
            print(subtitle)
        elif today_close<chiu_guan:
            subtitle="今日收盤價 "+str(today_close.round(4))+" 跌破或低於丘關 "+str(chiu_guan)
            print(subtitle)
        return subtitle,df
    except Exception as e:
            print("錯誤訊息:", e)

def stock_analysis_chiu_guan_makeplot(ticker_name,start_date,end_date,df,last_WK_3MA,bull_or_bear_boundary):  
    try:
        #print(df['Close'])
        #print("SMA3", SMA3)
        #print("SMA5", SMA5)
        #print("SMA8", SMA8)
        #print("SMA13", SMA13)
        #print("last day=", SMA13.index[-1].strftime('%Y-%m-%d'))
        #midbound=float(midbound["Close"])
        #https://github.com/nsrlive/FinTech/blob/master/15.%E9%80%9A%E9%81%93%E7%AA%81%E7%A0%B4%E7%AD%96%E7%95%A5.py
        #bbi=pd.DataFrame(stock["bbi"])
        titles="{} Chiu-guan, starts from {}".format(ticker_name,start_date)
        midbound=pd.DataFrame(df["midbound"])
        midbound2=mpf.make_addplot(midbound,color="yellow")
        #ref https://github.com/matplotlib/mplfinance/issues/216
        #apc=mpf.make_addplot(df['Volume'].iloc[4:],type = 'line',linestyle=' ',panel =1, mav = 10) #從算圖結果看來，這裡的MA應該是指量均線
        #fig,midbound =mpf.plot(df.iloc[4:], type='candlestick', volume=True,title = target_stock, tight_layout=True, mav=(5,42,252), style = s, returnfig=True, addplot = apc)
        #mpf.plot(df.iloc[4:], type='candlestick', volume=True,title = target_stock, tight_layout=True, mav=(5,42,252), style = s, returnfig=True, addplot = apc)
        #mpf.make_addplot(midbound)
        wkline_exam=mpf.make_addplot([last_WK_3MA]*df.shape[0],color="cyan")
        monthline_exam=mpf.make_addplot([bull_or_bear_boundary]*df.shape[0],color="red")
        mpf.plot(df,type="candlestick",style = binance_dark ,addplot = [midbound2,wkline_exam,monthline_exam], volume=True,title = titles, returnfig=True, tight_layout=True)       
        plt.savefig("fig_{}_chiu_guan_starts_from_{}.svg".format(ticker_name,start_date),dpi=350, bbox_inches="tight")#存成圖片（命名為股票代碼） #理論上會存在你打開這個檔案的位置
        #return subtitle, df
        #https://www.grenade.tw/blog/how-to-use-the-python-financial-analysis-visualization-module-mplfinance/
        #stucking on midbound issue
        #https://stackoverflow.com/questions/68317362/how-to-add-separate-lines-to-mplfinance-plot
        #mpf.plot(pd.DataFrame(df["bbi"]))
    except Exception as e:
            print("錯誤訊息:", e)
            
def stock_analysis_makeplot(ticker_name,start_date, end_date, interval,df):    
    try:
        titles="{}, starts from {}, day interval= {}".format(ticker_name,start_date,interval)
        #title2=subtitle
        #original
        if interval=='1d':
            apc=mpf.make_addplot(df['Volume'].iloc[4:],type = 'line',linestyle=' ',panel =1, mav = (5,10,20)) #從算圖結果看來，這裡的MA應該是指量均線
    #       mpf.plot(df.iloc[4:], type='candlestick', volume=True,title = titles, tight_layout=True, mav=(5,42,252), style = s, returnfig=True, addplot = apc) 
            mpf.plot(df.iloc[4:], type='candlestick', volume=True,title = titles, tight_layout=True, mav=(5,10,20,60,100,120,200,1000), style = binance_dark_day, returnfig=True, addplot = apc)       
        elif interval == '1wk':
            apc=mpf.make_addplot(df['Volume'].iloc[4:],type = 'line',linestyle=' ',panel =1, mav = 10) #從算圖結果看來，這裡的MA應該是指量均線
            mpf.plot(df.iloc[4:], type='candlestick', volume=True,title = titles, tight_layout=True, mav=(3,8,13,21,34,55), style = binance_dark, returnfig=True, addplot = apc)        
        elif interval == '1mo':
    #       mpf.plot(df.iloc[4:], type='candlestick', volume=True,title = titles, tight_layout=True, mav=(1,2,3,6,12,120), style = s, returnfig=True, addplot = apc)
    # 技術問題待查
            apc=mpf.make_addplot(df['Volume'].iloc[4:],type = 'line',linestyle=' ',panel =1, mav =(5,10,20)) #從算圖結果看來，這裡的MA應該是指量均線
            #plt.plot(df['SMA1'].iloc[4:], color="y")
            mpf.plot(df.iloc[4:], type='candlestick', volume=True,title = titles, tight_layout=True, mav=(2,3,6,12,120), style = binance_dark_month, returnfig=True, addplot = apc)
        elif interval == "30m":
            apc=mpf.make_addplot(df['Volume'].iloc[4:],type = 'line',linestyle=' ',panel =1, mav =(5,10,20)) #從算圖結果看來，這裡的MA應該是指量均線
            mpf.plot(df.iloc[4:], type='candlestick', volume=True,title = titles, tight_layout=True, mav=(20,60), style = binance_dark_30min, returnfig=True, addplot = apc)
        else:
            apc=mpf.make_addplot(df['Volume'].iloc[4:],type = 'line',linestyle=' ',panel =1, mav =(5,10,20)) #從算圖結果看來，這裡的MA應該是指量均線
            mpf.plot(df.iloc[4:], type='candlestick', volume=True,title = titles, tight_layout=True, mav=(20,60), style = binance_dark_30min, returnfig=True, addplot = apc)       
    #   plt.legend(loc='upper left')
        #new
        #mpf.plot(df.iloc[4:], type='candlestick', volume=True,title = target_stock, tight_layout=False, mav=(5,42,252), style = s, returnfig=True, addplot = apc)#,xlim=(xmin,xmax))
        #若要設252日線，你的時間區間要夠長
        #雖然程式碼沒明寫哪個顏色是多少日線（應該是系統自己設定的），但是用肉眼大致看得出來。
        #從算圖結果看來，這裡的MA應該是指成交價均線           
        plt.savefig("fig_{}_starts_from_{}_{}.svg".format(ticker_name,start_date,interval),dpi=350, bbox_inches="tight")#存成圖片（命名為股票代碼） #理論上會存在你打開這個檔案的位置    
    except Exception as e:
            print("錯誤訊息:", e)
            
def KDJ_Beta2(df):
    try:
        kdj_fig=plt.figure(figsize=(12,1))
        low_list = df["Close"].rolling(9, min_periods=1).min()
        high_list = df["High"].rolling(9, min_periods=1).max()
        rsv = (df["Close"] - low_list) / (high_list - low_list) * 100
        df["K"] = rsv.ewm(com=2, adjust=False).mean()
        df["D"] = df["K"].ewm(com=2, adjust=False).mean()
        df["J"] = 3 * df["K"] - 2 * df["D"]
        plt.plot(df["K"], label ="K", color="y")
        plt.plot(df["D"], label ="D", color="aqua")
        plt.plot(df["J"], label ="J", color= "lime")
        plt.legend()
        #plt.show()
        return kdj_fig    
    except Exception as e:
            print("錯誤訊息:", e)

def KDJ_Beta3(ticker_name, start_date, end_date, interval):
    try:
        df=stock_analysis(ticker_name, start_date, end_date, interval)
        low_list = df["Close"].rolling(9, min_periods=1).min()
        high_list = df["High"].rolling(9, min_periods=1).max()
        rsv = (df["Close"] - low_list) / (high_list - low_list) * 100
        df["K"] = rsv.ewm(com=2, adjust=False).mean()
        df["D"] = df["K"].ewm(com=2, adjust=False).mean()
        df["J"] = 3 * df["K"] - 2 * df["D"]
        if interval=="1wk":
            last_WK_3MA=df["SMA3"].iloc[-1]
            return df, last_WK_3MA
        elif interval=="1mo":
            bull_or_bear_boundary=(df.iloc[-3]["High"]+df.iloc[-3]["Low"])/2
            return df, bull_or_bear_boundary
    except Exception as e:
            print("錯誤訊息:", e)
            
            
def KDJ_plot(df):
    try:
        kdj_fig=plt.figure(figsize=(12,1))
        plt.plot(df["K"], label ="K", color="y")
        plt.plot(df["D"], label ="D", color="aqua")
        plt.plot(df["J"], label ="J", color= "lime")
        plt.legend(loc="upper left")
        plt.show()
        #為避免多次出現列印訊息造成視覺混淆，故把有做KDJ分析的訊息都改丟在這裡。日線則個別丟一個。      
        return kdj_fig
    except Exception as e:
            print("錯誤訊息:", e)
            
def odds_ratio_chiu_guan_simplified(ticker_name):
    try:
        msg, df=stock_analysis_chiu_guan(ticker_name, "2020-01-01", None)
        df["high_than_chiu_guan"]=df["Close"]>=df["midbound"]
        df["tomorrow_move"]=df["Close"].shift(periods=-1)
        df["change"]=(df["tomorrow_move"]-df["Close"])
        df["pct_change"]=(df["tomorrow_move"]-df["Close"])*100/df["Close"]
        df["tomorrow_higher"]=df["change"]>0
        df=df.dropna()
        df["correlation"]=df["high_than_chiu_guan"]==df["tomorrow_higher"]
        odds=df["correlation"].mean()
        #odds2=df["correlation"].sum()/df.shape[0]
        return df, odds
    except Exception as e:
            print("錯誤訊息:", e)

def stock_analysis_mixed(ticker_name, start_date, end_date, month_line_show_year_interval):
    try:       
        df1=stock_analysis(ticker_name, start_date, end_date, "1d")                
        stock_analysis_makeplot(ticker_name,start_date, end_date, "1d",df1)
        #df2=stock_analysis(ticker_name, start_date, end_date, "1wk")
        df2,last_WK_3MA=KDJ_Beta3(ticker_name, start_date, end_date, "1wk")
        kdj_week=KDJ_plot(df2)
        stock_analysis_makeplot(ticker_name,start_date, end_date, "1wk",df2)
        #df3=stock_analysis(ticker_name, (str((int(start_date[:4])-month_line_show_year_interval))+start_date[4:]), end_date, "1mo")    
        df3,bull_or_bear_boundary=KDJ_Beta3(ticker_name, (str((int(start_date[:4])-month_line_show_year_interval))+start_date[4:]), end_date, "1mo")
        kdj_month=KDJ_plot(df3)
        stock_analysis_makeplot(ticker_name,start_date, end_date, "1mo",df3)
        df4=stock_analysis_in_period(ticker_name,"1mo","30m")
        stock_analysis_makeplot(ticker_name,str(datetime.today()+relativedelta(months=-1)+relativedelta(days=-1))[0:10], end_date, "30m",df4)        
        chiuguan_message, df_bbi=stock_analysis_chiu_guan(ticker_name, start_date, end_date)
        stock_analysis_chiu_guan_makeplot(ticker_name,start_date,end_date,df_bbi,last_WK_3MA,bull_or_bear_boundary)        
        #https://stackoverflow.com/questions/4130922/how-to-increment-datetime-by-custom-months-in-python-without-using-library
        #https://stackoverflow.com/questions/4130922/how-to-increment-datetime-by-custom-months-in-python-without-using-library
        #df5, ma_2h=stock_analysis_in_period(ticker_name,"1mo","1h")        
        if df_bbi["Close"].iloc[-1]<last_WK_3MA:
             week_line_check="未通過高於3週線強勢檢核"
# #20250528 請將其列入選股程序中            
        else:
             week_line_check="通過高於3週線強勢檢核"
#             week3_check.append(ticker_name)
#         print(week_line_check)
        if df_bbi["Close"].iloc[-1]<bull_or_bear_boundary:
             month_check="月線趨勢仍然疲弱"
        else:
             month_check="月線強勢"
#             monthline_check.append(ticker_name)
#         print(month_check)
        return chiuguan_message, df_bbi, df1, df2, kdj_week ,df3, kdj_month, df4, last_WK_3MA, bull_or_bear_boundary, week_line_check, month_check
    except Exception as e:
            print("錯誤訊息:", e)
#yellow_5 表示大於丘關 
        

def stock_analysis_chiu_guan_simplified(ticker_name,start_date,end_date):  
    except_list1=[]
    try:        
        target_stock=ticker_name #台灣股票是「台灣股票代碼.TW」
        price_history = yf.Ticker(target_stock).history(start=start_date,end=end_date, # valid periods: 1d,5d,1mo,3mo,6mo,1y,2y,5y,10y,ytd,max
                                          #start='2016-01-01',end='2021-01-01'
                    interval="1d", # valid intervals: 1m,2m,5m,15m,30m,60m,90m,1h,1d,5d,1wk,1mo,3mo
                    actions=False)
        name_attribute = ['Open', 'High', 'Low', 'Close', 'Volume']
        df = pd.DataFrame(columns = name_attribute, data = price_history)
    #filename = f'~/data/TSLA.csv'
    #df.to_csv(filename)
    #stock = stock_pandas.StockDataFrame(price_history)
    #stock=stock.rename(columns={"Close":"close"})
    #df["close"]=df["Close"]
    #df["bbi"]=stock["bbi:3,6,12,24"]
    #https://stackoverflow.com/questions/11346283/renaming-column-names-in-pandas
    #ma5=stock['ma:5']
    #ma5_2=stock.exec('ma:5', create_column=True) # returns a numpy ndarray
    #https://github.com/kaelzhang/stock-pandas/blob/master/docs/README.md  
        df["SMA3"] = df['Close'].rolling(window = 3).mean()
        df["SMA5"] = df['Close'].rolling(window = 5).mean()
        df["SMA8"] = df['Close'].rolling(window = 8).mean()
        df["SMA13"] = df['Close'].rolling(window = 13).mean()
        df["midbound"] = (df["SMA3"] + df["SMA5"] + df["SMA8"] +df["SMA13"]) / 4
    #on internet are 3,6,12,24
    #midbound=midbound.dropna()
        midbound=pd.DataFrame(df["midbound"])
        chiu_guan=midbound.iloc[-1,-1].round(4)    
        today_close=df["Close"].iloc[-1]
        print(ticker_name,"截至", df.index[-1].strftime('%Y-%m-%d'),"丘關為：",chiu_guan, " 點/元")
        if today_close>=chiu_guan:
            subtitle="今日收盤價 "+str(today_close.round(4))+" 站上或高於丘關 "+str(chiu_guan)
            print(subtitle)
        elif today_close<chiu_guan:
            subtitle="今日收盤價 "+str(today_close.round(4))+" 跌破或低於丘關 "+str(chiu_guan)
            print(subtitle)
        return df
    except Exception as e:
            print("錯誤訊息:", e)
            except_list1.append(e)

def chiu_guan_simplified(ticker_name):
    try:
        except_list2=[]
        df=stock_analysis_chiu_guan_simplified(ticker_name, "2023-06-30", None)
        df["high_than_chiu_guan"]=df["Close"]>=df["midbound"]
        return df.tail(1)
    except Exception as e:
            print("錯誤訊息:", e)
            except_list2.append(e)
            
def advanced_selection(df_input): 
    except_list_df=[]
    
    df_stat=pd.DataFrame([], columns=['Open', 'High', 'Low', 'Close', 'Volume', 'SMA3',
                                          'SMA5', 'SMA8', 'SMA13', 'midbound', 'high_than_chiu_guan',
                                          'Symbol'])
    for i in df_input.index:     
         try:
             df1=chiu_guan_simplified(df_input["Symbol"][i])
             df1["Symbol"]=df_input["Company"][i]
             df_stat=pd.concat([df_stat,df1])
             sum_on_chiuguan=df_stat['high_than_chiu_guan'].sum() 
             rate_on_chiuguan=df_stat['high_than_chiu_guan'].mean()        
         except Exception as e:
             except_list_df.append([df_input["Symbol"][i],df_input["Company"][i],e])
             print("錯誤訊息:", e)
                            
    return except_list_df, df_stat, sum_on_chiuguan,rate_on_chiuguan

#def stock_analysis_for_selection(ticker_name, start_date, end_date,yellow_5,volume_5,mma,yellow_6,wma1,yellow_7,shortstrong,except_list): #, month_line_show_year_interval):    
def stock_analysis_for_selection(ticker_name, start_date, end_date): #, month_line_show_year_interval):        
    try:        
        msg,df1=stock_analysis_chiu_guan(ticker_name, start_date, end_date)
        df1["high_than_chiu_guan"]=df1["Close"]>=df1["midbound"]
        if df1["high_than_chiu_guan"].iloc[-1]==1:
            yellow_5.append(ticker_name)    
        else:
            green_6.append(ticker_name)
        if df1["Volume"].iloc[-1]>700000:
            #print(ticker_name, "當日成交量大於700張")
            volume_5.append(ticker_name)
        if df1["Close"].iloc[-1]>df1["Close"].iloc[-2]:
            #print("當日漲",(df1["Close"][-1]-df1["Close"][-2]).round(2),"元，或", ((df1["Close"][-1]-df1["Close"][-2])/df1["Close"][-2]*100).round(2),"％")
            ups.append(ticker_name)
        else:
            #print("當日跌",(df1["Close"][-1]-df1["Close"][-2]).round(2),"元，或", ((df1["Close"][-1]-df1["Close"][-2])/df1["Close"][-2]*100).round(2),"％")
            downs.append(ticker_name)
        df0=stock_analysis(ticker_name, start_date, end_date,"1d")
        if df0["Close"].iloc[-1]>df0["SMA60"].iloc[-1]:
            #print("衝破季線")
            mma.append(ticker_name)
        if df0["Close"].iloc[-1]<120:
            #print("便宜股")
            cheap.append(ticker_name)
        df2,last_WK_3MA=KDJ_Beta3(ticker_name, start_date, end_date, "1wk")
        if ((df2["J"].iloc[-1]>df2["K"].iloc[-1])&(df2["J"].iloc[-1]>df2["D"].iloc[-1])&(df2["K"].iloc[-1]>df2["D"].iloc[-1])):
            #print(ticker_name,"週KDJ黃金交叉")
            yellow_6.append(ticker_name)
        if df2["Close"].iloc[-1]>df2["SMA55"].iloc[-1]:
            #print("衝破年線")
            wma1.append(ticker_name)
        df3,bull_or_bear_boundary=KDJ_Beta3(ticker_name, start_date, end_date, "1mo")
        if ((df3["J"].iloc[-1]>df3["K"].iloc[-1])&(df3["J"].iloc[-1]>df3["D"].iloc[-1])&(df3["K"].iloc[-1]>df3["D"].iloc[-1])):
            #print(ticker_name,"月KDJ黃金交叉")
            yellow_7.append(ticker_name)
        #if df3["SMA2"][-1]>df3["SMA6"][-1]:
            #print("半年線（月）強勢")
            #mma.append(ticker_name)
        df4=stock_analysis_in_period(ticker_name,"1mo","30m")
        #if ((df4["Close"][-1]>df4["SMA20"][-1])&(df4["SMA20"][-1]>df4["SMA60"][-1])):
        if (df4["SMA20"].iloc[-1]>df4["SMA60"].iloc[-1]):
            #print(ticker_name, "30min線強勢")
            shortstrong.append(ticker_name)
        if df1["Close"].iloc[-1]<last_WK_3MA:
            week_line_check="未通過高於3週線強勢檢核"
#20250528 請將其列入選股程序中            
        else:
            week_line_check="通過高於3週線強勢檢核"
            week3_check.append(ticker_name)
        print(week_line_check)
        if df1["Close"].iloc[-1]<bull_or_bear_boundary:
            month_check="月線趨勢仍然疲弱"
        else:
            month_check="月線強勢"
            monthline_check.append(ticker_name)
        print(month_check)
    except Exception as e:
        except_list.append([ticker_name,e])
        print("錯誤訊息:", e)
                
def advanced_selection2(df_input):
        except_list=[]
        shortstrong=[]
        volume_5=[]
        yellow_5=[]
        yellow_6=[]
        yellow_7=[]     
        green_6=[]     
        wma1=[]
        mma=[]
        ups=[]
        downs=[]
        for i in df_input.index:
              try:
                  #globals()['ticker_'+i] = stock_analysis_mixed(df_input[i],"2023-04-16", None,5)
                  stock_analysis_for_selection(df_input["Symbol"][i], "2023-04-16", None,yellow_5,volume_5,yellow_6,yellow_7,wma1,mma,shortstrong,except_list)
              except Exception as e:
                  print("錯誤訊息:", e)
                  except_list.append(e)
        yellow8=list(set(yellow_5)&set(volume_5)&set(yellow_6)&set(yellow_7)&set(wma1)&set(mma)&set(shortstrong)) 

        # import csv
        # with open("yellow_8.csv", "w", newline="") as yellow_8_csv:
        #     writer = csv.writer(yellow_8_csv)
        #     writer.writerow(yellow8)        
        return shortstrong,volume_5,yellow_5,yellow_6,yellow_7,yellow8,wma1,mma,except_list
#%%
list_1212=["3296.TW","3689.TWO","2661.TW","2881.TW","3019.TW"]
for i in list_1212:
    globals()['ticker_'+i[0:4]]=stock_analysis_mixed(i,"2023-12-16", None,5)
#%%QQQ components
start_time=time.time()
Nasdaq100 = pd.read_csv("~\\Nextcloud\\Investment_Open\\qqq.csv",header=0)
n100_stat=pd.DataFrame([], columns=['Open',
 'High',
 'Low',
 'Close',
 'Volume',
 'SMA3',
 'SMA5',
 'SMA8',
 'SMA13',
 'midbound',
 'high_than_chiu_guan',
 'Symbol'])
#for i in Nasdaq100.index:
for i in Nasdaq100.index:    
    df=chiu_guan_simplified(Nasdaq100["Symbol"][i])
    df["Symbol"]=Nasdaq100["Company"][i]
    n100_stat=pd.concat([n100_stat,df])
    #print(li)
    #df=df.iloc[0]
    #n100_stat.append(df)
n100_stat['high_than_chiu_guan'].mean()    
n100_stat['high_than_chiu_guan'].sum()   

start_time2=time.time()
mid_time=time.time()
shortstrong=[]
volume_5=[]
yellow_5=[]
yellow_6=[]
yellow_7=[]
for i in Nasdaq100.index:
    #globals()['ticker_'+i] = stock_analysis_mixed(mylist[i],"2023-04-16", None,5)
    stock_analysis_for_selection(Nasdaq100["Symbol"][i], "2023-04-16", None,yellow_5,volume_5,yellow_6,yellow_7,shortstrong)
    
yellow8=list(set(yellow_5)&set(volume_5)&set(yellow_6)&set(yellow_7)&set(shortstrong)) 


with open("yellow_8.csv", "w", newline="") as yellow_8_csv:
    writer = csv.writer(yellow_8_csv)
    writer.writerow(yellow8)
end_time=time.time()
print("費時",time.time()-start_time,"秒") 
#%%Taiwan Stocks Sections,merge CSVs 後續修改請以此CELL為正統
if os.name=="posix":
    print("you are using Linux or Mac")
    pathname = '/home/{}/Investment_Open/tw_stocks'.format(os.getlogin())
else:
    print("you are using Windows")
    pathname = 'C:/Users/{}/Investment_Open/tw_stocks'.format(os.getlogin())
try:
    os.chdir(pathname)
except Exception:
    os.makedirs(pathname, exist_ok=True)
    os.chdir(pathname)
designated_date=str(date.today())
#designated_date="2025-04-15"
start_time=time.time()
except_list_TW1=[]
#https://saturncloud.io/blog/how-to-merge-two-csvs-using-pandas-in-python/
#https://www.geeksforgeeks.org/how-to-stack-multiple-pandas-dataframes/
#emerging=pd.read_csv("~\\Nextcloud\\Investment_Open\\emerging.csv",header=0)
#publish=pd.read_csv("~\\Nextcloud\\Investment_Open\\publish.csv",header=0)
otc=pd.read_csv("~/Nextcloud/Investment_Open/otc.csv",header=0,encoding = "big5hkscs")
otc["postfix"]=".TWO"
otc["Symbol"]=""
otc["Symbol"]=otc["Symbol"].str.cat([otc["公司代號"].astype(str),otc["postfix"].astype(str)])
twse=pd.read_csv("~/Nextcloud/Investment_Open/twse.csv",header=0,encoding = "big5hkscs")
twse["postfix"]=".TW"
twse["Symbol"]=""
twse["Symbol"]=twse["Symbol"].str.cat([twse["公司代號"].astype(str),twse["postfix"].astype(str)])
#邱老師的軟體只有上市櫃股票
merged_df = pd.concat([otc,twse],ignore_index=True, axis=0)
merged_df_stat=pd.DataFrame([], columns=['Open',
 'High',
 'Low',
 'Close',
 'Volume',  
 'SMA3',
 'SMA5',
 'SMA8',
 'SMA13',
 'midbound',
 'high_than_chiu_guan',
 'Symbol'])
# for i in merged_df.index:    
#     try:
#         df=chiu_guan_simplified(merged_df["Symbol"][i])
#         df["Symbol"]=merged_df["Company"][i]
#         merged_df_stat=pd.concat([merged_df_stat,df])
#     except Exception as e:
#         print("錯誤訊息:", e)
#         except_list_TW1.append([merged_df["Symbol"],e])
#         continue

# merged_df_stat['high_than_chiu_guan'].sum() 
# merged_df_stat['high_than_chiu_guan'].mean()
# print("===seg1 completed===")

#segment2
start_time2=time.time()
cheap=[]
mma=[]
except_list_TW=[]
except_list=[]
mid_time=time.time()
shortstrong=[]
volume_5=[]
yellow_5=[]
yellow_6=[]
yellow_7=[]
green_6=[] 
#green_6=[]    
wma1=[]
ups=[]
downs=[]
week3_check=[]
monthline_check=[]
for i in merged_df.index:
    #globals()['ticker_'+i] = stock_analysis_mixed(mylist[i],"2023-04-16", None,5)
    try:
        stock_analysis_for_selection(merged_df["Symbol"][i], "2024-09-01", (datetime.strptime(designated_date,"%Y-%m-%d")+ timedelta(days=1)))
    except Exception as e:
        print("錯誤訊息:", e)
        except_list_TW.append([merged_df["Symbol"],e])
    
    #ticker_name, start_date, end_date,yellow_5,volume_5,yellow_6,yellow_7,shortstrong,wma1,mma,except_list
#yellow8=list(set(yellow_5)&set(volume_5)&set(yellow_6)&set(mma)&set(wma1)&set(shortstrong))
yellow8=list(set(yellow_5)&set(volume_5)&set(yellow_6)&set(mma)&set(shortstrong)&set(cheap)&set(yellow_7)&set(wma1))

advance_decline_ratio=len(ups)/len(downs)
advance_decline_line=len(ups)-len(downs)
over_buy_over_sell=len(ups)-len(downs)

# #write csvs
csv_lists={"shortstrong":shortstrong,"volume_5":volume_5,"yellow_5":yellow_5,"yellow_6":yellow_6,"yellow_7":yellow_7,"wma1":wma1,"yellow8":yellow8,"green_6":green_6,"wma1":wma1,"ups":ups,"downs":downs}
# #csv_lists={shortstrong:"shortstrong",volume_5:"volume_5",yellow_5:"yellow_5",yellow_6:"yellow_6",yellow_7:"yellow_7",wma1:"wma1",yellow8:"yellow8"}
# #csv_lists_name=[,"volume_5","yellow_5","yellow_6","yellow_7","wma1","yellow8"]
database=pd.read_csv("tw_database.csv",index_col=0)
#database=pd.DataFrame([],columns=["date","category","ticker"])
for i in csv_lists:    
    df = pd.DataFrame(csv_lists[i],columns=["ticker"])
    df["date"]=designated_date
    #df["date"]="2025-05-27"
    df["category"]=i
    #df.to_csv("{}_TW_{}.csv".format(i,"2025-05-27"))#,columns=df,header="Quotes")
    df.to_csv("{}_TW_{}.csv".format(i,designated_date))#,columns=df,header="Quotes")
    database=pd.concat([database,df])
    #database=pd.concat([database,df])
database.to_csv("tw_database.csv")

# csv_lists2={"ups":len(ups),"downs":len(downs),"advance_decline_ratio":advance_decline_ratio,"advance_decline_line":advance_decline_line,"over_buy_over_sell":over_buy_over_sell}
# labels = ["Subject", "Property"]

# try:
#     with open("params.csv", "w") as f:
#         writer = csv.DictWriter(f, fieldnames=labels)
#         writer.writeheader()
#         writer.writerow(csv_lists2)
# except IOError:
#     print("I/O error")

#import csv
#with open("yellow_8.csv", "w", newline="") as yellow_8_csv:
    #writer = csv.writer(yellow_8_csv)
    #writer.writerow(yellow8)
#end_time=time.time()
#taiwan_allname=pd.read_csv("all.csv")
df_yellow8=pd.DataFrame(yellow8, columns=["Symbol"]).sort_values("Symbol")
namelist=df_yellow8.set_index("Symbol").join(merged_df.set_index("Symbol"), how="left", lsuffix='_left', rsuffix='_right')
namelist.to_csv("TW_Namelist_{}.csv".format(designated_date))#,columns=df,header="Quotes")
print("費時",time.time()-start_time,"秒")
yellow8.sort()
#抓圖用
for i in yellow8:
    globals()['analysis_'+i]=stock_analysis_mixed(i,"2024-07-01",None,5)
end_time=time.time()
print(end_time)
#conclusion
print("===============in conclusion===============")
print("當日台灣股市上漲家數",len(ups))
print("當日台灣股市下跌家數",len(downs))
print("當日台灣股市站上丘關數",len(yellow_5),"家，占上市總家數", len(merged_df),"家，之", round((len(yellow_5)/len(merged_df))*100,2),"％")
print("當日台灣股市ADR（漲跌比率）值為：", round(advance_decline_ratio,2))
print("當日台灣股市ADL（騰落指標）值為：", advance_decline_line)
print("當日台灣股市OBOS（超買超賣）值為：", over_buy_over_sell)
print("費時",time.time()-start_time,"秒")
#%%TW_Merged Functioned
otc=pd.read_csv("~/Nextcloud/Investment_Open/otc.csv",header=0)
twse=pd.read_csv("~/Nextcloud/Investment_Open/twse.csv",header=0)
#邱老師的軟體只有上市櫃股票
merged_df = pd.concat([otc,twse],ignore_index=True, axis=0)
start_time=time.time()
#merged_df_test=advanced_selection(merged_df)
merged_df_test2=advanced_selection2(merged_df)
end_time=time.time()
print("費時",time.time()-start_time,"秒")
#%%merge CSVs_USA
start_time=time.time()
if os.name=="posix":
    print("you are using Linux or Mac")
    pathname = '/home/{}/Investment_Open/US_stocks'.format(os.getlogin())
else:
    print("you are using Windows")
    pathname = 'C:/Users/{}/Investment_Open/US_stocks'.format(os.getlogin())
try:
    os.chdir(pathname)
except Exception:
    os.makedirs(pathname, exist_ok=True)
    os.chdir(pathname)
designated_date=str(date.today())
designated_date="2025-10-08"

NYSE1=pd.read_csv("https://cdn.jsdelivr.net/gh/ahmeterenodaci/New-York-Stock-Exchange--NYSE--including-Symbols-and-Logos/without_logo.csv")
NYSE2=pd.DataFrame([],columns=["Symbol","Name"])
NYSE2["Symbol"]=NYSE1["symbol"]
NYSE2["Name"]=NYSE1["name"]
NASDAQ=pd.read_csv("~/Nextcloud/Investment_Open/nasdaq_screener_1717160974784.csv")
NASDAQ2=pd.DataFrame([],columns=["Symbol","Name"])
NASDAQ2["Symbol"]=NASDAQ["Symbol"]
NASDAQ2["Name"]=NASDAQ2["Name"]
#https://saturncloud.io/blog/how-to-merge-two-csvs-using-pandas-in-python/
#https://www.geeksforgeeks.org/how-to-stack-multiple-pandas-dataframes/
#emerging=pd.read_csv("~\\Nextcloud\\Investment_Open\\emerging.csv",header=0)
#publish=pd.read_csv("~\\Nextcloud\\Investment_Open\\publish.csv",header=0)
NYSE_and_NASDAQ=pd.concat([NYSE2,NASDAQ2],ignore_index=True, axis=0)
NYSE_and_NASDAQ2=NYSE_and_NASDAQ
merged_df=NYSE_and_NASDAQ.drop_duplicates(subset=['Symbol'])

#merged_df = pd.concat([otc,twse],ignore_index=True, axis=0)
merged_df_stat=pd.DataFrame([], columns=['Open',
 'High',
 'Low',
 'Close',
 'Volume',  
 'SMA3',
 'SMA5',
 'SMA8',
 'SMA13',
 'midbound',
 'high_than_chiu_guan',
 'Symbol'])
# for i in merged_df.index:    
#     try:
#         df=chiu_guan_simplified(merged_df["Symbol"][i])
#         df["Symbol"]=merged_df["Company"][i]
#         merged_df_stat=pd.concat([merged_df_stat,df])
#     except Exception as e:
#         print("錯誤訊息:", e)
#         except_list_TW1.append([merged_df["Symbol"],e])
#         continue

# merged_df_stat['high_than_chiu_guan'].sum() 
# merged_df_stat['high_than_chiu_guan'].mean()
# print("===seg1 completed===")

#segment2
start_time2=time.time()
cheap=[]
mma=[]
except_list_TW=[]
except_list=[]
mid_time=time.time()
shortstrong=[]
volume_5=[]
yellow_5=[]
yellow_6=[]
yellow_7=[]
green_6=[]     
wma1=[]
ups=[]
downs=[]
week3_check=[]
monthline_check=[]
for i in merged_df.index:
    #globals()['ticker_'+i] = stock_analysis_mixed(mylist[i],"2023-04-16", None,5)
    try:
        stock_analysis_for_selection(merged_df["Symbol"][i], "2024-06-01", (datetime.strptime(designated_date,"%Y-%m-%d")+ timedelta(days=1)))
    except Exception as e:
        print("錯誤訊息:", e)
        except_list_TW.append([merged_df["Symbol"],e])
    
    #ticker_name, start_date, end_date,yellow_5,volume_5,yellow_6,yellow_7,shortstrong,wma1,mma,except_list
#yellow8=list(set(yellow_5)&set(volume_5)&set(yellow_6)&set(mma)&set(wma1)&set(shortstrong))
yellow8=list(set(yellow_5)&set(volume_5)&set(yellow_6)&set(mma)&set(shortstrong)&set(cheap)&set(yellow_7)&set(wma1))

advance_decline_ratio=len(ups)/len(downs)
advance_decline_line=len(ups)-len(downs)
over_buy_over_sell=len(ups)-len(downs)

# #write csvs
csv_lists={"shortstrong":shortstrong,"volume_5":volume_5,"yellow_5":yellow_5,"yellow_6":yellow_6,"yellow_7":yellow_7,"wma1":wma1,"yellow8":yellow8,"green_6":green_6,"wma1":wma1,"ups":ups,"downs":downs}
# #csv_lists={shortstrong:"shortstrong",volume_5:"volume_5",yellow_5:"yellow_5",yellow_6:"yellow_6",yellow_7:"yellow_7",wma1:"wma1",yellow8:"yellow8"}
# #csv_lists_name=[,"volume_5","yellow_5","yellow_6","yellow_7","wma1","yellow8"]
#database=pd.read_csv("US_database.csv",index_col=0)
database=pd.DataFrame([],columns=["date","category","ticker"])
for i in csv_lists:    
    df = pd.DataFrame(csv_lists[i],columns=["ticker"])
    df["date"]=designated_date
    #df["date"]="2025-05-27"
    df["category"]=i
    #df.to_csv("{}_TW_{}.csv".format(i,"2025-05-27"))#,columns=df,header="Quotes")
    df.to_csv("{}_US_{}.csv".format(i,designated_date))#,columns=df,header="Quotes")
    database=pd.concat([database,df])
    #database=pd.concat([database,df])
#database.to_csv("tw_database.csv")

# csv_lists2={"ups":len(ups),"downs":len(downs),"advance_decline_ratio":advance_decline_ratio,"advance_decline_line":advance_decline_line,"over_buy_over_sell":over_buy_over_sell}
# labels = ["Subject", "Property"]

# try:
#     with open("params.csv", "w") as f:
#         writer = csv.DictWriter(f, fieldnames=labels)
#         writer.writeheader()
#         writer.writerow(csv_lists2)
# except IOError:
#     print("I/O error")

#import csv
#with open("yellow_8.csv", "w", newline="") as yellow_8_csv:
    #writer = csv.writer(yellow_8_csv)
    #writer.writerow(yellow8)
#end_time=time.time()
#taiwan_allname=pd.read_csv("all.csv")
df_yellow8=pd.DataFrame(yellow8, columns=["Symbol"])
#namelist=df_yellow8.set_index("Symbol").join(merged_df.set_index("Symbol"), how="left", lsuffix='_left', rsuffix='_right')
#namelist.to_csv("TW_Namelist_{}.csv".format(designated_date))#,columns=df,header="Quotes")
print("費時",time.time()-start_time,"秒")

#抓圖用
for i in yellow8:
    globals()['analysis_'+i]=stock_analysis_mixed(i,"2024-07-01",None,5)
end_time=time.time()
print(end_time)
#conclusion
print("===============in conclusion===============")
print("日期為", designated_date)
print("當日上漲家數",len(ups))
print("當日下跌家數",len(downs))
print("當日站上丘關數",len(yellow_5),"家，占上市總家數", len(merged_df),"家，之", round((len(yellow_5)/len(merged_df))*100,2),"％")
print("當日ADR（漲跌比率）值為：", round(advance_decline_ratio,2))
print("當日ADL（騰落指標）值為：", advance_decline_line)
print("當日OBOS（超買超賣）值為：", over_buy_over_sell)
print("費時",time.time()-start_time,"秒")
#%%American Traded ETFs
start_time=time.time()
filename = "/home/fattabby/Nextcloud/Investment_Open/USETFs/"
try:
    os.chdir(pathname)
except Exception:
    os.makedirs(os.path.dirname(pathname), exist_ok=True)
    
merged_df=pd.read_excel("https://www.nyse.com/publicdocs/nyse/markets/nyse-arca/NYSE_Arca_Equities_LMM_Current.xlsx")

NYSE2=pd.DataFrame([],columns=["Symbol","ETP Name","Product Category","Lead Market Maker"])

#merged_df = pd.concat([otc,twse],ignore_index=True, axis=0)
merged_df_stat=pd.DataFrame([], columns=['Open',
 'High',
 'Low',
 'Close',
 'Volume',  
 'SMA3',
 'SMA5',
 'SMA8',
 'SMA13',
 'midbound',
 'high_than_chiu_guan',
 'Symbol'])
# for i in merged_df.index:    
#     try:
#         df=chiu_guan_simplified(merged_df["Symbol"][i])
#         df["Symbol"]=merged_df["Company"][i]
#         merged_df_stat=pd.concat([merged_df_stat,df])
#     except Exception as e:
#         print("錯誤訊息:", e)
#         except_list_TW1.append([merged_df["Symbol"],e])
#         continue

# merged_df_stat['high_than_chiu_guan'].sum() 
# merged_df_stat['high_than_chiu_guan'].mean()
# print("===seg1 completed===")

#segment2
start_time2=time.time()
mma=[]
except_list_TW=[]
except_list=[]
mid_time=time.time()
shortstrong=[]
volume_5=[]
yellow_5=[]
yellow_6=[]
yellow_7=[]
wma1=[]
for i in merged_df.index:
    #globals()['ticker_'+i] = stock_analysis_mixed(mylist[i],"2023-04-16", None,5)
    try:
        stock_analysis_for_selection(merged_df["Symbol"][i], "2023-04-16", None)
    except Exception as e:
        print("錯誤訊息:", e)
        except_list_TW.append([merged_df["Symbol"],e])
    
    #ticker_name, start_date, end_date,yellow_5,volume_5,yellow_6,yellow_7,shortstrong,wma1,mma,except_list
yellow8=list(set(yellow_5)&set(volume_5)&set(yellow_6)&set(mma)&set(wma1))#&set(shortstrong) 

#write csvs
csv_lists={"shortstrong":shortstrong,"volume_5":volume_5,"yellow_5":yellow_5,"yellow_6":yellow_6,"yellow_7":yellow_7,"wma1":wma1,"yellow8":yellow8}
#csv_lists={shortstrong:"shortstrong",volume_5:"volume_5",yellow_5:"yellow_5",yellow_6:"yellow_6",yellow_7:"yellow_7",wma1:"wma1",yellow8:"yellow8"}
#csv_lists_name=[,"volume_5","yellow_5","yellow_6","yellow_7","wma1","yellow8"]
database=pd.read_csv("US_ETF_database.csv",index_col=0)
#database=pd.DataFrame([],columns=["date","category","ticker"])
for i in csv_lists:    
    df = pd.DataFrame(csv_lists[i],columns=["ticker"])
    df["date"]=date.today()
    df["category"]=i
    df.to_csv("{}_US_ETFS_{}.csv".format(i,"2025-05-21"))#,columns=df,header="Quotes")
    database=pd.concat([database,df])
    #database=pd.concat([database,df])
database.to_csv("US_ETF_database.csv")
#df.to_csv("US_ETF_database.csv")
#抓圖用
for i in yellow8:
    globals()['analysis_'+i]=stock_analysis_mixed(i,"2023-06-16", None,5)
end_time=time.time()
print(end_time)
#import csv
#with open("yellow_8.csv", "w", newline="") as yellow_8_csv:
    #writer = csv.writer(yellow_8_csv)
    #writer.writerow(yellow8)
#end_time=time.time()
#taiwan_allname=pd.read_csv("all.csv")
#df_yellow8=pd.DataFrame(yellow8, columns=["Symbol"])
#namelist=df_yellow8.set_index("Symbol").join(merged_df.set_index("Symbol"), how="left", lsuffix='_left', rsuffix='_right')
#namelist.to_csv("US_ETF_Namelist_{}.csv".format(date.today()))#,columns=df,header="Quotes")
print("費時",time.time()-start_time,"秒")

#%%import csv
with open("yellow_8.csv", "w", newline="") as yellow_8_csv:
    writer = csv.writer(yellow_8_csv)
    writer.writerow(yellow8)
end_time=time.time()
print("費時",time.time()-start_time,"秒")
#write csvs
csv_lists={"shortstrong":shortstrong,"volume_5":volume_5,"yellow_5":yellow_5,"yellow_6":yellow_6,"yellow_7":yellow_7,"wma1":wma1,"yellow8":yellow8}
#csv_lists={shortstrong:"shortstrong",volume_5:"volume_5",yellow_5:"yellow_5",yellow_6:"yellow_6",yellow_7:"yellow_7",wma1:"wma1",yellow8:"yellow8"}
#csv_lists_name=[,"volume_5","yellow_5","yellow_6","yellow_7","wma1","yellow8"]
for i in csv_lists:
    df = pd.DataFrame(csv_lists[i])
    df.to_csv("{}_US_{}.csv".format(i,date.today()))#,columns=df,header="Quotes")
#%%write csv_s instruments
csv_lists={"shortstrong":shortstrong,"volume_5":volume_5,"yellow_5":yellow_5,"yellow_6":yellow_6,"yellow_7":yellow_7,"wma1":wma1,"yellow8":yellow8}
#csv_lists={shortstrong:"shortstrong",volume_5:"volume_5",yellow_5:"yellow_5",yellow_6:"yellow_6",yellow_7:"yellow_7",wma1:"wma1",yellow8:"yellow8"}
#csv_lists_name=[,"volume_5","yellow_5","yellow_6","yellow_7","wma1","yellow8"]
for i in csv_lists:
    df = pd.DataFrame(csv_lists[i])
    df.to_csv("{}_{}.csv".format(i,date.today()))#,columns=df,header="Quotes")
#%%
mid_time=time.time()
shortstrong=[]
volume_5_USA=[]
yellow_5_USA=[]
yellow_6_USA=[]
yellow_7_USA=[]
for i in NYSE_and_NASDAQ.index:
    #globals()['Symbol_'+i] = stock_analysis_mixed(mylist[i],"2023-04-16", None,5)
    stock_analysis_for_selection(NYSE_and_NASDAQ["Symbol"][i], "2023-04-16", None,yellow_5_USA,volume_5_USA,yellow_6_USA,yellow_7_USA,shortstrong)
    
yellow8=list(set(yellow_5_USA)&set(volume_5_USA)&set(yellow_6_USA)&set(yellow_7_USA)&set(shortstrong)) 

#import csv
with open("yellow_8.csv", "w", newline="") as yellow_8_csv:
    writer = csv.writer(yellow_8_csv)
    writer.writerow(yellow8)
end_time=time.time()
print("費時",end_time-start_time,"秒")


#%%odds verify(needs correction)
for i in yellow8:
    globals()['ticker_'+i] =odds_ratio_chiu_guan_simplified(i)[1]

#%%
list=["GME","NVDA","MSFT","AAPL","2330.TW"]
for i in list:
    globals()['odds_'+i]=odds_ratio_chiu_guan_simplified(i)[1]
    
TWII=odds_ratio_chiu_guan_simplified("^TWII")
NQ=odds_ratio_chiu_guan_simplified("^IXIC")


#%%

#df.shift(periods=-13)



#df.truncate(13,)

#%%
chiu_guan=midbound.iloc[-1,-1].round(4)    
today_close=df["Close"][-1]
print(ticker_name,"截至", df.index[-1].strftime('%Y-%m-%d'),"丘關為：",chiu_guan, " 點/元")
if today_close>=chiu_guan:
    subtitle="今日收盤價 "+str(today_close.round(4))+" 站上或高於丘關 "+str(chiu_guan)
    print(subtitle)
elif today_close<chiu_guan:
    subtitle="今日收盤價 "+str(today_close.round(4))+" 跌破或低於丘關 "+str(chiu_guan)
    print(subtitle)
#%%
if os.name=="posix":
    print("you are using Linux or Mac")
    pathname = '/home/{}/Investment_Open/main_indicies'.format(os.getlogin())
else:
    print("you are using Windows")
    pathname = 'C:/Users/{}/main_indicies'.format(os.getlogin())

try:
    os.chdir(pathname)
except Exception:
    os.makedirs(pathname, exist_ok=True)
    os.chdir(pathname)
#Commonly Used
mylist={#"TW_OTC":"^TWOII",
        "TW_Weighted":"^TWII",
        "TSMC_TW":"2330.TW",
        "NASDAQ_Composite":"^IXIC",
        "PHLX":"^SOX",
        "Nikkei225":"^N225",
        "KOSPI":"^KS11",
        "Singapore_Strait_Times":"^STI",
        "GDAXI":"^GDAXI",
        #"S&P_Biotech":"^SPSIBI",
        "LABU":"LABU",
        "TECL":"TECL",
        "S_and_P_500":"^GSPC",
        "DJIA":"^DJI",
        "TSMC_ADR":"TSM",
        "Bitcoin_USD":"BTC-USD"}

for i in mylist:
    globals()['ticker_'+i] = stock_analysis_mixed(mylist[i],"2024-10-01", None,5)
#%%simple 抓圖用
for i in yellow8:
    globals()['analysis_'+i]=stock_analysis_mixed(i,"2023-06-16", None,5)
#%%
yellow_5=[]
volume_5=[]
yellow_6=[]
yellow_7=[]
for i in mylist:
    globals()['ticker_'+i] = stock_analysis_mixed(mylist[i],"2023-04-16", None,5)
    stock_analysis_for_selection(mylist[i], "2023-04-16", None,yellow_5,volume_5,yellow_6,yellow_7)
yellow8=list(set(yellow_5)&set(volume_5)&set(yellow_6)&set(yellow_7))    
    
#%%

#%%
mylist2=["6753.TW", "4533.TWO", "8033.TW"]
for i in mylist2:
    stock_analysis_mixed(i, "2022-06-01", "2024-04-1ˊ",5)
#%%
#20240305
mylist2={"Hsinli":"4303.TWO",
         "Pogo":"6217.TWO",
         "Alcor":"8054.TWO",
         "EgisTec":"6462.TWO",
         "AlgolTek":"6684.TWO",
         "iCatch":"6695.TW",
         "Yuanjen":"1725.TW",
         "China_Glaze":"1809.TW"}    
for i in mylist2:
    globals()['ticker_'+mylist2[i]] = stock_analysis_mixed(mylist2[i],"2022-06-01", None,5)
'''
20231129 assumed portfolio
LABU all in longterm
TQQQ all in shortterm
___________________________
Verifications 20231130:
20231201 TQQQ failed
20231201 LABU succeed
    

#during holidays, please setup 短多中多長多, etc., vice versa.
'''
#%%
today=date.today()
FED_M1_weekly_link = 'https://fred.stlouisfed.org/graph/fredgraph.csv?bgcolor=%23e1e9f0&chart_type=line&drp=0&fo=open%20sans&graph_bgcolor=%23ffffff&height=450&mode=fred&recession_bars=on&txtcolor=%23444444&ts=12&tts=12&width=1168&nt=0&thu=0&trc=0&show_legend=yes&show_axis_titles=yes&show_tooltip=yes&id=WM1NS&scale=left&cosd=1975-01-06&coed=2022-10-31&line_color=%234572a7&link_values=false&line_style=solid&mark_type=none&mw=3&lw=2&ost=-99999&oet=99999&mma=0&fml=a&fq=Weekly%2C%20Ending%20Monday&fam=avg&fgst=lin&fgsnd=2020-02-01&line_index=1&transformation=lin&vintage_date={}&revision_date={}&nd=1975-01-06'.format(today,today) #已植入下載當日變數，不過系統只會抓到可用的該日變數
FED_M1_weekly=pd.read_csv(FED_M1_weekly_link)
#former
#FED_M1_monthly_seasonly_adjusted_link="https://fred.stlouisfed.org/graph/fredgraph.csv?bgcolor=%23e1e9f0&chart_type=line&drp=0&fo=open%20sans&graph_bgcolor=%23ffffff&height=450&mode=fred&recession_bars=on&txtcolor=%23444444&ts=12&tts=12&width=1168&nt=0&thu=0&trc=0&show_legend=yes&show_axis_titles=yes&show_tooltip=yes&id=M1SL&scale=left&cosd=1959-01-01&coed=2022-10-01&line_color=%234572a7&link_values=false&line_style=solid&mark_type=none&mw=3&lw=2&ost=-99999&oet=99999&mma=0&fml=a&fq=Monthly&fam=avg&fgst=lin&fgsnd=2020-02-01&line_index=1&transformation=lin&vintage_date={}&revision_date={}&nd=1959-01-01".format(today,today)
FED_M1_monthly_seasonly_adjusted_link="https://fred.stlouisfed.org/graph/fredgraph.csv?bgcolor=%23e1e9f0&chart_type=line&drp=0&fo=open%20sans&graph_bgcolor=%23ffffff&height=450&mode=fred&recession_bars=on&txtcolor=%23444444&ts=12&tts=12&width=1318&nt=0&thu=0&trc=0&show_legend=yes&show_axis_titles=yes&show_tooltip=yes&id=M1SL&scale=left&cosd=1959-01-01&coed=2023-10-01&line_color=%234572a7&link_values=false&line_style=solid&mark_type=none&mw=3&lw=2&ost=-99999&oet=99999&mma=0&fml=a&fq=Monthly&fam=avg&fgst=lin&fgsnd=2020-02-01&line_index=1&transformation=lin&vintage_date={}&revision_date={}&nd=1959-01-01".format(today,today)
#https://fred.stlouisfed.org/graph/fredgraph.csv?bgcolor=%23e1e9f0&chart_type=line&drp=0&fo=open%20sans&graph_bgcolor=%23ffffff&height=450&mode=fred&recession_bars=on&txtcolor=%23444444&ts=12&tts=12&width=1318&nt=0&thu=0&trc=0&show_legend=yes&show_axis_titles=yes&show_tooltip=yes&id=M1SL&scale=left&cosd=1959-01-01&coed=2023-10-01&line_color=%234572a7&link_values=false&line_style=solid&mark_type=none&mw=3&lw=2&ost=-99999&oet=99999&mma=0&fml=a&fq=Monthly&fam=avg&fgst=lin&fgsnd=2020-02-01&line_index=1&transformation=lin&vintage_date=2023-12-01&revision_date=2023-12-01&nd=1959-01-01
FED_M1_monthly_seasonly_adjusted=pd.read_csv(FED_M1_monthly_seasonly_adjusted_link)

FED_M1_monthly_seasonly_adjusted["Growth_Rate"]=""
FED_M1_monthly_seasonly_adjusted["Growth_Rate_percent"]=""
FED_M1_monthly_seasonly_adjusted["Week_of_the_Year"]=""
for i,j in zip(range(0,len(FED_M1_monthly_seasonly_adjusted)),range(12,len(FED_M1_monthly_seasonly_adjusted))):
    FED_M1_monthly_seasonly_adjusted["Growth_Rate"][j]=((FED_M1_monthly_seasonly_adjusted.iloc[j][1]-FED_M1_monthly_seasonly_adjusted.iloc[i][1])/FED_M1_monthly_seasonly_adjusted.iloc[i][1])
    FED_M1_monthly_seasonly_adjusted["Growth_Rate_percent"][j]=FED_M1_monthly_seasonly_adjusted["Growth_Rate"][j]*100

for i in range(len(FED_M1_monthly_seasonly_adjusted)):
    FED_M1_monthly_seasonly_adjusted["Week_of_the_Year"][i]=pd.Timestamp(FED_M1_monthly_seasonly_adjusted["DATE"][i])
    FED_M1_monthly_seasonly_adjusted["Week_of_the_Year"][i]=FED_M1_monthly_seasonly_adjusted["Week_of_the_Year"][i].strftime('%G-%V')
#%%for testing

IXIC_KDJ_wk=KDJ_Beta3("^IXIC","2022-09-01", None, "1wk")
IXIC_KDJ_month=KDJ_Beta3("^IXIC","2021-09-01", None, "1mo")

TWII_KDJ_wk=KDJ_Beta3("^TWII","2021-09-01", None, "1wk")
TWII_KDJ_wk=KDJ_Beta3("^TWII","2021-09-01", None, "1mo")
#%%
TWOII_general=stock_analysis_mixed("^TWOII","2022-01-01", None,5)
TWII_general= stock_analysis_mixed("^TWII","2022-01-01", None,5)
IXIC_general= stock_analysis_mixed("^IXIC","2022-09-01", None,5)
PHLX_general= stock_analysis_mixed("^SOX","2022-09-01", None,5)
Nikkei225=stock_analysis_mixed("^N225","2022-09-01", None,5)
GDAXI_general=stock_analysis_mixed("^GDAXI","2022-01-01", None,10)
LABU_general=stock_analysis_mixed("LABU","2021-01-01", None,5) 
TECL_general=stock_analysis_mixed("TECL","2021-01-01", None,5) 
#%%20231128 Lists
chiu_list=["3623.TWO","2313.TW","2211.TW","8089.TWO","4945.TWO","1513.TW",
           "3545.TW","2436.TW","5608.TW","3437.TW","2472.TW","3056.TW",
           "3060.TW","5236.TWO","2108.TW","2375.TW","3058.TW","6104.TWO",
           "3228.TWO","2230.TWO","2476.TW","6494.TWO","6462.TWO","6186.TWO",
           "4188.TWO","3041.TW"]           
#%%20240205_List
c1=["8096.TWO","2027.TW","4916.TW","5201.TWO","6148.TWO"]
c2=["2471.TW","2453.TW","2468.TW","5203.TW","4916.TW","3090.TW",
    "3029.TW","3645.TW","6546.TWO","6269.TW","6245.TWO","6112.TW",
    "4971.TWO","6140.TWO"]
for i in c1:
    globals()['ticker_'+i] = stock_analysis_mixed(i,"2023-12-01", None,5)
print("this is the end of chiu transacted")
for i in c2:
    globals()['ticker_'+i] = stock_analysis_mixed(i,"2023-12-01", None,5)
print("this is the end of chiu not-transacted")

#%%20240226_List
c1=["5608.TW","3685.TWO","4949.TW","4534.TWO"]

for i in c1:
    globals()['ticker_'+i] = stock_analysis_mixed(i,"2023-12-01", None,5)
print("this is the end of chiu transacted")

#%%KDJ Beta1
#https://blog.csdn.net/weixin_42322206/article/details/122446672
plt.figure(figsize=(12, 8))
low_list=df["Low"].rolling(window=9).min()
low_list.fillna(value=df["Low"].expanding().min(), inplace=True)
high_list = df["High"].rolling(window=9).max()
high_list.fillna(value=df["High"].expanding().max(), inplace=True)
rsv = (df["Close"] - low_list) / (high_list - low_list) * 100
df["KDJ_K"] = rsv.ewm(com=2).mean()  
 # pd.Series.ewm(rsv, com=2).mean()
df["KDJ_D"] = df["KDJ_K"].ewm(com=2).mean()
 # pd.Series.ewm(stock_datas["K"], com=2).mean()
df["KDJ_J"] = 3 * df["KDJ_K"] - 2 * df["KDJ_D"]
plt.plot(df["KDJ_K"], label ="K")
plt.plot(df["KDJ_D"], label ="D")
plt.plot(df["KDJ_J"], label ="J")
#%%KDJ_Beta2
#算是大致複製了Yeswin的結果
#https://inf.news/zh-hant/economy/4ec2a66c7d32bcdf2023fdf9db50453f.html
#import matplotlib.pyplot as plt
#https://matplotlib.org/stable/gallery/color/named_colors.html
plt.figure(figsize=(12,4))
low_list = df["Close"].rolling(9, min_periods=1).min()
high_list = df["High"].rolling(9, min_periods=1).max()
rsv = (df["Close"] - low_list) / (high_list - low_list) * 100
df["K"] = rsv.ewm(com=2, adjust=False).mean()
df["D"] = df["K"].ewm(com=2, adjust=False).mean()
df["J"] = 3 * df["K"] - 2 * df["D"]
plt.plot(df["K"], label ="K", color="y")
plt.plot(df["D"], label ="D", color="aqua")
plt.plot(df["J"], label ="J", color= "lime")
#plt.plot(df["Date"], df["K"], label ="K")
#plt.plot(df["Date"], df["D"], label ="D")
#plt.plot(df["date"], df["J"], label ="J")
plt.legend()
plt.show()
#%%KDJ_Beta3
#https://www.finlab.tw/python-%E7%B0%A1%E5%96%AE158%E7%A8%AE%E6%8A%80%E8%A1%93%E6%8C%87%E6%A8%99%E8%A8%88%E7%AE%97/

df["high"]=df["High"]
df["low"]=df["Low"]
df["close"]=df["Close"]

def talib2df(talib_output):
    if type(talib_output) == list:
        ret = pd.DataFrame(talib_output).transpose()
    else:
        ret = pd.Series(talib_output)
    ret.index = df['close'].index
    return ret;

talib2df(abstract.STOCH(df)).plot()
df['close'].plot(secondary_y=True)

#%%
stock_analysis_chiu_guan("^IXIC","2023-01-01", None, "1d") 
stock_analysis_chiu_guan("^SOX","2023-01-01", None, "1d") 
stock_analysis_chiu_guan("^TWII","2023-01-01", None, "1d") 
stock_analysis_chiu_guan("^GSPC","2023-01-01", None, "1d")
stock_analysis_chiu_guan("TECL","2023-01-01", None, "1d")    
#%%    

stock_analysis_chiu_guan("^TWII","2022-11-01",None,"1d")   
stock_analysis_chiu_guan("2885.TW","2022-11-01",None,"1d")   
#stock_analysis_chiu_guan("^TWO","2022-11-01",None,"1d")   

#%%
#Over the counter

#month average 1 2 3 6 12 120
#vol 5 10 20

#week
#ma 3 8 13 21 34 55
 
#day
#ma 3 5 8 13
#5、10、20、60、10、200

#%%
def MACD(df):
    macd, signal, hist = talib.MACD(df['Close'].values, fastperiod=12, slowperiod=26, signalperiod=9)
    df['MACD'] = macd
    df['MACD_DIF'] = signal
    df['HIST'] = hist
    fig, axes = plt.subplots(nrows=2)
    df['Close'].tail(200).plot(ax=axes[0])
    df[['MACD', 'MACD_DIF', 'HIST']].tail(200).plot(ax=axes[1])
MACD(df)    
    
#%%
#Talib MACD
macd, signal, hist = talib.MACD(df['Close'].values, fastperiod=12, slowperiod=26, signalperiod=9)
df['MACD'] = macd
df['MACD_DIF'] = signal
df['HIST'] = hist
fig, axes = plt.subplots(nrows=2)
df['Close'].tail(200).plot(ax=axes[0])
df[['MACD', 'MACD_DIF', 'HIST']].tail(200).plot(ax=axes[1])

