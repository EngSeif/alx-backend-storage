-- ranks country origins of bands
-- ordered by the number of (non-unique) fans

DELIMITER $$

CREATE TRIGGER valid_email
BEFORE UPDATE ON users 
FOR EACH ROW
BEGIN
    IF NEW.email <> OLD.email THEN
        SET NEW.valid_email = 0;
    END IF;
end $$

DELIMITER ;
