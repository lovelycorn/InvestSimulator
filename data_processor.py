import pandas as pd
import os;

# read data from .csv file, date in ascending order
def read():
    print(os.getcwd())
    path = os.getcwd() + '\data\\'
    name = '600745_all.csv'
    # Data has chinese, using gbk encoding.
    # Chinese code style: utf-8,gbk,gb2312,gb18030,cp936,big5, try them one by one.
    print(path + name)
    df = pd.read_csv(path + name, encoding='gbk')
    df_reverse = df.reindex(index=df.index[::-1])
    df_result = df_reverse.reset_index(drop=True)
    return(df_result)

# read data from .csv file, date in ascending order, and from start date to end time [start, end]
# for test now, reserved
# todo
def read_by_date(start, end):
    df = read()
    for index, row in df.iterrows():
        print(index)
        print(row["日期"])

df = read()
# for index, row in df.iterrows():
#     print(index)
#     print(row["日期"])