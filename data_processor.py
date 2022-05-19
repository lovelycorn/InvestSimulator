import pandas as pd
import os;

# read data from .csv file, date in ascending order
def read():
    # for windows
    #path = os.getcwd() + '\data\\'
    # for linux
    path = os.getcwd() + '/data//'
    name = '600745_all.csv'
    # Data has chinese, using gbk encoding.
    # Chinese code style: utf-8,gbk,gb2312,gb18030,cp936,big5, try them one by one.
    # step 1, read file
    df = pd.read_csv(path + name, encoding='gbk')
    # step 2, reverse the index
    df_reverse = df.reindex(index=df.index[::-1])
    df_result = df_reverse.reset_index(drop=True)
    # step 3, remove redundant column
    df_result.drop(["换手率", "成交量", "成交金额", "总市值", "流通市值"], axis=1, inplace=True)
    # step 4, format date as our way
    for index, row in df_result.iterrows():
        df_result.loc[index, "日期"] = row["日期"].replace("-", "")
    return df_result

# read data from .csv file, date in ascending order, and from start date to end time [start, end]
# now start and end should be marketing day and in the .csv file
# todo market day matching
def read_by_date(start, end):
    print("---------------------read_by_date start---------------------------")
    df = read()
    start_index = None
    end_index = None
    date_list = df["日期"]
    # todo
    # head_value = date_list[date_list.first_valid_index()]
    # tail_value = date_list[date_list.last_valid_index()]
    # start_index get backward value
    # end_index get forward value
    # if start < head_value:
    #     start_index = date_list.first_valid_index()
    # if end > tail_value:
    #     end_index = date_list.last_valid_index()
    for index, row in df.iterrows():
        if row["日期"] == start:
            start_index = index
        if row["日期"] == end:
            end_index = index
    df_result = df.iloc[start_index:end_index + 1,:]
    df_result = df_result.reset_index(drop=True)
    print("---------------------read_by_date end---------------------------")
    return df_result