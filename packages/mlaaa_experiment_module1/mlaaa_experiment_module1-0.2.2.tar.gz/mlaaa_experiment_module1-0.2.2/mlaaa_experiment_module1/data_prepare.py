import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import seaborn as sns
import plotly.express as px
import calendar
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import seaborn as sns
import plotly.express as px


def test_data(train_df,test_df):
  """
    Preparing the dataframes for Training and Testing 
  """
  test_col=train_df.iloc[:,0:6]
  df=pd.concat([test_col,test_df],axis=1)
  col=["id","dept_id","state_id","cat_id"]
  train_df=train_df.drop(columns=col)
  test_df=df.drop(columns=col)
  return train_df,test_df

def melt_df(df):
    """
    Melting the "d" column to have a single column.

    """
    l=['item_id','store_id']
    df= pd.melt(df, id_vars=l, var_name='d',value_name='sold').dropna()
    return df

def merge_df(df,cal,items):
  """
    Merging the data frame to develop a final training set and testing test.
  """
  merge1=pd.merge(df,cal,on="d",how='left')
  merge2 =pd.merge(merge1,items,on=["store_id","item_id","wm_yr_wk"],how='left')
  df=merge2.drop(columns="d")
  return df

def make_train(df):
  """
    Building a Target column and returns a final Training dataset
  """
  df=df.dropna()
  df=df.reset_index(drop=True)
  df['revenue'] = df['sold']*df['sell_price']
  df=df.drop(columns=["sell_price","sold","wm_yr_wk"]).reset_index(drop=True)
  # df.to_csv("train_df.csv",index=False)
  return df

def make_test(df):
  """
    Building a Target column and returns a final Testing dataset

  """
  df=df.dropna()
  df=df.reset_index(drop=True)
  df['revenue'] = df['sold']*df['sell_price']
  df=df.drop(columns=["sell_price","sold","wm_yr_wk"]).reset_index(drop=True)
  # df.to_csv("test_df.csv",index=False)
  return df

def make_data_train_test(train_df,test_df,cal,items):
  """
    Function that will perform all the above functions to develop a merged dataset.

    returns: Training and Testing Data
  """
  print("Starting with the Prediction Analysis........")
  train_df,test_df=test_data(train_df,test_df)
  print("\nPreparation of Testing Dataset using the indices of Training Dataset")
  train_melt=melt_df(train_df)
  print("Melting d column for Training Dataset done...")
  test_melt=melt_df(test_df)
  print("Melting d column for Testing Dataset done...")
  train_df=merge_df(train_melt,cal,items)
  print("Merging the Data for Training Data Done")
  test_df=merge_df(test_melt,cal,items)
  print("Merging the Data for Testing Data Done")
  train_df=make_train(train_df)
  print("Preparation for Training Dataset with Target Variable done")
  test_df=make_test(test_df)
  print("Preparation for Testing Dataset with Target Variable done")
  return train_df,test_df

