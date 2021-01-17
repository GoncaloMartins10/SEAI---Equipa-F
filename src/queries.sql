SELECT 
  t1.id_transformer,
  (t1.breakdown_voltage - t2.avg_breakdown)^2 as breakdown_distance,
  (t1.interfacial_tension - t2.avg_interfacial)^2 as interfacial_distance,
  t3.nominal_voltage,
  t1.datestamp
FROM (
	select 
	  id_transformer, 
	  breakdown_voltage, 
	  interfacial_tension,
	  datestamp
	from ges_ativos.oil_quality_measurements 
) as t1
CROSS JOIN (
	select 
	  id_transformer, 
	  AVG(breakdown_voltage) AS avg_breakdown, 
	  AVG(interfacial_tension) AS avg_interfacial
	from ges_ativos.oil_quality_measurements 
	WHERE id_transformer='SE7'
	GROUP BY id_transformer
) as t2
inner join ges_ativos.transformer as t3
on t3.id_transformer = t1.id_transformer
order by t1.id_transformer DESC, interfacial_distance




SELECT
  *, 
  row_number() over (partition by id_transformer order by datestamp)
FROM ges_ativos.oil_quality_measurements