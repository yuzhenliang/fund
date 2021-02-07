import csv
import os
import re
import pandas as pd
from functools import reduce
from pandas.core.frame import DataFrame


def removeBom(file):
    '''移除UTF-8文件的BOM字节'''
    BOM = b'\xef\xbb\xbf'
    existBom = lambda s: True if s == BOM else False

    f = open(file, 'rb')
    if existBom(f.read(3)):
        fbody = f.read()
        with open(file, 'wb') as f:
            f.write(fbody)


def csv_to_df(filename):
    with open(filename, encoding='utf-8') as f:
        reader = csv.reader(f)
        rows = [row for row in reader]

    result = pd.DataFrame(rows[1:], columns=rows[0])
    return result


if __name__ == '__main__':
    path = './fund_bill'
    os.chdir(path)
    dfs = []
    i = 0
    j = 0
    bill_names = os.listdir('.')
    for bill in bill_names:
        if re.match(".*csv$", str(bill)):
            removeBom(bill)
            locals()['df' + str(i)] = csv_to_df(bill)
            dfs.append(locals()['df' + str(i)])
            i = i + 1
    summary = reduce(lambda left, right: pd.merge(left, right, how='outer'), dfs)
    summary.to_csv('summary.csv', index=False)
