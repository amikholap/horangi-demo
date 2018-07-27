# Social network activity feed

The goal of this design document is to provide quantitative estimates and implementation overview of a social network activity feed.

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
