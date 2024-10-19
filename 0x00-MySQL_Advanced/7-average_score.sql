-- ranks country origins of bands
-- ordered by the number of (non-unique) fans

DELIMITER $$

CREATE PROCEDURE ComputeAverageScoreForUser(IN input_user_id INT)
BEGIN
    DECLARE correction_count INT DEFAULT 0;
    DECLARE project_sum FLOAT DEFAULT 0;

    -- Count the number of corrections for the given user
    SELECT COUNT(*) INTO correction_count
    FROM corrections
    WHERE user_id = input_user_id;

    -- Sum the scores from corrections for the given user
    SELECT SUM(score) INTO project_sum
    FROM corrections 
    WHERE user_id = input_user_id;

    -- Calculate and update the average score in the users table
    IF correction_count > 0 THEN
        UPDATE users 
        SET average_score = project_sum / correction_count
        WHERE id = input_user_id;
    ELSE
        UPDATE users 
        SET average_score = 0
        WHERE id = input_user_id;
    END IF;

END $$

DELIMITER ;