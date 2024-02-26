SELECT count(*) FROM scrapper_experiment2.scrap_postraw;
SELECT count(*) FROM scrapper_experiment2.scrap_bitstampdataminute where symbol = 'SCHEDULER_TEST';
SELECT * FROM scrapper_experiment2.scrap_errorlog;
DELETE FROM scrapper_experiment2.scrap_bitstampdataminute WHERE symbol = 'SCHEDULER_TEST';
SELECT * 
FROM scrapper_experiment2.scrap_bitstampdatahour
ORDER BY added_at DESC 
LIMIT 1;

-- DELETE FROM scrapper_experiment2.scrap_errorlog;

SELECT count(*) FROM scrapper_experiment2.scrap_postraw;

SELECT DATE(created_at) AS added_date, COUNT(*) AS record_count
FROM scrapper_experiment2.scrap_postraw
GROUP BY DATE(created_at)
ORDER BY DATE(created_at) DESC;

SELECT post_id, COUNT(*) AS count 
FROM scrapper_experiment2.scrap_postraw 
GROUP BY post_id 
ORDER BY count DESC;


SELECT count(*) FROM scrapper_experiment2.scrap_postraw_backup;

##delete duplicate post_id with oldest added_at
-- CREATE TABLE scrapper_experiment2.scrap_postraw_backup LIKE scrapper_experiment2.scrap_postraw;

-- INSERT INTO scrapper_experiment2.scrap_postraw_backup
-- SELECT * FROM scrapper_experiment2.scrap_postraw_backup;


-- DELETE scrap_errorpost
-- FROM scrap_errorpost
-- JOIN (
--     SELECT post_id, MIN(added_at) AS min_added_at
--     FROM scrap_errorpost
--     GROUP BY post_id
--     HAVING COUNT(*) > 1
-- ) AS duplicates ON scrap_errorpost.post_id = duplicates.post_id 
--                 AND scrap_errorpost.added_at = duplicates.min_added_at;




SELECT error_message, count(distinct post_id) FROM scrapper_experiment2.scrap_errorpost group by error_message;
SELECT DISTINCT post_id, count(*) as count FROM scrapper_experiment2.scrap_errorpost group by post_id order by count desc;
