from memsql.common import database, connection_pool
from threading import Thread, Event
from collections import namedtuple
import sys, time, random, signal, itertools, argparse, Queue

parser = argparse.ArgumentParser()
parser.add_argument('--db', help='specify the database containing ask_quotes and bid_quotes tables', default='stocks')
parser.add_argument('--num_iters', help='number of iterations for the generator', type=int, default=100)
parser.add_argument('--batch', help='blah', type=int, default=100)
args = parser.parse_args()
db = args.db
iters = args.num_iters

tickers = ['BLAH','DUH','UM','UHH','ERR','WUT','LOL','DERP','UP','DOWN']
exchanges = ['NYS','LON','NASDAQ','TYO','FRA']
BATCH = args.batch
MAX_PRICE_CHANGE = 1
BASE_VALUE = 5000

inserts = Queue.Queue()
Quote = namedtuple("Quote", ("ticker", "timestamp", "price", "size", "exchange"))

bases = { ticker: BASE_VALUE for ticker in tickers }

pool = connection_pool.ConnectionPool()

done = Event()

def _make_query(quotes, table):
    return ('insert into %s value' % table) + (','.join( ['("%s", %f, %d, %d, "%s")'] * BATCH ) % tuple(quotes))

def insert_worker():
    with pool.connect('127.0.0.1', 3306, 'root', '', db) as conn:
        while not done.is_set():
            ins = inserts.get()
            conn.execute(ins)

def cleanup(workers):
    print '\nExiting...'
    global done
    done.set()
    [w.join() for w in workers]

def signal_handler(signal, frame):
    print '\nExiting...'
    global done
    done.set()
    sys.exit(0)

if __name__ == '__main__':
    try:
        with pool.connect('127.0.0.1', 3306, 'root', '', db) as conn:
            pass
    except connection_pool.PoolConnectionException as e:
        print "Failed to connect to db: %s" % e
        sys.exit(1)

    workers = [ Thread(target=insert_worker) for _ in range(5) ]
    [ w.start() for w in workers ]

    signal.signal(signal.SIGINT, signal_handler)
    print "Press ctrl+c to stop generator"

    start_time = time.time()
    for i in range(iters):
        for ticker, price in bases.items():
            asks = []
            bids = []
            for j in range(BATCH):
                t = time.time() * 100000
                log = random.lognormvariate(1, .25)
                s = random.randrange(1, 100, 1)
                ask = Quote(ticker=ticker, timestamp=t, price=(price + log), size=s, exchange=exchanges[i%5])
                bid = Quote(ticker=ticker, timestamp=t, price=(price - log), size=s, exchange=exchanges[i%5])
                asks.append(ask)
                bids.append(bid)

            if i % 5 == 0:
                if ticker == 'UP':
                    price = price + 5
                elif ticker == 'DOWN':
                    price = price - 5
                else:
                    price = price + random.randint(-1 * MAX_PRICE_CHANGE, MAX_PRICE_CHANGE)
                bases[ticker] = price

            inserts.put(_make_query(list(itertools.chain(*asks)), 'ask_quotes'))
            inserts.put(_make_query(list(itertools.chain(*bids)), 'bid_quotes'))

    total_time = time.time() - start_time
    cleanup(workers)

    with pool.connect('127.0.0.1', 3306, 'root', '', db) as conn:
        num_asks = conn.query('select count(*) as c from ask_quotes where timestamp > %d;' % (start_time * 100000))[0].c
        num_bids = conn.query('select count(*) as c from bid_quotes where timestamp > %d;' % (start_time * 100000))[0].c
    total_inserts = num_asks + num_bids
    print "\nGenerated and inserted " + str(total_inserts) + " records in " + str(total_time) + " seconds."
    print str(total_inserts / total_time) + " quotes/second"
    print str((total_inserts / total_time) * 23400) + " quotes/NYSE trading day" # 23400 seconds in NYSE trading day
    print inserts.qsize()
    pool.close()
