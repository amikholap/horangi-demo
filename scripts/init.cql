CREATE KEYSPACE IF NOT EXISTS demo WITH replication = { 'class': 'SimpleStrategy', 'replication_factor': 3};

CREATE TABLE IF NOT EXISTS demo.user (
    username text PRIMARY KEY
);

CREATE TABLE IF NOT EXISTS demo.follow (
    followee_username text,
    follower_username text,
    created_at timestamp,
    PRIMARY KEY (followee_username, follower_username)
) WITH CLUSTERING ORDER BY (follower_username ASC);

CREATE TABLE IF NOT EXISTS demo.action (
    actor_username text,
    created_at timestamp,
    id uuid,
    object text,
    target_username text,
    verb text,
    PRIMARY KEY (actor_username, created_at)
) WITH CLUSTERING ORDER BY (created_at DESC);


CREATE TABLE IF NOT EXISTS demo.related_action (
    object text,
    actor_username text,
    created_at timestamp,
    id uuid,
    target_username text,
    verb text,
    PRIMARY KEY (object, actor_username, created_at)
) WITH CLUSTERING ORDER BY (actor_username ASC, created_at DESC);


INSERT INTO demo.user (username) VALUES ('ales');
INSERT INTO demo.user (username) VALUES ('eric');
INSERT INTO demo.user (username) VALUES ('ivan');
INSERT INTO demo.user (username) VALUES ('niko');


INSERT INTO demo.follow (followee_username, follower_username, created_at) VALUES ('ales', 'eric', toTimestamp(now()));
INSERT INTO demo.follow (followee_username, follower_username, created_at) VALUES ('ales', 'ivan', toTimestamp(now()));
INSERT INTO demo.follow (followee_username, follower_username, created_at) VALUES ('ales', 'niko', toTimestamp(now()));
INSERT INTO demo.follow (followee_username, follower_username, created_at) VALUES ('eric', 'ales', toTimestamp(now()));
INSERT INTO demo.follow (followee_username, follower_username, created_at) VALUES ('eric', 'ivan', toTimestamp(now()));
INSERT INTO demo.follow (followee_username, follower_username, created_at) VALUES ('eric', 'niko', toTimestamp(now()));
INSERT INTO demo.follow (followee_username, follower_username, created_at) VALUES ('ivan', 'ales', toTimestamp(now()));
INSERT INTO demo.follow (followee_username, follower_username, created_at) VALUES ('ivan', 'eric', toTimestamp(now()));
INSERT INTO demo.follow (followee_username, follower_username, created_at) VALUES ('ivan', 'niko', toTimestamp(now()));
INSERT INTO demo.follow (followee_username, follower_username, created_at) VALUES ('niko', 'ales', toTimestamp(now()));
INSERT INTO demo.follow (followee_username, follower_username, created_at) VALUES ('niko', 'eric', toTimestamp(now()));
INSERT INTO demo.follow (followee_username, follower_username, created_at) VALUES ('niko', 'ivan', toTimestamp(now()));
