-- barrier --
INSERT INTO osmaxx.misc_l
  SELECT osm_id as osm_id,
	osm_timestamp as lastchange,
	CASE
	 WHEN osm_id<0 THEN 'R' -- Relation
	 ELSE 'W' 		-- Way
	 END AS geomtype,
	ST_Multi(way) AS geom,
	'barrier' as aggtype,
-- Combining different tags into barrier tag --
	case
 	 when barrier in ('gate','fence','city_wall', 'hedge', 'wall','avalanche_protection','retaining_wall', 'border_control') then barrier
	 else 'barrier'
	end AS type,

	name as name,
	"name:en" as name_en,
	"name:fr" as name_fr,
	"name:es" as name_es,
	"name:de" as name_de,
	int_name as name_int,
	transliterate(name) as label,
	cast(tags as text) as tags
  FROM osm_line
  WHERE barrier is not null

UNION
  SELECT osm_id as osm_id,
	osm_timestamp as lastchange,
	CASE
	 WHEN osm_id<0 THEN 'R' -- Relation
	 ELSE 'W' 		-- Way
	 END AS geomtype,
	ST_Multi(ST_ExteriorRing (way)) AS geom,
	'barrier' as aggtype,
-- Combining different tags into barrier tag --
	case
 	 when barrier in ('gate','fence','city_wall', 'hedge', 'wall','avalanche_protection','retaining_wall', 'border_control') then barrier
	 else 'barrier'
	end AS type,

	name as name,
	"name:en" as name_en,
	"name:fr" as name_fr,
	"name:es" as name_es,
	"name:de" as name_de,
	int_name as name_int,
	transliterate(name) as label,
	cast(tags as text) as tags
  FROM osm_polygon
  WHERE  barrier is not null;
