# This module is for simple startegy, just naive and simple one :)
# via https://zhuanlan.zhihu.com/p/158879633
import data_processor as dp

# define key values in lifecycle
# initial value
stock_code = 000000
start_time = 20000101 #YYYYMMDD
end_time = 20500101 #YYYYMMDD
capital_money = 0.0 #start-up captial
data = None

# dynamic value
date = None
price = 0.0
position = 0.0
amount = 0.0
profit = 0.0

# init this life cycle
def init(code, start, end, quantity):
    print("-------------------------init start-------------------------")
    global stock_code
    stock_code = code
    global data
    data = dp.read_by_date(start, end)
    global start_time
    start_time = start
    global date
    date = start
    global end_time
    end_time = end
    for index, row in data.iterrows():
        if row["日期"] == start:
            print("find this point")
            print(row)
            global capital_money
            capital_money = quantity * row["收盘价"]
            global amount
            amount = quantity * row["收盘价"]
    print("-------------------------init end-------------------------")

# make decision using this simple strategy, day by day
def do_with_simple(data):
    print("-------------------------do_simple start-------------------------")
    suspended_count = 0
    for index, row in data.iterrows():
        # step 1, load trading day and previous trading day
        if row["收盘价"] == 0:
            suspended_count += 1
            continue
        # step 2, update dynamic price

        # step 3, calculate amount and profit
    print(count)
    print("-------------------------do_simple end-------------------------")

# show result for this life cycle
def show_report():
    pass

# test init()
init(600745, "19990104", "20220304", 100)

# test do_with_simple
do_with_simple(data)