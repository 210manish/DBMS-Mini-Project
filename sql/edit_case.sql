UPDATE Cases
SET status = (status+1)%2
WHERE case_id = %s;

