import pandas as pd
import os;

# read data from .csv file, date in ascending order
def read():
    path = os.getcwd() + '\data\\'
    name = '600745_all.csv'
    # Data has chinese, using gbk encoding.
    # Chinese code style: utf-8,gbk,gb2312,gb18030,cp936,big5, try them one by one.
    # step 1, read file
    df = pd.read_csv(path + name, encoding='gbk')
    # step 2, reverse the index
    df_reverse = df.reindex(index=df.index[::-1])
    df_result = df_reverse.reset_index(drop=True)
    # step 3, format date as our way
    for index, row in df_result.iterrows():
        df_result.loc[index, "日期"] = row["日期"].replace("-", "")
    print(df_result)
    return(df_result)

# read data from .csv file, date in ascending order, and from start date to end time [start, end]
# for test now, reserved
# todo
def read_by_date(start, end):
    df = read()
    start_index = None
    end_index = None
    for index, row in df.iterrows():
        print(row["日期"])
        if row["日期"] == start:
            start_index = index
        if row["日期"] == end:
            end_index = index
    return df.loc()