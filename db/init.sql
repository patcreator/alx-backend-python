-- messaging_app/db/init.sql
-- This file runs when the MySQL container starts
CREATE DATABASE IF NOT EXISTS messaging_db;
GRANT ALL PRIVILEGES ON messaging_db.* TO 'messaging_user'@'%';
FLUSH PRIVILEGES;