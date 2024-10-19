-- ranks country origins of bands
-- ordered by the number of (non-unique) fans

DELIMITER $$

CREATE PROCEDURE ComputeAverageWeightedScoreForUsers()
BEGIN
    UPDATE users u
    SET u.average_score = (
        SELECT 
            IFNULL(SUM(c.score * (SELECT weight FROM projects WHERE id = c.project_id)) / SUM((SELECT weight FROM projects WHERE id = c.project_id)), 0)
        FROM corrections c
        WHERE c.user_id = u.id
    );
END $$

DELIMITER ;
