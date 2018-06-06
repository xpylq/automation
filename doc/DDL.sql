drop database if exists automation;
create database automation CHARACTER SET 'utf8' COLLATE 'utf8_general_ci';
use automation;
DROP TABLE IF EXISTS `automation_user`;
CREATE TABLE `automation_user` (
  `id` BIGINT(20) NOT NULL AUTO_INCREMENT,
  `name` VARCHAR(32) NOT NULL COMMENT '账号',
  `password` VARCHAR(64) NOT NULL COMMENT '密码',
  `type` INT NOT NULL COMMENT '账号类型(1:豆瓣,2:知乎)',
  `isNew` INT NOT NULL DEFAULT '1' COMMENT '是否才注册(0:已注册,1:才注册)',
  `loginFlag` INT  NOT NULL DEFAULT '0' COMMENT '登录状态(0:未登录,1:已登录)',
  `cookies` VARCHAR (2000) DEFAULT NULL  COMMENT 'cookie序列化',
   PRIMARY KEY (`id`),
   INDEX `idx_type_loginFlag` (`type`,`loginFlag`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='用户表';