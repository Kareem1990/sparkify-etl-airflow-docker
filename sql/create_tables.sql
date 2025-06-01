-- Drop existing tables
DROP TABLE IF EXISTS songplays;
DROP TABLE IF EXISTS users;
DROP TABLE IF EXISTS songs;
DROP TABLE IF EXISTS artists;
DROP TABLE IF EXISTS time;
DROP TABLE IF EXISTS staging_events;
DROP TABLE IF EXISTS staging_songs;

-- Staging tables
CREATE TABLE staging_events (
    artist          VARCHAR(256),
    auth            VARCHAR(256),
    firstName       VARCHAR(256),
    gender          VARCHAR(10),
    itemInSession   INTEGER,
    lastName        VARCHAR(256),
    length          FLOAT8,
    level           VARCHAR(50),
    location        VARCHAR(256),
    method          VARCHAR(20),
    page            VARCHAR(50),
    registration    BIGINT,
    sessionId       INTEGER,
    song            VARCHAR(256),
    status          INTEGER,
    ts              BIGINT,
    userAgent       VARCHAR(256),
    userId          INTEGER
);

CREATE TABLE staging_songs (
    num_songs        INTEGER,
    artist_id        VARCHAR(50),
    artist_latitude  FLOAT8,
    artist_longitude FLOAT8,
    artist_location  VARCHAR(256),
    artist_name      VARCHAR(256),
    song_id          VARCHAR(50),
    title            VARCHAR(256),
    duration         FLOAT8,
    year             INTEGER
);

-- Fact table
CREATE TABLE songplays (
    songplay_id    INTEGER IDENTITY(0,1) PRIMARY KEY,
    start_time     TIMESTAMP NOT NULL,
    user_id        INTEGER NOT NULL,
    level          VARCHAR(50),
    song_id        VARCHAR(50),
    artist_id      VARCHAR(50),
    session_id     INTEGER,
    location       VARCHAR(256),
    user_agent     VARCHAR(256)
);

-- Dimension tables
CREATE TABLE users (
    user_id    INTEGER PRIMARY KEY,
    first_name VARCHAR(256),
    last_name  VARCHAR(256),
    gender     VARCHAR(10),
    level      VARCHAR(50)
);

CREATE TABLE songs (
    song_id   VARCHAR(50) PRIMARY KEY,
    title     VARCHAR(256),
    artist_id VARCHAR(50),
    year      INTEGER,
    duration  FLOAT8
);

CREATE TABLE artists (
    artist_id VARCHAR(50) PRIMARY KEY,
    name      VARCHAR(256),
    location  VARCHAR(256),
    latitude  FLOAT8,
    longitude FLOAT8
);

CREATE TABLE time (
    start_time TIMESTAMP PRIMARY KEY,
    hour       INTEGER,
    day        INTEGER,
    week       INTEGER,
    month      INTEGER,
    year       INTEGER,
    weekday    INTEGER
);
