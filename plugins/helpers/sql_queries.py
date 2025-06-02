class SqlQueries:
    # Query to load data into the songplays fact table
    songplay_table_insert = """
        INSERT INTO songplays (
            start_time, user_id, level, song_id, artist_id, session_id, location, user_agent
        )
        SELECT DISTINCT
            TIMESTAMP 'epoch' + se.ts / 1000 * INTERVAL '1 second' AS start_time,
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
        WHERE se.page = 'NextSong';
    """

    # Query to populate users dimension table from staging_events
    user_table_insert = """
        SELECT DISTINCT
            userId,
            firstName,
            lastName,
            gender,
            level
        FROM staging_events
        WHERE userId IS NOT NULL;
    """

    # Query to populate songs dimension table from staging_songs
    song_table_insert = """
        SELECT DISTINCT
            song_id,
            title,
            artist_id,
            year,
            duration
        FROM staging_songs;
    """

    # Query to populate artists dimension table from staging_songs
    artist_table_insert = """
        SELECT DISTINCT
            artist_id,
            artist_name,
            artist_location,
            artist_latitude,
            artist_longitude
        FROM staging_songs;
    """

    # Query to populate time dimension table from songplays
    time_table_insert = """
        SELECT DISTINCT
            start_time,
            EXTRACT(hour FROM start_time)      AS hour,
            EXTRACT(day FROM start_time)       AS day,
            EXTRACT(week FROM start_time)      AS week,
            EXTRACT(month FROM start_time)     AS month,
            EXTRACT(year FROM start_time)      AS year,
            EXTRACT(weekday FROM start_time)   AS weekday
        FROM songplays;
    """
