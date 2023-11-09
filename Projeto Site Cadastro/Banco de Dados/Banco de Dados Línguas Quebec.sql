CREATE DATABASE  IF NOT EXISTS `cadastroelogin` /*!40100 DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci */ /*!80016 DEFAULT ENCRYPTION='N' */;
USE `cadastroelogin`;
-- MySQL dump 10.13  Distrib 8.0.34, for Win64 (x86_64)
--
-- Host: localhost    Database: cadastroelogin
-- ------------------------------------------------------
-- Server version	8.2.0

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `alunos`
--

DROP TABLE IF EXISTS `alunos`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `alunos` (
  `matricula` int NOT NULL,
  `senha` varchar(30) NOT NULL,
  PRIMARY KEY (`matricula`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `alunos`
--

LOCK TABLES `alunos` WRITE;
/*!40000 ALTER TABLE `alunos` DISABLE KEYS */;
INSERT INTO `alunos` VALUES (12032835,'38439348'),(33283282,'27282762'),(38264592,'27382764833');
/*!40000 ALTER TABLE `alunos` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `dados_alunos`
--

DROP TABLE IF EXISTS `dados_alunos`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `dados_alunos` (
  `matricula_aluno` int NOT NULL,
  `email_aluno` varchar(30) NOT NULL,
  `senha_aluno` varchar(30) NOT NULL,
  `cpf_aluno` varchar(15) NOT NULL,
  `numero_aluno` varchar(20) NOT NULL,
  `nome_aluno` varchar(50) NOT NULL,
  UNIQUE KEY `email_aluno` (`email_aluno`),
  UNIQUE KEY `cpf_aluno` (`cpf_aluno`),
  UNIQUE KEY `nome_aluno` (`nome_aluno`),
  KEY `matricula_aluno` (`matricula_aluno`),
  CONSTRAINT `dados_alunos_ibfk_1` FOREIGN KEY (`matricula_aluno`) REFERENCES `alunos` (`matricula`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `dados_alunos`
--

LOCK TABLES `dados_alunos` WRITE;
/*!40000 ALTER TABLE `dados_alunos` DISABLE KEYS */;
INSERT INTO `dados_alunos` VALUES (33283282,'carolina423@gmail.com','27282762','464.328.392-43','(32) 98486-7783','Carolina'),(38264592,'daviteste@gmail.com','27382764833','849.373.947-38','(84) 93748-4093','Davi'),(12032835,'jao239@gmail.com','38439348','492.023.790-00','(37) 48967-5947','Joao');
/*!40000 ALTER TABLE `dados_alunos` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `dados_professores`
--

DROP TABLE IF EXISTS `dados_professores`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `dados_professores` (
  `id_professor` int NOT NULL,
  `email_professor` varchar(30) NOT NULL,
  `senha_professor` varchar(30) NOT NULL,
  `cpf_professor` varchar(15) NOT NULL,
  `numero_professor` varchar(20) NOT NULL,
  `nome_professor` varchar(50) NOT NULL,
  UNIQUE KEY `email_professor` (`email_professor`),
  UNIQUE KEY `cpf_professor` (`cpf_professor`),
  UNIQUE KEY `nome_professor` (`nome_professor`),
  KEY `id_professor` (`id_professor`),
  CONSTRAINT `dados_professores_ibfk_1` FOREIGN KEY (`id_professor`) REFERENCES `professores` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `dados_professores`
--

LOCK TABLES `dados_professores` WRITE;
/*!40000 ALTER TABLE `dados_professores` DISABLE KEYS */;
/*!40000 ALTER TABLE `dados_professores` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `professores`
--

DROP TABLE IF EXISTS `professores`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `professores` (
  `id` int NOT NULL,
  `senha` varchar(30) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `professores`
--

LOCK TABLES `professores` WRITE;
/*!40000 ALTER TABLE `professores` DISABLE KEYS */;
/*!40000 ALTER TABLE `professores` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2023-11-08 23:18:20
