-- create database upkaranamitra.db (sqlite3 upkaranmitra.db)
CREATE TABLE `address` (
    `id` INTEGER PRIMARY KEY AUTOINCREMENT,
    `address_line1` TEXT NOT NULL,
    `address_line2` TEXT,
    `village` TEXT NOT NULL,
    `city` TEXT NOT NULL,
    `state` TEXT NOT NULL,
    `country` TEXT NOT NULL,
    `zipcode` INTEGER NOT NULL
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