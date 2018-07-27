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
