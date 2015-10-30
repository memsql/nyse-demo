CREATE DATABASE IF NOT EXISTS stocks;
USE stocks;

DROP VIEW IF EXISTS `ask_view`;
DROP VIEW IF EXISTS `bid_view`;
DROP TABLE IF EXISTS `bid_temp`;
DROP TABLE IF EXISTS `ask_temp`;
DROP TABLE IF EXISTS `bid_quotes`;
DROP TABLE IF EXISTS `ask_quotes`;

CREATE TABLE `ask_quotes` (
    `ticker` char(4) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
    `ts` BIGINT UNSIGNED NOT NULL,
    `ask_price` MEDIUMINT(8) UNSIGNED NOT NULL,
    `ask_size` SMALLINT(5) UNSIGNED NOT NULL,
    `exchange` ENUM('NYS','LON','NASDAQ','TYO','FRA') CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
    KEY `ticker` (`ticker`,`ts`),
    /*!90618 SHARD */ KEY `ticker_2` (`ticker`)
);

CREATE TABLE `bid_quotes` (
    `ticker` char(4) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
    `ts` BIGINT UNSIGNED NOT NULL,
    `bid_price` MEDIUMINT(8) UNSIGNED NOT NULL,
    `bid_size` SMALLINT(5) UNSIGNED NOT NULL,
    `exchange` ENUM('NYS','LON','NASDAQ','TYO','FRA') CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
    KEY `ticker` (`ticker`,`ts`),
    /*!90618 SHARD */ KEY `ticker_2` (`ticker`)
);

CREATE VIEW ask_view as
SELECT ticker, ts, ask_price, ask_size, exchange
FROM ask_quotes
WHERE (`ask_quotes`.`ts` > ((UNIX_TIMESTAMP() - 1) * 100000));

CREATE VIEW bid_view as
SELECT ticker, ts, bid_price, bid_size, exchange
FROM bid_quotes
WHERE (`bid_quotes`.`ts` > ((UNIX_TIMESTAMP() - 1 ) * 100000));
