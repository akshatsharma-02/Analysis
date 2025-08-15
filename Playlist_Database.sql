use playlist_analysis;
create table song(
	track_id varchar(50),
    track_name varchar(50),
    track_artists varchar(50),
    track_album varchar(50),
    track_release_date date,
    track_popularity integer,
    track_duration time,
    track_danceability double,
    track_energy integer,
    track_loudness double,
    track_speechiness double,
    track_acousticness double,
    track_url varchar(200)
);
drop table song;
create table song(
	track_id varchar(50),
    track_name varchar(50),
    track_artists varchar(50),
    track_album varchar(50),
    track_release_date date,
    track_popularity integer,
    track_duration time,
    track_danceability double,
    track_energy integer,
    track_loudness double,
    track_speechiness double,
    track_acousticness double,
    track_url varchar(200)
);
select * from song;
