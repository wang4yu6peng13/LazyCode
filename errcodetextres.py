# -*- coding:utf-8 -*-
import os
import sys
import datetime
import re


SPACE4 = "    "


def modify_file(file_name):
    with open(file_name, 'r', encoding='utf-8') as f1, open(file_name+".lua", "a", encoding="utf-8") as f2:
        f2.write(make_comment(True))
        for line in f1:
            line = deal_line(line)
            if line != "":
                f2.write(line)
        f2.write(make_comment(False))


def deal_line(line):
    line = line.strip()
    line = get_info(line)
    return line


def get_info(line):
    if '<protocol' in line:
        m = re.search(r'name\s*=\s*"(.*?)"', line)
        if m:
            name = m.group(1)
            return '%s = {\n' % (name)
    if '</protocol>' in line:
        return '},\n\n'
    m = re.search(r'<enum.*value="(.*?)".*/>\s*(.*)', line)
    if m:
        index = m.group(1)
        text = "未知！！！" if m.group(2) == "" else m.group(2)
        return '%s[%s] = "%s",\n' % (SPACE4, index, text)
    return ""


def make_comment(is_start):
    return '<!-- ===== %s %s ===== -->\n' % ('START' if is_start else ' END ', datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))


if __name__ == '__main__':
    if len(sys.argv) <= 1:
        print("需要参数，参数为文件名")
        os.system('pause')
    else:
        modify_file(sys.argv[1])
