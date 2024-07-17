USE covid19;

DROP VIEW IF EXISTS latest_condition;

CREATE VIEW latest_condition AS
SELECT *
FROM condition_details_table cdt
WHERE (cdt.userID, cdt.condition_date) IN (
    SELECT userID, MAX(condition_date) AS max_date
    FROM condition_details_table
    GROUP BY userID
);

DROP VIEW IF EXISTS latest_action;

CREATE VIEW latest_action AS
SELECT *
FROM action_table 
WHERE (action_table.userID,action_table.action_date_start) IN (
    SELECT userID,MAX(action_date_start) as max_date
    FROM action_table
    GROUP BY userID
);

CREATE VIEW latest_vaccination as 
SELECT *
FROM vaccination_table as vt
WHERE (vt.userID,vt.vaccination_num) IN (
    SELECT userID,MAX(vaccination_num) as max_num
    FROM vaccination_table
    GROUP BY userID
);

SELECT 
    user_table.user_num,
    user_table.user_name,
    latest_condition.body_temp,
    latest_condition.condition_date,
    latest_action.action_date_start,
    latest_vaccination.vaccination_num,
    latest_vaccination.vaccination_date
FROM user_table
LEFT JOIN latest_action
ON user_table.userID = latest_action.userID
LEFT JOIN latest_condition
on user_table.userID=latest_condition.userID
LEFT JOIN latest_vaccination
on user_table.userID=latest_vaccination.userID
;

-- SELECT * FROM latest_condition;
-- SELECT * FROM latest_action;
