# -*- coding:utf-8 -*-
import sys


def gen_vector_variable(name, max_num, value_type):
    names = ""
    for num in range(int(max_num)):
        names += name + ("0%d," % (num+1))
    res = '<variable name="%s" type="vector" value="%s" size="%s" from="%s"/>' % (
        name+"s", value_type, max_num, names[:-1])
    print(res)


if __name__ == '__main__':
    if len(sys.argv) < 4:
        print("需要3个参数：变量名 最大个数 value类型")
    else:
        gen_vector_variable(sys.argv[1], sys.argv[2], sys.argv[3])
