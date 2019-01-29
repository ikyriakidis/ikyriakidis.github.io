---
layout: post
title:  "Simple rest mock server as a docker container"
date:   2019-01-29 10:00:00 +0200
categories: docker mock testing
---
I am currently working on a task where I need to test a fairly simple system with a lot of exernal dependencies. I am a big fun of Docker because it makes it easy to set up and tear down services and aplications.
For the purpose of my task I choose to use [JSON Server](https://github.com/typicode/json-server) that provides REST API mocking based on plain JSON.

 
Build the docker images using the following Dockerfile

{% highlight raw %}
ROM node:8.6-slim

RUN npm install -g json-server

WORKDIR /data
VOLUME /data

EXPOSE 80

ENTRYPOINT ["json-server", "/data/data.json", "--port", "80", "--host", "0.0.0.0"]
{% endhighlight %}


Create the data.json file and fill it with data.

{% highlight raw %}
{
  "posts": [
    { "id": 1, "title": "json-server", "author": "typicode" }
  ],
  "comments": [
    { "id": 1, "body": "some comment", "postId": 1 }
  ],
  "profile": { "name": "typicode" }
}
{% endhighlight %}


Run the container by executing

{% highlight raw %}
docker run -d -p 80:80 -v /data.json:/data/data.json mockserver:1.0.0
{% endhighlight %}

