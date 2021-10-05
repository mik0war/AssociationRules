from PyARMViz import datasets, adjacency_graph_plotly
from apriori_python import apriori
from fpgrowth_py import fpgrowth
from efficient_apriori import apriori as efficient_apriori
import PyARMViz

import pandas as pd
import csv

import time

import matplotlib.pyplot as plt


def parse_xlsx(book_root, list_name, column_name):
    sheet = pd.read_excel(pd.ExcelFile(book_root), sheet_name=list_name)

    transactions = []

    for item in sheet[column_name].values.tolist():
        transactions.append(item.split("; "))

    return transactions


def parse_csv(filename):
    transactions = []

    with open(filename) as f_obj:
        item_list = csv.reader(f_obj)
        hour = "09"
        item = set()
        for row in item_list:
            if row[1][:2] == hour:
                item.add(row[3])

            else:
                transactions.append(list(item))
                item = set()
                item.add(row[3])
                hour = row[1][:2]

    return transactions


def apriori_func(transactions, min_support, min_confidence):
    _, rules = apriori(transactions, minSup=min_support, minConf=min_confidence)
    return rules


def efficiency_apriori_func(transactions, min_support, min_confidence):
    _, rules = efficient_apriori(
        transactions, min_support, min_confidence, output_transaction_ids=True)
    return rules


def fpgrowth_func(transactions, min_support, min_confidence):
    _, rules = fpgrowth(transactions, minSupRatio=min_support, minConf=min_confidence)
    return rules


def print_rules(rules, name):
    print(name)
    step = 1
    for rule in rules:
        print(f"{step}. {rule}")
        step += 1
    print('\n')


def print_diagram(names, values):
    plt.bar(names, values)
    plt.show()


def create_rules(func, transactions, min_sup, min_conf):
    start_time = time.time()
    rules = func(transactions, min_sup, min_conf)
    return time.time() - start_time, rules


def main():
    print("1. Тестовые данные;\n"
          "2. Большие данные")
    answer = input()
    transactions = []

    if answer == "1":
        transactions = parse_xlsx(
            book_root="Association_rules.xlsx",
            list_name='Список покупок',
            column_name='Список покупок')
    elif answer == "2":
        transactions = parse_csv("BreadBasket_DMS.csv")

    print("Support:")
    min_support = float(input())
    print("Confidence:")
    min_confidence = float(input())

    rules = [0, 0, 0]
    final_time = [0, 0, 0]
    functions = [apriori_func, efficiency_apriori_func, fpgrowth_func]
    function_names = ["Apriori", "Efficient_apriori", "Fpgrowth"]

    for num in range(0, 3):
        final_time[num], rules[num] = create_rules(
            functions[num], transactions,
            min_support, min_confidence)

    print_diagram(function_names, final_time)

    for num in range(0, 3):
        print_rules(rules[num], name=function_names[num])

    rules1 = datasets.load_shopping_rules()
    PyARMViz.metadata_scatter_plot(rules1)
    # adjacency_graph_plotly(rules[1])


if __name__ == '__main__':
    main()
