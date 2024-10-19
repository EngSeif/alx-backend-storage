-- ranks country origins of bands
-- ordered by the number of (non-unique) fans

DELIMITER $$

CREATE PROCEDURE ComputeAverageWeightedScoreForUser(IN user_id INT)
BEGIN
    DECLARE total_weight_score FLOAT DEFAULT 0;
    DECLARE total_weight INT DEFAULT 0;

    SELECT 
    SUM(c.score * (SELECT p.weight FROM projects p WHERE p.id = c.project_id))
    INTO total_weight_score
    FROM corrections c
    WHERE c.user_id = user_id;

    SELECT SUM((SELECT p.weight FROM projects p WHERE p.id = c.project_id))
    INTO total_weight
    FROM corrections c
    WHERE c.user_id = user_id;

    IF total_weight > 0 THEN
        UPDATE users
        SET average_score = total_weight_score / total_weight
        WHERE id = user_id;
    ELSE
        UPDATE users
        SET average_score = avg_weighted_score
        WHERE id = user_id;
    END IF;
END $$

DELIMITER ;