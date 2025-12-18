CREATE TABLE IF NOT EXISTS `post` (
  `id` int NOT NULL AUTO_INCREMENT,
  `created` timestamp NOT NULL DEFAULT (now()),
  `author` varchar(50) NOT NULL,
  `message` text NOT NULL,
  PRIMARY KEY (`id`)
);