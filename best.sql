USE stocks;

SELECT
    ticker, ask_price, ask_size, exchange, timestamp 
FROM
    ask_view
WHERE
    ticker='BLAH'
ORDER BY
    ask_price ASC, ask_size DESC limit 25;

SELECT
    ticker, ask_price best_ask, max(ask_size) AS ask_size, exchange
FROM 
    ask_view
        INNER JOIN
    (
    SELECT 
        min(ask_price) AS ask_price, exchange, ticker
    FROM 
        ask_view
    WHERE 
        ticker='BLAH'
    GROUP BY 
        exchange
    ) AS t2
USING 
    (ticker, exchange, ask_price)
WHERE 
    ticker='BLAH'
GROUP BY 
    exchange;

SELECT
    ticker, bid_price, bid_size, exchange 
FROM
    bid_view
WHERE
    ticker='BLAH'
ORDER BY
    bid_price DESC, bid_size DESC limit 25;

SELECT
    ticker, bid_price best_bid, max(bid_size) AS bid_size, exchange, timestamp
FROM 
    bid_view
        INNER JOIN
    (
    SELECT 
        max(bid_price) AS bid_price, exchange, ticker
    FROM 
        bid_view
    WHERE 
        ticker='BLAH'
    GROUP BY 
        exchange
    ) AS t2
USING 
    (ticker, exchange, bid_price)
WHERE 
    ticker='BLAH'
GROUP BY 
    exchange
