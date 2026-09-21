---
layout: default
permalink: /secret/
title: playground
description: A hidden page.
nav: false
sitemap: false
---

{%- comment -%}
DESIGN.md §8.8. `layout: default`, not `page`: the gem's `page.liquid` prints
`.post-title`, and here the oversized "playground" is the title.

Three separate things keep this page quiet, and none of them implies the others:
`nav: false` keeps it out of the menu and out of the search palette (al_search
indexes only pages whose `nav` is true), `sitemap: false` keeps it out of
sitemap.xml, and `robots.txt` asks crawlers not to fetch it. A `robots:` front
matter key would do nothing: no gem template reads one.

The widget cards below are placeholders. Replace them, or drive them from a data
file once there is more than a handful.
{%- endcomment -%}

<div class="secret">
  <p class="secret__note">// hidden from menus. you found it.</p>

  <h1 class="secret__title">playground</h1>
  <p class="secret__subtitle">things that do not belong on a page yet</p>

  <div class="secret__grid">
    <article class="secret__card">
      <p class="secret__tag">WIDGET / PLACEHOLDER</p>
      <h2 class="secret__name">nothing here yet</h2>
      <p class="secret__desc">
        This card is the shape a widget takes: a small label, a name, and a line
        or two saying what it does. Replace it when the first one exists.
      </p>
    </article>

    <article class="secret__card">
      <p class="secret__tag">WIDGET / PLACEHOLDER</p>
      <h2 class="secret__name">nor here</h2>
      <p class="secret__desc">
        Two cards are enough to show the grid. The layout reflows to one column
        on narrow screens.
      </p>
    </article>

  </div>

  <p class="secret__footnote">// each widget should be embeddable in a post</p>
</div>
