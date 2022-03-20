# This module is for simple startegy, just naive and simple one :)
# via https://zhuanlan.zhihu.com/p/158879633
# todo object-oriented transform next part
import data_processor as dp
# define key values in lifecycle
# initial value
g_table = None

# init this life cycle
# @code stock code of your choice
# @start the time you enter
# @end the time you leave
# @quantity number of stock
# @expected_rate rate of expected 
def init(code, start, end, quantity, expected_rate, handle):
    print("-------init start-------")
    global g_table
    g_table = dp.read_by_date(start, end)
    print(g_table.first_valid_index())
    start_data = g_table.iloc[g_table.first_valid_index()]
    if start_data["开盘价"] == 0:
        print("sorry, you meet a suspended day")
        return
    capital_money = quantity * start_data["开盘价"]
    # add my report data column
    # static value part
    g_table["初始股价"] = g_table.at[g_table.first_valid_index(), "开盘价"]

    up_limit = capital_money * (1 + expected_rate)
    down_limit = capital_money * (1 - expected_rate)
    g_table["期望上限"] = up_limit
    g_table["期望下限"] = down_limit
    # dynamic value part
    g_table.at[g_table.first_valid_index(), "成本"] = capital_money
    g_table.at[g_table.first_valid_index(), "持股数"] = quantity
    g_table.at[g_table.first_valid_index(), "场内资金"] = capital_money
    g_table.at[g_table.first_valid_index(), "总涨幅"] = 0.00 # 总收益 / 场内资金
    g_table.at[g_table.first_valid_index(), "收益"] = 0
    g_table.at[g_table.first_valid_index(), "买进次数"] = 0
    g_table.at[g_table.first_valid_index(), "卖出次数"] = 0
    g_table.at[g_table.first_valid_index(), "总操作次数"] = 0
    print(g_table)
    print("-------init end-------")

# update data by row
def update_today(table, index):
    # step 1, calculate
    pre_row = table.iloc[index - 1]
    row = table.iloc[index]

    # 
    # step 2, update into table

# make decision using this simple strategy, day by day
def do_with_simple(table):
    print("-------do_simple start-------")
    global g_table
    suspended_count = 0
    pre_index = 0
    today_index = 1
    for index, row in table.iterrows():
        # pass the first line
        if index == 0:
            print("first line, let's go")
            continue
        #case 1, suspended day, pass
        if row["收盘价"] == 0:
            suspended_count += 1
            continue
        #case 2, normal trading day, More than 5% increase
        if float(row["涨跌幅"]) >= 5:
            print("up to 5%, operation sale")
            update_today(table, index)
            continue
        #case 3, normal trading day, Less than 5% increase
        if float(row["涨跌幅"]) <= -5:
            print("down to -5%, operation buy")
            update_today(table, index)
            continue
    print("g table in do with simple")
    print(g_table)
    print("-------do_simple end-------")

# show result for this life cycle
def show_report():
    pass

# test init()
print("**********************************************************************")
print("************************simple policy begin *********************************")
print("**********************************************************************")

init(600745, "19990104", "20220304", 15000, 0.3, 100)

# test do_with_simple
do_with_simple(g_table)

print("**********************************************************************")
print("************************simple policy end *********************************")
print("**********************************************************************")