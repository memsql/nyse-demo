from scipy import stats
from memsql.common import connection_pool
import time, sys, signal, argparse

TICKERS = [
    'BLAH', 'DUH', 'UM', 'UHH', 'ERR',
    'WUT', 'LOL', 'DERP', 'UP', 'DOWN'
]

parser = argparse.ArgumentParser()
parser.add_argument('--ticker', help='Specify the ticker to investigate.', choices=TICKERS, default=TICKERS[0])
parser.add_argument('--db', help='Specify the database.', default='stocks')
parser.add_argument('--host', help='Specify the database host.', type=str, default='127.0.0.1')
parser.add_argument('--user', help='Specify the database user.', type=str, default='root')
parser.add_argument('--port', help='Specify the database port.', type=int, default=3306)
parser.add_argument('--password', help='Specify the database user password.', default='')
args = parser.parse_args()

pool = connection_pool.ConnectionPool()
db_args = [args.host, args.port, args.user, args.password, args.db]


def signal_handler(signal, frame):
    print '\nExiting...'
    sys.exit(0)


def regress():
    unsuccessful_tries = 0

    while True:
        with pool.connect(*db_args) as c:
            a = c.query('''
    SELECT ask_price, ts
    FROM (
        SELECT * 
        FROM ask_quotes
        ORDER BY ts DESC LIMIT 10000) window
    JOIN (
        SELECT AVG(ask_price) avg_ask
        FROM ask_quotes WHERE ticker = "{0}") avg
    JOIN (
            SELECT STD(ask_price) std_ask
            FROM ask_quotes
            WHERE ticker = "{0}") std
    WHERE ticker="{0}"
        AND abs(ask_price - avg.avg_ask) < (std.std_ask);
    '''.format(args.ticker))
            x = [a[i]['ts'] for i in range(len(a)-1)]
            y = [a[i]['ask_price'] for i in range(len(a)-1)]

        if len(a) > 0:
            slope, intercept, r_value, p_value, std_err = stats.linregress(x,y)
            print '\nTicker: %s' % args.ticker
            print 'Time: %s' % time.time()
            print 'Slope: %s' % slope
            print 'R squared: %s' % r_value**2
            print 'Standard error: %s' % std_err
            print '\n-------------------------------'
        else:
            unsuccessful_tries += 1
            if (unsuccessful_tries > 9):
                print "Too many unsuccessful tries. Make sure gen.py is running. Exiting."
                sys.exit(0)


if __name__ == '__main__':
    print "Press CTRL+C to stop."
    signal.signal(signal.SIGINT, signal_handler)
    regress()
