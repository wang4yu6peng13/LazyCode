# -*- coding:utf-8 -*-
import os
import sys
import datetime
from enum import Enum


class StructureType(Enum):
    null = 0
    const_table = 1
    table = 2
    enum = 3


SPACE4 = "    "
TABLE_ID = '<key colName="模板ID" name="id" type="int" range="[%s,%s]" global="true"/>'
TABLE_NAME = '<variable colName="模板名" name="templateName" type="string"/>'
XML_HEAD = '<?xml version="1.0" encoding="utf-8" standalone="no"?>'
XML_FOOT = '%s</namespace>\n</namespace>\n' % (SPACE4)
ID_LEN = 9


NAMESPACE1 = ""
NAMESPACE2 = ""
PATH = ""
STRUCTURE = StructureType.null


def modify_file(file_name):
    with open(file_name, 'r', encoding='utf-8') as f1, open(file_name+".xml", "a", encoding="utf-8") as f2:
        f2.write(make_comment(True))
        for line in f1:
            line = deal_line(line)
            if line != "":
                f2.write(line)
        f2.write(deal_foot())
        f2.write(make_comment(False))


def deal_line(line):
    line = line.lstrip()
    line = remove_comment(line)
    line = namespace_path(line)
    line = deal_table_line(line)
    return line


def remove_comment(line):
    return "" if line.startswith("//") else line


def namespace_path(line):
    if line.startswith("<0"):
        global NAMESPACE1, NAMESPACE2, PATH
        if NAMESPACE1 == "" and NAMESPACE2 == "" and PATH == "":
            strings = line.split()
            if len(strings) < 4:
                raise RuntimeError("<0行缺少参数，需要3个参数")
            NAMESPACE1, NAMESPACE2, PATH = strings[1], strings[2], strings[3]
            return '%s\n<namespace name="%s">\n%s<namespace name="%s">\n%s<path dir="%s"/>\n\n' % (XML_HEAD, NAMESPACE1, SPACE4, NAMESPACE2, SPACE4*2, PATH)
    return line


def deal_table_line(line):
    if STRUCTURE == StructureType.null:
        return table_head(line)
    else:
        return table_line(line)


def table_head(line):
    global STRUCTURE
    if line.startswith("<1"):
        strings = line.split()
        if len(strings) < 3:
            raise RuntimeError("<1行缺少参数，至少需要2个参数")
        STRUCTURE = StructureType.const_table
        return '%s<const_table name="%s" file="%s.xlsx">\n' % (SPACE4*2, strings[1], strings[2])
    if line.startswith("<2"):
        strings = line.split()
        if len(strings) < 4:
            raise RuntimeError("<2行缺少参数，至少需要3个参数")
        STRUCTURE = StructureType.table
        return '%s<table name="%s" file="%s_%s.xlsx">\n%s%s\n%s%s\n\n' % (SPACE4*2, strings[1], strings[3], strings[2], SPACE4*3, table_id(strings[3]), SPACE4*3, TABLE_NAME)
    if line.startswith("<3"):
        strings = line.split()
        if len(strings) < 2:
            raise RuntimeError("<3行缺少参数，至少需要1个参数")
        STRUCTURE = StructureType.enum
        return '%s<enum name="%s" type="int">\n' % (SPACE4*2, strings[1])
    return line


def table_line(line):
    global STRUCTURE
    if line.startswith("1>"):
        STRUCTURE = StructureType.null
        return '%s</const_table>\n\n' % (SPACE4*2)
    if line.startswith("2>"):
        STRUCTURE = StructureType.null
        return '%s</table>\n\n' % (SPACE4*2)
    if line.startswith("3>"):
        STRUCTURE = StructureType.null
        return '%s</enum>\n\n' % (SPACE4*2)
    strings = line.split()
    if len(strings) < 3:
        raise RuntimeError("字段定义缺少参数，至少需要3个参数")
    if STRUCTURE == StructureType.const_table:
        return '%s<variable desc="%s" name="%s" type="%s"%s/>\n' % (SPACE4*3, strings[0], strings[1].upper(), strings[2], ' local="true"' if strings[2] == 'string' else '')
    if STRUCTURE == StructureType.table:
        return '%s<variable colName="%s" name="%s" type="%s"%s/>\n' % (SPACE4*3, strings[0], strings[1], strings[2], ' local="true"' if strings[2] == 'string' else '')
    if STRUCTURE == StructureType.enum:
        return '%s<case value="%s" name="%s" str="%s"/>\n' % (SPACE4*3, strings[0], strings[1].upper(), strings[2])
    return line


def make_comment(is_start):
    return '<!-- ===== %s %s ===== -->\n' % ('START' if is_start else ' END ', datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))


def deal_foot():
    return '' if NAMESPACE1 == "" and NAMESPACE2 == "" and PATH == "" else XML_FOOT


def table_id(id):
    id_len = len(id)
    add_len = ID_LEN - id_len
    if add_len <= 0:
        raise RuntimeError("表的编号位数%d要小于%d" % (id_len, ID_LEN))
    start_id, end_id = '%s%s' % (id, '0'*add_len), '%s%s' % (id, '9'*add_len)
    return TABLE_ID % (start_id, end_id)


if __name__ == '__main__':
    if len(sys.argv) <= 1:
        print("需要参数，参数为文件名")
        os.system('pause')
    else:
        modify_file(sys.argv[1])
