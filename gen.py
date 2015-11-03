#!/usr/bin/env python

from memsql.common import connection_pool
from threading import Thread, Event
from collections import namedtuple
import sys, time, random, signal, itertools, argparse, Queue

parser = argparse.ArgumentParser()
parser.add_argument('--db', help='Specify the database.', default='stocks')
parser.add_argument('--host', help='Specify the database host.', type=str, default='127.0.0.1')
parser.add_argument('--user', help='Specify the database user.', type=str, default='root')
parser.add_argument('--port', help='Specify the database port.', type=int, default=3306)
parser.add_argument('--password', help='Specify the database user password.', default='')
parser.add_argument('--iters', help='Number of iterations for the generator.', type=int, default=100)
parser.add_argument('--batch', help='The insert batch size.', type=int, default=250)
parser.add_argument('--base', help='The base value of each ticker.', type=int, default=5000)
parser.add_argument('--max', help='Maximum price change.', type=int, default=5)
args = parser.parse_args()

SECS_IN_NYSE_DAY = 23400
TICKERS = [
    'BLAH', 'DUH', 'UM', 'UHH', 'ERR',
    'WUT', 'LOL', 'DERP', 'UP', 'DOWN'
]

EXCHANGES = [
    'NYS', 'LON', 'NASDAQ', 'TYO', 'FRA'
]

inserts = Queue.Queue()
pool = connection_pool.ConnectionPool()
db_args = [args.host, args.port, args.user, args.password, args.db]
done = Event()
Quote = namedtuple("Quote", ("ticker", "ts", "price", "size", "exchange"))

def _make_query(quotes, table):
    return ('INSERT INTO %s VALUE' % table) + \
        (','.join(['("%s", %f, %d, %d, "%s")'] * args.batch) % tuple(quotes))

def _insert_worker():
    while not done.is_set():
        with pool.connect(*db_args) as c:
            ins = inserts.get()
            c.execute(ins)

def _signal_handler(signal, frame):
    print '\nExiting...'
    done.set()
    sys.exit(0)


if __name__ == '__main__':
    workers = [Thread(target=_insert_worker) for _ in range(5)]

    signal.signal(signal.SIGINT, _signal_handler)
    print "Press CTRL+C to stop generator."

    print '\nStarting...'
    for w in workers:
        w.start()

    bases = {
        ticker: args.base for ticker in TICKERS
    }

    start_time = time.time()

    for i in range(args.iters):
        for ticker, price in bases.items():
            asks = []
            bids = []

            for j in range(args.batch):
                t = time.time() * 100000
                log = random.lognormvariate(1, .25)
                s = random.randrange(1, 100, 1)
                x = EXCHANGES[i % 5]
                asks.append(
                    Quote(ticker=ticker, ts=t, price=(price + log), size=s, exchange=x)
                )
                bids.append(
                    Quote(ticker=ticker, ts=t, price=(price - log), size=s, exchange=x)
                )

            if i % 5 == 0:
                if ticker == 'UP':
                    price = price + 5
                elif ticker == 'DOWN':
                    price = price - 5
                else:
                    price = price + random.randint(-1 * args.max, args.max)
                bases[ticker] = price

            inserts.put(_make_query(list(itertools.chain(*asks)), 'ask_quotes'))
            inserts.put(_make_query(list(itertools.chain(*bids)), 'bid_quotes'))

    total_time = time.time() - start_time

    done.set()
    for w in workers:
        w.join()

    with pool.connect(*db_args) as c:
        num_asks = c.query('''
            SELECT COUNT(*) AS c
            FROM ask_quotes
            WHERE ts > %d;
        ''' % start_time)[0].c

        num_bids = c.query('''
            SELECT COUNT(*) AS c
            FROM bid_quotes
            WHERE ts > %d;
        ''' % start_time)[0].c

        total_inserts = float(num_asks + num_bids)

        print "\nGenerated and inserted %d records in %d seconds." % (total_inserts, total_time)
        print "%s quotes/second" % str(total_inserts / total_time)
        print "%s quotes/NYSE trading day" % ((total_inserts / total_time) * SECS_IN_NYSE_DAY)

    pool.close()
