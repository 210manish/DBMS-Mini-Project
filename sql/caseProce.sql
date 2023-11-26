DELIMITER //

CREATE PROCEDURE InsertNewCase(
         IN case_id VARCHAR(20),
         IN p_o_c VARCHAR(25),
         IN det_id VARCHAR(20),
         IN status BOOLEAN,
         IN case_details VARCHAR(520)
     )
     BEGIN
         DECLARE duplicateCase INT;

         -- Check if a case with the same ID already exists
         SELECT COUNT(*) INTO duplicateCase
         FROM Cases
         WHERE case_details = case_details;

         IF duplicateCase > 0 THEN
             -- Raise a custom error if a duplicate case is found
             SIGNAL SQLSTATE '45000'
                 SET MESSAGE_TEXT = 'A case with the same details already exists.';
         ELSE
             -- Insert the new case into the database
             INSERT INTO Cases(case_id, p_o_c, det_id,status,case_details)
                 VALUES
                 (case_id, p_o_c, det_id,status,case_details);
         END IF;
     END;
     //

     DELIMITER ;