# Future Work

The project in its current state should satisfy all functional requirements but have some very inefficient operations.  
The future work should eliminate this inefficiencies by adding caches and asynchronous event processing.

### Caches
In-memory caching layer is completely absent which leaves a lot of room for performance improvements.  
While some hot spots may not be obvious until they become bottlenecks but there is a place that would clearly limit system's scalability.  
It's the friends feed.  
Currently the feed is served from Cassandra and the query to collect required activities touches all partitions.  
As proposed in design doc the feed can be cached using an in-memory data grid like Redis and update incrementally.  

### Asynchronous Event Processing
Currently all operations are performed in a blocking manner while processing user request.  
It adds unnecessary latency and introduces a possibility of data structures becoming out-of-sync if an error happens half-way during request processing.  
To avoid it the application should instead emit events to a durable distributed queue like Apache Kafka.  
The events then can be processed independently by multiple workers each doing its part of the job.  
Restoring from the last commited offset after crashes and making the workers logic idempotent would ensure eventual data consistency.
