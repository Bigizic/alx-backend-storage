-- a SQL script that ranks country origins of bands, ordered by
-- the number of (non-unique) fans
SELECT origin, SUM(nb_fans) as total_fans
FROM bands
GROUP BY origin
ORDER BY total_fans DESC;
