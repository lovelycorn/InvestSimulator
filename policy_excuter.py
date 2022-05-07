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
def init(code, start, end, quantity, pool_money, deal_size):
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
    capital_money = quantity * start_data["收盘价"] # 以收盘价买入，总价即买入市值
    # dynamic value part, daily settlement
    g_table.at[g_table.first_valid_index(), "股票市值"] = capital_money
    g_table.at[g_table.first_valid_index(), "结存数量"] = quantity
    g_table.at[g_table.first_valid_index(), "结存成本"] = capital_money   #结存股票成本= ∑股票买入价格*数量- ∑股票卖出成本 ∑股票卖出成本=∑股票卖出时的单位成本*数量
    g_table.at[g_table.first_valid_index(), "单位成本"] = g_table.at[g_table.first_valid_index(), "结存成本"] / g_table.at[g_table.first_valid_index(), "结存数量"]  # 单位成本 = 成本 / 股数
    g_table.at[g_table.first_valid_index(), "股票浮盈亏"] = g_table.at[g_table.first_valid_index(), "股票市值"] - g_table.at[g_table.first_valid_index(), "结存成本"]  # 股票市值 - 结存成本
    g_table.at[g_table.first_valid_index(), "处置收益总额"] = 0 # 处置收益=（处置股票价格 - 单位成本）*交易数量 累加
    g_table.at[g_table.first_valid_index(), "收益总额"] = g_table.at[g_table.first_valid_index(), "处置收益总额"] +  g_table.at[g_table.first_valid_index(), "股票浮盈亏"] # 处置收益总额 + 股票浮盈亏
    g_table.at[g_table.first_valid_index(), "收益率"] =  g_table.at[g_table.first_valid_index(), "股票浮盈亏"] / g_table.at[g_table.first_valid_index(), "结存成本"] # 收益总额/ 结存成本
    g_table.at[g_table.first_valid_index(), "买进次数"] = 0
    g_table.at[g_table.first_valid_index(), "卖出次数"] = 0
    g_table.at[g_table.first_valid_index(), "总操作次数"] = 0
    # add my report data column
    print(g_table)
    print("-------init end-------")

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
            table.at[index, "股票市值"] = table.at[pre_index, "股票市值"]
            table.at[index, "结存数量"] = table.at[pre_index, "结存数量"]
            table.at[index, "结存成本"] = table.at[pre_index, "结存成本"]
            table.at[index, "单位成本"] = table.at[pre_index, "单位成本"]
            table.at[index, "股票浮盈亏"] =  table.at[pre_index, "股票浮盈亏"]
            table.at[index, "处置收益总额"] = table.at[pre_index, "处置收益总额"]
            table.at[index, "收益总额"] = table.at[pre_index, "收益总额"]
            table.at[index, "收益率"] = table.at[pre_index, "收益率"]
            table.at[index, "买进次数"] = table.at[pre_index, "买进次数"]
            table.at[index, "卖出次数"] = table.at[pre_index, "卖出次数"]
            table.at[index, "总操作次数"] = table.at[pre_index, "总操作次数"]
            continue
        # 正常交易日
        pre_index = index - 1
        hold_size = table.at[pre_index, "结存数量"]
        current_price = ((table.at[index, "开盘价"] + table.at[index, "收盘价"]) / 2)
        new_captal = deal_size * current_price
        # 操作
        if float(table.at[pre_index, "涨跌幅"]) <= -5:
            # 执行买入策略
            table.at[index, "结存数量"] = hold_size + deal_size
            table.at[index, "股票市值"] = table.at[index, "结存数量"] * current_price # 股票现价 * 结存数量
            table.at[index, "结存成本"] = table.at[pre_index, "结存成本"] + deal_size * current_price #结存股票成本= ∑股票买入价格*数量- ∑股票卖出成本  ∑股票卖出成本=∑股票卖出时的单位成本*数量
            table.at[index, "单位成本"] = table.at[index, "结存成本"] / table.at[index, "结存数量"] # 单位成本 = 结存成本 / 结存数量
            table.at[index, "股票浮盈亏"] = table.at[index, "股票市值"] - table.at[index, "结存成本"]  # 股票市值 - 结存成本
            table.at[index, "处置收益总额"] = table.at[pre_index, "处置收益总额"] + 0 # 买入操作无处置收益
            table.at[index, "收益总额"] = table.at[index, "处置收益总额"] + table.at[index, "股票浮盈亏"]  # 处置收益总额 + 股票浮盈亏
            table.at[index, "收益率"] = table.at[index, "收益总额"] / table.at[index, "结存成本"] # 收益总额/ 结存成本
            table.at[index, "买进次数"] = table.at[pre_index, "买进次数"] + 1
            table.at[index, "卖出次数"] = table.at[pre_index, "卖出次数"] 
            table.at[index, "总操作次数"] = table.at[pre_index, "总操作次数"] + 1
        elif float(table.at[pre_index, "涨跌幅"]) >= 5:
            # 执行卖出策略
            table.at[index, "结存数量"] = hold_size - deal_size
            table.at[index, "股票市值"] = table.at[index, "结存数量"] * current_price # 股票现价 * 结存数量
            table.at[index, "结存成本"] = table.at[pre_index, "结存成本"] - table.at[pre_index, "单位成本"] * deal_size # 结存股票成本= ∑股票买入价格*数量- ∑股票卖出成本  ∑股票卖出成本=∑股票卖出时的单位成本*数量
            table.at[index, "单位成本"] = table.at[index, "结存成本"] / table.at[index, "结存数量"] # 单位成本 = 结存成本 / 结存数量
            table.at[index, "股票浮盈亏"] = table.at[index, "股票市值"] - table.at[index, "结存成本"]  # 股票市值 - 结存成本
            table.at[index, "处置收益总额"] = table.at[pre_index, "处置收益总额"] + (current_price - table.at[pre_index, "单位成本"])*deal_size # 处置收益= 处置收益 +（处置股票价格 - 单位成本）*交易数量
            table.at[index, "收益总额"] = table.at[index, "处置收益总额"] + table.at[index, "股票浮盈亏"]  # 处置收益总额 + 股票浮盈亏
            table.at[index, "收益率"] = table.at[index, "收益总额"] / table.at[index, "结存成本"] # 收益总额/ 结存成本            
            table.at[index, "买进次数"] = table.at[pre_index, "买进次数"]
            table.at[index, "卖出次数"] = table.at[pre_index, "卖出次数"] + 1 
            table.at[index, "总操作次数"] = table.at[pre_index, "总操作次数"] + 1
        else:
            # 无策略，复制
            table.at[index, "结存数量"] = table.at[pre_index, "结存数量"]
            table.at[index, "结存成本"] = table.at[pre_index, "结存成本"]
            table.at[index, "单位成本"] = table.at[pre_index, "单位成本"]
            table.at[index, "处置收益总额"] = table.at[pre_index, "处置收益总额"]
            table.at[index, "买进次数"] = table.at[pre_index, "买进次数"]
            table.at[index, "卖出次数"] = table.at[pre_index, "卖出次数"]
            table.at[index, "总操作次数"] = table.at[pre_index, "总操作次数"]
        
        # 收盘结算
        table.at[index, "股票市值"] = table.at[index, "结存数量"] * table.at[index, "收盘价"] # 股票现价 * 结存数量
        table.at[index, "股票浮盈亏"] = table.at[index, "股票市值"] - table.at[index, "结存成本"]  # 股票市值 - 结存成本
        table.at[index, "收益总额"] = table.at[index, "处置收益总额"] + table.at[index, "股票浮盈亏"]  # 处置收益总额 + 股票浮盈亏
        table.at[index, "收益率"] = table.at[index, "收益总额"] / table.at[index, "结存成本"] # 收益总额/ 结存成本

    print("g table in do with simple")
    print(g_table)
    print("-------do_simple end-------")

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

init(600745, "20210108", "20210225", 1000, 0.3, 100)

# test do_with_simple
do_with_simple(g_table, 100)

# save result into .csv files
export_result(g_table)
print("**********************************************************************")
print("************************simple policy end *********************************")
print("**********************************************************************")