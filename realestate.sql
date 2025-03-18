-- --------------------------------------------------------
-- Host:                         127.0.0.1
-- Server version:               8.0.30 - MySQL Community Server - GPL
-- Server OS:                    Win64
-- HeidiSQL Version:             12.1.0.6537
-- --------------------------------------------------------

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET NAMES utf8 */;
/*!50503 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;


-- Dumping database structure for realestate
CREATE DATABASE IF NOT EXISTS `tdbsoft_realestate` /*!40100 DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci */ /*!80016 DEFAULT ENCRYPTION='N' */;
USE `tdbsoft_realestate`;

-- Dumping structure for table realestate.about_content
DROP TABLE IF EXISTS `about_content`;
CREATE TABLE IF NOT EXISTS `about_content` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `content` longtext NOT NULL,
  `published` tinyint(1) NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `property_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  KEY `about_content_property_id_5156302e_fk_properties_id` (`property_id`),
  CONSTRAINT `about_content_property_id_5156302e_fk_properties_id` FOREIGN KEY (`property_id`) REFERENCES `properties` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 ;

-- Dumping data for table realestate.about_content: ~0 rows (approximately)

-- Dumping structure for table realestate.account_customuser
DROP TABLE IF EXISTS `account_customuser`;
CREATE TABLE IF NOT EXISTS `account_customuser` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `password` varchar(128) NOT NULL,
  `last_login` datetime(6) DEFAULT NULL,
  `is_superuser` tinyint(1) NOT NULL,
  `first_name` varchar(150) NOT NULL,
  `last_name` varchar(150) NOT NULL,
  `is_staff` tinyint(1) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `date_joined` datetime(6) NOT NULL,
  `username` varchar(150) DEFAULT NULL,
  `email` varchar(254) NOT NULL,
  `user_type` varchar(1) NOT NULL,
  `gender` varchar(10) NOT NULL,
  `profile_pic` varchar(100) DEFAULT NULL,
  `other_name` varchar(200) NOT NULL,
  `address` longtext NOT NULL,
  `fcm_token` longtext NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `updated_at` datetime(6) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `email` (`email`),
  UNIQUE KEY `username` (`username`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 ;

-- Dumping data for table realestate.account_customuser: ~2 rows (approximately)
INSERT IGNORE INTO `account_customuser` (`id`, `password`, `last_login`, `is_superuser`, `first_name`, `last_name`, `is_staff`, `is_active`, `date_joined`, `username`, `email`, `user_type`, `gender`, `profile_pic`, `other_name`, `address`, `fcm_token`, `created_at`, `updated_at`) VALUES
	(1, 'pbkdf2_sha256$600000$7aCPuZTxVAJK3kzovJX5SP$klpZw/PKNiZcTH9Yh4bAGMCWoMANFPa0IUkygGl60is=', '2023-08-11 15:02:37.000000', 1, 'admin', 'admin', 1, 1, '2023-08-10 21:48:25.000000', 'admin', 'admin@admin.com', '2', 'Male', '', '', '', '', '2023-08-10 21:48:25.906436', '2023-08-16 06:35:13.621859'),
	(2, 'pbkdf2_sha256$600000$G442Ln5Qb2lA3ROsg1IOcd$NlCe4bA7KsHLO3WH+Q5IRpwBZafKr0fqOL0aLJ82UBk=', '2023-08-14 14:13:50.041247', 1, 'Wicliffe', 'Wara', 1, 1, '2023-08-11 11:07:40.000000', 'obuon', 'obuon.wara@fernbrookapartments.com', '1', 'Male', 'profiles/Screenshot12.png', '', '', '', '2023-08-11 11:07:40.735344', '2023-08-11 11:08:22.057966'),
	(4, 'pbkdf2_sha256$600000$NSI0eRVjJoV9cP04B1XS5U$Vop6bFkvUvWJfIw1ly31iBhNX4NhTddqvStUmLTrccY=', '2023-08-11 17:30:36.240120', 0, 'Jane', 'Doe', 0, 1, '2023-08-11 17:27:17.269134', 'titusowuor30', 'titusowuor30@gmail.com', '4', 'M', '', 'Doe', '1234', '', '2023-08-11 17:27:17.271141', '2023-08-11 17:30:10.199444');

-- Dumping structure for table realestate.account_customuser_groups
DROP TABLE IF EXISTS `account_customuser_groups`;
CREATE TABLE IF NOT EXISTS `account_customuser_groups` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `customuser_id` bigint NOT NULL,
  `group_id` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `account_customuser_groups_customuser_id_group_id_7e51db7b_uniq` (`customuser_id`,`group_id`),
  KEY `account_customuser_groups_group_id_2be9f6d7_fk_auth_group_id` (`group_id`),
  CONSTRAINT `account_customuser_g_customuser_id_b6c60904_fk_account_c` FOREIGN KEY (`customuser_id`) REFERENCES `account_customuser` (`id`),
  CONSTRAINT `account_customuser_groups_group_id_2be9f6d7_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 ;

-- Dumping data for table realestate.account_customuser_groups: ~0 rows (approximately)

-- Dumping structure for table realestate.account_customuser_user_permissions
DROP TABLE IF EXISTS `account_customuser_user_permissions`;
CREATE TABLE IF NOT EXISTS `account_customuser_user_permissions` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `customuser_id` bigint NOT NULL,
  `permission_id` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `account_customuser_user__customuser_id_permission_650e378f_uniq` (`customuser_id`,`permission_id`),
  KEY `account_customuser_u_permission_id_f4aec423_fk_auth_perm` (`permission_id`),
  CONSTRAINT `account_customuser_u_customuser_id_03bcc114_fk_account_c` FOREIGN KEY (`customuser_id`) REFERENCES `account_customuser` (`id`),
  CONSTRAINT `account_customuser_u_permission_id_f4aec423_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 ;

-- Dumping data for table realestate.account_customuser_user_permissions: ~0 rows (approximately)

-- Dumping structure for table realestate.auth_group
DROP TABLE IF EXISTS `auth_group`;
CREATE TABLE IF NOT EXISTS `auth_group` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(150) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 ;

-- Dumping data for table realestate.auth_group: ~0 rows (approximately)

-- Dumping structure for table realestate.auth_group_permissions
DROP TABLE IF EXISTS `auth_group_permissions`;
CREATE TABLE IF NOT EXISTS `auth_group_permissions` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `group_id` int NOT NULL,
  `permission_id` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_group_permissions_group_id_permission_id_0cd325b0_uniq` (`group_id`,`permission_id`),
  KEY `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` (`permission_id`),
  CONSTRAINT `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  CONSTRAINT `auth_group_permissions_group_id_b120cbf9_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 ;

-- Dumping data for table realestate.auth_group_permissions: ~0 rows (approximately)

-- Dumping structure for table realestate.auth_permission
DROP TABLE IF EXISTS `auth_permission`;
CREATE TABLE IF NOT EXISTS `auth_permission` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  `content_type_id` int NOT NULL,
  `codename` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_permission_content_type_id_codename_01ab375a_uniq` (`content_type_id`,`codename`),
  CONSTRAINT `auth_permission_content_type_id_2f476e4b_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=137 DEFAULT CHARSET=utf8mb4 ;

-- Dumping data for table realestate.auth_permission: ~136 rows (approximately)
INSERT IGNORE INTO `auth_permission` (`id`, `name`, `content_type_id`, `codename`) VALUES
	(1, 'Can add log entry', 1, 'add_logentry'),
	(2, 'Can change log entry', 1, 'change_logentry'),
	(3, 'Can delete log entry', 1, 'delete_logentry'),
	(4, 'Can view log entry', 1, 'view_logentry'),
	(5, 'Can add permission', 2, 'add_permission'),
	(6, 'Can change permission', 2, 'change_permission'),
	(7, 'Can delete permission', 2, 'delete_permission'),
	(8, 'Can view permission', 2, 'view_permission'),
	(9, 'Can add group', 3, 'add_group'),
	(10, 'Can change group', 3, 'change_group'),
	(11, 'Can delete group', 3, 'delete_group'),
	(12, 'Can view group', 3, 'view_group'),
	(13, 'Can add content type', 4, 'add_contenttype'),
	(14, 'Can change content type', 4, 'change_contenttype'),
	(15, 'Can delete content type', 4, 'delete_contenttype'),
	(16, 'Can view content type', 4, 'view_contenttype'),
	(17, 'Can add session', 5, 'add_session'),
	(18, 'Can change session', 5, 'change_session'),
	(19, 'Can delete session', 5, 'delete_session'),
	(20, 'Can view session', 5, 'view_session'),
	(21, 'Can add site', 6, 'add_site'),
	(22, 'Can change site', 6, 'change_site'),
	(23, 'Can delete site', 6, 'delete_site'),
	(24, 'Can view site', 6, 'view_site'),
	(25, 'Can add user', 7, 'add_customuser'),
	(26, 'Can change user', 7, 'change_customuser'),
	(27, 'Can delete user', 7, 'delete_customuser'),
	(28, 'Can view user', 7, 'view_customuser'),
	(29, 'Can add setup', 8, 'add_setup'),
	(30, 'Can change setup', 8, 'change_setup'),
	(31, 'Can delete setup', 8, 'delete_setup'),
	(32, 'Can view setup', 8, 'view_setup'),
	(33, 'Can add site config', 9, 'add_siteconfig'),
	(34, 'Can change site config', 9, 'change_siteconfig'),
	(35, 'Can delete site config', 9, 'delete_siteconfig'),
	(36, 'Can view site config', 9, 'view_siteconfig'),
	(37, 'Can add testimonial', 10, 'add_testimonial'),
	(38, 'Can change testimonial', 10, 'change_testimonial'),
	(39, 'Can delete testimonial', 10, 'delete_testimonial'),
	(40, 'Can view testimonial', 10, 'view_testimonial'),
	(41, 'Can add services', 11, 'add_services'),
	(42, 'Can change services', 11, 'change_services'),
	(43, 'Can delete services', 11, 'delete_services'),
	(44, 'Can view services', 11, 'view_services'),
	(45, 'Can add about', 12, 'add_about'),
	(46, 'Can change about', 12, 'change_about'),
	(47, 'Can delete about', 12, 'delete_about'),
	(48, 'Can view about', 12, 'view_about'),
	(49, 'Can add invoice', 13, 'add_invoice'),
	(50, 'Can change invoice', 13, 'change_invoice'),
	(51, 'Can delete invoice', 13, 'delete_invoice'),
	(52, 'Can view invoice', 13, 'view_invoice'),
	(53, 'Can add property owner', 14, 'add_propertyowner'),
	(54, 'Can change property owner', 14, 'change_propertyowner'),
	(55, 'Can delete property owner', 14, 'delete_propertyowner'),
	(56, 'Can view property owner', 14, 'view_propertyowner'),
	(57, 'Can add agent', 15, 'add_agent'),
	(58, 'Can change agent', 15, 'change_agent'),
	(59, 'Can delete agent', 15, 'delete_agent'),
	(60, 'Can view agent', 15, 'view_agent'),
	(61, 'Can add lease', 16, 'add_lease'),
	(62, 'Can change lease', 16, 'change_lease'),
	(63, 'Can delete lease', 16, 'delete_lease'),
	(64, 'Can view lease', 16, 'view_lease'),
	(65, 'Can add lease term', 17, 'add_leaseterm'),
	(66, 'Can change lease term', 17, 'change_leaseterm'),
	(67, 'Can delete lease term', 17, 'delete_leaseterm'),
	(68, 'Can view lease term', 17, 'view_leaseterm'),
	(69, 'Can add property', 18, 'add_property'),
	(70, 'Can change property', 18, 'change_property'),
	(71, 'Can delete property', 18, 'delete_property'),
	(72, 'Can view property', 18, 'view_property'),
	(73, 'Can add property unit images', 19, 'add_propertyunitimages'),
	(74, 'Can change property unit images', 19, 'change_propertyunitimages'),
	(75, 'Can delete property unit images', 19, 'delete_propertyunitimages'),
	(76, 'Can view property unit images', 19, 'view_propertyunitimages'),
	(77, 'Can add units', 20, 'add_units'),
	(78, 'Can change units', 20, 'change_units'),
	(79, 'Can delete units', 20, 'delete_units'),
	(80, 'Can view units', 20, 'view_units'),
	(81, 'Can add property images', 21, 'add_propertyimages'),
	(82, 'Can change property images', 21, 'change_propertyimages'),
	(83, 'Can delete property images', 21, 'delete_propertyimages'),
	(84, 'Can view property images', 21, 'view_propertyimages'),
	(85, 'Can add enquiries', 22, 'add_enquiries'),
	(86, 'Can change enquiries', 22, 'change_enquiries'),
	(87, 'Can delete enquiries', 22, 'delete_enquiries'),
	(88, 'Can view enquiries', 22, 'view_enquiries'),
	(89, 'Can add notice', 23, 'add_notice'),
	(90, 'Can change notice', 23, 'change_notice'),
	(91, 'Can delete notice', 23, 'delete_notice'),
	(92, 'Can view notice', 23, 'view_notice'),
	(93, 'Can add notice feedback', 24, 'add_noticefeedback'),
	(94, 'Can change notice feedback', 24, 'change_noticefeedback'),
	(95, 'Can delete notice feedback', 24, 'delete_noticefeedback'),
	(96, 'Can view notice feedback', 24, 'view_noticefeedback'),
	(97, 'Can add payment', 25, 'add_payment'),
	(98, 'Can change payment', 25, 'change_payment'),
	(99, 'Can delete payment', 25, 'delete_payment'),
	(100, 'Can view payment', 25, 'view_payment'),
	(101, 'Can add staff salary payment', 26, 'add_staffsalarypayment'),
	(102, 'Can change staff salary payment', 26, 'change_staffsalarypayment'),
	(103, 'Can delete staff salary payment', 26, 'delete_staffsalarypayment'),
	(104, 'Can view staff salary payment', 26, 'view_staffsalarypayment'),
	(105, 'Can add deduction', 27, 'add_deduction'),
	(106, 'Can change deduction', 27, 'change_deduction'),
	(107, 'Can delete deduction', 27, 'delete_deduction'),
	(108, 'Can view deduction', 27, 'view_deduction'),
	(109, 'Can add earning', 28, 'add_earning'),
	(110, 'Can change earning', 28, 'change_earning'),
	(111, 'Can delete earning', 28, 'delete_earning'),
	(112, 'Can view earning', 28, 'view_earning'),
	(113, 'Can add staff', 29, 'add_staff'),
	(114, 'Can change staff', 29, 'change_staff'),
	(115, 'Can delete staff', 29, 'delete_staff'),
	(116, 'Can view staff', 29, 'view_staff'),
	(117, 'Can add staff salary', 30, 'add_staffsalary'),
	(118, 'Can change staff salary', 30, 'change_staffsalary'),
	(119, 'Can delete staff salary', 30, 'delete_staffsalary'),
	(120, 'Can view staff salary', 30, 'view_staffsalary'),
	(121, 'Can add tenant', 31, 'add_tenant'),
	(122, 'Can change tenant', 31, 'change_tenant'),
	(123, 'Can delete tenant', 31, 'delete_tenant'),
	(124, 'Can view tenant', 31, 'view_tenant'),
	(125, 'Can add tenant_ kin', 32, 'add_tenant_kin'),
	(126, 'Can change tenant_ kin', 32, 'change_tenant_kin'),
	(127, 'Can delete tenant_ kin', 32, 'delete_tenant_kin'),
	(128, 'Can view tenant_ kin', 32, 'view_tenant_kin'),
	(129, 'Can add tenant_ employment_ details', 33, 'add_tenant_employment_details'),
	(130, 'Can change tenant_ employment_ details', 33, 'change_tenant_employment_details'),
	(131, 'Can delete tenant_ employment_ details', 33, 'delete_tenant_employment_details'),
	(132, 'Can view tenant_ employment_ details', 33, 'view_tenant_employment_details'),
	(133, 'Can add tenant_ business_ details', 34, 'add_tenant_business_details'),
	(134, 'Can change tenant_ business_ details', 34, 'change_tenant_business_details'),
	(135, 'Can delete tenant_ business_ details', 34, 'delete_tenant_business_details'),
	(136, 'Can view tenant_ business_ details', 34, 'view_tenant_business_details');

-- Dumping structure for table realestate.core_setup
DROP TABLE IF EXISTS `core_setup`;
CREATE TABLE IF NOT EXISTS `core_setup` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `logo` varchar(100) NOT NULL,
  `support_reply_email_name` varchar(255) DEFAULT NULL,
  `support_reply_email` varchar(255) DEFAULT NULL,
  `email_password` varchar(255) DEFAULT NULL,
  `email_port` int DEFAULT NULL,
  `email_backed` varchar(100) DEFAULT NULL,
  `email_host` varchar(255) DEFAULT NULL,
  `fail_silently` tinyint(1) DEFAULT NULL,
  `use_tls` tinyint(1) DEFAULT NULL,
  `code_place_holders` longtext,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 ;

-- Dumping data for table realestate.core_setup: ~0 rows (approximately)
INSERT IGNORE INTO `core_setup` (`id`, `logo`, `support_reply_email_name`, `support_reply_email`, `email_password`, `email_port`, `email_backed`, `email_host`, `fail_silently`, `use_tls`, `code_place_holders`) VALUES
	(1, 'logo/logo_GyvJSAu-removebg-preview_oTym63E.png', 'Fernbrook Apartments', 'info@fernbrookapartments.com', 'Fernbrook@2023', 587, 'smtp', 'mail.fernbrookapartments.com', 0, 1, '');

-- Dumping structure for table realestate.core_siteconfig
DROP TABLE IF EXISTS `core_siteconfig`;
CREATE TABLE IF NOT EXISTS `core_siteconfig` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `key` varchar(50) NOT NULL,
  `value` varchar(200) NOT NULL,
  `config_id` int NOT NULL,
  `picked` tinyint(1) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `core_siteconfig_key_b3eafd0e` (`key`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4 ;

-- Dumping data for table realestate.core_siteconfig: ~5 rows (approximately)
INSERT IGNORE INTO `core_siteconfig` (`id`, `key`, `value`, `config_id`, `picked`) VALUES
	(1, 'site_title', 'Real Estate Admin', 1, 0),
	(2, 'site_slogan', 'Create . Innovate . Excel', 1, 0),
	(3, 'site_addres', 'Excel Building, Kisumu, 1235 St.', 1, 0),
	(4, 'site_email', 'info@ferbrook.co.ke|www.ferbrookapartments.co.ke', 1, 0),
	(5, 'tel', '+2547 000 000 001', 1, 0);

-- Dumping structure for table realestate.django_admin_log
DROP TABLE IF EXISTS `django_admin_log`;
CREATE TABLE IF NOT EXISTS `django_admin_log` (
  `id` int NOT NULL AUTO_INCREMENT,
  `action_time` datetime(6) NOT NULL,
  `object_id` longtext,
  `object_repr` varchar(200) NOT NULL,
  `action_flag` smallint unsigned NOT NULL,
  `change_message` longtext NOT NULL,
  `content_type_id` int DEFAULT NULL,
  `user_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  KEY `django_admin_log_content_type_id_c4bce8eb_fk_django_co` (`content_type_id`),
  KEY `django_admin_log_user_id_c564eba6_fk_account_customuser_id` (`user_id`),
  CONSTRAINT `django_admin_log_content_type_id_c4bce8eb_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`),
  CONSTRAINT `django_admin_log_user_id_c564eba6_fk_account_customuser_id` FOREIGN KEY (`user_id`) REFERENCES `account_customuser` (`id`),
  CONSTRAINT `django_admin_log_chk_1` CHECK ((`action_flag` >= 0))
) ENGINE=InnoDB AUTO_INCREMENT=42 DEFAULT CHARSET=utf8mb4 ;

-- Dumping data for table realestate.django_admin_log: ~36 rows (approximately)
INSERT IGNORE INTO `django_admin_log` (`id`, `action_time`, `object_id`, `object_repr`, `action_flag`, `change_message`, `content_type_id`, `user_id`) VALUES
	(1, '2023-08-10 22:15:04.218270', '1', 'admin admin', 2, '[{"changed": {"fields": ["User type", "Gender"]}}]', 7, 1),
	(2, '2023-08-11 11:07:40.736346', '2', ' ', 1, '[{"added": {}}]', 7, 1),
	(3, '2023-08-11 11:08:22.063964', '2', 'Wicliffe Wara', 2, '[{"changed": {"fields": ["First name", "Last name", "User type", "Gender", "Profile pic"]}}]', 7, 1),
	(4, '2023-08-11 11:09:54.967125', '1', 'obuon.wara@fernbrookapartments.com', 1, '[{"added": {}}]', 14, 2),
	(5, '2023-08-11 11:12:23.565981', '1', '/media/logo/logo_GyvJSAu-removebg-preview_oTym63E.png', 1, '[{"added": {}}]', 8, 2),
	(6, '2023-08-11 11:15:33.818706', '1', 'test - 001', 1, '[{"added": {}}]', 20, 2),
	(7, '2023-08-11 11:38:14.964175', '2', '202322300000001 - 0.00', 3, '', 25, 2),
	(8, '2023-08-11 11:38:14.968174', '1', '202322300000001 - 0.00', 3, '', 25, 2),
	(9, '2023-08-11 11:41:30.833154', '1', '/media/logo/logo_GyvJSAu-removebg-preview_oTym63E.png', 2, '[{"changed": {"fields": ["Support reply email", "Email host"]}}]', 8, 2),
	(10, '2023-08-11 11:49:15.488187', '3', '202322300000001 - 3000.00', 3, '', 25, 2),
	(11, '2023-08-11 12:00:43.177038', '6', '202322300000001 - 3000.00', 3, '', 25, 2),
	(12, '2023-08-11 12:00:43.180037', '5', '202322300000001 - 3000.00', 3, '', 25, 2),
	(13, '2023-08-11 12:00:43.184048', '4', '202322300000001 - 3000.00', 3, '', 25, 2),
	(14, '2023-08-11 12:01:02.377356', '1', 'rent Invoice for Lease: test - 001 - jane.doe@gmail.com', 2, '[{"changed": {"fields": ["Balance", "Status"]}}]', 13, 2),
	(15, '2023-08-11 12:05:23.635796', '1', 'rent Invoice for Lease: test - 001 - jane.doe@gmail.com', 2, '[{"changed": {"fields": ["Balance"]}}]', 13, 2),
	(16, '2023-08-11 12:09:15.533515', '1', 'rent Invoice for Lease: test - 001 - jane.doe@gmail.com', 2, '[{"changed": {"fields": ["Balance"]}}]', 13, 2),
	(17, '2023-08-11 12:09:38.410180', '8', '202322300000001 - 3000.00', 3, '', 25, 2),
	(18, '2023-08-11 12:09:49.886443', '7', '202322300000001 - 3000.00', 3, '', 25, 2),
	(19, '2023-08-11 12:15:09.646502', '1', '/media/logo/logo_GyvJSAu-removebg-preview_oTym63E.png', 2, '[{"changed": {"fields": ["Email port"]}}]', 8, 2),
	(20, '2023-08-11 12:15:40.710269', '1', 'rent Invoice for Lease: test - 001 - jane.doe@gmail.com', 2, '[{"changed": {"fields": ["Status"]}}]', 13, 2),
	(21, '2023-08-11 12:30:45.973735', '3', 'Jane Doe', 2, '[{"changed": {"fields": ["Email", "Gender"]}}]', 7, 2),
	(22, '2023-08-11 12:50:15.312216', '3', 'Jane Doe', 2, '[{"changed": {"fields": ["password"]}}]', 7, 2),
	(23, '2023-08-11 13:56:49.004683', '1', '/media/property_units/images/photo2_cyUaWMh_avHIqen.png', 1, '[{"added": {}}]', 19, 2),
	(24, '2023-08-11 13:56:57.279857', '2', '/media/property_units/images/img_6.jpg', 1, '[{"added": {}}]', 19, 2),
	(25, '2023-08-11 13:57:16.640650', '1', '/media/property/images/partment_2_xkQUFn0.jpg', 1, '[{"added": {}}]', 21, 2),
	(26, '2023-08-11 13:57:23.923316', '2', '/media/property/images/partment_3_6dF4jWy.jpg', 1, '[{"added": {}}]', 21, 2),
	(27, '2023-08-11 13:57:42.804225', '1', 'Fernbrook Apartments', 2, '[{"changed": {"fields": ["Units", "Description", "Amenities"]}}]', 18, 2),
	(28, '2023-08-11 13:59:50.911434', '1', 'titusowuor30@gmail.com', 2, '[{"changed": {"fields": ["Content", "Published"]}}]', 10, 2),
	(29, '2023-08-11 13:59:58.681311', '1', 'titusowuor30@gmail.com', 2, '[{"changed": {"fields": ["Property"]}}]', 10, 2),
	(30, '2023-08-11 15:02:17.152558', '1', 'admin@admin.com', 1, '[{"added": {}}]', 15, 2),
	(31, '2023-08-11 15:04:03.558854', '1', 'admin admin', 2, '[{"changed": {"fields": ["User type"]}}]', 7, 1),
	(32, '2023-08-11 15:11:21.475676', '1', 'test - 001 - titusowuor30@gmail.com', 2, '[{"changed": {"fields": ["Is active"]}}]', 16, 1),
	(33, '2023-08-11 15:23:37.662459', '1', 'rent Invoice for Lease: test - 001 - titusowuor30@gmail.com', 2, '[]', 13, 1),
	(34, '2023-08-11 15:25:23.362671', '1', 'welcome - 2023-08-11', 1, '[{"added": {}}]', 23, 1),
	(35, '2023-08-11 17:13:47.545629', '1', 'welcome - 2023-08-11', 2, '[{"changed": {"fields": ["Description"]}}]', 23, 1),
	(36, '2023-08-11 17:27:06.725492', '3', 'Jane Doe', 3, '', 7, 1),
	(37, '2023-08-11 17:30:10.205445', '4', 'Jane Doe', 2, '[{"changed": {"fields": ["password"]}}]', 7, 1),
	(38, '2023-08-11 17:39:03.871829', '1', 'welcome - 2023-08-11', 2, '[{"changed": {"fields": ["Description", "Read"]}}]', 23, 1),
	(39, '2023-08-11 17:45:25.179291', '2', 'rent Invoice for Lease: test - 001 - titusowuor30@gmail.com', 2, '[{"changed": {"fields": ["Balance", "Status"]}}]', 13, 1),
	(40, '2023-08-15 21:58:06.419157', '21', '202322300708765 - 1.00', 2, '[{"changed": {"fields": ["Payment method", "Description"]}}]', 25, 2),
	(41, '2023-08-15 21:58:16.221054', '20', '202322300708765 - 1.00', 2, '[{"changed": {"fields": ["Payment method", "Description"]}}]', 25, 2);

-- Dumping structure for table realestate.django_content_type
DROP TABLE IF EXISTS `django_content_type`;
CREATE TABLE IF NOT EXISTS `django_content_type` (
  `id` int NOT NULL AUTO_INCREMENT,
  `app_label` varchar(100) NOT NULL,
  `model` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `django_content_type_app_label_model_76bd3d3b_uniq` (`app_label`,`model`)
) ENGINE=InnoDB AUTO_INCREMENT=35 DEFAULT CHARSET=utf8mb4 ;

-- Dumping data for table realestate.django_content_type: ~34 rows (approximately)
INSERT IGNORE INTO `django_content_type` (`id`, `app_label`, `model`) VALUES
	(7, 'account', 'customuser'),
	(1, 'admin', 'logentry'),
	(3, 'auth', 'group'),
	(2, 'auth', 'permission'),
	(4, 'contenttypes', 'contenttype'),
	(12, 'core', 'about'),
	(11, 'core', 'services'),
	(8, 'core', 'setup'),
	(9, 'core', 'siteconfig'),
	(10, 'core', 'testimonial'),
	(13, 'invoices', 'invoice'),
	(15, 'landlords', 'agent'),
	(14, 'landlords', 'propertyowner'),
	(16, 'leases', 'lease'),
	(17, 'leases', 'leaseterm'),
	(22, 'notices', 'enquiries'),
	(23, 'notices', 'notice'),
	(24, 'notices', 'noticefeedback'),
	(25, 'payments', 'payment'),
	(26, 'payroll', 'staffsalarypayment'),
	(18, 'property', 'property'),
	(21, 'property', 'propertyimages'),
	(19, 'property', 'propertyunitimages'),
	(20, 'property', 'units'),
	(5, 'sessions', 'session'),
	(6, 'sites', 'site'),
	(27, 'staff', 'deduction'),
	(28, 'staff', 'earning'),
	(29, 'staff', 'staff'),
	(30, 'staff', 'staffsalary'),
	(31, 'tenants', 'tenant'),
	(34, 'tenants', 'tenant_business_details'),
	(33, 'tenants', 'tenant_employment_details'),
	(32, 'tenants', 'tenant_kin');

-- Dumping structure for table realestate.django_migrations
DROP TABLE IF EXISTS `django_migrations`;
CREATE TABLE IF NOT EXISTS `django_migrations` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `app` varchar(255) NOT NULL,
  `name` varchar(255) NOT NULL,
  `applied` datetime(6) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=44 DEFAULT CHARSET=utf8mb4 ;

-- Dumping data for table realestate.django_migrations: ~36 rows (approximately)
INSERT IGNORE INTO `django_migrations` (`id`, `app`, `name`, `applied`) VALUES
	(1, 'contenttypes', '0001_initial', '2023-08-10 21:47:39.299367'),
	(2, 'contenttypes', '0002_remove_content_type_name', '2023-08-10 21:47:39.364378'),
	(3, 'auth', '0001_initial', '2023-08-10 21:47:39.567893'),
	(4, 'auth', '0002_alter_permission_name_max_length', '2023-08-10 21:47:39.620596'),
	(5, 'auth', '0003_alter_user_email_max_length', '2023-08-10 21:47:39.630594'),
	(6, 'auth', '0004_alter_user_username_opts', '2023-08-10 21:47:39.640596'),
	(7, 'auth', '0005_alter_user_last_login_null', '2023-08-10 21:47:39.651597'),
	(8, 'auth', '0006_require_contenttypes_0002', '2023-08-10 21:47:39.657600'),
	(9, 'auth', '0007_alter_validators_add_error_messages', '2023-08-10 21:47:39.667597'),
	(10, 'auth', '0008_alter_user_username_max_length', '2023-08-10 21:47:39.678596'),
	(11, 'auth', '0009_alter_user_last_name_max_length', '2023-08-10 21:47:39.688596'),
	(12, 'auth', '0010_alter_group_name_max_length', '2023-08-10 21:47:39.725603'),
	(13, 'auth', '0011_update_proxy_permissions', '2023-08-10 21:47:39.736595'),
	(14, 'auth', '0012_alter_user_first_name_max_length', '2023-08-10 21:47:39.748596'),
	(15, 'account', '0001_initial', '2023-08-10 21:47:40.150877'),
	(16, 'admin', '0001_initial', '2023-08-10 21:47:40.271860'),
	(17, 'admin', '0002_logentry_remove_auto_add', '2023-08-10 21:47:40.287502'),
	(18, 'admin', '0003_logentry_add_action_flag_choices', '2023-08-10 21:47:40.311472'),
	(19, 'landlords', '0001_initial', '2023-08-10 21:47:40.538759'),
	(20, 'property', '0001_initial', '2023-08-10 21:47:41.066095'),
	(21, 'core', '0001_initial', '2023-08-10 21:47:41.397145'),
	(22, 'tenants', '0001_initial', '2023-08-10 21:47:41.761525'),
	(23, 'leases', '0001_initial', '2023-08-10 21:47:42.014878'),
	(24, 'invoices', '0001_initial', '2023-08-10 21:47:42.112745'),
	(25, 'notices', '0001_initial', '2023-08-10 21:47:42.368845'),
	(26, 'payments', '0001_initial', '2023-08-10 21:47:42.506275'),
	(27, 'staff', '0001_initial', '2023-08-10 21:47:43.180985'),
	(28, 'payroll', '0001_initial', '2023-08-10 21:47:43.277355'),
	(29, 'sessions', '0001_initial', '2023-08-10 21:47:43.328313'),
	(30, 'sites', '0001_initial', '2023-08-10 21:47:43.359389'),
	(31, 'sites', '0002_alter_domain_unique', '2023-08-10 21:47:43.384467'),
	(32, 'invoices', '0002_remove_invoice_is_paid_invoice_invoice_id_and_more', '2023-08-11 10:21:26.612310'),
	(33, 'payments', '0002_remove_payment_lease_remove_payment_tenant_and_more', '2023-08-11 10:21:26.950736'),
	(34, 'tenants', '0002_alter_tenant_date_of_birth', '2023-08-11 10:21:26.981985'),
	(35, 'invoices', '0003_invoice_balance_alter_invoice_amount_and_more', '2023-08-11 11:43:44.970076'),
	(36, 'tenants', '0003_alter_tenant_date_of_birth', '2023-08-11 11:43:44.985700'),
	(37, 'invoices', '0004_alter_invoice_due_date', '2023-08-15 20:39:53.347480'),
	(38, 'notices', '0002_alter_notice_description', '2023-08-15 20:39:53.398489'),
	(39, 'payments', '0003_payment_batch_id', '2023-08-15 20:39:53.474473'),
	(40, 'tenants', '0004_alter_tenant_date_of_birth', '2023-08-15 20:39:53.504082'),
	(41, 'invoices', '0005_alter_invoice_due_date', '2023-08-15 20:48:47.921649'),
	(42, 'payments', '0004_remove_payment_batch_id', '2023-08-15 20:48:47.950652'),
	(43, 'tenants', '0005_alter_tenant_date_of_birth', '2023-08-15 20:48:47.981515');

-- Dumping structure for table realestate.django_session
DROP TABLE IF EXISTS `django_session`;
CREATE TABLE IF NOT EXISTS `django_session` (
  `session_key` varchar(40) NOT NULL,
  `session_data` longtext NOT NULL,
  `expire_date` datetime(6) NOT NULL,
  PRIMARY KEY (`session_key`),
  KEY `django_session_expire_date_a5c62663` (`expire_date`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 ;

-- Dumping data for table realestate.django_session: ~4 rows (approximately)
INSERT IGNORE INTO `django_session` (`session_key`, `session_data`, `expire_date`) VALUES
	('2bao0ok3qa6x0bhop4ck4sn551w828tb', '.eJxVjMEOwiAQRP-FsyHQ0sJ69N5vILsLSNVAUtqT8d9tkx70Npn3Zt7C47Zmv7W4-DmIq9Di8tsR8jOWA4QHlnuVXMu6zCQPRZ60yamG-Lqd7t9Bxpb3NZMlZVzfaecAgeLAPesu7SkSazUCGjsmlSyD5kSDMjEoTL2F4ACS-HwB8Zs4dQ:1qUDWR:sdPkcXJUxxRScFHemm3LsdHB4AhZwVPF816mwVG20DM', '2023-08-24 21:48:47.753062'),
	('da9o1dck1r8ox30eno584ib6elt1emqt', '.eJxVjMsOwiAQRf-FtSEgMKUu3fcbyAwzSNW0SR8r478rSRe6usk9J-elEu5bTfsqSxpZXZRXp9-PMD9kaoDvON1mnedpW0bSTdEHXfUwszyvh_sXqLjWlg3Z5K4TZsHooiGAvkRPRbID6R3Dd7H3Fs_BB7LkPBRgNmIjFDLq_QH3pzg-:1qUVy8:fpAHZrHJB8ipdZ4mxPYo_982Dzx16D53uQMIkCAKtRo', '2023-08-25 17:30:36.249121'),
	('jj9j7s9an3b8zl57bycsm07d2ibyyd9o', '.eJxVjDsOwjAQRO_iGlmO418o6XMGa9e7xgHkSHFSIe5OIqWAYpp5b-YtImxriVvjJU4krkKLy2-HkJ5cD0APqPdZprmuy4TyUORJmxxn4tftdP8OCrSyryFbBrQ2KXbJeQy2185rNJQzOEbi7EhZYu_NYLIPijIMe3zXhd6h-HwBFQk5Bw:1qVYKM:ZdG30Kp0SoZTehWG6MIoHkmeb4cu_chLfFbKpSzxSCw', '2023-08-28 14:13:50.051252'),
	('mytplr7xli444woznhlfl9aokwrp5zb3', '.eJxVjMEOwiAQRP-FsyHQ0sJ69N5vILsLSNVAUtqT8d9tkx70Npn3Zt7C47Zmv7W4-DmIq9Di8tsR8jOWA4QHlnuVXMu6zCQPRZ60yamG-Lqd7t9Bxpb3NZMlZVzfaecAgeLAPesu7SkSazUCGjsmlSyD5kSDMjEoTL2F4ACS-HwB8Zs4dQ:1qUVxi:OZAIFWsBgUkSoaCqXRyR0Ox1iT8vElSqx7RLlTwS-WI', '2023-08-25 17:30:10.224443');

-- Dumping structure for table realestate.django_site
DROP TABLE IF EXISTS `django_site`;
CREATE TABLE IF NOT EXISTS `django_site` (
  `id` int NOT NULL AUTO_INCREMENT,
  `domain` varchar(100) NOT NULL,
  `name` varchar(50) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `django_site_domain_a2e37b91_uniq` (`domain`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 ;

-- Dumping data for table realestate.django_site: ~0 rows (approximately)
INSERT IGNORE INTO `django_site` (`id`, `domain`, `name`) VALUES
	(1, 'example.com', 'example.com');

-- Dumping structure for table realestate.invoices_invoice
DROP TABLE IF EXISTS `invoices_invoice`;
CREATE TABLE IF NOT EXISTS `invoices_invoice` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `invoice_type` varchar(20) NOT NULL,
  `amount` decimal(8,2) NOT NULL,
  `description` longtext NOT NULL,
  `due_date` date NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `updated_at` datetime(6) NOT NULL,
  `lease_id` bigint NOT NULL,
  `invoice_id` varchar(100) NOT NULL,
  `status` varchar(50) NOT NULL,
  `balance` decimal(8,2) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `invoices_invoice_lease_id_085c85e7_fk_leases_id` (`lease_id`),
  CONSTRAINT `invoices_invoice_lease_id_085c85e7_fk_leases_id` FOREIGN KEY (`lease_id`) REFERENCES `leases` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 ;

-- Dumping data for table realestate.invoices_invoice: ~1 rows (approximately)
INSERT IGNORE INTO `invoices_invoice` (`id`, `invoice_type`, `amount`, `description`, `due_date`, `created_at`, `updated_at`, `lease_id`, `invoice_id`, `status`, `balance`) VALUES
	(2, 'rent', 4000.00, 'Invoice for Rent 2000 and Deposit 2000 for new Lease #2', '2023-08-16', '2023-08-11 17:27:45.090547', '2023-08-16 06:35:07.915326', 2, '202322300708765', 'Partial', 996.00);

-- Dumping structure for table realestate.landlords_agent
DROP TABLE IF EXISTS `landlords_agent`;
CREATE TABLE IF NOT EXISTS `landlords_agent` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `mobile_number` varchar(13) NOT NULL,
  `national_id` varchar(10) DEFAULT NULL,
  `ID_Snapshot` varchar(100) DEFAULT NULL,
  `owner_id` bigint NOT NULL,
  `user_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `user_id` (`user_id`),
  KEY `landlords_agent_owner_id_10e1af38_fk_landlords_propertyowner_id` (`owner_id`),
  CONSTRAINT `landlords_agent_owner_id_10e1af38_fk_landlords_propertyowner_id` FOREIGN KEY (`owner_id`) REFERENCES `landlords_propertyowner` (`id`),
  CONSTRAINT `landlords_agent_user_id_aec7b0ea_fk_account_customuser_id` FOREIGN KEY (`user_id`) REFERENCES `account_customuser` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 ;

-- Dumping data for table realestate.landlords_agent: ~0 rows (approximately)
INSERT IGNORE INTO `landlords_agent` (`id`, `mobile_number`, `national_id`, `ID_Snapshot`, `owner_id`, `user_id`) VALUES
	(1, '+254743793901', NULL, '', 1, 1);

-- Dumping structure for table realestate.landlords_propertyowner
DROP TABLE IF EXISTS `landlords_propertyowner`;
CREATE TABLE IF NOT EXISTS `landlords_propertyowner` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `mobile_number` varchar(13) NOT NULL,
  `national_id` varchar(10) DEFAULT NULL,
  `ID_Snapshot` varchar(100) DEFAULT NULL,
  `user_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `user_id` (`user_id`),
  CONSTRAINT `landlords_propertyow_user_id_5dff2206_fk_account_c` FOREIGN KEY (`user_id`) REFERENCES `account_customuser` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 ;

-- Dumping data for table realestate.landlords_propertyowner: ~0 rows (approximately)
INSERT IGNORE INTO `landlords_propertyowner` (`id`, `mobile_number`, `national_id`, `ID_Snapshot`, `user_id`) VALUES
	(1, '', NULL, '', 2);

-- Dumping structure for table realestate.leases
DROP TABLE IF EXISTS `leases`;
CREATE TABLE IF NOT EXISTS `leases` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `start_date` date NOT NULL,
  `end_date` date DEFAULT NULL,
  `monthly_rent` decimal(8,2) NOT NULL,
  `security_deposit` decimal(8,2) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `leased_by_id` bigint NOT NULL,
  `property_unit_id` bigint NOT NULL,
  `tenant_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  KEY `leases_leased_by_id_19ba31fe_fk_account_customuser_id` (`leased_by_id`),
  KEY `leases_property_unit_id_b8e6c80b_fk_units_id` (`property_unit_id`),
  KEY `leases_tenant_id_9b3f9a65_fk_tenants_tenant_id` (`tenant_id`),
  CONSTRAINT `leases_leased_by_id_19ba31fe_fk_account_customuser_id` FOREIGN KEY (`leased_by_id`) REFERENCES `account_customuser` (`id`),
  CONSTRAINT `leases_property_unit_id_b8e6c80b_fk_units_id` FOREIGN KEY (`property_unit_id`) REFERENCES `units` (`id`),
  CONSTRAINT `leases_tenant_id_9b3f9a65_fk_tenants_tenant_id` FOREIGN KEY (`tenant_id`) REFERENCES `tenants_tenant` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 ;

-- Dumping data for table realestate.leases: ~0 rows (approximately)
INSERT IGNORE INTO `leases` (`id`, `start_date`, `end_date`, `monthly_rent`, `security_deposit`, `is_active`, `leased_by_id`, `property_unit_id`, `tenant_id`) VALUES
	(2, '2023-08-11', '2023-08-11', 2000.00, 2000.00, 1, 1, 1, 2);

-- Dumping structure for table realestate.lease_terms
DROP TABLE IF EXISTS `lease_terms`;
CREATE TABLE IF NOT EXISTS `lease_terms` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `late_payment_fine` decimal(8,2) NOT NULL,
  `uilities_description` varchar(500) NOT NULL,
  `utilities_amount` decimal(8,2) NOT NULL,
  `term_number` int unsigned NOT NULL,
  `term_description` longtext NOT NULL,
  `accepted` tinyint(1) NOT NULL,
  `lease_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  KEY `lease_terms_lease_id_c36d5dc4_fk_leases_id` (`lease_id`),
  CONSTRAINT `lease_terms_lease_id_c36d5dc4_fk_leases_id` FOREIGN KEY (`lease_id`) REFERENCES `leases` (`id`),
  CONSTRAINT `lease_terms_chk_1` CHECK ((`term_number` >= 0))
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 ;

-- Dumping data for table realestate.lease_terms: ~0 rows (approximately)
INSERT IGNORE INTO `lease_terms` (`id`, `late_payment_fine`, `uilities_description`, `utilities_amount`, `term_number`, `term_description`, `accepted`, `lease_id`) VALUES
	(1, 0.00, 'Electricity,Water,Gabbage management,swimming pool,gym', 0.00, 1001, 'Description here', 1, 2);

-- Dumping structure for table realestate.notices_enquiries
DROP TABLE IF EXISTS `notices_enquiries`;
CREATE TABLE IF NOT EXISTS `notices_enquiries` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `fullname` varchar(100) NOT NULL,
  `email` varchar(100) NOT NULL,
  `mobile_number` varchar(13) NOT NULL,
  `date` date NOT NULL,
  `message` longtext NOT NULL,
  `read` tinyint(1) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 ;

-- Dumping data for table realestate.notices_enquiries: ~0 rows (approximately)

-- Dumping structure for table realestate.notices_notice
DROP TABLE IF EXISTS `notices_notice`;
CREATE TABLE IF NOT EXISTS `notices_notice` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `notice_type` varchar(100) NOT NULL,
  `notify_group_of_users` varchar(50) DEFAULT NULL,
  `notice_date` date NOT NULL,
  `description` longtext NOT NULL,
  `reason` varchar(255) DEFAULT NULL,
  `read` tinyint(1) NOT NULL,
  `notify_specific_user_id` bigint DEFAULT NULL,
  `user_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  KEY `notices_notice_notify_specific_user_47a381b9_fk_account_c` (`notify_specific_user_id`),
  KEY `notices_notice_user_id_62c74e71_fk_account_customuser_id` (`user_id`),
  CONSTRAINT `notices_notice_notify_specific_user_47a381b9_fk_account_c` FOREIGN KEY (`notify_specific_user_id`) REFERENCES `account_customuser` (`id`),
  CONSTRAINT `notices_notice_user_id_62c74e71_fk_account_customuser_id` FOREIGN KEY (`user_id`) REFERENCES `account_customuser` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 ;

-- Dumping data for table realestate.notices_notice: ~0 rows (approximately)
INSERT IGNORE INTO `notices_notice` (`id`, `notice_type`, `notify_group_of_users`, `notice_date`, `description`, `reason`, `read`, `notify_specific_user_id`, `user_id`) VALUES
	(1, 'welcome', '4', '2023-08-11', '<h1>WELCOME NEW TENANT</h1>\r\n<h4>Dear Mr./Mrs./Miss</h4>\r\n<p>It is our pleasure to welcome you to your new home. We hope that you will be very happy here and will try our best to make sure that you are always satisfied. <br />Thankyou for selecting Fernbrook Apartments and we sincerely hope that you find your new home comfortable and enjoyable. <br />If we can be of any assistance to you, please let us know.</p>\r\n<div>\r\n<div>For any assistance contact our system admin Mr. Felix phone&nbsp;0769620042</div>\r\n</div>\r\n<p><br /><strong>Yours sincerely, <br />Wycliffe George/ Director</strong></p>', 'Reason here', 0, NULL, 2);

-- Dumping structure for table realestate.notices_noticefeedback
DROP TABLE IF EXISTS `notices_noticefeedback`;
CREATE TABLE IF NOT EXISTS `notices_noticefeedback` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `notice_date` date NOT NULL,
  `reply` longtext NOT NULL,
  `read` tinyint(1) NOT NULL,
  `notice_id` bigint NOT NULL,
  `user_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  KEY `notices_noticefeedback_notice_id_c9449122_fk_notices_notice_id` (`notice_id`),
  KEY `notices_noticefeedback_user_id_bf5dd736_fk_account_customuser_id` (`user_id`),
  CONSTRAINT `notices_noticefeedback_notice_id_c9449122_fk_notices_notice_id` FOREIGN KEY (`notice_id`) REFERENCES `notices_notice` (`id`),
  CONSTRAINT `notices_noticefeedback_user_id_bf5dd736_fk_account_customuser_id` FOREIGN KEY (`user_id`) REFERENCES `account_customuser` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 ;

-- Dumping data for table realestate.notices_noticefeedback: ~0 rows (approximately)

-- Dumping structure for table realestate.payments_payment
DROP TABLE IF EXISTS `payments_payment`;
CREATE TABLE IF NOT EXISTS `payments_payment` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `amount` decimal(8,2) NOT NULL,
  `description` longtext NOT NULL,
  `date_paid` date NOT NULL,
  `outstanding_balance` decimal(8,2) NOT NULL,
  `invoice_id` bigint DEFAULT NULL,
  `payment_method` varchar(100) NOT NULL,
  `transaction_code` varchar(16) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `payments_payment_invoice_id_a1a432c8_fk_invoices_invoice_id` (`invoice_id`),
  CONSTRAINT `payments_payment_invoice_id_a1a432c8_fk_invoices_invoice_id` FOREIGN KEY (`invoice_id`) REFERENCES `invoices_invoice` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=24 DEFAULT CHARSET=utf8mb4 ;

-- Dumping data for table realestate.payments_payment: ~2 rows (approximately)
INSERT IGNORE INTO `payments_payment` (`id`, `amount`, `description`, `date_paid`, `outstanding_balance`, `invoice_id`, `payment_method`, `transaction_code`) VALUES
	(18, 4000.00, '<h2>Payment of invoice #2 in full!</h2>                    <h3>Invoice Details</h3>                    <p><b>Invoice ID</b>:202322300708765</p>                    <p><b>Invoice Amount</b>:4000.00</p>                    <p><b>Balance</b>:0.0</p>                    <p><b>Due Date</b>:2023-08-16</p><p>Rent Installment</p>', '2023-08-11', 0.00, 2, 'cash', '443uGd4t'),
	(19, 1000.00, '<h2 style=\'color:green;\'>Payment of invoice #202322300708765 partially!</h2>                    <h3>Invoice Details</h3>                    <p><b>Invoice ID</b>:202322300708765</p>                    <p><b>Invoice Amount</b>:4000.00</p>                    <p><b>Balance</b>:1000.0</p>                    <p><b>Due Date</b>:2023-08-16</p><p>Rent Installment</p>', '2023-08-11', 1000.00, 2, 'cash', '4YiJ829f'),
	(20, 1.00, '<h2 style="color: green;">Payment of invoice #202322300708765 partially!</h2>\r\n<h3>Invoice Details</h3>\r\n<p><strong>Invoice ID</strong>:202322300708765</p>\r\n<p><strong>Invoice Amount</strong>:4000.00</p>\r\n<p><strong>Balance</strong>:999.0</p>\r\n<p><strong>Due Date</strong>:2023-08-16</p>\r\n<p>Rent Installment</p>', '2023-08-16', 999.00, 2, 'mobile', 'RHG7894U33'),
	(21, 1.00, '<h2 style="color: green;">Payment of invoice #202322300708765 partially!</h2>\r\n<h3>Invoice Details</h3>\r\n<p><strong>Invoice ID</strong>:202322300708765</p>\r\n<p><strong>Invoice Amount</strong>:4000.00</p>\r\n<p><strong>Balance</strong>:998.0</p>\r\n<p><strong>Due Date</strong>:2023-08-16</p>\r\n<p>Rent Installment</p>', '2023-08-16', 998.00, 2, 'mobile', 'RHG0897AQ0'),
	(22, 1.00, '<h2 style=\'color:green;\'>Payment of invoice #202322300708765 partially!</h2>                    <h3>Invoice Details</h3>                    <p><b>Invoice ID</b>:202322300708765</p>                    <p><b>Invoice Amount</b>:4000.00</p>                    <p><b>Balance</b>:997.0</p>                    <p><b>Due Date</b>:2023-08-16</p><p>Rent Installment</p>', '2023-08-16', 997.00, 2, 'Mobile Money', 'RHG1899RIP'),
	(23, 1.00, '<h2 style=\'color:green;\'>Payment of invoice #202322300708765 partially!</h2>                    <h3>Invoice Details</h3>                    <p><b>Invoice ID</b>:202322300708765</p>                    <p><b>Invoice Amount</b>:4000.00</p>                    <p><b>Balance</b>:996.0</p>                    <p><b>Due Date</b>:2023-08-16</p><p>Rent Installment</p>', '2023-08-16', 996.00, 2, 'Mobile Money', 'RHG18PC8MV');

-- Dumping structure for table realestate.properties
DROP TABLE IF EXISTS `properties`;
CREATE TABLE IF NOT EXISTS `properties` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `address` varchar(255) NOT NULL,
  `city` varchar(255) NOT NULL,
  `country` varchar(255) NOT NULL,
  `property_type` varchar(20) NOT NULL,
  `property_name` varchar(255) NOT NULL,
  `description` longtext NOT NULL,
  `amenities` longtext NOT NULL,
  `property_status` varchar(20) NOT NULL,
  `year_built` int unsigned NOT NULL,
  `square_footage` int unsigned NOT NULL,
  `is_featured` tinyint(1) NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `updated_at` datetime(6) NOT NULL,
  `owner_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  KEY `properties_owner_id_f88fce84_fk_landlords_propertyowner_id` (`owner_id`),
  CONSTRAINT `properties_owner_id_f88fce84_fk_landlords_propertyowner_id` FOREIGN KEY (`owner_id`) REFERENCES `landlords_propertyowner` (`id`),
  CONSTRAINT `properties_chk_1` CHECK ((`year_built` >= 0)),
  CONSTRAINT `properties_chk_2` CHECK ((`square_footage` >= 0))
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 ;

-- Dumping data for table realestate.properties: ~0 rows (approximately)
INSERT IGNORE INTO `properties` (`id`, `address`, `city`, `country`, `property_type`, `property_name`, `description`, `amenities`, `property_status`, `year_built`, `square_footage`, `is_featured`, `created_at`, `updated_at`, `owner_id`) VALUES
	(1, 'addr', 'Oyugis', 'Kenya', 'apartment', 'Fernbrook Apartments', '<p>The best homes in Oyugis</p>', '<p>N/A</p>', 'available', 2023, 20, 1, '2023-08-11 11:16:58.297311', '2023-08-11 13:57:42.799227', 1);

-- Dumping structure for table realestate.properties_units
DROP TABLE IF EXISTS `properties_units`;
CREATE TABLE IF NOT EXISTS `properties_units` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `property_id` bigint NOT NULL,
  `units_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `properties_units_property_id_units_id_e5e3215b_uniq` (`property_id`,`units_id`),
  KEY `properties_units_units_id_f10de146_fk_units_id` (`units_id`),
  CONSTRAINT `properties_units_property_id_25cf38d5_fk_properties_id` FOREIGN KEY (`property_id`) REFERENCES `properties` (`id`),
  CONSTRAINT `properties_units_units_id_f10de146_fk_units_id` FOREIGN KEY (`units_id`) REFERENCES `units` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 ;

-- Dumping data for table realestate.properties_units: ~0 rows (approximately)
INSERT IGNORE INTO `properties_units` (`id`, `property_id`, `units_id`) VALUES
	(1, 1, 1);

-- Dumping structure for table realestate.property_images
DROP TABLE IF EXISTS `property_images`;
CREATE TABLE IF NOT EXISTS `property_images` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `image` varchar(100) NOT NULL,
  `property_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  KEY `property_images_property_id_16381827_fk_properties_id` (`property_id`),
  CONSTRAINT `property_images_property_id_16381827_fk_properties_id` FOREIGN KEY (`property_id`) REFERENCES `properties` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 ;

-- Dumping data for table realestate.property_images: ~2 rows (approximately)
INSERT IGNORE INTO `property_images` (`id`, `image`, `property_id`) VALUES
	(1, 'property/images/partment_2_xkQUFn0.jpg', 1),
	(2, 'property/images/partment_3_6dF4jWy.jpg', 1);

-- Dumping structure for table realestate.property_unit_images
DROP TABLE IF EXISTS `property_unit_images`;
CREATE TABLE IF NOT EXISTS `property_unit_images` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `image` varchar(100) NOT NULL,
  `property_unit_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  KEY `property_unit_images_property_unit_id_ad2a94d7_fk_units_id` (`property_unit_id`),
  CONSTRAINT `property_unit_images_property_unit_id_ad2a94d7_fk_units_id` FOREIGN KEY (`property_unit_id`) REFERENCES `units` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 ;

-- Dumping data for table realestate.property_unit_images: ~2 rows (approximately)
INSERT IGNORE INTO `property_unit_images` (`id`, `image`, `property_unit_id`) VALUES
	(1, 'property_units/images/photo2_cyUaWMh_avHIqen.png', 1),
	(2, 'property_units/images/img_6.jpg', 1);

-- Dumping structure for table realestate.services
DROP TABLE IF EXISTS `services`;
CREATE TABLE IF NOT EXISTS `services` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `service_name` varchar(100) NOT NULL,
  `service_img_or_icon` varchar(100) DEFAULT NULL,
  `content` longtext NOT NULL,
  `published` tinyint(1) NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `property_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  KEY `services_property_id_b3423874_fk_properties_id` (`property_id`),
  CONSTRAINT `services_property_id_b3423874_fk_properties_id` FOREIGN KEY (`property_id`) REFERENCES `properties` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 ;

-- Dumping data for table realestate.services: ~0 rows (approximately)

-- Dumping structure for table realestate.staff
DROP TABLE IF EXISTS `staff`;
CREATE TABLE IF NOT EXISTS `staff` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `mobile_number` varchar(13) NOT NULL,
  `national_id` varchar(10) DEFAULT NULL,
  `ID_Snapshot` varchar(100) DEFAULT NULL,
  `position` varchar(100) NOT NULL,
  `date_of_joining` date NOT NULL,
  `created_by_id` bigint NOT NULL,
  `user_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `user_id` (`user_id`),
  KEY `staff_created_by_id_874d75d7_fk_account_customuser_id` (`created_by_id`),
  CONSTRAINT `staff_created_by_id_874d75d7_fk_account_customuser_id` FOREIGN KEY (`created_by_id`) REFERENCES `account_customuser` (`id`),
  CONSTRAINT `staff_user_id_e6242ba6_fk_account_customuser_id` FOREIGN KEY (`user_id`) REFERENCES `account_customuser` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 ;

-- Dumping data for table realestate.staff: ~0 rows (approximately)

-- Dumping structure for table realestate.staff_deduction
DROP TABLE IF EXISTS `staff_deduction`;
CREATE TABLE IF NOT EXISTS `staff_deduction` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `name` varchar(100) NOT NULL,
  `amount` decimal(10,2) NOT NULL,
  `staff_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  KEY `staff_deduction_staff_id_517844f1_fk_staff_id` (`staff_id`),
  CONSTRAINT `staff_deduction_staff_id_517844f1_fk_staff_id` FOREIGN KEY (`staff_id`) REFERENCES `staff` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 ;

-- Dumping data for table realestate.staff_deduction: ~0 rows (approximately)

-- Dumping structure for table realestate.staff_earning
DROP TABLE IF EXISTS `staff_earning`;
CREATE TABLE IF NOT EXISTS `staff_earning` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `name` varchar(100) NOT NULL,
  `amount` decimal(10,2) NOT NULL,
  `staff_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  KEY `staff_earning_staff_id_9722e4a5_fk_staff_id` (`staff_id`),
  CONSTRAINT `staff_earning_staff_id_9722e4a5_fk_staff_id` FOREIGN KEY (`staff_id`) REFERENCES `staff` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 ;

-- Dumping data for table realestate.staff_earning: ~0 rows (approximately)

-- Dumping structure for table realestate.staff_payments
DROP TABLE IF EXISTS `staff_payments`;
CREATE TABLE IF NOT EXISTS `staff_payments` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `month` int unsigned NOT NULL,
  `year` int unsigned NOT NULL,
  `date_of_pyament` datetime(6) NOT NULL,
  `net_pay` decimal(10,2) NOT NULL,
  `staff_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  KEY `staff_payments_staff_id_89d3aacf_fk_staff_id` (`staff_id`),
  CONSTRAINT `staff_payments_staff_id_89d3aacf_fk_staff_id` FOREIGN KEY (`staff_id`) REFERENCES `staff` (`id`),
  CONSTRAINT `staff_payments_chk_1` CHECK ((`month` >= 0)),
  CONSTRAINT `staff_payments_chk_2` CHECK ((`year` >= 0))
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 ;

-- Dumping data for table realestate.staff_payments: ~0 rows (approximately)

-- Dumping structure for table realestate.staff_salary
DROP TABLE IF EXISTS `staff_salary`;
CREATE TABLE IF NOT EXISTS `staff_salary` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `net_salary` decimal(10,2) NOT NULL,
  `staff_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  KEY `staff_salary_staff_id_1ff48e83_fk_staff_id` (`staff_id`),
  CONSTRAINT `staff_salary_staff_id_1ff48e83_fk_staff_id` FOREIGN KEY (`staff_id`) REFERENCES `staff` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 ;

-- Dumping data for table realestate.staff_salary: ~0 rows (approximately)

-- Dumping structure for table realestate.staff_salary_deductions
DROP TABLE IF EXISTS `staff_salary_deductions`;
CREATE TABLE IF NOT EXISTS `staff_salary_deductions` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `staffsalary_id` bigint NOT NULL,
  `deduction_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `staff_salary_deductions_staffsalary_id_deduction_70b7127e_uniq` (`staffsalary_id`,`deduction_id`),
  KEY `staff_salary_deducti_deduction_id_95b4f40b_fk_staff_ded` (`deduction_id`),
  CONSTRAINT `staff_salary_deducti_deduction_id_95b4f40b_fk_staff_ded` FOREIGN KEY (`deduction_id`) REFERENCES `staff_deduction` (`id`),
  CONSTRAINT `staff_salary_deducti_staffsalary_id_6a44f38d_fk_staff_sal` FOREIGN KEY (`staffsalary_id`) REFERENCES `staff_salary` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 ;

-- Dumping data for table realestate.staff_salary_deductions: ~0 rows (approximately)

-- Dumping structure for table realestate.staff_salary_earnings
DROP TABLE IF EXISTS `staff_salary_earnings`;
CREATE TABLE IF NOT EXISTS `staff_salary_earnings` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `staffsalary_id` bigint NOT NULL,
  `earning_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `staff_salary_earnings_staffsalary_id_earning_id_559936f5_uniq` (`staffsalary_id`,`earning_id`),
  KEY `staff_salary_earnings_earning_id_702ecb72_fk_staff_earning_id` (`earning_id`),
  CONSTRAINT `staff_salary_earnings_earning_id_702ecb72_fk_staff_earning_id` FOREIGN KEY (`earning_id`) REFERENCES `staff_earning` (`id`),
  CONSTRAINT `staff_salary_earnings_staffsalary_id_af1285bf_fk_staff_salary_id` FOREIGN KEY (`staffsalary_id`) REFERENCES `staff_salary` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 ;

-- Dumping data for table realestate.staff_salary_earnings: ~0 rows (approximately)

-- Dumping structure for table realestate.tenants_tenant
DROP TABLE IF EXISTS `tenants_tenant`;
CREATE TABLE IF NOT EXISTS `tenants_tenant` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `current_status` varchar(10) NOT NULL,
  `date_of_birth` date NOT NULL,
  `National_ID` varchar(10) NOT NULL,
  `date_of_registration` date NOT NULL,
  `mobile_number` varchar(13) NOT NULL,
  `others` longtext,
  `created_by_id` bigint NOT NULL,
  `user_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `user_id` (`user_id`),
  KEY `tenants_tenant_created_by_id_f3e30a24_fk_account_customuser_id` (`created_by_id`),
  CONSTRAINT `tenants_tenant_created_by_id_f3e30a24_fk_account_customuser_id` FOREIGN KEY (`created_by_id`) REFERENCES `account_customuser` (`id`),
  CONSTRAINT `tenants_tenant_user_id_bbceef8a_fk_account_customuser_id` FOREIGN KEY (`user_id`) REFERENCES `account_customuser` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 ;

-- Dumping data for table realestate.tenants_tenant: ~0 rows (approximately)
INSERT IGNORE INTO `tenants_tenant` (`id`, `current_status`, `date_of_birth`, `National_ID`, `date_of_registration`, `mobile_number`, `others`, `created_by_id`, `user_id`) VALUES
	(2, 'active', '2023-08-11', '8993381', '2023-08-11', '+254743793901', 'N/A', 1, 4);

-- Dumping structure for table realestate.tenants_tenant_business_details
DROP TABLE IF EXISTS `tenants_tenant_business_details`;
CREATE TABLE IF NOT EXISTS `tenants_tenant_business_details` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `business_name` varchar(100) NOT NULL,
  `license_number` varchar(100) NOT NULL,
  `tax_id` varchar(100) NOT NULL,
  `business_email` varchar(100) NOT NULL,
  `business_address` longtext NOT NULL,
  `business_description` longtext NOT NULL,
  `tenant_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  KEY `tenants_tenant_busin_tenant_id_e52467fa_fk_tenants_t` (`tenant_id`),
  CONSTRAINT `tenants_tenant_busin_tenant_id_e52467fa_fk_tenants_t` FOREIGN KEY (`tenant_id`) REFERENCES `tenants_tenant` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 ;

-- Dumping data for table realestate.tenants_tenant_business_details: ~0 rows (approximately)

-- Dumping structure for table realestate.tenants_tenant_employment_details
DROP TABLE IF EXISTS `tenants_tenant_employment_details`;
CREATE TABLE IF NOT EXISTS `tenants_tenant_employment_details` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `employment_status` varchar(50) NOT NULL,
  `emplyment_title` varchar(100) NOT NULL,
  `employment_postion` varchar(100) NOT NULL,
  `employer_contact` varchar(13) NOT NULL,
  `employer_email` varchar(100) NOT NULL,
  `employer_address` longtext NOT NULL,
  `tenant_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  KEY `tenants_tenant_emplo_tenant_id_3d07b6ff_fk_tenants_t` (`tenant_id`),
  CONSTRAINT `tenants_tenant_emplo_tenant_id_3d07b6ff_fk_tenants_t` FOREIGN KEY (`tenant_id`) REFERENCES `tenants_tenant` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 ;

-- Dumping data for table realestate.tenants_tenant_employment_details: ~0 rows (approximately)

-- Dumping structure for table realestate.tenants_tenant_kin
DROP TABLE IF EXISTS `tenants_tenant_kin`;
CREATE TABLE IF NOT EXISTS `tenants_tenant_kin` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `name` varchar(200) NOT NULL,
  `phone` varchar(13) NOT NULL,
  `relation` varchar(100) NOT NULL,
  `emergency_name` varchar(100) NOT NULL,
  `emergency_phone_number` varchar(13) NOT NULL,
  `emergency_email` varchar(100) NOT NULL,
  `emergency_adress` longtext NOT NULL,
  `emergency_physical_adress` longtext NOT NULL,
  `tenant_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  KEY `tenants_tenant_kin_tenant_id_b15f1153_fk_tenants_tenant_id` (`tenant_id`),
  CONSTRAINT `tenants_tenant_kin_tenant_id_b15f1153_fk_tenants_tenant_id` FOREIGN KEY (`tenant_id`) REFERENCES `tenants_tenant` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 ;

-- Dumping data for table realestate.tenants_tenant_kin: ~0 rows (approximately)
INSERT IGNORE INTO `tenants_tenant_kin` (`id`, `name`, `phone`, `relation`, `emergency_name`, `emergency_phone_number`, `emergency_email`, `emergency_adress`, `emergency_physical_adress`, `tenant_id`) VALUES
	(2, 'Wicliffe Wara', '+254743793901', 'Husband', 'Obuon', '+254743793901', 'obuon.wara@fernbrookapartments.com', '1234', '1234', 2);

-- Dumping structure for table realestate.testimonials
DROP TABLE IF EXISTS `testimonials`;
CREATE TABLE IF NOT EXISTS `testimonials` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `designation` varchar(100) NOT NULL,
  `rating` varchar(1) NOT NULL,
  `content` longtext NOT NULL,
  `published` tinyint(1) NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `property_id` bigint DEFAULT NULL,
  `user_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  KEY `testimonials_property_id_0143456c_fk_properties_id` (`property_id`),
  KEY `testimonials_user_id_ae44a7e2_fk_account_customuser_id` (`user_id`),
  CONSTRAINT `testimonials_property_id_0143456c_fk_properties_id` FOREIGN KEY (`property_id`) REFERENCES `properties` (`id`),
  CONSTRAINT `testimonials_user_id_ae44a7e2_fk_account_customuser_id` FOREIGN KEY (`user_id`) REFERENCES `account_customuser` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 ;

-- Dumping data for table realestate.testimonials: ~1 rows (approximately)

-- Dumping structure for table realestate.units
DROP TABLE IF EXISTS `units`;
CREATE TABLE IF NOT EXISTS `units` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `title` varchar(100) NOT NULL,
  `unit_code` varchar(100) NOT NULL,
  `description` longtext NOT NULL,
  `rental_price` decimal(8,2) NOT NULL,
  `square_footage` int unsigned NOT NULL,
  `bedrooms` int unsigned NOT NULL,
  `bathrooms` int unsigned NOT NULL,
  `unit_type` varchar(20) NOT NULL,
  `is_featured` tinyint(1) NOT NULL,
  `is_available` tinyint(1) NOT NULL,
  PRIMARY KEY (`id`),
  CONSTRAINT `units_chk_1` CHECK ((`square_footage` >= 0)),
  CONSTRAINT `units_chk_2` CHECK ((`bedrooms` >= 0)),
  CONSTRAINT `units_chk_3` CHECK ((`bathrooms` >= 0))
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 ;

-- Dumping data for table realestate.units: ~0 rows (approximately)
INSERT IGNORE INTO `units` (`id`, `title`, `unit_code`, `description`, `rental_price`, `square_footage`, `bedrooms`, `bathrooms`, `unit_type`, `is_featured`, `is_available`) VALUES
	(1, 'test', '001', '<p>Test 001</p>', 3000.00, 6, 1, 1, '1br', 1, 1);

-- Dumping structure for table realestate.units_property_unit_images
DROP TABLE IF EXISTS `units_property_unit_images`;
CREATE TABLE IF NOT EXISTS `units_property_unit_images` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `units_id` bigint NOT NULL,
  `propertyunitimages_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `units_property_unit_imag_units_id_propertyunitima_430f91ca_uniq` (`units_id`,`propertyunitimages_id`),
  KEY `units_property_unit__propertyunitimages_i_a853ea1c_fk_property_` (`propertyunitimages_id`),
  CONSTRAINT `units_property_unit__propertyunitimages_i_a853ea1c_fk_property_` FOREIGN KEY (`propertyunitimages_id`) REFERENCES `property_unit_images` (`id`),
  CONSTRAINT `units_property_unit_images_units_id_113cf4fd_fk_units_id` FOREIGN KEY (`units_id`) REFERENCES `units` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- Dumping data for table realestate.units_property_unit_images: ~0 rows (approximately)

/*!40103 SET TIME_ZONE=IFNULL(@OLD_TIME_ZONE, 'system') */;
/*!40101 SET SQL_MODE=IFNULL(@OLD_SQL_MODE, '') */;
/*!40014 SET FOREIGN_KEY_CHECKS=IFNULL(@OLD_FOREIGN_KEY_CHECKS, 1) */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40111 SET SQL_NOTES=IFNULL(@OLD_SQL_NOTES, 1) */;
