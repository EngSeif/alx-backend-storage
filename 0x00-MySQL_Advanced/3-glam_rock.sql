-- ranks country origins of bands
-- ordered by the number of (non-unique) fans

SELECT 
    band_name,
    COALESCE(split, 2022) - formed AS lifespan
FROM 
    metal_bands
WHERE 
    style LIKE '%Glam Rock%'
ORDER BY 
    lifespan DESC;
