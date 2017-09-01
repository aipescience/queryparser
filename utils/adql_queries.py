queries = [

"""SELECT POINT('icrs', 10, 10) FROM db.b;""",
"""SELECT CIRCLE('ICRS', RA, -20/4., 1) FROM db.b""",
"""SELECT BOX('ICRS', 25.4, -20, 1, 1) FROM db.b""",
"""SELECT TOP 10 AREA(CIRCLE('ICRS', RA, -20, 1)) FROM db.b""",
"""SELECT TOP 10 CONTAINS(POINT('ICRS', 0, 0), CIRCLE('ICRS', 0, 0, 1)) FROM db.b""",
"""SELECT DISTANCE(POINT('ICRS', 0, 0), POINT('ICRS', 0, 1)) FROM db.b""",
"""SELECT INTERSECTS(CIRCLE('ICRS', 0, 0, 10), BOX('ICRS', 2, 0, 10, 10)) FROM db.b""",
"""SELECT TOP 10 AREA(CIRCLE('ICRS',  25.4, -20, 1)) FROM db.b""",
"""SELECT CENTROID(CIRCLE('ICRS', RA, -20/4., 1)) FROM db.b""",
"""
SELECT TOP 10 DISTANCE(POINT('ICRS',0,0), POINT('ICRS',"VII/233/xsc".RAJ2000,"VII/233/xsc".DEJ2000))
FROM db."VII/233/xsc"
""",
"""
SELECT *
FROM db."II/246/out"
WHERE 1=CONTAINS(POINT('ICRS',"II/246/out".RAJ2000,"II/246/out".DEJ2000), CIRCLE('ICRS',0,0, 10/60))
""",
"""
SELECT *
FROM db."II/295/SSTGC",db."II/293/glimpse"
WHERE 1=CONTAINS(POINT('ICRS',"II/295/SSTGC".RAJ2000,"II/295/SSTGC".DEJ2000), BOX('GALACTIC', 0, 0, 30/60., 10/60.)) 
  AND 1=CONTAINS(POINT('ICRS',"II/295/SSTGC".RAJ2000,"II/295/SSTGC".DEJ2000), CIRCLE('ICRS',"II/293/glimpse".RAJ2000,"II/293/glimpse".DEJ2000, 2/3600.))
""",
"""
SELECT RA,DE FROM db."tycho2"
WHERE 1=CONTAINS(POINT('ICRS', "tycho2".RA, "tycho2".DE), CIRCLE('ICRS', 75.35, -69.7, 10))
""",
"""
SELECT TOP 1 source_id, ra, dec, DISTANCE(POINT('ICRS',ra,dec), 
       POINT('ICRS',266.41683,-29.00781)) AS dist
   FROM GDR1.gaia_source 
   WHERE 1=CONTAINS(POINT('ICRS',ra,dec),CIRCLE('ICRS',266.41683,-29.00781, 0.08333333))
""",
"""SELECT polygon('ICRS', 0, 0, 0, 1, 1, 1, 1, 0) FROM db.b""",
"""SELECT a FROM db.b""",
"""
SELECT DISTANCE(
POINT('ICRS', ra, dec),
POINT('ICRS', 266.41683, -29.00781)) AS dist
FROM gaiadr1.gaia_source
WHERE 1=CONTAINS(
POINT('ICRS', ra, dec),
CIRCLE('ICRS', 266.41683, -29.00781, 0.08333333))
ORDER BY dist ASC
""",
"""
SELECT *
FROM gaiadr1.gaia_source
WHERE 1=CONTAINS(
POINT('ICRS',ra,dec),
CIRCLE('ICRS',266.41683,-29.00781, 0.08333333))
AND phot_g_mean_mag>=10 AND phot_g_mean_mag<15
ORDER BY phot_g_mean_mag ASC
""",
""" 
SELECT *
FROM gaiadr1.tgas_source
WHERE parallax >= 15 AND parallax <= 50
AND phot_g_mean_mag >= 9 and phot_g_mean_mag <= 9.5
""",
"""
SELECT TOP 10 distance(
POINT('ICRS', hip.ra, hip.de),
POINT('ICRS', gaia.ra, gaia.dec)) AS dist
FROM gaiadr1.gaia_source AS gaia, "public".hipparcos AS hip
WHERE 1=CONTAINS(
POINT('ICRS', hip.ra, hip.de),
CIRCLE('ICRS', gaia.ra, gaia.dec, 0.000277777777778)
)
""",
""" 
SELECT crossmatch_positional(
"public",'hipparcos',
'gaiadr1','gaia_source',
1.0,
'xmatch_hipparcos_gaia')
FROM dual;
""",
""" 
SELECT TOP 10
gaia_healpix_index(6, source_id) AS healpix_6,
count(*) / 0.83929 as sources_per_sq_deg,
avg(astrometric_n_good_obs_al) AS avg_n_good_al,
avg(astrometric_n_good_obs_ac) AS avg_n_good_ac,
avg(astrometric_n_good_obs_al + astrometric_n_good_obs_ac) AS avg_n_good,
avg(astrometric_excess_noise) as avg_excess_noise
FROM gaiadr1.tgas_source
GROUP BY healpix_6
""",
""" 
SELECT gaia.source_id, gaia.hip,
gaia.phot_g_mean_mag + 5 * log10(gaia.parallax) - 10 AS g_mag_abs_gaia,
gaia.phot_g_mean_mag + 5 * log10(hip.plx) - 10 AS g_mag_abs_hip
FROM gaiadr1.tgas_source AS gaia
INNER JOIN "public".hipparcos_newreduction AS hip
ON gaia.hip = hip.hip
WHERE gaia.parallax/gaia.parallax_error >= 5 AND
hip.plx/hip.e_plx >= 5 AND
hip.e_b_v > 0.0 and hip.e_b_v <= 0.05 AND
hip.b_v >= 1.0 AND hip.b_v <= 1.1 AND
2.5 / log(10) * gaia.phot_g_mean_flux_error / gaia.phot_g_mean_flux <= 0.05
""",
""" 
SELECT g_mag_abs_hip_index / 5. AS g_mag_abs_hip, count(g_mag_abs_hip_index) AS freq FROM (
SELECT floor((gaia.phot_g_mean_mag + 5 * log10(hip.plx) - 10) * 5) AS g_mag_abs_hip_index
FROM gaiadr1.tgas_source AS gaia
INNER JOIN "public".hipparcos_newreduction AS hip
ON gaia.hip = hip.hip
WHERE gaia.parallax/gaia.parallax_error >= 5 AND
hip.plx/hip.e_plx >= 5 AND
hip.e_b_v > 0.0 and hip.e_b_v <= 0.05 AND
hip.b_v >= 1.0 and hip.b_v <= 1.1 AND
2.5 / log(10) * gaia.phot_g_mean_flux_error / gaia.phot_g_mean_flux <= 0.05
) AS subquery
GROUP BY g_mag_abs_hip_index
ORDER BY g_mag_abs_hip
""",
""" 
SELECT TOP 10 gaia.source_id,
gaia.phot_g_mean_mag + 5 * log10(gaia.parallax) - 10 AS g_mag_abs ,
gaia.phot_g_mean_mag - tmass.ks_m AS g_min_ks
FROM gaiadr1.tgas_source AS gaia
INNER JOIN gaiadr1.tmass_best_neighbour AS xmatch
ON gaia.source_id = xmatch.source_id
INNER JOIN gaiadr1.tmass_original_valid AS tmass
ON tmass.tmass_oid = xmatch.tmass_oid
WHERE gaia.parallax/gaia.parallax_error >= 5 AND
ph_qual = 'AAA' AND
sqrt(power(2.5 / log(10) * gaia.phot_g_mean_flux_error
/ gaia.phot_g_mean_flux, 2) ) <= 0.05 AND
sqrt(power(2.5/log(10)*gaia.phot_g_mean_flux_error
/ gaia.phot_g_mean_flux, 2)
+ power(tmass.ks_msigcom, 2)) <= 0.05
""",
""" 
SELECT
g_min_ks_index / 10 AS g_min_ks,
g_mag_abs_index / 10 AS g_mag_abs,
count(*) AS n
FROM (
SELECT TOP 10 gaia.source_id,
floor((gaia.phot_g_mean_mag+5*log10(gaia.parallax)-10) * 10) AS g_mag_abs_index,
floor((gaia.phot_g_mean_mag-tmass.ks_m) * 10) AS g_min_ks_index
FROM gaiadr1.tgas_source AS gaia
INNER JOIN gaiadr1.tmass_best_neighbour AS xmatch
ON gaia.source_id = xmatch.source_id
INNER JOIN gaiadr1.tmass_original_valid AS tmass
ON tmass.tmass_oid = xmatch.tmass_oid
WHERE gaia.parallax/gaia.parallax_error >= 5 AND
ph_qual = 'AAA' AND
sqrt(power(2.5 / log(10) * gaia.phot_g_mean_flux_error / gaia.phot_g_mean_flux, 2)) <= 0.05 AND
sqrt(power(2.5 / log(10) * gaia.phot_g_mean_flux_error / gaia.phot_g_mean_flux, 2)
+ power(tmass.ks_msigcom, 2)) <= 0.05
)AS subquery
GROUP BY g_min_ks_index, g_mag_abs_index
""",
""" 
SELECT
curves.observation_time,
mod(curves.observation_time - rrlyrae.epoch_g, rrlyrae.p1)
/ rrlyrae.p1 AS phase,
curves.g_magnitude,
2.5 / log(10) * curves.g_flux_error / curves.g_flux
AS g_magnitude_error
FROM gaiadr1.phot_variable_time_series_gfov AS curves
INNER JOIN gaiadr1.rrlyrae AS rrlyrae
ON rrlyrae.source_id = curves.source_id
WHERE rrlyrae.source_id = 5284240582308398080
""",
""" 
SELECT gaia.*
FROM gaiadr1.phot_variable_time_series_gfov AS gaia
INNER JOIN gaiadr1.cepheid AS cep
on gaia.source_id = cep.source_id
""",
""" 
SELECT gaia.*
FROM gaiadr1.phot_variable_time_series_gfov AS gaia
INNER JOIN gaiadr1.rrlyrae AS rr
ON gaia.source_id = rr.source_id
""",
""" 
SELECT stat.num_observations_processed, cep.*
FROM gaiadr1.phot_variable_time_series_gfov_statistical_parameters AS stat
INNER JOIN gaiadr1.cepheid AS cep
ON stat.source_id = cep.source_id
""",
""" 
SELECT stat.num_observations_processed, rr.*
FROM gaiadr1.phot_variable_time_series_gfov_statistical_parameters AS stat
INNER JOIN gaiadr1.rrlyrae AS rr
ON stat.source_id = rr.source_id
""",
""" 
SELECT source_id, ra, dec, coord1(prop) AS ra_1950, coord2(prop) AS dec_1950 FROM (
SELECT gaia.source_id, ra, dec,
EPOCH_PROP_POS(ra, dec, parallax, pmra, pmdec, 0, ref_epoch, 1950) AS prop
FROM gaiadr1.tgas_source AS gaia
WHERE contains(
POINT('ICRS', gaia.ra, gaia.dec),
CIRCLE('ICRS', 56.75, 24.12, 5)) = 1
AND sqrt(power(gaia.pmra - 20.5, 2) + power(gaia.pmdec + 45.5, 2)) < 6.0
) AS subquery
""",
"""
SELECT POLYGON('ICRS', 1.0, -1.0, 2.0, -2.0, 3.0, -3.0) FROM db.tab
""",
"""
SELECT COUNT(*) FROM db.tab;
""",
"""
SELECT ACOS(DISTANCE(POINT('ICRS', 1.0, 1.0), POINT('ICRS', "atan", de))) FROM bla;
"""
]
