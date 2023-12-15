-- a SQL script that creates a stored procedure
-- ComputeAverageWeightedScoreForUser that computes and store the
-- average weighted score for a student.
DROP PROCEDURE IF EXISTS ComputeAverageWeightedScoreForUser;
DELIMITER $$

CREATE PROCEDURE ComputeAverageWeightedScoreForUser(IN user_id INT)
BEGIN
    DECLARE total_weighted_score DECIMAL(10, 2) DEFAULT 0;
    DECLARE total_weight DECIMAL(10, 2) DEFAULT 0;
    DECLARE average_score DECIMAL(10, 2);

    SELECT SUM(score * weight), SUM(weight)
    INTO total_weighted_score, total_weight
    FROM scores
    WHERE user_id = user_id;

    IF total_weight = 0 THEN
        SET average_score = 0;
    ELSE
        SET average_score = total_weighted_score / total_weight;
    END IF;

    INSERT INTO average_weighted_scores (user_id, average_score)
    VALUES (user_id, average_score)
    ON DUPLICATE KEY UPDATE average_score = average_score;

END $$
DELIMITER ;
