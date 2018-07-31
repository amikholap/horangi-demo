# horangi-demo
Demo social network activity feed

#### Setup
The easiest way to start the project is to use minikube – local kubernetes cluster.  
For installation instructions please refer to https://kubernetes.io/docs/tasks/tools/install-minikube/
After minikube is installed use `make start` to run all components.  
It will display a URL that should be used to access application endpoints.  
You can make HTTP requests to the defined endpoints right after it.  
The database is initialized with 4 users each following others – `ales`, `eric`, `ivan`, `niko`.

#### Example Requests

`curl -X POST "$URL/api/actions/" -d '{ "actor": "eric", "verb": "post", "object": "post:1", "target": null }' -H 'Content-Type: application/json'`

`curl -X POST "$URL/api/actions/" -d '{ "actor": "ivan", "verb": "like", "object": "post:1", "target": "eric" }' -H 'Content-Type: application/json'`

`curl -X POST "$URL/api/actions/" -d '{ "actor": "niko", "verb": "share", "object": "post:1", "target": "eric" }' -H 'Content-Type: application/json'`

`curl "$URL/api/my-feed/?actor=eric&page=0&per_page=10"`

`curl "$URL/api/friends-feed/?actor=eric&page=0&per_page=10"`

`curl "$URL/api/related-actions/?username=eric&object=post:1`
