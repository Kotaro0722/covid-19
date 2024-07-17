USE covid19;

SELECT *
FROM user_table
LEFT JOIN action_table
ON user_table.userID = action_table.userID;
