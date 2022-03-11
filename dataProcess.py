import pandas as pd
import os;
print("helllllllo");
print(os.getcwd());
path = os.getcwd() + '\data\\';
name = '600745_all.csv'
# 网易财经拉下来的数据含有中文，使用gbk编码
# 常见的中文编码包括：utf-8,gbk,gb2312,gb18030,cp936,big5等，我们可以逐一试过去，确定之后再修改read_csv()的encoding参数值即可。
#df = pd.read_csv('600745_all.csv', encoding='gbk');
print(path + name);
df = pd.read_csv(path + name, encoding='gbk');
print(df);
