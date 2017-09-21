
queries = [
    (
        """
        SELECT
        g_min_ks_index / 10 AS g_min_ks,
        g_mag_abs_index / 10 AS g_mag_abs,
        count(*) AS n
        FROM (
            SELECT TOP 10 gaia.source_id,
            floor((gaia.phot_g_mean_mag+5*log10(gaia.parallax)-10) * 10)
                AS g_mag_abs_index,
            floor((gaia.phot_g_mean_mag-tmass.ks_m) * 10)
                AS g_min_ks_index
            FROM gaiadr1.tgas_source AS gaia
            INNER JOIN gaiadr1.tmass_best_neighbour AS xmatch
            ON gaia.source_id = xmatch.source_id
            INNER JOIN gaiadr1.tmass_original_valid AS tmass
            ON tmass.tmass_oid = xmatch.tmass_oid
            WHERE gaia.parallax/gaia.parallax_error >= 5 AND
            xmatch.ph_qual = 'AAA' AND
            sqrt(power(2.5 / log(10) * gaia.phot_g_mean_flux_error /
                       gaia.phot_g_mean_flux, 2)) <= 0.05 AND
            sqrt(power(2.5 / log(10) * gaia.phot_g_mean_flux_error /
                       gaia.phot_g_mean_flux, 2)
            + power(tmass.ks_msigcom, 2)) <= 0.05
        )AS subquery
        GROUP BY g_min_ks_index, g_mag_abs_index
        """,
        ('gaiadr1.tgas_source.source_id', 'gaiadr1.tgas_source.phot_g_mean_mag',
         'gaiadr1.tgas_source.parallax',
         'gaiadr1.tmass_best_neighbour.source_id',
         'gaiadr1.tmass_best_neighbour.tmass_oid',
         'gaiadr1.tmass_original_valid.tmass_oid',
         'gaiadr1.tgas_source.parallax_error',
         'gaiadr1.tgas_source.phot_g_mean_flux',
         'gaiadr1.tgas_source.phot_g_mean_flux_error',
         'gaiadr1.tmass_original_valid.ks_m',
         'gaiadr1.tmass_best_neighbour.ph_qual',
         'gaiadr1.tmass_original_valid.ks_msigcom',
         ),
        ('limit', 'where', 'join', 'group by'),
        ('sqrt', 'log10', 'log', 'count', 'floor', 'power')
    ),
    (
        """
        select dist from db.spatial where exists 
        (select * from db.misc where dist=misc.mass);
        """,
        (),
        (),
        (),
        (),
        """
        """
        )
]
