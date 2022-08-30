create table experience (
id int primary key auto_increment,
min_exp	int,
max_exp	int,
min	int,
medium int,
max int  );

insert into experience (min_exp, max_exp, min, medium, max) values (0,2,14,21,31);
insert into experience (min_exp, max_exp, min, medium, max) values (2,4,14,21,32);
insert into experience (min_exp, max_exp, min, medium, max) values (4,6,14,21,36);
insert into experience (min_exp, max_exp, min, medium, max) values (6,8,14,21,38);
insert into experience (min_exp, max_exp, min, medium, max) values (8,10,14,21,40);
insert into experience (min_exp, max_exp, min, medium, max) values (10,12,12,18,21);
insert into experience (min_exp, max_exp, min, medium, max) values (12,14,12,18,19);
insert into experience (min_exp, max_exp, min, medium, max) values (14,16,12,15,18);
insert into experience (min_exp, max_exp, min, medium, max) values (16,18,12,11,14);
insert into experience (min_exp, max_exp, min, medium, max) values (18,20,6,7,9);
insert into experience (min_exp, max_exp, min, medium, max) values (20,50,5,6,8);


select * from experience;