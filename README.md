# irakliskyriakidis.eu

Personal site for Iraklis Kyriakidis. A single static page — no generator, no
build step, no dependencies. Hand-written HTML and CSS.

Served by **GitHub Pages** from the `master` branch. Push and it is live in
about a minute.

## Files

    index.html          the whole site
    404.html            not-found page
    assets/css/style.css the only stylesheet
    img/                hero images (1280 and 1920 wide, WebP)
    CNAME               custom domain — do not delete, Pages reads this
    .nojekyll           tells Pages to publish the files as-is, skipping Jekyll
    sitemap.xml         one URL, maintained by hand
    robots.txt

## Editing

Open `index.html` and edit it. There is nothing to compile.

## Local preview

    python -m http.server 4000 --directory .

Then open http://localhost:4000.

## DNS

The apex is four A records at GitHub's Pages IPs; `www` is a CNAME. Registrar
is Papaki.

    @      A       185.199.108.153
    @      A       185.199.109.153
    @      A       185.199.110.153
    @      A       185.199.111.153
    www    CNAME   irakliskyriakidis.eu

## History

The Jekyll blog that used to live here — five posts from 2019, on the
`blog.irakliskyriakidis.eu` subdomain — is preserved on the **`old-blog`**
branch, along with its layouts, config and images. The stylesheet in this repo
still carries the blog styles (`.post-list`, `.archive`, `.prose`,
`.article-nav`), so restoring it later is mostly a matter of bringing the
`_posts` and `_layouts` folders back.
