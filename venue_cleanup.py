import duckdb

conn = duckdb.connect("ipl.duckdb")

conn.execute("""
DROP TABLE IF EXISTS venue_mapping
""")

conn.execute("""
CREATE TABLE venue_mapping AS

SELECT
    venue,

    CASE

        WHEN venue LIKE '%Chinnaswamy%'
        THEN 'M Chinnaswamy Stadium'

        WHEN venue LIKE '%Wankhede%'
        THEN 'Wankhede Stadium'

        WHEN venue LIKE '%Chepauk%'
        THEN 'MA Chidambaram Stadium'

        WHEN venue LIKE '%Eden Gardens%'
        THEN 'Eden Gardens'

        WHEN venue LIKE '%Rajiv Gandhi%'
        THEN 'Rajiv Gandhi International Stadium'

        WHEN venue LIKE '%Sawai Mansingh%'
        THEN 'Sawai Mansingh Stadium'

        WHEN venue LIKE '%DY Patil%'
        THEN 'Dr DY Patil Sports Academy'

        WHEN venue LIKE '%Feroz Shah Kotla%'
        THEN 'Arun Jaitley Stadium'

        WHEN venue LIKE '%Arun Jaitley%'
        THEN 'Arun Jaitley Stadium'

        ELSE venue

    END AS venue_clean

FROM (
    SELECT DISTINCT venue
    FROM matches
)
""")

print("Venue mapping created successfully")

conn.close()