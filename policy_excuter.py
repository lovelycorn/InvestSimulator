# This module is for simple startegy, just naive and simple one :)
# via https://zhuanlan.zhihu.com/p/158879633
import data_processor as dp

# define key values in lifecycle
# initial value
stock_code = 000000
start_time = 20000101 #YYYYMMDD
end_time = 20500101 #YYYYMMDD
capital_money = 0.0
data = dp.read()

# dynamic value
value = 0.0
position = 0.0
amount = 0.0
profit = 0.0

# init this life cycle
def init():
    pass

# make decision using this simple strategy, day by day
def do_simple(data):
    startDate = "2000-1-1"
    endDate = "2050-1-1"
    initialCost = 0.00
    print("this is simple")

# show result for this life cycle
def show_report():
    pass

init()
do_simple(data)