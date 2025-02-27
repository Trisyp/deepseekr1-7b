import argparse
import os
# 1.创建一个ArgumentParser类的对象
parser = argparse.ArgumentParser(description="path")  # description里面的字符串内容可以随便填，描述对象是用来干什么的

# 2.一系列的add_argument()
home_dir = os.getcwd()
parser.add_argument("--root_dir", type=str, default=home_dir)

# 3.调用对象的parse_args()方法
args = parser.parse_args()

# 4.输出对象的属性
root_dir = args.root_dir
