#!/bin/python

import matplotlib.pyplot as plt
from memsql.common import database
import sys
from scipy import stats
import numpy as np
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('--ticker', help='specify the database containing ask_quotes and bid_quotes tables', default='BLAH')
args = parser.parse_args()
ticker = args.ticker

def make_list(result, attribute):
    arr = []
    for r in result:
        arr.append(getattr(r, attribute))
    return arr

with database.connect(host="127.0.0.1", port=3306, user = "root", database = "stocks") as conn:
    asks_query = "select * from ask_quotes where ticker='%s'" % ticker
    bids_query = "select * from bid_quotes where ticker='%s'" % ticker

a = conn.query(asks_query) 
b = conn.query(bids_query)
tsa = make_list(a, 'timestamp')
apa = make_list(a, 'ask_price')
tsb = make_list(b, 'timestamp')
apb = make_list(b, 'bid_price')
plt.plot(tsa, apa, 'ro', label='Ask quotes')
plt.plot(tsb, apb, 'bo', label='Bid quotes')
plt.title('Bids and Asks for %s' % ticker)
plt.legend()

plt.show()
