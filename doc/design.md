# Social network activity feed

The goal of this design document is to provide quantitative estimates and implementation overview of a social network activity feed.  
Requirements – https://gist.github.com/ivanchoo/9d9a6d6b3beef0c6d9fa2bb168202555

## Numbers

Let's design for a successfull social network with active users and make the following estimates:  
  * 500M MAU.
  * 300M DAU.
  * An average user
    * submits 2 posts and 5 likes/shares a day.
    * checks his friends' feed 10 times a day.
    * follows/unfollows 15 other users per month.
  * An average post is 512 characters long.

This would result in
  * 600M new posts and 1,5B likes/shares every day.
  * Assuming an even load from the global audience it would be ~7k new posts and ~17k likes/shares per second.
  * And ~35k friends' feed requests per second.
  * And ~3k follow/unfollow operations per second.
  * Assuming 69B of metadata per action (32B user UUID, 32B post UUID, 4B timestamp, 1B action type) the write load would be ~4MB/s for posts and ~1MB/s for likes/shares summing up to 5MB/s of activity data.
  * Or 421GB of activity data per day.
  * Follow/unfollow operations add extra 68B metadata * 3k op/sec = ~0.2MB/s = ~17GB/day.


## API

> All API responses include `data=endpoint-specific-payload`, `status={"success","error"}` and optional `errors=["error1", "error2", ...]` fields.  
> `status` field should be checked by client to ensure a successfull operation.  
> `errors` field would be present in case of `status="error"` and contain a list of error codes.  
> This approach would allow to separate application logic errors from HTTP errors and provide a consistent response format across all endpoints.

The system must support the following API methods:

#### 1. Submit a typed action (post, like, share).  
*Note: I've omitted `target` field mentioned in the requirements since it can be inferred from the object. Allowing to specify another target would result in undefined behaviour. It was probably left from follow/unfollow activities which were extracted to separate endpoints.*

Request:
```
  POST /api/actions/
  {
    "actor: "ivan",
    "verb": "like",
    "object": "post",
    "content": "The first post."
  }
```

Content is an optional field that is allowed only for `object=post` requests.

Response:
```
  {
    "data":
      {
        "actor: "ivan",
        "verb": "like",
        "object": "post:1",
        "content": "The first post."
      },
    "status": "success"
  }
```

#### 2. Get user's own activity feed.

Request:  
```GET /api/my-feed/?page={page}```

Response:
```
{
  "data" :
    [
      {
        "actor": "ivan",
        "verb": "share",
        "object": "post:1",
        "content": null,
        "datetime": "2018-07-25T18:35:22"
      },
      {
        "actor": "ivan",
        "verb": "post",
        "object": "post:2",
        "content": "The second post.",
        "datetime": "2018-07-25T19:55:33",
        "related":
          [
            {
              "actor": "niko",
              "verb": "like",
              "object": "post:2",
              "content": null
            },
            {
              "actor": "eric",
              "verb": "like",
              "object": "post:2",
              "content": null
            }
          ]
      },
      ...
    ],
  "status": "success"
}
```

#### 3. Follow / unfollow

Request:
```
POST /api/follow/
{
  "user": "niko"
}
```

Response:
```
{
  "data": null,
  "status": "success"
}
```

Request:
```
POST /api/unfollow/
{
  "user": "niko"
}
```

Response:
```
{
  "data": null,
  "status": "success"
}
```

#### 4. Get user friends' activity feed.

Request:  
```GET /api/friends-feed/?page={page}```

Response:
```
{
  "data" :
    [
      {
        "actor": "nico",
        "verb": "share",
        "object": "post:2",
        "content": null,
        "datetime": "2018-07-25T18:35:22"
      },
      {
        "actor": "eric",
        "verb": "post",
        "object": "post:3",
        "content": "The third post.",
        "datetime": "2018-07-25T19:55:33",
        "related":
          [
            {
              "actor": "niko",
              "verb": "like",
              "object": "post:3",
              "content": null
            },
            {
              "actor": "ivan",
              "verb": "like",
              "object": "post:3",
              "content": null
            }
          ]
      },
      ...
    ],
  "status": "success"
}
```


## Data access patterns

Designing for optimal performace requires knowledge of the ways the data are read and written.  
It determines the choice of data structures and storage technologies.

For a social network feed we have:

#### 1. List of people that a user follows
Required to filter the global activity feed.

#### 2. List of user's actions and related actions ordered by time
It's the user's own feed.

#### 3. List of friends' actions and related actions
It's the user's friends feed.

#### 4. Access by id for all objects
Not required by the current API but likely to be useful in the future.


## Implementation overview

At a high level the implementation would require and API backend and a persistent data storage.  
API backend is stateless and should be rather generic so I'll focus on effective data layout and access.

The simplest way to go is to use just a single (possibly replicated) SQL database such as Oracle, PostgresSQL or Amazon Aurora.  
It would support all required functionality, provide data consistency with transactions and effective queries with indexes.  
Yet the estimated data volume of about 400GB/day is overwhelming for an out-of-the-box relational database deployment.  
It's probably too much for any database accepting writes and keeping all the data on a single node.

An obvious solution is to shard the dataset.  
This would spread read/write throughput and storage capacity over multiple shards allowing to handle the desired load and more on demand.  
All mainstream RDBMS support sharding so it's a solved problem.

A natural way to shard social network data is by unique user identifier.  
This would keep all user's data on the same shard and allow effective read queries like a list of people the user follows or user's feed.  
The problem arises with friends' feed.  
To fetch it we would need to scan up to all shards in the system.
It scales badly by not reducing read load with the number of shards and it's slow because of lots of requests and the latency tail issue.  
That's really bad considering that friend's feed would probably be the most popular type of request.  
Other sharding schemes suffer from the same problem.  
It seems that you can't fit all the data you need to serve the request on a single shard.

Facebook's solution to this problem is to keep prepared feeds for most of the users in an in-memory cache.  
This enables very fast responses to friends' feed query but amplifies writes by updating caches for all user's followers.  
To avoid the percieved delay when posting an activity we can update the caches asynchronously so there will be a period in range of hundreds of milliseconds when some caches are stale.  
A good choice of a queueing system would be Kafka or Amazon Kinesis due to their ability to shard data flows into multiple partitions spreading read and write loads.

Let's assume that feed page size is 10 items and it's enough to store the first 3 pages of the feed in cache.  
Further pages need to be served from the disk of other shards.
To store caches for all 300M daily active users we'd need this amount of RAM:  
`300M * 10 * 3 * (2/5 * 581B + 3/5 * 69B) = ~2.4TB`
> I've assumed that 2/5 of the feed are posts of 581B and 3/5 are likes/shares of 69B.  
> This amount of RAM is readily available on modern hardware and the scale is achievable with in-memory data grids such as Redis or Hazelcast.

To enrich the feed with related objects I'd go with another caching layer to store mappings of relations `post_id -> list<action>`.  
To store a list of related actions for posts for the last week we'd need this amount of RAM:  
`600M * 7 * 69B * 16 = 4.5TB`
> Assuming an average post has 16 related actions.

To serve the related actions for a feed I'd suggest another API endpoint that accepts a list of post ids and returns the related actions.  
It would allow to start rendering the feed on client's device while fetching additional information in the background.

Yet if the list of related actions is used only to present counters and stats to the user it would be better to store the aggregated counters and stats themselves.  
A post may have tens of thouthands of likes/shares and having several such posts in your feed would result in slow load times and extra battery usage due to deserializing large volume of JSON data.

#### SQL vs NoSQL
I've mentioned that RDBMS can do the job storing, sharding and providing access to the data.  
Yet given such data access patterns that we have a NoSQL solution may be considered.  
Current data access doesn't imply any complex joins or unavoidable transactions across multiple operations.  
The most common pattern is sequential access that can be effectively handled by clustering the data.  
The main advantages of NoSQL solutions are better performance within the allowed set of operations and native (re-)sharding support.  
Good candidates are Apache Cassandra and Amazon DynamoDB.  
The latter has Amazon DynamoDB Accelerator feature with enables easy to setup caching layer for common queries.  
