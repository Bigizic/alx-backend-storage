-- a SQL script that lists all bands with Glam rock as their main style,
-- ranked by their longevity
SELECT band_name, (2022 - formed) - (2022 - split) AS lifespan
FROM metal_bands
WHERE style LIKE '%Glam rock%';
ORDER BY lifespan DESC;