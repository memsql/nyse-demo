CREATE DATABASE IF NOT EXISTS stocks;
USE stocks;

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
