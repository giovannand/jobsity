/* 
 *  Trips with similar origin, destination, and time of day should be grouped together
 *  5 clusters was setting to exclude intersections and allow visualize some grouped data
 * For higher datasets, we can change the group by date(trip_datetime) to group by date(trip_datetime) and EXTRACT(hour FROM  trip_datetime)
 * */
select count(id),bbox_origin, bbox_dest , date(trip_datetime)

from trips 
left join 
(
select kmean as kmean_origin, count(*) as total_origin, ST_SetSRID(ST_Extent(geom), 4326) as bbox_origin 
FROM
(
    SELECT ST_ClusterKMeans(data_points , 5) OVER() AS kmean, ST_Centroid(data_points) as geom
    FROM (
			select origin_coord as data_points from trips 
			union all 
			select destination_coord as data_points from trips  
		) as all_points 
) tsub
GROUP BY kmean
)
 as clusters on  ST_Covers(ST_SetSRID(clusters.bbox_origin,4326),ST_SetSRID(trips.origin_coord,4326))
left join 
(
SELECT kmean as kmean_dest, count(*) as total_dest, ST_SetSRID(ST_Extent(geom), 4326) as bbox_dest
FROM
(
    SELECT ST_ClusterKMeans(data_points , 5) OVER() AS kmean, ST_Centroid(data_points) as geom
    FROM (
			select origin_coord as data_points from trips 
			union all 
			select destination_coord as data_points from trips  
		) as all_points 
) tsub
GROUP BY kmean
)
 as clusters_destination on  ST_Covers(ST_SetSRID(clusters_destination.bbox_dest,4326),ST_SetSRID(trips.destination_coord ,4326))

 group BY bbox_origin, bbox_dest , date(trip_datetime) 
;

/* 
 *  Develop a way to obtain the weekly average number of trips for an area, defined by a
 *	bounding box (given by coordinates) or by a region
 *  
 * 
 * */

select 
	AVG(qtd_trips),
	region 
FROM (
		SELECT  
			EXTRACT(WEEK FROM  trip_datetime) as week,
			region,
			COUNT(id) as qtd_trips
		from trips
		group by region , EXTRACT(WEEK FROM  trip_datetime) 
		
		) as q
group by region

