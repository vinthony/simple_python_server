# ************************************************************
# Sequel Pro SQL dump
# Version 4096
#
# http://www.sequelpro.com/
# http://code.google.com/p/sequel-pro/
#
# Host: 127.0.0.1 (MySQL 5.6.14)
# Database: awesome
# Generation Time: 2015-03-16 08:47:11 +0000
# ************************************************************


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;


# Dump of table award
# ------------------------------------------------------------

DROP TABLE IF EXISTS `award`;

CREATE TABLE `award` (
  `id` varchar(50) CHARACTER SET utf8 NOT NULL DEFAULT '',
  `award_year` varchar(50) CHARACTER SET utf8 NOT NULL DEFAULT '',
  `award_content` mediumtext CHARACTER SET utf8 NOT NULL,
  `award_user_id` varchar(50) CHARACTER SET utf8 NOT NULL DEFAULT '',
  `award_is_show` tinyint(1) NOT NULL DEFAULT '1',
  `created_at` double NOT NULL,
  `award_title` varchar(255) CHARACTER SET utf8 DEFAULT NULL,
  `award_type` int(1) DEFAULT '1',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

LOCK TABLES `award` WRITE;
/*!40000 ALTER TABLE `award` DISABLE KEYS */;

INSERT INTO `award` (`id`, `award_year`, `award_content`, `award_user_id`, `award_is_show`, `created_at`, `award_title`, `award_type`)
VALUES
	('001426481989592b169645528fd4c2e86b072c111623c0b000','2006','测试内容','010601',1,1426481989.59198,'测试标题',1),
	('00142648210189880e37c9862274c949f9200e3cf0ee674000','2006','测试内容2','010601',1,1426482101.898692,'测试标题2',1),
	('001426483932235170d81695637454ab5737ef464fa0d2a000','2014','文章','010601',1,1426483932.235616,'位置呢',1);

/*!40000 ALTER TABLE `award` ENABLE KEYS */;
UNLOCK TABLES;


# Dump of table college
# ------------------------------------------------------------

DROP TABLE IF EXISTS `college`;

CREATE TABLE `college` (
  `id` int(50) NOT NULL,
  `college_name` varchar(50) CHARACTER SET utf8 DEFAULT NULL,
  `college_id` int(11) DEFAULT NULL,
  `created_at` double DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

LOCK TABLES `college` WRITE;
/*!40000 ALTER TABLE `college` DISABLE KEYS */;

INSERT INTO `college` (`id`, `college_name`, `college_id`, `created_at`)
VALUES
	(1,'信息学院',1,NULL),
	(2,'水产与生命学院',2,NULL),
	(3,'人文学院',3,NULL),
	(4,'社会科学部',4,NULL),
	(5,'高等职业技术学院',5,NULL),
	(6,'食品学院',6,NULL),
	(7,'爱恩学院',7,NULL),
	(8,'海洋科学学院',8,NULL),
	(9,'经济管理学院',9,NULL),
	(10,'工程学院',10,NULL),
	(11,'外国语学院',11,NULL),
	(12,'继续教育学院',12,NULL),
	(13,'国际文化交流学院',13,NULL),
	(14,'海洋科学研究院',14,NULL);

/*!40000 ALTER TABLE `college` ENABLE KEYS */;
UNLOCK TABLES;


# Dump of table users
# ------------------------------------------------------------

DROP TABLE IF EXISTS `users`;

CREATE TABLE `users` (
  `id` varchar(50) NOT NULL,
  `sno` varchar(10) NOT NULL DEFAULT '',
  `password` varchar(50) NOT NULL DEFAULT '670b14728ad9902aecba32e22fa4f6bd',
  `identify` tinyint(1) NOT NULL,
  `name` varchar(50) NOT NULL,
  `year` int(4) unsigned NOT NULL DEFAULT '2006',
  `created_at` double NOT NULL,
  `college` int(2) DEFAULT '1',
  `email` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `idx_email` (`sno`),
  KEY `idx_created_at` (`created_at`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

LOCK TABLES `users` WRITE;
/*!40000 ALTER TABLE `users` DISABLE KEYS */;

INSERT INTO `users` (`id`, `sno`, `password`, `identify`, `name`, `year`, `created_at`, `college`, `email`)
VALUES
	('0000000000000','000000','670b14728ad9902aecba32e22fa4f6bd',1,'admin',2006,0,1,'000000@student.edu.cn'),
	('001426264704077f08bc4a152c0435785fbd6d54b2dab9d000','010601','e3ceb5881a0a1fdaad01296d7554868d',0,'杨鑫',2006,1426264704.077751,1,'010601@student.edu.cn'),
	('001426302183266a96fcbb2064e43bba51a04945d50a15d000','010602','670b14728ad9902aecba32e22fa4f6bd',0,'马力',2006,1426302183.266904,1,'010602@student.edu.cn'),
	('00142630630270023ba2afc977847398c7d08da164d15ef000','010603','670b14728ad9902aecba32e22fa4f6bd',0,'李明',2006,1426306302.7006,1,'010603@student.edu.cn'),
	('001426307580905300c72a41d4f45ec99bbd6fa0738d4ae000','081101','670b14728ad9902aecba32e22fa4f6bd',0,'陈玺',2011,1426307580.905265,8,'081101@student.edu.cn'),
	('001426307661934f0f9532eeacc432f8a832bc67d859453000','041201','670b14728ad9902aecba32e22fa4f6bd',0,'刘东',2012,1426307661.934671,4,'041201@student.edu.cn'),
	('001426307732474e7c22a8fb5024429ae388a221bf76383000','041202','670b14728ad9902aecba32e22fa4f6bd',0,'刘名',2012,1426307732.474273,4,'041202@student.edu.cn'),
	('0014264807137250a7df8a4b7074b2cba573515d2d27e0a000','010604','670b14728ad9902aecba32e22fa4f6bd',0,'王美',2006,1426480713.725091,1,'010604@student.edu.cn'),
	('001426480761483a10a099c00844b9d85965e7210728f18000','010605','670b14728ad9902aecba32e22fa4f6bd',0,'王美丽',2006,1426480761.48347,1,'010605@student.edu.cn'),
	('0014264807721397cdd1b28a3ba42d68d6cef5ea1453015000','010606','670b14728ad9902aecba32e22fa4f6bd',0,'刘妹',2006,1426480772.139795,1,'010606@student.edu.cn');

/*!40000 ALTER TABLE `users` ENABLE KEYS */;
UNLOCK TABLES;



/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;
/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
