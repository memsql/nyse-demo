from scipy import stats
import numpy as np
from memsql.common import database
import time, sys, signal
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('--ticker', help='specify the database containing ask_quotes and bid_quotes tables', default='BLAH')
args = parser.parse_args()
ticker = args.ticker

print "Press ctrl+c to stop..."

def signal_handler(signal, frame):
    print '\nExiting...'
    sys.exit(0)
    
signal.signal(signal.SIGINT, signal_handler)

fails = 0

while True:
    with database.connect(host="127.0.0.1", port=3306, user = "root", database = "stocks") as conn:
        a = conn.query('SELECT ask_price, timestamp FROM ask_view JOIN (SELECT Avg(ask_price) avg_ask FROM ask_view WHERE ticker = "{0}") avg JOIN (SELECT Std(ask_price) std_ask FROM ask_view WHERE ticker = "{0}") std where ticker = "{0}" AND abs(ask_price - avg.avg_ask) < (std.std_ask);'.format(ticker)) 
        x = [a[i]['timestamp'] for i in range(len(a)-1)]
        y = [a[i]['ask_price'] for i in range(len(a)-1)]
    
    try:
        slope, intercept, r_value, p_value, std_err = stats.linregress(x,y)
        fails = 0
        print '\nTicker: ' + ticker
        print 'Time: ' + str(time.time())
        print 'Slope: ' + str(slope)
        print 'R squared: ' + str(r_value**2)
        print 'Standard error: ' + str(std_err)
        print '\n-------------------------------'
    except ValueError:
        fails += 1
        print 'The query returned an invalid value, probably because `ask_view` is empty.'
        if (fails > 9):
            print "Too many fails. Exiting..."
            sys.exit(0)
