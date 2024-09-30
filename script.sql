WITH CombinedProperties AS (
    SELECT
        w.well_id,
        w.well_row,
        w.well_column,
        w.property_name AS well_property_name,
        w.property_value AS well_property_value,
        p.property_name AS plate_property_name,
        p.property_value AS plate_property_value,
        e.property_name AS experiment_property_name,
        e.property_value AS experiment_property_value
    FROM
        wells w
    LEFT JOIN
        plates p ON w.plate_id = p.plate_id
    LEFT JOIN
        experiments e ON p.experiment_id = e.experiment_id
),
FinalProperties AS (
    SELECT
        well_id,
        well_row,
        well_column,
        COALESCE(well_property_name, plate_property_name, experiment_property_name) AS property_name,
        COALESCE(well_property_value, plate_property_value, experiment_property_value) AS property_value
    FROM
        CombinedProperties
)

SELECT
    well_id,
    well_row,
    well_column,
    property_name,
    property_value
FROM
    FinalProperties;
