-- a SQL script that creates a stored procedure
-- ComputeAverageWeightedScoreForUsers that computes and store
-- the average weighted score for all students
DELIMITER $$

CREATE PROCEDURE ComputeAverageWeightedScoreForUsers()
BEGIN
	DECLARE done INT DEFAULT FALSE;
	DECLARE user_id_val INT;
	DECLARE total_score DECIMAL(10, 2);
	DECLARE total_weight DECIMAL(10, 2);
	DECLARE average_score DECIMAL(10, 2);

	DECLARE users_cursor CURSOR FOR 

	SELECT DISTINCT user_id FROM scores;

	DECLARE CONTINUE HANDLER FOR NOT FOUND SET done = TRUE;

	OPEN users_cursor;
	read_loop: LOOP
	FETCH users_cursor INTO user_id_val;
	IF done THEN
		LEAVE read_loop;
	END IF;

	SELECT SUM(score * weight), SUM(weight)
	INTO total_score, total_weight
	FROM scores
        WHERE user_id = user_id_val;

        IF total_weight > 0 THEN
            SET average_score = total_score / total_weight;
        ELSE
            SET average_score = 0;
        END IF;

        INSERT INTO average_weighted_scores (user_id, average_score)
        VALUES (user_id_val, average_score)
        ON DUPLICATE KEY UPDATE average_score = average_score;
    END LOOP;

    CLOSE users_cursor;
    
END $$

DELIMITER ;
