class SqlQueries:
    # Query to load data into the songplays fact table
    # This includes joins between staging_events and staging_songs
    songplay_table_insert = """
SELECT DISTINCT
    TIMESTAMP 'epoch' + se.ts/1000 * INTERVAL '1 second' AS start_time,
    se.userId AS user_id,
    se.level,
    ss.song_id,
    ss.artist_id,
    se.sessionId AS session_id,
    se.location,
    se.userAgent AS user_agent
FROM staging_events se
JOIN staging_songs ss
  ON se.song = ss.title
 AND se.artist = ss.artist_name
 AND se.length = ss.duration
WHERE se.page = 'NextSong';
"""

    # Query to extract distinct user data from staging_events for users dimension table
    user_table_insert = """
SELECT DISTINCT userId, firstName, lastName, gender, level
FROM staging_events
WHERE userId IS NOT NULL;
"""

    # Query to extract distinct song data from staging_songs for songs dimension table
    song_table_insert = """
SELECT DISTINCT song_id, title, artist_id, year, duration
FROM staging_songs;
"""

    # Query to extract distinct artist data from staging_songs for artists dimension table
    artist_table_insert = """
SELECT DISTINCT artist_id, artist_name, artist_location, artist_latitude, artist_longitude
FROM staging_songs;
"""

    # Query to derive time-related fields from songplays.start_time for the time dimension table
    time_table_insert = """
SELECT DISTINCT
    start_time,
    EXTRACT(hour FROM start_time),
    EXTRACT(day FROM start_time),
    EXTRACT(week FROM start_time),
    EXTRACT(month FROM start_time),
    EXTRACT(year FROM start_time),
    EXTRACT(weekday FROM start_time)
FROM songplays;
"""
