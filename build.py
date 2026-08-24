#!/usr/bin/env python3
"""
Renders blog/posts/*.md into static HTML under blog/.

    python build.py

Requires:  pip install markdown

There is no server-side anything: this writes plain HTML files that GitHub
Pages serves as-is. Run it after adding or editing a post, then commit both
the .md source and the generated .html.
"""
import re
import html
import pathlib
import datetime
import xml.sax.saxutils as xu

import markdown

ROOT = pathlib.Path(__file__).parent
POSTS_DIR = ROOT / "blog" / "posts"
BLOG_DIR = ROOT / "blog"
SITE = "https://irakliskyriakidis.eu"
SITE_HOST = "irakliskyriakidis.eu"
AUTHOR = "Iraklis Kyriakidis"
GA_ID = "G-KW6CQ3XWPH"

# Pages that exist outside the blog, for the sitemap.
STATIC_PAGES = [("/", "1.0"), ("/cv/", "0.8"), ("/blog/", "0.7")]


def dashes(text):
    """House style: hyphens, never en or em dashes."""
    return text.replace("—", "-").replace("–", "-")


def external_links(html_text):
    """Open links to other sites in a new tab.

    Applied to every post automatically, so a post never has to remember the
    attributes. Internal links keep the same tab: sending a reader away from
    your own site to read your own site is just annoying.
    """
    def rewrite(match):
        href = match.group(1)
        if SITE_HOST in href:
            return match.group(0)
        return '<a href="%s" target="_blank" rel="noopener noreferrer"' % href

    return re.sub(r'<a href="(https?://[^"]+)"', rewrite, html_text)


def read_posts():
    posts = []
    for path in sorted(POSTS_DIR.glob("*.md")):
        if path.name.startswith("_"):
            continue
        raw = path.read_text(encoding="utf-8")
        if not raw.startswith("---"):
            raise SystemExit("%s: missing front matter" % path.name)
        _, front, body = raw.split("---", 2)

        meta = {}
        for line in front.strip().splitlines():
            if ":" in line:
                key, value = line.split(":", 1)
                meta[key.strip().lower()] = value.strip()

        for required in ("title", "date"):
            if not meta.get(required):
                raise SystemExit("%s: front matter needs '%s'" % (path.name, required))

        try:
            date = datetime.date.fromisoformat(meta["date"][:10])
        except ValueError:
            raise SystemExit("%s: date must be YYYY-MM-DD" % path.name)

        md = markdown.Markdown(extensions=["fenced_code", "tables", "attr_list", "sane_lists"])
        posts.append({
            "slug": path.stem,
            "title": dashes(meta["title"]),
            "date": date,
            "description": dashes(meta.get("description", "")),
            "tags": [t.strip() for t in meta.get("tags", "").split(",") if t.strip()],
            "body": external_links(dashes(md.convert(dashes(body.strip())))),
            "url": "/blog/%s/" % path.stem,
        })

    posts.sort(key=lambda p: p["date"], reverse=True)
    return posts


HEAD = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>%(title)s</title>
  <meta name="description" content="%(description)s">
  <link rel="canonical" href="%(canonical)s">

  <meta property="og:type" content="%(ogtype)s">
  <meta property="og:title" content="%(ogtitle)s">
  <meta property="og:description" content="%(description)s">
  <meta property="og:url" content="%(canonical)s">
  <meta property="og:image" content="%(site)s/img/og-card.png">
  <meta name="twitter:card" content="summary_large_image">

  <link rel="icon" href="/img/favicon.svg" type="image/svg+xml">
  <link rel="icon" href="/img/favicon-32.png" sizes="32x32" type="image/png">
  <link rel="apple-touch-icon" href="/img/favicon-180.png">

  <link rel="alternate" type="application/rss+xml" title="%(author)s" href="/blog/feed.xml">

  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Montserrat:wght@600;700&amp;family=Lora:ital,wght@0,400;0,600;1,400&amp;display=swap">
  <link rel="stylesheet" href="/assets/css/style.css">
%(extrahead)s
  <!-- Google tag (gtag.js) -->
  <script async src="https://www.googletagmanager.com/gtag/js?id=%(ga)s"></script>
  <script>
    window.dataLayer = window.dataLayer || [];
    function gtag(){dataLayer.push(arguments);}
    gtag('js', new Date());

    gtag('config', '%(ga)s');
  </script>
</head>
<body class="%(bodyclass)s">

<a class="skip" href="#main">Skip to content</a>

<header class="nav is-stuck" id="site-nav">
  <div class="wrap nav-inner">
      <a class="nav-brand" href="/" aria-label="Home">
        <svg viewBox="14 15 40 34" width="26" height="22" fill="currentColor" aria-hidden="true">
          <rect x="16" y="17" width="6" height="30"/>
          <rect x="30" y="17" width="6" height="30"/>
          <polygon points="36,31 45,17 52,17 41,33"/>
          <polygon points="36,31 41,29 52,47 45,47"/>
        </svg>
      </a>
    <nav aria-label="Main">
      <a href="/#work">Work</a>
      <a href="/#experience">Experience</a>
      <a href="/blog/" aria-current="page">Blog</a>
      <a href="/cv/">CV</a>
      <a href="/#contact">Contact</a>
    </nav>
  </div>
</header>

<main id="main">
"""

FOOT = """</main>

<footer class="footer">
  <div class="wrap">
    <p class="footer-meta">&copy; 2011-<span id="year">%(year)s</span> %(author)s</p>
  </div>
</footer>

<script>
  var y = document.getElementById('year');
  if (y) y.textContent = new Date().getFullYear();
</script>
</body>
</html>
"""


def shell(body, **kw):
    kw.setdefault("extrahead", "")
    kw.setdefault("ogtype", "website")
    kw.setdefault("bodyclass", "blog-page")
    kw.setdefault("ogtitle", kw["title"])
    kw.update(site=SITE, author=AUTHOR, ga=GA_ID, year=datetime.date.today().year)
    return (HEAD % kw) + body + (FOOT % kw)


def esc(text):
    return html.escape(text, quote=True)


POST_LD = """  <script type="application/ld+json">
  {
    "@context": "https://schema.org",
    "@type": "BlogPosting",
    "headline": "%(title)s",
    "description": "%(description)s",
    "datePublished": "%(date)s",
    "author": { "@type": "Person", "name": "%(author)s", "url": "%(site)s/" },
    "mainEntityOfPage": "%(canonical)s",
    "image": "%(site)s/img/og-card.png"
  }
  </script>
"""


def render_post(post, newer, older):
    nav = []
    if older:
        nav.append('<a class="prev" href="%s"><span>Previous</span>%s</a>'
                   % (older["url"], esc(older["title"])))
    if newer:
        nav.append('<a class="next" href="%s"><span>Next</span>%s</a>'
                   % (newer["url"], esc(newer["title"])))

    tags = ""
    if post["tags"]:
        tags = ('\n    <ul class="tags" aria-label="Tags">%s</ul>'
                % "".join("<li>%s</li>" % esc(t) for t in post["tags"]))

    body = """<article class="wrap narrow article">
  <header class="article-head">
    <p class="eyebrow"><a href="/blog/">Blog</a></p>
    <h1>%(title)s</h1>
    <p class="article-meta"><time datetime="%(iso)s">%(nice)s</time></p>%(tags)s
  </header>

  <div class="prose">
%(content)s
  </div>

  <nav class="article-nav" aria-label="Other posts">
%(nav)s
  </nav>
</article>
""" % {
        "title": esc(post["title"]),
        "iso": post["date"].isoformat(),
        "nice": fmt_date(post["date"]),
        "tags": tags,
        "content": post["body"],
        "nav": "\n".join("    " + n for n in nav),
    }

    canonical = SITE + post["url"]
    ld = POST_LD % {"title": esc(post["title"]), "description": esc(post["description"]),
                    "date": post["date"].isoformat(), "author": AUTHOR,
                    "site": SITE, "canonical": canonical}

    return shell(body,
                 title="%s | %s" % (esc(post["title"]), AUTHOR),
                 ogtitle=esc(post["title"]),
                 description=esc(post["description"]),
                 canonical=canonical,
                 ogtype="article",
                 extrahead=ld)


def render_index(posts):
    if posts:
        items = []
        for p in posts:
            desc = ("\n        <p>%s</p>" % esc(p["description"])) if p["description"] else ""
            items.append("""      <li>
        <time datetime="%s">%s</time>
        <a href="%s">%s</a>%s
      </li>""" % (p["date"].isoformat(), fmt_date(p["date"]), p["url"], esc(p["title"]), desc))
        listing = '    <ul class="archive">\n%s\n    </ul>' % "\n".join(items)
    else:
        listing = "    <p>Nothing published yet.</p>"

    body = """<div class="wrap narrow article">
  <header class="article-head">
    <h1>Blog</h1>
    <p class="article-meta">Notes on backend systems, infrastructure and whatever else holds my attention.</p>
  </header>

%s

  <p><a class="more-link" href="/blog/feed.xml">RSS feed</a></p>
</div>
""" % listing

    return shell(body,
                 title="Blog | %s" % AUTHOR,
                 ogtitle="Blog",
                 description="Notes on backend systems, infrastructure and whatever else holds my attention.",
                 canonical=SITE + "/blog/")


def write_sitemap(posts):
    today = datetime.date.today().isoformat()
    rows = ['  <url><loc>%s%s</loc><lastmod>%s</lastmod><priority>%s</priority></url>'
            % (SITE, path, today, pri) for path, pri in STATIC_PAGES]
    for p in posts:
        rows.append('  <url><loc>%s%s</loc><lastmod>%s</lastmod><priority>0.6</priority></url>'
                    % (SITE, p["url"], p["date"].isoformat()))
    xml = ('<?xml version="1.0" encoding="UTF-8"?>\n'
           '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
           + "\n".join(rows) + "\n</urlset>\n")
    (ROOT / "sitemap.xml").write_text(xml, encoding="utf-8", newline="\n")


def write_feed(posts):
    items = []
    for p in posts[:20]:
        stamp = datetime.datetime.combine(p["date"], datetime.time(9, 0))
        items.append("""    <item>
      <title>%s</title>
      <link>%s%s</link>
      <guid isPermaLink="true">%s%s</guid>
      <pubDate>%s</pubDate>
      <description>%s</description>
    </item>""" % (xu.escape(p["title"]), SITE, p["url"], SITE, p["url"],
                  stamp.strftime("%a, %d %b %Y %H:%M:%S +0000"),
                  xu.escape(p["description"])))

    xml = """<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0" xmlns:atom="http://www.w3.org/2005/Atom">
  <channel>
    <title>%s</title>
    <link>%s/blog/</link>
    <description>Notes on backend systems, infrastructure and whatever else holds my attention.</description>
    <language>en</language>
    <atom:link href="%s/blog/feed.xml" rel="self" type="application/rss+xml" />
%s
  </channel>
</rss>
""" % (AUTHOR, SITE, SITE, "\n".join(items))
    (BLOG_DIR / "feed.xml").write_text(xml, encoding="utf-8", newline="\n")


MONTHS = ["January", "February", "March", "April", "May", "June",
          "July", "August", "September", "October", "November", "December"]


def fmt_date(d):
    """Portable: strftime('%-d') is not available on Windows."""
    return "%d %s %d" % (d.day, MONTHS[d.month - 1], d.year)


def main():
    posts = read_posts()

    for index, post in enumerate(posts):
        newer = posts[index - 1] if index > 0 else None
        older = posts[index + 1] if index + 1 < len(posts) else None
        out_dir = BLOG_DIR / post["slug"]
        out_dir.mkdir(parents=True, exist_ok=True)
        (out_dir / "index.html").write_text(
            render_post(post, newer, older), encoding="utf-8", newline="\n")
        print("  blog/%s/index.html" % post["slug"])

    (BLOG_DIR / "index.html").write_text(render_index(posts), encoding="utf-8", newline="\n")
    print("  blog/index.html")

    write_feed(posts)
    print("  blog/feed.xml")

    write_sitemap(posts)
    print("  sitemap.xml")

    print("\n%d post%s built." % (len(posts), "" if len(posts) == 1 else "s"))


if __name__ == "__main__":
    main()
