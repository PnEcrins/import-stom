DELETE FROM gn_monitoring.t_base_sites
WHERE base_site_name LIKE 'Distroit%' AND id_base_site NOT IN (SELECT id_base_site
                                                            FROM gn_monitoring.t_base_visits);