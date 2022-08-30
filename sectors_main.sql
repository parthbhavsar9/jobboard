CREATE TABLE `sectors` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(100) DEFAULT NULL,
  `percentage` int DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=8 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

insert into sectors (name, percentage) values ('Banking',3);
insert into sectors (name, percentage) values ('Energy',6);
insert into sectors (name, percentage) values ('Information',9);
insert into sectors (name, percentage) values ('Healthcare',3);
insert into sectors (name, percentage) values ('Travel',6);
insert into sectors (name, percentage) values ('Construction',9);
insert into sectors (name, percentage) values ('Education',3);

select * from sectors;
