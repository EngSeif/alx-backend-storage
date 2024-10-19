-- ranks country origins of bands
-- ordered by the number of (non-unique) fans

DELIMITER $$

CREATE PROCEDURE ComputeAverageScoreForUser(IN input_user_id INT)
BEGIN
    DECLARE avg_score DECIMAL(5, 2);

    SELECT AVG(score) INTO avg_score
    FROM corrections
    WHERE user_id = user_id;

    UPDATE users 
    SET average_score = IFNULL(avg_score, 0)
    WHERE id = input_user_id;

END $$

DELIMITER ;