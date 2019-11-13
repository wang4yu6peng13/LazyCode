# -*- coding:utf-8 -*-
import os
import re
import sys
import datetime

SPACE4 = "    "

NAMESPACE1 = ""
NAMESPACE2 = ""


def modify_file(file_name):
    with open(file_name, 'r', encoding='utf-8') as f1, open(file_name+".xml", "a", encoding="utf-8") as f2:
        f2.write(make_comment(True))
        for line in f1:
            line = deal_line(line)
            f2.write(line)
        f2.write(make_comment(False))


def deal_line(line):
    line = line.replace("\t", SPACE4)
    get_namespaces(line)
    line = remove_line(line)
    line = deal_table_line(line)
    line = deal_enum_line(line)
    line = remove_tag(line)
    line = deal_variable_line(line)
    return line


def get_namespaces(line):
    if "<namespace" in line:
        global NAMESPACE1, NAMESPACE2
        m = re.search(r'namespace\s+name\s*=\s*"(.*?)"', line)
        if m:
            if NAMESPACE1 == "":
                NAMESPACE1 = m.group(1)
            elif NAMESPACE1 != "" and NAMESPACE2 == "":
                NAMESPACE2 = m.group(1)


def remove_line(line):
    if "<path" in line or 'colName="模板名' in line:
        return ""
    return line


def deal_table_line(line):
    if "<table" in line or "<const_table" in line:
        m = re.search(r'file\s*=\s*"(.*?)"', line)
        if m:
            xlsx_name = m.group(1)
            comments = '%s<!-- %s -->\n' % (SPACE4*2, xlsx_name)
        m = re.search(r'name\s*=\s*"(.*?)"', line)
        if m:
            name = m.group(1)
            line = comments + '%s<%stable export="" name="%s" from="mzm.gsp.%s.%s.%s">\n' % (
                SPACE4*2, "const_" if "const_" in line else "", name, NAMESPACE1, NAMESPACE2, name)
    return line


def deal_enum_line(line):
    if "<enum" in line:
        line = line.replace("enum", 'enum export="all"')
    return line


def remove_tag(line):
    if "ref=" in line:
        m = re.compile(r'\s+ref\s*=".*?"')
        line = re.sub(m, "", line)
    if "range=" in line:
        m = re.compile(r'\s+range\s*=".*?"')
        line = re.sub(m, "", line)
    if "canNull=" in line:
        m = re.compile(r'\s+canNull\s*=".*?"')
        line = re.sub(m, "", line)
    if "local=" in line:
        m = re.compile(r'\s+local\s*=".*?"')
        line = re.sub(m, "", line)
    if "global=" in line:
        m = re.compile(r'\s+global\s*=".*?"')
        line = re.sub(m, "", line)
    if "default=" in line:
        m = re.compile(r'\s+default\s*=".*?"')
        line = re.sub(m, "", line)
    return line


def deal_variable_line(line):
    if "type=" in line:
        m = re.compile(r'type\s*=\s*".+?\..+?\..+?\..+?\..+"')
        line = re.sub(m, 'type="int"', line)
    return line


def make_comment(is_start):
    return '\n<!-- ===== %s %s ===== -->\n' % ('START' if is_start else ' END ', datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))


if __name__ == '__main__':
    if len(sys.argv) <= 1:
        print("需要参数，参数为文件名")
        os.system('pause')
    else:
        modify_file(sys.argv[1])
