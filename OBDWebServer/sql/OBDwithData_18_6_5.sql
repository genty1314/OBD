-- MySQL dump 10.16  Distrib 10.1.33-MariaDB, for Linux (x86_64)
--
-- Host: localhost    Database: OBD
-- ------------------------------------------------------
-- Server version	10.1.33-MariaDB

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `authority`
--

DROP TABLE IF EXISTS `authority`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `authority` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  `codename` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name_UNIQUE` (`name`),
  UNIQUE KEY `authoritycol_UNIQUE` (`codename`)
) ENGINE=InnoDB AUTO_INCREMENT=10 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `authority`
--

LOCK TABLES `authority` WRITE;
/*!40000 ALTER TABLE `authority` DISABLE KEYS */;
INSERT INTO `authority` VALUES (1,'添加管理员','add_manager'),(2,'修改管理员','change_manager'),(3,'删除管理员','delete_manager'),(4,'添加用户','add_user'),(5,'修改用户','change_user'),(6,'删除用户','delete_user'),(7,'添加图片','add_picture'),(8,'修改图片','change_picture'),(9,'删除图片','delete_picture');
/*!40000 ALTER TABLE `authority` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `manager`
--

DROP TABLE IF EXISTS `manager`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `manager` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `email` varchar(255) NOT NULL,
  `managername` varchar(150) NOT NULL,
  `password` varchar(128) NOT NULL,
  `is_active` tinyint(1) NOT NULL DEFAULT '0',
  `create_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `last_login` datetime DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE KEY `email_UNIQUE` (`email`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8 COMMENT='manager information table';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `manager`
--

LOCK TABLES `manager` WRITE;
/*!40000 ALTER TABLE `manager` DISABLE KEYS */;
INSERT INTO `manager` VALUES (1,'1@qq.com','初始管理员','d033e22ae348aeb5660fc2140aec35850c4da997',1,'2018-04-12 15:21:52','2018-05-31 14:28:30'),(2,'aka@gmail.com','测试管理员2','7c4a8d09ca3762af61e59520943dc26494f8941b',1,'2018-04-25 22:18:53','2018-04-25 22:19:17'),(4,'123@qq.com','test2','7c4a8d09ca3762af61e59520943dc26494f8941b',1,'2018-04-25 22:44:27','2018-04-25 22:44:27');
/*!40000 ALTER TABLE `manager` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `obdnote`
--

DROP TABLE IF EXISTS `obdnote`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `obdnote` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `obd_code` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL,
  `note_category` int(11) NOT NULL DEFAULT '1',
  `note` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL,
  `obdnotecol` datetime DEFAULT CURRENT_TIMESTAMP,
  `pic1_path` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL,
  `pic2_path` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL,
  `pic3_path` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=16 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `obdnote`
--

LOCK TABLES `obdnote` WRITE;
/*!40000 ALTER TABLE `obdnote` DISABLE KEYS */;
INSERT INTO `obdnote` VALUES (1,'752HC/GJ493/GF003/OBD0001',0,'123123','2018-05-29 17:44:19','notepic/2018_05_29_17_22_42_70c096e348a57308f2472c857347c22f.jpg','notepic/2018_05_29_17_22_42_46934d2796f2032302079e7488f86fbd.jpg',''),(2,'752HC/GJ493/GF003/OBD0001',0,'123123','2018-05-29 17:47:32','notepic/2018_05_29_17_47_32_2bd02a7adeecfd59b4f1eae7f1bb4d98.jpg','notepic/2018_05_29_17_47_32_211f8e8dd1973d8c58dcd61c54c97bca.jpg',''),(3,'752HY/GJ136/OBD0002',1,'123123123','2018-05-29 17:58:02','notepic/2018_05_29_17_58_02_9723d0b3f29664ba5ffaeb34c106691b.jpg','',''),(4,'752HY/GJ136/OBD0002',1,'12313','2018-05-29 17:59:56','notepic/2018_05_29_17_59_56_2bd02a7adeecfd59b4f1eae7f1bb4d98.jpg','notepic/2018_05_29_17_59_56_211f8e8dd1973d8c58dcd61c54c97bca.jpg','notepic/2018_05_29_17_59_56_1cd12c06fd2e1ffc7687c1370951284c.jpg'),(5,'752HC/GJ493/GF003/OBD0001',1,'666','2018-05-29 18:02:54','notepic/2018_05_29_18_02_54_2bd02a7adeecfd59b4f1eae7f1bb4d98.jpg','notepic/2018_05_29_18_02_54_211f8e8dd1973d8c58dcd61c54c97bca.jpg','notepic/2018_05_29_18_02_54_fd680b23229ccdfe6540647e2335f904.jpg'),(6,'123',1,'还行','2018-05-29 18:27:45','notepic/2018_05_29_18_27_45_ad47c938f433582023b42c731ee8c786.jpg','notepic/2018_05_29_18_27_45_d429846cc227c1204765fe7eebbed6c3.jpg',''),(7,'123',1,'厉害了','2018-05-29 18:30:58','notepic/2018_05_29_18_30_58_ff11a097a00f87cb6e7e548e970c49e4.jpg','notepic/2018_05_29_18_30_58_2c09f0bc076ac99ba8fefc50232c676d.jpg',''),(8,'752HC/GJ493/GF003/OBD0001',0,'[1,0,0,1,0,0,1,0,1]','2018-05-29 19:15:08','','',''),(9,'752HC.JKC00/GF050/OBD0001',0,'123','2018-05-29 19:18:40','','',''),(10,'752HY/GJ136/OBD0002',1,'asdfasdf','2018-05-29 19:21:35','notepic/2018_05_29_19_21_35_9723d0b3f29664ba5ffaeb34c106691b.jpg','notepic/2018_05_29_19_21_35_fb82aa001f1826ca5dfe1868cabe4757.jpg',''),(11,'123',0,'11101','2018-05-29 19:24:28','','',''),(12,'752HY/GJ136/OBD0002',1,'1231321','2018-05-29 19:26:44','notepic/2018_05_29_19_26_44_fbb8c7dd23fb950de1c73f4d03250fe8.jpg','notepic/2018_05_29_19_26_44_f4e96ef051a881d436084085c5203dd7.jpg','notepic/2018_05_29_19_26_44_cbf220e33f8537b8f0cbdab677362870.jpg'),(13,'752HC.JKC00/GF050/OBD0001',1,'123123','2018-05-30 15:42:31','notepic/2018_05_30_15_42_31_78477150966594101ee9ce85593a586e.JPG','notepic/2018_05_30_15_42_31_7c054206dbfbe01c10d0a0d0de382dc5.jpg',''),(14,'752HC/GJ493/GF003/OBD0001',1,'1231','2018-05-31 08:11:12','notepic/2018_05_31_08_11_12_fbb8c7dd23fb950de1c73f4d03250fe8.jpg','notepic/2018_05_31_08_11_12_76b5fac249992e928cbfde735bfd5140.jpg',''),(15,'752HC/GJ493/GF003/OBD0001',1,'qety','2018-05-31 08:13:59','notepic/2018_05_31_08_13_59_350252296ffaa8f98b85205484c05cbf.jpg','notepic/2018_05_31_08_13_59_efc29b52118bc0f7f18638daf7adba35.jpg','');
/*!40000 ALTER TABLE `obdnote` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `picture`
--

DROP TABLE IF EXISTS `picture`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `picture` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `code` varchar(255) DEFAULT NULL,
  `name` varchar(255) DEFAULT NULL,
  `address` varchar(255) DEFAULT NULL,
  `GPS` varchar(255) DEFAULT NULL,
  `port_direction` int(11) NOT NULL COMMENT '端口朝向：\n0：上\n1：下\n2：左\n3：右',
  `zero_port_pos` int(11) NOT NULL COMMENT '0口位置：\n0：上\n1：下\n2：左\n3：右',
  `port_sort` int(1) NOT NULL COMMENT '端口排序\n0：顺时针\n1：逆时针',
  `picture_path` varchar(255) NOT NULL,
  `confirmed_picture_path` varchar(255) DEFAULT NULL,
  `ports_occupy` varchar(255) DEFAULT NULL,
  `is_correct` int(1) DEFAULT '0',
  `uncorrect_msg` varchar(255) DEFAULT NULL,
  `create_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `update_time` datetime DEFAULT NULL ON UPDATE CURRENT_TIMESTAMP COMMENT '端口排序方式\n0：顺时针\n1：逆时针',
  `user_id` int(11) DEFAULT NULL,
  `manager_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `fk_picture_user1_idx` (`user_id`),
  KEY `fk_picture_manager1_idx` (`manager_id`),
  CONSTRAINT `fk_picture_manager1` FOREIGN KEY (`manager_id`) REFERENCES `manager` (`id`) ON DELETE SET NULL ON UPDATE SET NULL,
  CONSTRAINT `fk_picture_user1` FOREIGN KEY (`user_id`) REFERENCES `user` (`id`) ON DELETE SET NULL ON UPDATE SET NULL
) ENGINE=InnoDB AUTO_INCREMENT=229 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `picture`
--

LOCK TABLES `picture` WRITE;
/*!40000 ALTER TABLE `picture` DISABLE KEYS */;
INSERT INTO `picture` VALUES (166,'752HC.JKC00/GF050/OBD0001','仲恺潼湖塘光村原有外杆P1932/GF050/OBD0001','惠州市仲恺高新区潼湖镇塘光村1号居民房对面101房','114.15461;23.41718',0,0,0,'uploadpic/2018_05_29_16_00_57_2bd02a7adeecfd59b4f1eae7f1bb4d98.jpg','confirmedpic/2018_05_29_16_00_57_4cf39d836999ea11fc8b57e5c510c53b.jpg','[1, 0, 0, 1, 1, 1, 1, 0, 1]',1,'success','2018-05-29 16:02:09',NULL,1,NULL),(167,'752HC.JKC00/GF050/OBD0001','仲恺潼湖塘光村原有外杆P1932/GF050/OBD0001','惠州市仲恺高新区潼湖镇塘光村1号居民房对面101房','114.15461;23.41718',0,0,0,'uploadpic/2018_05_29_16_03_30_2bd02a7adeecfd59b4f1eae7f1bb4d98.jpg','confirmedpic/2018_05_29_16_03_30_285f7ec8300404c95d367579d16d2699.jpg','[1, 0, 0, 1, 1, 1, 1, 0, 1]',1,'success','2018-05-29 16:04:49',NULL,1,NULL),(168,'752HY/GJ136/OBD0002','银山开发区光交箱/OBD0002','惠州市惠阳区良井镇湘信工业区(北方树工艺品有限公司)办公楼1楼103房','0;0',0,0,0,'uploadpic/2018_05_29_16_07_42_f55eadf4d3fc4d23d156823934228e22.jpg','confirmedpic/2018_05_29_16_07_42_3d35e880e9cf078d30866fd218ed350d.jpg','[1, 0, 1, 0, 0, 0, 0, 0, 1]',1,'success','2018-05-29 16:09:00',NULL,1,NULL),(169,'752HC/GJ493/GF003/OBD0001','冰塘小组236号后面集资楼6楼/GF003/OBD0001','惠州市惠城区河南岸街道办事处冰塘村（小组）(236号后面集资楼)','114.428438151201;23.0462469284539',0,0,0,'uploadpic/2018_05_29_16_18_40_70c096e348a57308f2472c857347c22f.jpg','confirmedpic/2018_05_29_16_18_40_ed164f6866c71d026ddcdfce06bd0a6c.jpg','[1, 0, 0, 1, 0, 0, 1, 0, 1]',1,'success','2018-05-29 16:20:02',NULL,1,NULL),(170,'752HC.JKC00/GF050/OBD0001','仲恺潼湖塘光村原有外杆P1932/GF050/OBD0001','惠州市仲恺高新区潼湖镇塘光村1号居民房对面101房','114.15461;23.41718',0,0,0,'uploadpic/2018_05_29_16_42_39_2bd02a7adeecfd59b4f1eae7f1bb4d98.jpg','confirmedpic/2018_05_29_16_42_39_f320e424827bb1098cd9dbc840e0ef0f.jpg','[1, 0, 0, 1, 1, 1, 1, 0, 1]',1,'success','2018-05-29 16:42:53',NULL,1,NULL),(171,'752HC.JKC00/GF050/OBD0001','仲恺潼湖塘光村原有外杆P1932/GF050/OBD0001','惠州市仲恺高新区潼湖镇塘光村1号居民房对面101房','114.15461;23.41718',0,0,0,'uploadpic/2018_05_29_16_44_09_2bd02a7adeecfd59b4f1eae7f1bb4d98.jpg','confirmedpic/2018_05_29_16_44_09_9db03b9b0076336a26376ad02da485f9.jpg','[1, 0, 0, 1, 1, 1, 1, 0, 1]',1,'success','2018-05-29 16:44:23',NULL,1,NULL),(172,'752HC/GJ493/GF003/OBD0001','冰塘小组236号后面集资楼6楼/GF003/OBD0001','惠州市惠城区河南岸街道办事处冰塘村（小组）(236号后面集资楼)','114.428438151201;23.0462469284539',0,0,0,'uploadpic/2018_05_29_16_51_21_70c096e348a57308f2472c857347c22f.jpg','confirmedpic/2018_05_29_16_51_21_1726bb5b0a8bfffe50f72dd0e012ffa9.jpg','[1, 0, 0, 1, 0, 0, 1, 0, 1]',1,'success','2018-05-29 16:51:34',NULL,1,NULL),(173,'752HC/GJ493/GF003/OBD0001','冰塘小组236号后面集资楼6楼/GF003/OBD0001','惠州市惠城区河南岸街道办事处冰塘村（小组）(236号后面集资楼)','114.428438151201;23.0462469284539',0,0,0,'uploadpic/2018_05_29_16_57_35_78477150966594101ee9ce85593a586e.JPG','confirmedpic/2018_05_29_16_57_35_ba99c12c97e8bba818909cbb55092fbe.JPG','[1, 0, 0, 0, 1, 0, 0, 1, 1]',1,'success','2018-05-29 16:58:07',NULL,1,NULL),(174,'752HC/GJ493/GF003/OBD0001','冰塘小组236号后面集资楼6楼/GF003/OBD0001','惠州市惠城区河南岸街道办事处冰塘村（小组）(236号后面集资楼)','114.428438151201;23.0462469284539',0,0,0,'uploadpic/2018_05_29_17_29_34_70c096e348a57308f2472c857347c22f.jpg','confirmedpic/2018_05_29_17_29_34_9b9a4a13b50ac8f5ff5479cbb54155d8.jpg','[1, 0, 0, 1, 0, 0, 1, 0, 1]',1,'success','2018-05-29 17:29:48',NULL,1,NULL),(175,'752HC/GJ493/GF003/OBD0001','冰塘小组236号后面集资楼6楼/GF003/OBD0001','惠州市惠城区河南岸街道办事处冰塘村（小组）(236号后面集资楼)','114.428438151201;23.0462469284539',0,0,0,'uploadpic/2018_05_29_17_46_27_78477150966594101ee9ce85593a586e.JPG','confirmedpic/2018_05_29_17_46_27_6913e10d5095650092f2b1515d522279.JPG','[1, 0, 0, 0, 1, 0, 0, 1, 1]',1,'success','2018-05-29 17:47:01',NULL,1,NULL),(176,'752HY/GJ136/OBD0002','银山开发区光交箱/OBD0002','惠州市惠阳区良井镇湘信工业区(北方树工艺品有限公司)办公楼1楼103房','0;0',0,0,0,'uploadpic/2018_05_29_17_57_27_96b040e643fd51c0b36d7f07dda18365.jpg','confirmedpic/2018_05_29_17_57_27_dae81715a279653155eddf7296bd8e13.jpg','[1, 0, 1, 0, 0, 0, 0, 0, 1]',1,'success','2018-05-29 17:57:42',NULL,1,NULL),(177,'752HY/GJ136/OBD0002','银山开发区光交箱/OBD0002','惠州市惠阳区良井镇湘信工业区(北方树工艺品有限公司)办公楼1楼103房','0;0',0,0,0,'uploadpic/2018_05_29_17_59_01_f55eadf4d3fc4d23d156823934228e22.jpg','confirmedpic/2018_05_29_17_59_01_92e353e700f8676929831da6531203f1.jpg','[1, 0, 1, 0, 0, 0, 0, 0, 1]',1,'success','2018-05-29 17:59:17',NULL,1,NULL),(178,'752HC/GJ493/GF003/OBD0001','冰塘小组236号后面集资楼6楼/GF003/OBD0001','惠州市惠城区河南岸街道办事处冰塘村（小组）(236号后面集资楼)','114.428438151201;23.0462469284539',0,0,0,'uploadpic/2018_05_29_18_01_36_78477150966594101ee9ce85593a586e.JPG','confirmedpic/2018_05_29_18_01_36_c9a6d07ac9e7b9f996f3e5464d4dff9a.JPG','[1, 0, 0, 0, 1, 0, 0, 1, 1]',1,'success','2018-05-29 18:02:12',NULL,1,NULL),(179,'752HC/GJ493/GF003/OBD0001','冰塘小组236号后面集资楼6楼/GF003/OBD0001','惠州市惠城区河南岸街道办事处冰塘村（小组）(236号后面集资楼)','114.428438151201;23.0462469284539',0,0,0,'uploadpic/2018_05_29_18_10_10_70c096e348a57308f2472c857347c22f.jpg','confirmedpic/2018_05_29_18_10_10_ebb8ffa4675a6e047649a3e302dde9fd.jpg','[1, 0, 0, 1, 0, 0, 1, 0, 1]',1,'success','2018-05-29 18:10:28',NULL,1,NULL),(180,'752HC/GJ493/GF003/OBD0001','冰塘小组236号后面集资楼6楼/GF003/OBD0001','惠州市惠城区河南岸街道办事处冰塘村（小组）(236号后面集资楼)','114.428438151201;23.0462469284539',0,0,0,'uploadpic/2018_05_29_18_17_03_78477150966594101ee9ce85593a586e.JPG','confirmedpic/2018_05_29_18_17_03_f6277b89f578ec12b29584a16fe5f5e6.JPG','[1, 0, 0, 0, 1, 0, 0, 1, 1]',1,'success','2018-05-29 18:17:42',NULL,1,NULL),(181,'752HY/GJ136/OBD0002','银山开发区光交箱/OBD0002','惠州市惠阳区良井镇湘信工业区(北方树工艺品有限公司)办公楼1楼103房','0;0',0,0,0,'uploadpic/2018_05_29_18_21_46_f55eadf4d3fc4d23d156823934228e22.jpg','confirmedpic/2018_05_29_18_21_46_e4c3e0683fd3f2c6a09aa2c10cae946d.jpg','[1, 0, 1, 0, 0, 0, 0, 0, 1]',1,'success','2018-05-29 18:22:06',NULL,1,NULL),(182,'752HC.JKC00/GF050/OBD0001','仲恺潼湖塘光村原有外杆P1932/GF050/OBD0001','惠州市仲恺高新区潼湖镇塘光村1号居民房对面101房','114.15461;23.41718',0,0,0,'uploadpic/2018_05_29_18_23_38_fbb8c7dd23fb950de1c73f4d03250fe8.jpg','confirmedpic/2018_05_29_18_23_38_9cd22468d844b153660ab8f3dc9a231a.jpg','[1, 0, 1, 0, 0, 1, 0, 0, 1]',1,'success','2018-05-29 18:24:00',NULL,1,NULL),(187,'752HC/GJ493/GF003/OBD0001','冰塘小组236号后面集资楼6楼/GF003/OBD0001','惠州市惠城区河南岸街道办事处冰塘村（小组）(236号后面集资楼)','114.428438151201;23.0462469284539',0,0,0,'uploadpic/2018_05_29_19_08_24_70c096e348a57308f2472c857347c22f.jpg','confirmedpic/2018_05_29_19_08_24_82938f348d0b82a5af94f3849f508164.jpg','[1, 0, 0, 1, 0, 0, 1, 0, 1]',1,'success','2018-05-29 19:08:37',NULL,1,NULL),(188,'752HC.JKC00/GF050/OBD0001','仲恺潼湖塘光村原有外杆P1932/GF050/OBD0001','惠州市仲恺高新区潼湖镇塘光村1号居民房对面101房','114.15461;23.41718',0,0,0,'uploadpic/2018_05_29_19_18_12_2bd02a7adeecfd59b4f1eae7f1bb4d98.jpg','confirmedpic/2018_05_29_19_18_12_694a13fa36f2ac226284e203e4c3af95.jpg','[1, 0, 0, 1, 1, 1, 1, 0, 1]',1,'success','2018-05-29 19:18:25',NULL,1,NULL),(189,'752HY/GJ136/OBD0002','银山开发区光交箱/OBD0002','惠州市惠阳区良井镇湘信工业区(北方树工艺品有限公司)办公楼1楼103房','0;0',0,0,0,'uploadpic/2018_05_29_19_20_44_96b040e643fd51c0b36d7f07dda18365.jpg','confirmedpic/2018_05_29_19_20_44_dcd8878d6229df4df091cbb574b8381d.jpg','[1, 0, 1, 0, 0, 0, 0, 0, 1]',1,'success','2018-05-29 19:20:57',NULL,1,NULL),(191,'752HY/GJ136/OBD0002','银山开发区光交箱/OBD0002','惠州市惠阳区良井镇湘信工业区(北方树工艺品有限公司)办公楼1楼103房','0;0',0,0,0,'uploadpic/2018_05_29_19_25_35_f55eadf4d3fc4d23d156823934228e22.jpg','confirmedpic/2018_05_29_19_25_35_2057439fd25c9d5a023eb440072eb12d.jpg','[1, 0, 1, 0, 0, 0, 0, 0, 1]',1,'success','2018-05-29 19:25:50',NULL,1,NULL),(192,'752HC.JKC00/GF050/OBD0001','仲恺潼湖塘光村原有外杆P1932/GF050/OBD0001','惠州市仲恺高新区潼湖镇塘光村1号居民房对面101房','114.15461;23.41718',0,0,0,'uploadpic/2018_05_30_15_41_44_2bd02a7adeecfd59b4f1eae7f1bb4d98.jpg','confirmedpic/2018_05_30_15_41_44_4aaac9a52c00ece772f62558e465df0e.jpg','[1, 0, 0, 1, 1, 1, 1, 0, 1]',1,'success','2018-05-30 15:42:00',NULL,1,NULL),(193,'752HC.JKC00/GF050/OBD0001','仲恺潼湖塘光村原有外杆P1932/GF050/OBD0001','惠州市仲恺高新区潼湖镇塘光村1号居民房对面101房','114.15461;23.41718',0,0,0,'uploadpic/2018_05_31_07_59_29_2bd02a7adeecfd59b4f1eae7f1bb4d98.jpg','confirmedpic/2018_05_31_07_59_29_63d570b5ef1f56d41e1f3178891debac.jpg','[1, 0, 0, 1, 1, 1, 1, 0, 1]',1,'success','2018-05-31 07:59:43',NULL,1,NULL),(194,'752HY/GJ136/OBD0002','银山开发区光交箱/OBD0002','惠州市惠阳区良井镇湘信工业区(北方树工艺品有限公司)办公楼1楼103房','0;0',0,0,0,'uploadpic/2018_05_31_08_06_04_f55eadf4d3fc4d23d156823934228e22.jpg','confirmedpic/2018_05_31_08_06_04_0de8a6bd5e37d5c5f54015e827c07236.jpg','[1, 0, 1, 0, 0, 0, 0, 0, 1]',1,'success','2018-05-31 08:06:19',NULL,1,NULL),(195,'752HC.JKC00/GF050/OBD0001','仲恺潼湖塘光村原有外杆P1932/GF050/OBD0001','惠州市仲恺高新区潼湖镇塘光村1号居民房对面101房','114.15461;23.41718',0,0,0,'uploadpic/2018_05_31_08_07_53_2bd02a7adeecfd59b4f1eae7f1bb4d98.jpg','confirmedpic/2018_05_31_08_07_53_aa41ab2d9bae3927802f1819e5d04609.jpg','[1, 0, 0, 1, 1, 1, 1, 0, 1]',1,'success','2018-05-31 08:08:08',NULL,1,NULL),(196,'752HC/GJ493/GF003/OBD0001','冰塘小组236号后面集资楼6楼/GF003/OBD0001','惠州市惠城区河南岸街道办事处冰塘村（小组）(236号后面集资楼)','114.428438151201;23.0462469284539',0,0,0,'uploadpic/2018_05_31_08_10_11_78477150966594101ee9ce85593a586e.JPG','confirmedpic/2018_05_31_08_10_11_b86d0b48097c85d8e219676911295d5b.JPG','[1, 0, 0, 0, 1, 0, 0, 1, 1]',1,'success','2018-05-31 08:10:44',NULL,1,NULL),(197,'752HC/GJ493/GF003/OBD0001','冰塘小组236号后面集资楼6楼/GF003/OBD0001','惠州市惠城区河南岸街道办事处冰塘村（小组）(236号后面集资楼)','113.353794:23.139846',0,0,0,'uploadpic/2018_05_31_08_12_24_70c096e348a57308f2472c857347c22f.jpg','confirmedpic/2018_05_31_08_12_24_fc70d148f5774838070f6b5e3c17a8e1.jpg','[1, 0, 0, 1, 0, 0, 1, 0, 1]',1,'success','2018-05-31 08:12:37',NULL,1,NULL),(201,'752HC.JKC00/GF050/OBD0001','仲恺潼湖塘光村原有外杆P1932/GF050/OBD0001','惠州市仲恺高新区潼湖镇塘光村1号居民房对面101房','114.15461;23.41718',0,0,0,'uploadpic/2018_05_31_09_27_54_2bd02a7adeecfd59b4f1eae7f1bb4d98.jpg','confirmedpic/2018_05_31_09_27_54_d23d13d6a2241490558f30c209ab02e1.jpg','[1, 0, 0, 1, 1, 1, 1, 0, 1]',1,'success','2018-05-31 09:28:08',NULL,1,NULL),(211,'752HC.JKC00/GF050/OBD0001','仲恺潼湖塘光村原有外杆P1932/GF050/OBD0001','惠州市仲恺高新区潼湖镇塘光村1号居民房对面101房','113.353012:23.140558',0,0,0,'uploadpic/2018_05_31_10_12_29_2bd02a7adeecfd59b4f1eae7f1bb4d98.jpg','confirmedpic/2018_05_31_10_12_29_d1dc3de25a0a20683e4208363787aff7.jpg','[1, 0, 0, 1, 1, 1, 1, 0, 1]',1,'success','2018-05-31 10:12:48',NULL,1,NULL),(221,'752HC.JKC00/GF050/OBD0001','仲恺潼湖塘光村原有外杆P1932/GF050/OBD0001','惠州市仲恺高新区潼湖镇塘光村1号居民房对面101房','113.353002:23.140551',0,0,0,'uploadpic/2018_05_31_14_29_45_2bd02a7adeecfd59b4f1eae7f1bb4d98.jpg','confirmedpic/2018_05_31_14_29_45_b62f94d68c900f732d56b4586c0866a0.jpg','[1, 0, 0, 1, 1, 1, 1, 0, 1]',1,'success','2018-05-31 14:30:23',NULL,1,NULL),(222,'752HC/GJ493/GF003/OBD0001','冰塘小组236号后面集资楼6楼/GF003/OBD0001','惠州市惠城区河南岸街道办事处冰塘村（小组）(236号后面集资楼)','113.353013:23.140538',0,0,0,'uploadpic/2018_05_31_14_35_40_70c096e348a57308f2472c857347c22f.jpg','confirmedpic/2018_05_31_14_35_40_66ac3faf2384d6dba2a5a5555f8bbda5.jpg','[1, 0, 0, 1, 0, 0, 1, 0, 1]',1,'success','2018-05-31 14:36:17',NULL,1,NULL),(223,'','','','',3,3,0,'uploadpic/2018_05_31_14_44_29_b45abf705a537f373514d5bc5dc9f387.jpg','confirmedpic/2018_05_31_14_44_29_bb57aa8c88f11f745d576f37da1797c0.jpg','[1, 0, 0, 1, 0, 0, 1, 0, 1]',0,'QrcodeFail','2018-05-31 14:45:08',NULL,1,NULL),(224,'752HC.JKC00/GF050/OBD0001','仲恺潼湖塘光村原有外杆P1932/GF050/OBD0001','惠州市仲恺高新区潼湖镇塘光村1号居民房对面101房','114.15461;23.41718',3,3,0,'uploadpic/2018_05_31_14_48_13_2bd02a7adeecfd59b4f1eae7f1bb4d98.jpg','confirmedpic/2018_05_31_14_48_13_36c6f5ebc0160b52ecc3819311de03d1.jpg','[1, 0, 0, 1, 1, 1, 1, 0, 1]',1,'success','2018-05-31 14:48:57',NULL,1,NULL),(225,'752HC.JKC00/GF050/OBD0001','仲恺潼湖塘光村原有外杆P1932/GF050/OBD0001','惠州市仲恺高新区潼湖镇塘光村1号居民房对面101房','114.15461;23.41718',3,3,0,'uploadpic/2018_05_31_14_52_36_fbb8c7dd23fb950de1c73f4d03250fe8.jpg','confirmedpic/2018_05_31_14_52_36_0df3ec4aca8d9ca62c7bc2ab0dfe332d.jpg','[1, 0, 1, 0, 0, 1, 0, 0, 1]',1,'success','2018-05-31 14:53:19',NULL,1,NULL),(226,'752HC.JKC00/GF050/OBD0001','仲恺潼湖塘光村原有外杆P1932/GF050/OBD0001','惠州市仲恺高新区潼湖镇塘光村1号居民房对面101房','114.15461;23.41718',3,3,0,'uploadpic/2018_05_31_14_59_49_2bd02a7adeecfd59b4f1eae7f1bb4d98.jpg','confirmedpic/2018_05_31_14_59_49_a1fc38a65f0f40b3effb653d55adf439.jpg','[1, 0, 0, 1, 1, 1, 1, 0, 1]',1,'success','2018-05-31 15:00:35',NULL,1,NULL),(227,'752HC.JKC00/GF050/OBD0001','仲恺潼湖塘光村原有外杆P1932/GF050/OBD0001','惠州市仲恺高新区潼湖镇塘光村1号居民房对面101房','114.15461;23.41718',0,1,0,'uploadpic/2018_05_31_15_06_25_2bd02a7adeecfd59b4f1eae7f1bb4d98.jpg','confirmedpic/2018_05_31_15_06_25_5966b91ca766800ffe414dbc9d2858b5.jpg','[1, 0, 0, 1, 1, 1, 1, 0, 1]',1,'success','2018-05-31 15:07:13',NULL,1,NULL),(228,'752HY/GJ136/OBD0002','银山开发区光交箱/OBD0002','惠州市惠阳区良井镇湘信工业区(北方树工艺品有限公司)办公楼1楼103房','0;0',0,1,0,'uploadpic/2018_05_31_15_22_01_f55eadf4d3fc4d23d156823934228e22.jpg','confirmedpic/2018_05_31_15_22_01_0e7c12e7b082f0f863718841f9cf38a0.jpg','[1, 0, 1, 0, 0, 0, 0, 0, 1]',1,'success','2018-05-31 15:22:56',NULL,1,NULL);
/*!40000 ALTER TABLE `picture` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `role`
--

DROP TABLE IF EXISTS `role`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `role` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  `content` varchar(255) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name_UNIQUE` (`name`),
  UNIQUE KEY `content_UNIQUE` (`content`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `role`
--

LOCK TABLES `role` WRITE;
/*!40000 ALTER TABLE `role` DISABLE KEYS */;
INSERT INTO `role` VALUES (1,'超级管理员','增，删，查，查用户；增，删，查，改图片，增，删，查，改管理员；增，删，查，改角色和角色权限,查看log'),(2,'普通管理员','增，删，查，查用户；增，删，查，改图片'),(3,'图片管理员','增，删，查，改图片信息');
/*!40000 ALTER TABLE `role` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `role_has_authority`
--

DROP TABLE IF EXISTS `role_has_authority`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `role_has_authority` (
  `role_id` int(11) NOT NULL,
  `authority_id` int(11) NOT NULL,
  PRIMARY KEY (`role_id`,`authority_id`),
  KEY `fk_role_has_authority_authority1_idx` (`authority_id`),
  KEY `fk_role_has_authority_role_idx` (`role_id`),
  CONSTRAINT `fk_role_has_authority_authority1` FOREIGN KEY (`authority_id`) REFERENCES `authority` (`id`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  CONSTRAINT `fk_role_has_authority_role` FOREIGN KEY (`role_id`) REFERENCES `role` (`id`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `role_has_authority`
--

LOCK TABLES `role_has_authority` WRITE;
/*!40000 ALTER TABLE `role_has_authority` DISABLE KEYS */;
INSERT INTO `role_has_authority` VALUES (1,1),(1,2),(1,3),(1,4),(1,5),(1,6),(1,7),(1,8),(1,9),(2,4),(2,5),(2,6),(2,7),(2,8),(2,9),(3,7),(3,8),(3,9);
/*!40000 ALTER TABLE `role_has_authority` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `role_has_manager`
--

DROP TABLE IF EXISTS `role_has_manager`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `role_has_manager` (
  `role_id` int(11) NOT NULL,
  `manager_id` int(11) NOT NULL,
  PRIMARY KEY (`role_id`,`manager_id`),
  KEY `fk_role_has_manager_manager1_idx` (`manager_id`),
  KEY `fk_role_has_manager_role1_idx` (`role_id`),
  CONSTRAINT `fk_role_has_manager_manager1` FOREIGN KEY (`manager_id`) REFERENCES `manager` (`id`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  CONSTRAINT `fk_role_has_manager_role1` FOREIGN KEY (`role_id`) REFERENCES `role` (`id`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `role_has_manager`
--

LOCK TABLES `role_has_manager` WRITE;
/*!40000 ALTER TABLE `role_has_manager` DISABLE KEYS */;
INSERT INTO `role_has_manager` VALUES (1,1),(2,2);
/*!40000 ALTER TABLE `role_has_manager` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `user`
--

DROP TABLE IF EXISTS `user`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `user` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `email` varchar(255) NOT NULL,
  `username` varchar(150) NOT NULL,
  `password` varchar(128) NOT NULL,
  `is_active` tinyint(1) NOT NULL DEFAULT '0',
  `create_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `last_login` datetime DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE KEY `email_UNIQUE` (`email`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8 COMMENT='manager information table';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `user`
--

LOCK TABLES `user` WRITE;
/*!40000 ALTER TABLE `user` DISABLE KEYS */;
INSERT INTO `user` VALUES (1,'1@qq.com','初始用户','7c4a8d09ca3762af61e59520943dc26494f8941b',1,'2018-04-12 15:24:00','2018-05-31 16:10:20');
/*!40000 ALTER TABLE `user` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2018-06-05 11:09:20
