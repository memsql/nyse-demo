from memsql.common import connection_pool
from scipy import stats
import sys, signal, argparse
import matplotlib

# Force matplotlib to not use any Xwindows backend.
import matplotlib.pyplot as plt

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

def plot():
    with pool.connect(*db_args) as c:
        asks_query = "SELECT * FROM ask_quotes WHERE ticker='%s';" % args.ticker
        bids_query = "SELECT * FROM bid_quotes WHERE ticker='%s';" % args.ticker

        a = c.query(asks_query)
        tsa = [getattr(i, 'ts') for i in a]
        apa = [getattr(i, 'ask_price') for i in a]

        b = c.query(bids_query)
        tsb = [getattr(i, 'ts') for i in b]
        apb = [getattr(i, 'bid_price') for i in b]

        plt.plot(tsa, apa, 'ro', label='Ask quotes')
        plt.plot(tsb, apb, 'bo', label='Bid quotes')
        plt.title('Bids and Asks for %s' % args.ticker)
        plt.legend(numpoints=1)

        plt.show()

if __name__ == '__main__':
    print "Press CTRL+C to stop."
    signal.signal(signal.SIGINT, signal_handler)
    plot()
