use stocks;

DROP VIEW IF EXISTS `ask_view`;
DROP VIEW IF EXISTS `bid_view`;
DROP TABLE IF EXISTS `bid_temp`;
DROP TABLE IF EXISTS `ask_temp`;
DROP TABLE IF EXISTS `bid_quotes`;
DROP TABLE IF EXISTS `ask_quotes`;

CREATE TABLE `ask_quotes` (
  `ticker` char(4) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `timestamp` bigint unsigned NOT NULL,
  `ask_price` mediumint(8) unsigned NOT NULL,
  `ask_size` smallint(5) unsigned NOT NULL,
  `exchange` enum('NYS','LON','NASDAQ','TYO','FRA') CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  KEY `ticker` (`ticker`,`timestamp`),
  /*!90618 SHARD */ KEY `ticker_2` (`ticker`)
);

CREATE TABLE `bid_quotes` (
  `ticker` char(4) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `timestamp` bigint unsigned NOT NULL,
  `bid_price` mediumint(8) unsigned NOT NULL,
  `bid_size` smallint(5) unsigned NOT NULL,
  `exchange` enum('NYS','LON','NASDAQ','TYO','FRA') CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  KEY `ticker` (`ticker`,`timestamp`),
  /*!90618 SHARD */ KEY `ticker_2` (`ticker`)
);

CREATE VIEW ask_view as 
SELECT
    ticker, timestamp, ask_price, ask_size, exchange
FROM
    ask_quotes
WHERE
    (`ask_quotes`.`timestamp` > (( UNIX_TIMESTAMP()-1)*100000));

CREATE VIEW bid_view as 
SELECT
    ticker, timestamp, bid_price, bid_size, exchange
FROM
    bid_quotes
WHERE
    (`bid_quotes`.`timestamp` > (( UNIX_TIMESTAMP()-1)*100000));


