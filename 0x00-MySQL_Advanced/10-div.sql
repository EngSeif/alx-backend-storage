-- ranks country origins of bands
-- ordered by the number of (non-unique) fans

DELIMITER $$

CREATE FUNCTION SafeDiv(a INT,b INT)
RETURNS FLOAT
DETERMINISTIC
BEGIN
    IF b = 0 THEN
        RETURN 0;
    ELSE
        RETURN a / b;
    END IF;

END $$

DELIMITER ;
