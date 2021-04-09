CREATE TABLE `economic` (
    `guild_id` INT,
    `member_id` INT,
    `bank_balance` INT,
    `wallet_balance` INT
);

-- server activity table
CREATE TABLE `server_activity` (
    `guild_id` INT,
    `member_id` INT,
    `user_server_activity` INT,
    `user_level` INT
);

CREATE TABLE `economic_shop_item` (
    `guild_id` INT,
    `role_id` INT,
    `prise` INT
);

CREATE TABLE `graphics_cards` (
   `guild_id` INT,
   `member_id` INT,
   `graphics_cards_name` TEXT,
   `graphics_cards_amount` INT
);


CREATE TABLE `is_mining` (
   `guild_id` INT,
   `member_id` INT,
   `mining` INT
);
