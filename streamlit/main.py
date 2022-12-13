# library imports

import streamlit as st
import pandas as pd
import numpy as np
from pathlib import Path
from os.path import realpath,dirname
import os
import csv
import matplotlib.pyplot as plt

from typing import List,Any

#freq = 'd'

freq_option = st.selectbox('Date Level Selector',['Year','Quarter','Month','Week','Day'])
freq_dict = {
     'Year':'y'
    ,'Month':'m'
    ,'Quarter':'q'
    ,'Week':'w'
    ,'Day':'d'
}


freq = freq_dict.get(freq_option)


SHEET_TYPES = {
     'date': 'datetime64[ns]'
    ,'category':str
    ,'type':str
    ,'amount':np.dtype('float32')
    ,'description':str
    ,'amount_cents':np.dtype('int32')
}

SHEET_COLUMNS = list(SHEET_TYPES.keys())


CATEGORIES = [

     'Transportation'
    ,'Daily Living'
    ,'Entertainment'
    ,'Subscriptions'
    ,'Home Expenses'
    ,'Health'
    ,'Savings'
    ,'Misc'
    ,'Obligations'
    ,'Charity And Gifts'
]

def transform_g_sheet_array(array:List[List[Any]])->pd.DataFrame:
    if array[0] != SHEET_COLUMNS:
        raise ValueError("Invalid sheet passed.")
    #TODO: add additional arguements
    df = pd.DataFrame(data=array[1:],columns=array[0])

    for col, dtype in SHEET_TYPES.items():
        df[col] = df[col].astype(dtype)

    return df



def make_dataframe()->pd.DataFrame:
    root_path = Path(dirname(realpath(__file__)))
    csv_folder_path = root_path/'..'/'csvs'
 

    for root,dirs,files in os.walk(csv_folder_path):
        dfs = list()
        for file in files:
            if file.endswith('.csv'):
                with open(csv_folder_path/file,mode='r') as f:
                    reader = csv.reader(f)
                    dfs.append(transform_g_sheet_array(array=[row for row in reader]))

    dfs = pd.concat(dfs,axis=0,sort=True).reset_index(drop=True)
    return dfs

def process_dataframe(df:pd.DataFrame)->pd.DataFrame:
    all_dates = pd.date_range(start= df.date.min(),end=df.date.max(),freq='D')
    index = pd.MultiIndex.from_product([all_dates,CATEGORIES],names=['date','category'])

    full_df = pd.DataFrame(index=index).reset_index(drop=False)

    new_df = full_df.merge(df,left_on=['date','category'],right_on=['date','category'],how='left')
    new_df.amount_cents = new_df.amount_cents.replace(np.nan,0)
    new_df.amount = new_df.amount.replace(np.nan,0)

    new_df = new_df.groupby(['date','category'],as_index=False)[['amount_cents']].sum()
    new_df['amount_cents']  = new_df.amount_cents/100
    new_df = new_df.set_index(keys="date")


    plot_df = new_df.groupby([pd.Grouper(freq=freq),'category']).sum().reset_index(drop=False)
    pivot_df = plot_df.pivot(index='date',columns='category',values='amount_cents')

    return pivot_df




df = make_dataframe()
pivot_df = process_dataframe(df=df)

total = pivot_df.sum()
total.name = 'Category'


total = total.to_frame()



st.text("Total")
fig,ax = plt.subplots(1)
bar_1 = ax.bar(x = range(len(total)),height = total.Category,tick_label = total.index.astype(str))
ax.tick_params(axis='x',labelrotation=90)
ax.bar_label(bar_1,label_type='edge')
st.pyplot(fig)
#st.dataframe(total) # removed since we have a graph now


st.text("Total by time")
total_by_time = pivot_df.T.sum().to_frame().rename({0:'Total by time'},axis=1)
#st.dataframe(total_by_time) removed since we have a graph now

fig,ax = plt.subplots(1)
bar_1 = ax.bar(x=range(len(total_by_time)),height=total_by_time['Total by time'],tick_label=total_by_time.index.astype(str))
ax.tick_params(axis='x',labelrotation=90)
ax.bar_label(bar_1,label_type='edge')
st.pyplot(fig)

st.text("Categories by time")
st.dataframe(pivot_df.T)

category = st.selectbox('Category',CATEGORIES)

fig,ax = plt.subplots(1)
bar_1 = ax.bar(x=range(len(pivot_df)),height=pivot_df[category],tick_label=pivot_df.index.astype(str))
ax.tick_params(axis='x',labelrotation=90)
ax.bar_label(bar_1,label_type='edge')
st.pyplot(fig)


