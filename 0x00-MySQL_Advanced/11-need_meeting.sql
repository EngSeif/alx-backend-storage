-- ranks country origins of bands
-- ordered by the number of (non-unique) fans

CREATE VIEW need_meeting As
SELECT name from students
WHERE score < 80
AND (last_meeting IS NULL OR last_meeting < NOW() - INTERVAL 1 MONTH);
