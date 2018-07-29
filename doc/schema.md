# Database schema

Apache Cassandra is used for this demo.  
Partition keys are highlighted in bold, clustering keys are highlighted in italic.


### User
column|type
------|----
**username**|text


### Follow
column|type
------|----
**followee_username**|text
follower_username|text
followed_at|timestamp


### Action
column|type
------|----
**creator_username**|text
*created_at*|timestamp
id|uuid
verb|text
object|text
target_username|text
