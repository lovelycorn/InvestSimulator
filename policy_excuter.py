# This module is for simple startegy, just naive and simple one :)
# via https://zhuanlan.zhihu.com/p/158879633
# todo object-oriented transform next part
import data_processor as dp
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
    capital_money = quantity * start_data["开盘价"]
    # add my report data column
    # static value part
    g_table["初始股价"] = g_table.at[g_table.first_valid_index(), "开盘价"]

    up_limit = capital_money * (1 + expected_rate)
    down_limit = capital_money * (1 - expected_rate)
    g_table["期望上限"] = up_limit
    g_table["期望下限"] = down_limit
    # dynamic value part, daily settlement
    g_table.at[g_table.first_valid_index(), "持股数"] = quantity
    g_table.at[g_table.first_valid_index(), "成本"] = capital_money
    amount = capital_money * (1 + (start_data["涨跌幅"] / 100))
    profit = amount - capital_money
    g_table.at[g_table.first_valid_index(), "场内资金"] = amount
    g_table.at[g_table.first_valid_index(), "收益"] = profit # 场内资金 - 成本
    g_table.at[g_table.first_valid_index(), "总涨幅"] =  profit / capital_money # 总利润 / 总成本
    g_table.at[g_table.first_valid_index(), "操作码"] = 0 # 0--不操作, 1--买进, -1--卖出
    g_table.at[g_table.first_valid_index(), "买进次数"] = 0
    g_table.at[g_table.first_valid_index(), "卖出次数"] = 0
    g_table.at[g_table.first_valid_index(), "总操作次数"] = 0
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
            table.at[index, "成本"] = table.at[pre_index, "成本"] 
            table.at[index, "场内资金"] = table.at[pre_index, "场内资金"]
            table.at[index, "收益"] = table.at[pre_index, "收益"] 
            table.at[index, "总涨幅"] =  table.at[pre_index, "总涨幅"] 
            table.at[index, "买进次数"] = table.at[pre_index, "买进次数"] 
            table.at[index, "卖出次数"] = table.at[pre_index, "卖出次数"] 
            table.at[index, "总操作次数"] = table.at[pre_index, "总操作次数"] 
            table.at[next_index, "操作码"] = table.at[index, "操作码"] 
            continue

        next_index = index + 1
        pre_index = index - 1
        # do_operate()
        if row["操作码"] == 1:
            # 执行买入策略
            table.at[index, "持股数"] = table.at[pre_index, "持股数"] + deal_size
            table.at[index, "成本"] = table.at[pre_index, "成本"] + deal_size * table.at[index, "开盘价"]
            table.at[index, "场内资金"] = table.at[pre_index, "场内资金"] + deal_size * table.at[index, "开盘价"]
            table.at[index, "收益"] = table.at[pre_index, "收益"]
            table.at[index, "总涨幅"] = table.at[index, "收益"] / table.at[index, "成本"]
            table.at[index, "买进次数"] = table.at[pre_index, "买进次数"] + 1
            table.at[index, "卖出次数"] = table.at[pre_index, "卖出次数"] 
            table.at[index, "总操作次数"] = table.at[pre_index, "总操作次数"] + 1
        elif row["操作码"] == -1:
            # 执行卖出策略
            table.at[index, "持股数"] = table.at[pre_index, "持股数"] - deal_size
            table.at[index, "成本"] = table.at[pre_index, "成本"] - deal_size * table.at[index, "开盘价"]
            table.at[index, "场内资金"] = table.at[pre_index, "场内资金"] - deal_size * table.at[index, "开盘价"]
            table.at[index, "收益"] = table.at[pre_index, "收益"]
            table.at[index, "总涨幅"] = table.at[index, "收益"] / table.at[index, "成本"]
            table.at[index, "买进次数"] = table.at[pre_index, "买进次数"]
            table.at[index, "卖出次数"] = table.at[pre_index, "卖出次数"] + 1
            table.at[index, "总操作次数"] = table.at[pre_index, "总操作次数"] + 1
        else:
            # 无策略，复制
            table.at[index, "成本"] = table.at[pre_index, "成本"]
            table.at[index, "持股数"] = table.at[pre_index, "持股数"]
            table.at[index, "场内资金"] = table.at[pre_index, "场内资金"]
            table.at[index, "收益"] = table.at[pre_index, "收益"]
            table.at[index, "总涨幅"] = table.at[pre_index, "总涨幅"]
            table.at[index, "买进次数"] = table.at[pre_index, "买进次数"]
            table.at[index, "卖出次数"] = table.at[pre_index, "卖出次数"]
            table.at[index, "总操作次数"] = table.at[pre_index, "总操作次数"]
        
        # do decision
        #case 1, normal trading day, More than 5% increase
        if float(row["涨跌幅"]) >= 5:
            print("up to 5%, operation sale")
            table.at[next_index, "操作码"] = -1
            continue
        #case 2, normal trading day, Less than 5% increase
        if float(row["涨跌幅"]) <= -5:
            print("down to -5%, operation buy")
            table.at[next_index, "操作码"] = 1
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