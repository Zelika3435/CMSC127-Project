/*M!999999\- enable the sandbox mode */ 
-- MariaDB dump 10.19-11.4.7-MariaDB, for Win64 (AMD64)
--
-- Host: localhost    Database: student_membership_db
-- ------------------------------------------------------
-- Server version	11.4.7-MariaDB

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*M!100616 SET @OLD_NOTE_VERBOSITY=@@NOTE_VERBOSITY, NOTE_VERBOSITY=0 */;

--
-- Table structure for table `member`
--

DROP TABLE IF EXISTS `member`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `member` (
  `member_id` int(11) NOT NULL AUTO_INCREMENT,
  `student_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`member_id`),
  KEY `student_id` (`student_id`),
  CONSTRAINT `member_ibfk_1` FOREIGN KEY (`student_id`) REFERENCES `student` (`student_id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `member`
--

LOCK TABLES `member` WRITE;
/*!40000 ALTER TABLE `member` DISABLE KEYS */;
/*!40000 ALTER TABLE `member` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `membership`
--

DROP TABLE IF EXISTS `membership`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `membership` (
  `membership_id` int(11) NOT NULL AUTO_INCREMENT,
  `batch` varchar(20) DEFAULT NULL,
  `mem_status` varchar(50) DEFAULT 'active',
  `committee` varchar(50) DEFAULT NULL,
  `org_id` int(11) DEFAULT NULL,
  `student_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`membership_id`),
  UNIQUE KEY `unique_student_org` (`student_id`,`org_id`),
  KEY `org_id` (`org_id`),
  CONSTRAINT `membership_ibfk_1` FOREIGN KEY (`org_id`) REFERENCES `organization` (`org_id`) ON DELETE CASCADE,
  CONSTRAINT `membership_ibfk_2` FOREIGN KEY (`student_id`) REFERENCES `student` (`student_id`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `membership`
--

LOCK TABLES `membership` WRITE;
/*!40000 ALTER TABLE `membership` DISABLE KEYS */;
INSERT INTO `membership` VALUES
(1,'2024-2025','active','Finance',1,8),
(2,'2022-2023','active','Publication',1,1);
/*!40000 ALTER TABLE `membership` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `organization`
--

DROP TABLE IF EXISTS `organization`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `organization` (
  `org_id` int(11) NOT NULL AUTO_INCREMENT,
  `org_name` varchar(255) NOT NULL,
  PRIMARY KEY (`org_id`),
  UNIQUE KEY `org_name` (`org_name`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `organization`
--

LOCK TABLES `organization` WRITE;
/*!40000 ALTER TABLE `organization` DISABLE KEYS */;
INSERT INTO `organization` VALUES
(1,'Alliance of Computer Science Students');
/*!40000 ALTER TABLE `organization` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `payment`
--

DROP TABLE IF EXISTS `payment`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `payment` (
  `payment_id` int(11) NOT NULL AUTO_INCREMENT,
  `amount` decimal(10,2) DEFAULT NULL,
  `payment_date` date DEFAULT NULL,
  `term_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`payment_id`),
  KEY `term_id` (`term_id`),
  CONSTRAINT `payment_ibfk_1` FOREIGN KEY (`term_id`) REFERENCES `term` (`term_id`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `payment`
--

LOCK TABLES `payment` WRITE;
/*!40000 ALTER TABLE `payment` DISABLE KEYS */;
INSERT INTO `payment` VALUES
(1,1000.00,'2025-05-26',1),
(2,500.00,'2025-05-26',3),
(3,800.00,'2025-05-26',2),
(4,100.00,'2025-05-26',3),
(5,100.00,'2025-05-26',3);
/*!40000 ALTER TABLE `payment` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `student`
--

DROP TABLE IF EXISTS `student`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `student` (
  `student_id` int(11) NOT NULL AUTO_INCREMENT,
  `first_name` varchar(255) NOT NULL,
  `last_name` varchar(255) NOT NULL,
  `gender` varchar(20) NOT NULL,
  `degree_program` varchar(255) NOT NULL,
  `standing` varchar(20) NOT NULL,
  PRIMARY KEY (`student_id`)
) ENGINE=InnoDB AUTO_INCREMENT=27 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `student`
--

LOCK TABLES `student` WRITE;
/*!40000 ALTER TABLE `student` DISABLE KEYS */;
INSERT INTO `student` VALUES
(1,'John','Smith','Male','BS Computer Science','Junior'),
(2,'Maria','Garcia','Female','BS Information Technology','Senior'),
(3,'James','Johnson','Male','BS Computer Science','Sophomore'),
(4,'Sarah','Williams','Female','BS Information Systems','Freshman'),
(5,'Michael','Brown','Male','BS Computer Science','Senior'),
(6,'Emily','Davis','Female','BS Information Technology','Junior'),
(7,'David','Miller','Male','BS Computer Science','Sophomore'),
(8,'Jessica','Wilson','Female','BS Information Systems','Freshman'),
(9,'Robert','Moore','Male','BS Computer Science','Senior'),
(10,'Jennifer','Taylor','Female','BS Information Technology','Junior'),
(11,'William','Anderson','Male','BS Computer Science','Sophomore'),
(12,'Lisa','Thomas','Female','BS Information Systems','Freshman'),
(13,'Richard','Jackson','Male','BS Computer Science','Senior'),
(14,'Michelle','White','Female','BS Information Technology','Junior'),
(15,'Joseph','Harris','Male','BS Computer Science','Sophomore'),
(16,'Amanda','Martin','Female','BS Information Systems','Freshman'),
(17,'Charles','Thompson','Male','BS Computer Science','Senior'),
(18,'Melissa','Garcia','Female','BS Information Technology','Junior'),
(19,'Thomas','Martinez','Male','BS Computer Science','Sophomore'),
(20,'Nicole','Robinson','Female','BS Information Systems','Freshman'),
(21,'Daniel','Clark','Male','BS Computer Science','Senior'),
(22,'Stephanie','Rodriguez','Female','BS Information Technology','Junior'),
(23,'Paul','Lewis','Male','BS Computer Science','Sophomore'),
(24,'Rebecca','Lee','Female','BS Information Systems','Freshman'),
(25,'Mark','Walker','Male','BS Computer Science','Senior'),
(26,'Sage','Patricio','Female','BS Political Science','Junior');
/*!40000 ALTER TABLE `student` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `term`
--

DROP TABLE IF EXISTS `term`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `term` (
  `term_id` int(11) NOT NULL AUTO_INCREMENT,
  `semester` varchar(20) DEFAULT NULL,
  `payment_status` varchar(20) DEFAULT 'unpaid',
  `role` varchar(50) DEFAULT '',
  `term_start` date DEFAULT NULL,
  `term_end` date DEFAULT NULL,
  `acad_year` varchar(20) DEFAULT NULL,
  `fee_amount` decimal(10,2) DEFAULT NULL,
  `fee_due` date DEFAULT NULL,
  `balance` decimal(10,2) DEFAULT 0.00,
  `membership_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`term_id`),
  KEY `membership_id` (`membership_id`),
  CONSTRAINT `term_ibfk_1` FOREIGN KEY (`membership_id`) REFERENCES `membership` (`membership_id`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `term`
--

LOCK TABLES `term` WRITE;
/*!40000 ALTER TABLE `term` DISABLE KEYS */;
INSERT INTO `term` VALUES
(1,'1st','paid','Member','2021-01-14','2024-06-22','2023-2024',1000.00,'2024-06-22',0.00,1),
(2,'2nd','paid','Secretary','2024-01-26','2024-06-23','2023-2024',1000.00,'2024-06-23',0.00,1),
(3,'2nd','partial','President','2024-01-26','2024-06-23','2023-2024',1000.00,'2024-06-23',0.00,2);
/*!40000 ALTER TABLE `term` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*M!100616 SET NOTE_VERBOSITY=@OLD_NOTE_VERBOSITY */;

-- Dump completed on 2025-05-26  2:10:21
