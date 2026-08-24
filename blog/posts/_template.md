---
title: Sentence case, no trailing full stop
date: 2026-01-01
description: One or two real sentences. This becomes the meta description, the summary on the blog index, and the RSS description, so write it as prose rather than a keyword list. Aim for under 160 characters.
tags: dotnet, aml, architecture
---

Open with the problem, not a preamble. A reader who arrived from a search
result wants to know within two sentences whether this page solves their
problem. "In this post we will explore..." tells them nothing.

## Use h2 for sections

The page already provides the h1 from the title above, so start at `##`.
Never put an `#` heading in the body: two h1 elements on a page is a real
SEO problem, not a stylistic one.

Code goes in fenced blocks, with a language where it helps:

```csharp
public sealed record Transaction(string Id, decimal Amount);
```

Images live under `assets/blog/<slug>/` and are referenced from the site
root, so they keep working regardless of which page embeds them:

![Describe what the image shows, for screen readers and for when it 404s](/assets/blog/example-slug/screenshot.png)

Links are plain markdown: [like this](https://example.com). Internal links
should be root-relative, [like this](/blog/some-other-post/), so they survive
any future change of domain.

## House style

- Hyphens only. No en or em dashes anywhere. The build enforces this, but
  write it correctly and the diff stays clean.
- The filename is the URL. `blog/posts/my-post.md` publishes to
  `/blog/my-post/`, so pick the slug deliberately and do not rename it after
  publishing without adding a redirect.
- The `date` is display and ordering only. It does not affect the URL.
- `tags` are comma separated and rendered as-is.

## Publishing

1. Copy this file to `blog/posts/<slug>.md` and write the post.
2. Run `python build.py` from the repository root.
3. Commit both the `.md` source and the generated HTML, then push.

The site is live about a minute later. This file is ignored by the build
because its name starts with an underscore.
