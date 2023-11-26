DELIMITER //
CREATE TRIGGER restrict_case_access
BEFORE SELECT ON cases
FOR EACH ROW
BEGIN
    DECLARE detective_id INT;
    SET detective_id = (SELECT detective_id FROM detectives WHERE detective_id = NEW.detective_id);
END;
//
DELIMITER ;
