# irakliskyriakidis.eu

Personal site and blog for Iraklis Kyriakidis. Static HTML and CSS, served by
**GitHub Pages** from the `master` branch. Push and it is live in about a minute.

## Layout

    index.html            the one-page landing site
    cv/index.html         full CV, with a print stylesheet
    404.html              not-found page
    blog/posts/*.md       blog post sources - the only files you edit
    blog/posts/_template.md   copy this to start a new post
    blog/<slug>/index.html    generated, do not edit by hand
    blog/index.html       generated post archive
    blog/feed.xml         generated RSS
    sitemap.xml           generated
    build.py              renders the Markdown into the HTML above
    serve.py              start/stop the local preview server
    Makefile              shortcuts for the two scripts above
    assets/css/style.css  the only stylesheet
    assets/blog/<slug>/   images used by posts
    img/                  hero, favicons, share card
    CNAME                 custom domain - do not delete, Pages reads this
    .nojekyll             publish files as-is, skipping Jekyll

The landing page, CV and 404 are hand-written HTML and have no build step.
Only the blog is generated.

## Commands

    make deps     install the one Python dependency (markdown)
    make build    render blog/posts/*.md into static HTML
    make run      build, then serve at http://localhost:4000
    make stop     stop the preview server
    make status   is the preview server running?
    make clean    delete generated blog output (sources are untouched)

`make run` starts the server in the background and writes its pid to
`.server.pid`, so `make stop` can find it later. If that file is lost, stop
falls back to whatever process is listening on the port, so an orphaned
server can always be cleaned up.

`make` is a thin wrapper: `build.py` and `serve.py` can be called directly
with `python` if you prefer.

## Writing a post

1. Copy `blog/posts/_template.md` to `blog/posts/<slug>.md`. The filename is
   the URL: `my-post.md` publishes to `/blog/my-post/`.
2. Write it. The template documents the front matter and house style.
3. Run `make build`.
4. Commit the `.md` and the generated HTML together, then push.

`build.py` regenerates every post, the archive, the RSS feed and the sitemap
on each run, so it is always safe to re-run. Files starting with `_` are
ignored, which is why the template is not published.

## House style

Hyphens, never en or em dashes. `build.py` rewrites them in post output, but
the hand-written pages need it done by hand.

## Adding a page

There is no shared layout for the hand-written pages, so a new one needs the
head block, nav, footer and analytics snippet copied from an existing page.
Add it to `STATIC_PAGES` in `build.py` so it lands in the sitemap.

## History

The original Jekyll blog is preserved on the **`old-blog`** branch. Its five
2019 posts were migrated into `blog/posts/` as plain Markdown; the Jekyll
layouts, config and Gemfile were not carried over.
