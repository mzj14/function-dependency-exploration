from itertools import combinations
from random import sample
from collections import defaultdict

import sys, getopt

def readTableFromFile(file_name):
    with open(file_name, 'r') as f:
        raw_str = f.read().strip()
    rows_str = raw_str.split('\n')
    print('rows_str = ', len(rows_str))
    print('end = ', rows_str[-1])
    table = []
    for row_str in rows_str:
        row = row_str.split(',')
        table.append(row)
    return table, len(table), len(table[0])

def slugify(elements):
    return ' '.join(map(str, sorted(elements)))

def computeRHS(comb, rhs):
    comb_copy = comb.copy()
    result = entire_attributes.copy()
    for attribute_id in comb:
        comb_copy.remove(attribute_id)
        comb_str = slugify(comb_copy)
        if comb_str in rhs:
            result &= rhs[comb_str]
        else:
            return set(), False
        comb_copy.add(attribute_id)
    return result, True

def computePartition(comb, partition):
    result = list()
    num1, num2 = sample(comb, 2)
    partition_1 = partition[slugify(comb - {num1})]
    partition_2 = partition[slugify(comb - {num2})]
    for group_1 in partition_1:
        temp = group_1.copy()
        for group_2 in partition_2:
            k = group_1 & group_2
            if k:
                temp -= k
                result.append(k)
        if temp:
            result.append(temp)
    return result

def chainValue(row, attribute_ids):
    result = []
    for attribute_id in sorted(attribute_ids):
        result.append(row[attribute_id])
    return ' '.join(result)

def groupByAttribute(table, attribute_ids):
    result = defaultdict(set)
    for i in range(len(table)):
        attribute_value = chainValue(table[i], attribute_ids)
        b = result[attribute_value]
        b.add(i)
    return len(result)

def testValidity(comb, e, p):
    return p[slugify(comb)] == p[slugify(comb - {e})]

def recordDependency(comb, e):
    return [x + 1 for x in sorted(comb - {e})], [e + 1]

def outputDependency(a):
    print("total dependency num: ", len(a))
    for x in a:
        print(slugify(x[0]), ' -> ', slugify(x[1]))

def showUsage():
    print('''
          Options and arguments:
          -h                      : show option message
          -i  name                : specify the file which stores the input data
          -o  name                : specify the file which the function dependencies will be written to
          --breaker=character     : specify the breaker which separate each column in input file
          Usage example:
          python <name>.py -i input.txt -o output.txt --breaker=,
          ''')

if __name__ == "__main__":
    table, row_count, column_count = readTableFromFile('test_data.txt')

    # print(table)
    print('row_count = ', row_count)
    print('column_count = ', column_count)

    rhs = dict()
    partition = dict()
    entire_attributes = set(range(column_count))

    # init RHS for level 1
    for attribute_id in range(column_count):
        rhs[slugify({attribute_id})] = entire_attributes.copy()

    # init partition for level 1
    for attribute_id in range(column_count):
        partition[slugify({attribute_id})] = groupByAttribute(table, {attribute_id})
        # print(partition[slugify({attribute_id})])

    # level-wise algorithm
    ans = list()
    for size in range(2, column_count + 1):
        print('--------------------------------------------')
        print('size = ', size)
        # enumerate all subsets with specific size
        combs = map(set, list(combinations(range(column_count), size)))
        for comb in combs:
            print(comb)
            rhs_result, belonged = computeRHS(comb, rhs)
            # print('belonged = ', belonged)
            if not belonged or not rhs_result:
                continue
            candidates = comb & rhs_result
            # print('candidates = ', candidates)
            # partition_result = computePartition(comb, partition)
            partition_result = groupByAttribute(table, comb)
            partition[slugify(comb)] = partition_result
            valid = False
            for e in candidates:
                if testValidity(comb, e, partition):
                    ans.append(recordDependency(comb, e))
                    print(comb, e)
                    rhs_result.remove(e)
                    valid = True
            if valid:
                rhs_result -= entire_attributes - comb
            if rhs_result:
                rhs[slugify(comb)] = rhs_result
    ans.sort()
    outputDependency(ans)