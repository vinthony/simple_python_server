

drop database if exists student_manager;

create database student_manager;

use student_manager;


create table users (
    `id` varchar(50) not null,
    `email` varchar(50) not null,
    `password` varchar(50) not null,
    `identify` bool not null,
    `name` varchar(50) not null,
    `image` varchar(500) not null,
    `created_at` real not null,
    unique key `idx_email` (`email`),
    key `idx_created_at` (`created_at`),
    primary key (`id`)
) engine=innodb default charset=utf8;

create table award (
    `id` varchar(50) not null,
    `award_name` varchar(50) not null,
    `award_user_id` varchar(50) not null,
    `award_is_show` varchar(200) not null,
    `award_content` mediumtext not null,
    `created_at` real not null,
    key `idx_created_at` (`created_at`),
    primary key (`id`)
) engine=innodb default charset=utf8;

create table college (
    `id` varchar(50) not null,
    `college_id` varchar(50) not null,
    `college_name` varchar(50) not null,
    `created_at` real not null,
    key `idx_created_at` (`created_at`),
    primary key (`id`)
) engine=innodb default charset=utf8;

insert into users (`id`, `email`, `password`, `admin`, `name`, `created_at`) values ('0010018336417540987fff4508f43fbaed718e263442526000', 'admin@example.com', 'e10adc3949ba59abbe56e057f20f883e', 1, 'Administrator', 1402909113.628);