# -*- coding:utf-8 -*-
import os
import sys
import datetime


SPACE4 = ' ' * 4
STATUS_ENUM = '<enum value="" name="%s" description="%s"/>\n'


def modify_file(file_name):
    with open(file_name, 'r', encoding='utf-8') as f1, open(file_name+".xml", "a", encoding="utf-8") as f2:
        f2.write(make_comment(True))
        list = []
        total_len = deal_line_status_enum(list, f1, f2)
        f2.write('\n')
        deal_line_status_cfg(list, f2)
        f2.write('\n')
        deal_line_status_cfg_state(list, f2, total_len)
        f2.write(make_comment(False))


def deal_line_status_enum(list, f1, f2):
    total_len = 0
    for line in f1:
        line = line.strip()
        name, description = line.split()
        total_len = max(total_len, len(name))
        new_line = STATUS_ENUM % (name, description)
        f2.write(new_line)
        list.append(line)
    return total_len


def deal_line_status_cfg(list, f2):
    for line in list:
        name, description = line.split()
        new_line = '<status name="%s" comment="%s" toClient="true">\n%s<disallow%s>\n</status>\n' % (
            name, description, SPACE4, '/' if name.startswith('ACTION') else '>\n%s</disallow' % (SPACE4))
        f2.write(new_line)


def deal_line_status_cfg_state(list, f2, total_len):
    for line in list:
        name, description = line.split()
        new_line = '<state name="%s"%stip=""/> %s\n' % (
            name, ' ' * (total_len + 1 - len(name)), '不能'+description)
        f2.write(new_line)


def make_comment(is_start):
    return '<!-- ===== %s %s ===== -->\n' % ('START' if is_start else ' END ', datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))


if __name__ == '__main__':
    if len(sys.argv) <= 1:
        print("需要参数，参数为文件名")
        os.system('pause')
    else:
        modify_file(sys.argv[1])
