---
layout: post
title:  "Jekyll as a docker container"
date:   2019-01-29 14:00:00 +0200
categories: docker jekyll
---
I am a big fun of Docker and I hate installing software on my laptop. I was an early adopter of virtual machines and I have always installed all my development tools on a virtual machine. I really liked the idea of Jekyll and it kind of reminds me the old days, when we used to build web sites using [FrontPage](https://en.wikipedia.org/wiki/Microsoft_FrontPage).

Jekyll required [Ruby](https://jekyllrb.com/docs/installation/windows/#installing-jekyll) and that was a showstopper for using it. Docker to the rescue again. In the [following github project](https://github.com/envygeeks/jekyll-docker), you can find a containerized version of jekyll where all of these dependencies are available in the container

In order to get started, execute the following command:

{% highlight raw %}
  mkdir -p ~/Projects/blog ; cd ~/Projects/blog
  docker run --rm --volume="$PWD:/srv/jekyll" -it jekyll/jekyll:3.5 jekyll new .
{% endhighlight %}

If everything went smoothly then you a new site was created in the current folder by the container. You should be able to see a bunch of files and directories in the blog directory.

{% highlight raw %}
.gitignore
404.html
_config.yml
_posts
_posts/2018-04-01-welcome-to-jekyll.markdown
about.md
Gemfile
Gemfile.lock
index.md
{% endhighlight %}

In order to build it, execute the following command:

{% highlight raw %}
docker run --rm --volume="$PWD:/srv/jekyll" -it jekyll/jekyll:3.5 jekyll build
{% endhighlight %}

A new directory was created, "_site" containing your actual website (html based on the markdown posts). 

You can run it locally by executing:

{% highlight raw %}
docker run --name newblog --volume="$PWD:/srv/jekyll" -p 3000:4000 -it jekyll/jekyll:3.5 jekyll serve --watch --drafts
{% endhighlight %}


