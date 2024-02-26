-- First, create the tables in the destination schema if they don't exist
CREATE TABLE IF NOT EXISTS scrapper_experiment2.scrap_errorpost AS
SELECT * FROM scrapper_experiment.scrap_errorpost WHERE 1=0; -- This creates an empty table with the same structure

CREATE TABLE IF NOT EXISTS scrapper_experiment2.scrap_postraw AS
SELECT * FROM scrapper_experiment.scrap_postraw WHERE 1=0; -- This creates an empty table with the same structure

-- Then, insert data into the newly created tables from the source schema
INSERT INTO scrapper_experiment2.scrap_errorpost
SELECT * FROM scrapper_experiment.scrap_errorpost;

INSERT INTO scrapper_experiment2.scrap_postraw
SELECT * FROM scrapper_experiment.scrap_postraw;