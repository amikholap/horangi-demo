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
