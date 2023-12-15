-- a SQL script that creates a trigger that resets the attribute
-- valid_email only when the email has been changed.
DROP TRIGGER IF EXISTS listen_email;
DELIMITER $$
CREATE TRIGGER listen_email
BEFORE UPDATE ON users
FOR EACH ROW
BEGIN
	IF NEW.email <> OLD.email THEN
		SET NEW.valid_email = (SELECT COLUMN_DEFAULT
			FROM information_schema.COLUMNS
			WHERE TABLE_NAME = 'users'
			AND COLUMN_NAME = 'valid_email');
        END IF;
END $$
DELIMITER ;
