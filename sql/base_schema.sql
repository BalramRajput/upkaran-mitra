-- create database upkaranamitra.db (sqlite3 upkaranmitra.db)

CREATE TABLE `country` (
    `country_id` INTEGER PRIMARY KEY,
    `country_name` TEXT NOT NULL
);

CREATE TABLE `state` (
    `state_id` INTEGER PRIMARY KEY,
    `state_name` TEXT NOT NULL,
    `country_id` INTEGER NOT NULL,
    FOREIGN KEY (`country_id`) REFERENCES `country` (`country_id`) ON DELETE CASCADE
);

CREATE TABLE `district` (
    `district_id` INTEGER PRIMARY KEY,
    `district_name` TEXT NOT NULL,
    `state_id` INTEGER NOT NULL,
    FOREIGN KEY (`state_id`) REFERENCES `state` (`state_id`) ON DELETE CASCADE
);

CREATE TABLE `sub_district` (
    `sub_district_id` INTEGER PRIMARY KEY,
    `sub_district_name` TEXT NOT NULL,
    `district_id` INTEGER NOT NULL,
    FOREIGN KEY (`district_id`) REFERENCES `district` (`district_id`) ON DELETE CASCADE
);

CREATE TABLE `village` (
    `village_id` INTEGER PRIMARY KEY,
    `village_name` TEXT NOT NULL,
    `sub_district_id` INTEGER NOT NULL,
    FOREIGN KEY (`sub_district_id`) REFERENCES `sub_district` (`sub_district_id`) ON DELETE CASCADE
);

CREATE INDEX `idx_sub_district_id` ON `village`(`sub_district_id`);
CREATE INDEX `idx_district_id` ON `sub_district`(`district_id`);
CREATE INDEX `idx_state_id` ON `district`(`state_id`);
CREATE INDEX `idx_country_id` ON `state`(`country_id`);


CREATE TABLE `address` (
    `id` INTEGER PRIMARY KEY AUTOINCREMENT,
    `address_line1` TEXT NOT NULL,
    `address_line2` TEXT,
    `village_id` INTEGER NOT NULL,
    `zipcode` INTEGER NOT NULL,
    FOREIGN KEY (`village_id`) REFERENCES `village`(`village_id`)
);

CREATE TABLE `user`(
    `id` INTEGER PRIMARY KEY AUTOINCREMENT,
    `name` TEXT,
    `phone_number` TEXT NOT NULL UNIQUE,
    `email` TEXT,
    `password` TEXT NOT NULL,
    `address_id` INTEGER NOT NULL,
    FOREIGN KEY (`address_id`) REFERENCES `address`(`id`)
);

CREATE TABLE `equipment_category`(
    `id` INTEGER PRIMARY KEY AUTOINCREMENT,
    `name` TEXT NOT NULL,
    `is_vehicle_type` INTEGER NOT NULL CHECK (`is_vehicle_type` IN (0,1))
);

CREATE TABLE `user_equipments`(
    `id` INTEGER PRIMARY KEY AUTOINCREMENT,
    `user_id` INTEGER NOT NULL,
    `name` TEXT,
    `equipment_category_id` INTEGER NOT NULL,
    `used_for` TEXT,
    `image` BLOB,
    `rate` INTEGER,
    `unit` TEXT,
    `specification` TEXT,
    FOREIGN KEY (`user_id`) REFERENCES `user`(`id`),
    FOREIGN KEY (`equipment_category_id`) REFERENCES `equipment_category`(`id`)
);

CREATE TABLE `booking`(
    `id` INTEGER PRIMARY KEY AUTOINCREMENT,
    `user_id` INTEGER NOT NULL,
    `user_equipment_id` INTEGER NOT NULL,
    `booked_at` TEXT,
    `started_at` TEXT,
    `completed_at` TEXT,
    `amount` INTEGER,
    `is_payment_done` INTEGER NOT NULL CHECK (`is_payment_done` IN (0,1)),
    FOREIGN KEY (`user_id`) REFERENCES `user`(`id`)
    FOREIGN KEY (`user_equipment_id`) REFERENCES `user_equipments`(`id`)
);

ALTER TABLE `user_equipments` ADD COLUMN `is_available` INTEGER NOT NULL CHECK (`is_available` IN (0,1));