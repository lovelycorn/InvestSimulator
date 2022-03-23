# This module is for simple startegy, just naive and simple one :)
# via https://zhuanlan.zhihu.com/p/158879633
# todo object-oriented transform next part
import data_processor as dp
import time
import os;
# define key values in lifecycle
# initial value
g_table = None
g_deal_size = 0
# init this life cycle
# @code stock code of your choice
# @start the time you enter
# @end the time you leave
# @quantity number of stock
# @expected_rate rate of expected
def init(code, start, end, quantity, expected_rate, deal_size):
    print("-------init start-------")
    global g_table
    g_table = dp.read_by_date(start, end)
    print(g_table.first_valid_index())
    global g_deal_size
    g_deal_size = deal_size
    start_data = g_table.iloc[g_table.first_valid_index()]
    if start_data["开盘价"] == 0:
        print("sorry, you meet a suspended day")
        return
    capital_money = quantity * start_data["收盘价"]
    # dynamic value part, daily settlement
    g_table.at[g_table.first_valid_index(), "持股数"] = quantity
    g_table.at[g_table.first_valid_index(), "每股成本"] = g_table.at[g_table.first_valid_index(), "收盘价"]
    g_table.at[g_table.first_valid_index(), "总成本"] = capital_money
    #amount = float(capital_money) * (1 + (float(start_data["涨跌幅"]) / 100))
    #profit = amount - capital_money
    amount = capital_money
    profit = 0
    g_table.at[g_table.first_valid_index(), "场内资金"] = amount
    g_table.at[g_table.first_valid_index(), "落盘收益"] = 0
    g_table.at[g_table.first_valid_index(), "收益"] = profit # 场内资金 - 总成本
    g_table.at[g_table.first_valid_index(), "总涨幅"] =  profit / capital_money # 总利润 / 总成本
    g_table.at[g_table.first_valid_index(), "买进次数"] = 0
    g_table.at[g_table.first_valid_index(), "卖出次数"] = 0
    g_table.at[g_table.first_valid_index(), "总操作次数"] = 0
    # add my report data column
    up_limit = capital_money * (1 + expected_rate)
    down_limit = capital_money * (1 - expected_rate)
    #g_table["期望上限"] = up_limit
    #g_table["期望下限"] = down_limit
    print(g_table)
    print("-------init end-------")


# do operation at the begining of a day
def do_operate():
    pass

# settlement at the end of a day
def settle_today(table, index):
    # step 1, calculate
    pre_row = table.iloc[index - 1]
    row = table.iloc[index]
    # 
    # step 2, update into table

# make decision using this simple strategy, day by day
def do_with_simple(table, deal_size):
    print("-------do_simple start-------")
    global g_table
    suspended_count = 0
    for index, row in table.iterrows():
        # pass the first line
        if index == 0:
            print("first line, let's go")
            continue
        # pass and copy when suspended day
        if row["收盘价"] == 0:
            suspended_count += 1
            table.at[index, "持股数"] = table.at[pre_index, "持股数"]
            table.at[index, "每股成本"] = table.at[pre_index, "每股成本"]
            table.at[index, "总成本"] = table.at[pre_index, "总成本"]
            table.at[index, "场内资金"] = table.at[pre_index, "场内资金"]
            table.at[index, "落盘收益"] = table.at[pre_index, "落盘收益"]
            table.at[index, "收益"] = table.at[pre_index, "收益"]
            table.at[index, "总涨幅"] =  table.at[pre_index, "总涨幅"]
            table.at[index, "买进次数"] = table.at[pre_index, "买进次数"]
            table.at[index, "卖出次数"] = table.at[pre_index, "卖出次数"]
            table.at[index, "总操作次数"] = table.at[pre_index, "总操作次数"]
            continue
        pre_index = index - 1
        hold_size = table.at[pre_index, "持股数"]
        new_captal = deal_size * ((table.at[index, "开盘价"] + table.at[index, "收盘价"]) / 2)
        # 操作
        if float(table.at[pre_index, "涨跌幅"]) <= -5:
            # 执行买入策略
            table.at[index, "持股数"] = hold_size + deal_size
            table.at[index, "每股成本"] = (table.at[pre_index, "总成本"] + new_captal) / (hold_size + deal_size) # (总成本 + 新买进) / 持股数
            table.at[index, "总成本"] = table.at[pre_index, "总成本"] + new_captal
            table.at[index, "场内资金"] = table.at[pre_index, "场内资金"] + new_captal
            table.at[index, "落盘收益"] = table.at[pre_index, "落盘收益"]
            table.at[index, "收益"] = table.at[pre_index, "收益"]
            table.at[index, "总涨幅"] = table.at[index, "收益"] / table.at[index, "总成本"]
            table.at[index, "买进次数"] = table.at[pre_index, "买进次数"] + 1
            table.at[index, "卖出次数"] = table.at[pre_index, "卖出次数"] 
            table.at[index, "总操作次数"] = table.at[pre_index, "总操作次数"] + 1
        elif float(table.at[pre_index, "涨跌幅"]) >= 5:
            # 执行卖出策略
            table.at[index, "持股数"] = hold_size - deal_size
            table.at[index, "每股成本"] = (table.at[pre_index, "总成本"] - new_captal) / (hold_size - deal_size)
            table.at[index, "总成本"] = table.at[pre_index, "总成本"] - new_captal
            table.at[index, "场内资金"] = table.at[pre_index, "场内资金"] - new_captal
            table.at[index, "落盘收益"] = table.at[pre_index, "落盘收益"] + (new_captal - (table.at[index, "每股成本"] * deal_size))
            table.at[index, "收益"] = table.at[pre_index, "收益"]
            table.at[index, "总涨幅"] = table.at[index, "收益"] / table.at[index, "总成本"]
            table.at[index, "买进次数"] = table.at[pre_index, "买进次数"]
            table.at[index, "卖出次数"] = table.at[pre_index, "卖出次数"] + 1
            table.at[index, "总操作次数"] = table.at[pre_index, "总操作次数"] + 1
        else:
            # 无策略，复制
            table.at[index, "持股数"] = table.at[pre_index, "持股数"]
            table.at[index, "每股成本"] = table.at[pre_index, "每股成本"]
            table.at[index, "总成本"] = table.at[pre_index, "总成本"]
            table.at[index, "场内资金"] = table.at[pre_index, "场内资金"]
            table.at[index, "落盘收益"] = table.at[pre_index, "落盘收益"]
            table.at[index, "收益"] = table.at[pre_index, "收益"]
            table.at[index, "总涨幅"] = table.at[pre_index, "总涨幅"]
            table.at[index, "买进次数"] = table.at[pre_index, "买进次数"]
            table.at[index, "卖出次数"] = table.at[pre_index, "卖出次数"]
            table.at[index, "总操作次数"] = table.at[pre_index, "总操作次数"]
        
        # 结算
        table.at[index, "场内资金"] = table.at[index, "收盘价"] * table.at[index, "持股数"]  # 收盘价 * 持股数
        table.at[index, "收益"] = table.at[index, "场内资金"] - table.at[index, "总成本"] # 场内资金 - 总成本
        table.at[index, "总涨幅"] = table.at[index, "收益"] / table.at[index, "总成本"] # 收益 / 总成本
    print("g table in do with simple")
    print(g_table)
    print("-------do_simple end-------")

# show result for this life cycle
def show_report():
    pass

# save result into .csv files 
def export_result(table):
    # code_date
    path = os.getcwd() + '\\report\\'
    print(time.strftime("%Y%m%d%H%M%S", time.localtime()))
    file_name = time.strftime("%Y%m%d%H%M%S", time.localtime()) + ".csv"
    print(path + file_name)
    # 保存 dataframe
    table.to_csv(path + file_name)


# test init()
print("**********************************************************************")
print("************************simple policy begin *********************************")
print("**********************************************************************")

init(600745, "20210108", "20210225", 15000, 0.3, 100)

# test do_with_simple
do_with_simple(g_table, 100)

# save result into .csv files
export_result(g_table)
print("**********************************************************************")
print("************************simple policy end *********************************")
print("**********************************************************************")