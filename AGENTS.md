# Agent Guidelines for al-folio (v1.x)

**This file is the authoritative entry point for coding agents working in this repo.** Read it before making any change. It is intentionally short and tool-neutral; it links to the one place each longer-form fact lives.

`al-folio` v1.x is a **thin Jekyll starter, not a theme**. This repo owns starter wiring, example content, docs, and cross-plugin tests. All runtime — layouts, includes, Sass, Liquid tags, filters, feature JS — lives in versioned gems published under [`al-org-dev`](https://github.com/al-org-dev).

## Route your change

Find your change on the left; edit only what is on the right.

| Your change                                                                                                              | Goes in                                                                                                       |
| ------------------------------------------------------------------------------------------------------------------------ | ------------------------------------------------------------------------------------------------------------- |
| Dependency pin, plugin activation, feature flag                                                                          | this repo: `Gemfile` **and** `_config.yml` (both — see below)                                                 |
| Example/demo content, bibliography, data files                                                                           | this repo: `_pages`, `_posts`, `_projects`, `_news`, `_teachings`, `_books`, `_data`                          |
| Documentation                                                                                                            | this repo: `docs/` (long-form) or this file (agent rules)                                                     |
| Cross-plugin integration test, visual parity test                                                                        | this repo: `test/integration_*.sh`, `test/visual/`                                                            |
| Plugin catalog metadata                                                                                                  | this repo: `_data/featured_plugins.yml`                                                                       |
| A layout, include, or Sass partial                                                                                       | the owning gem — start with `al_folio_core`                                                                   |
| A Liquid tag or filter, or what a tag renders                                                                            | the gem that registers it — see the [delegation table](docs/ARCHITECTURE.md#wrapper-to-tag-to-gem-delegation) |
| Feature behavior (search, math, charts, comments, cookies, icons, CV, distill, analytics, images, newsletter, citations) | that feature's gem — see [`docs/BOUNDARIES.md`](docs/BOUNDARIES.md)                                           |
| Component/unit test for gem-owned behavior                                                                               | the owning gem, not here                                                                                      |
| A feature with no existing owner                                                                                         | open a plugin proposal issue first, then a standalone plugin repo                                             |

[`docs/BOUNDARIES.md`](docs/BOUNDARIES.md) is the authoritative area-to-gem table. [`docs/ARCHITECTURE.md`](docs/ARCHITECTURE.md) explains how the pieces connect.

## Stop sign — lifted in this repo

> **This is clapkong.github.io, a site built _from_ the al-folio template, not the `alshedivat/al-folio` starter.** The stop sign below is upstream's rule and does **not** bind us. Shadowing a gem-owned file is the officially supported way to customize a user site.

Upstream forbids these paths, because in the starter repo that runtime belongs to the gems:

```
_layouts/   _includes/   _sass/   _scripts/   assets/tailwind/   tailwind.config.js   assets/webfonts/
```

Here they are expected: the re-skin planned in `.claude/PLAN.md` M1–M2 creates several deliberately. See [local overrides: your site vs. this repo](docs/ARCHITECTURE.md#local-overrides-your-site-vs-this-repo).

`test/style_contract.js` enforced that boundary and **was deleted on 2026-09-21** (PLAN.md M0-S0.3), along with its `npm run lint:style-contract` script and its `unit-tests.yml` step. It would have failed on every legal override. Deleting it also gave up its other assertions — that `_config.yml` keeps `theme: al_folio_core` and the required plugins, that `third_party_libraries` SRI pins exist, and that `al_math` is pinned to a released version. **Nothing checks those now**, so when you edit the `Gemfile` or `_config.yml` plugin list, verify by hand that the two lists still agree (see failure mode 2 below).

## Failures that produce no error message

Read [`docs/ARCHITECTURE.md`](docs/ARCHITECTURE.md#failure-modes-that-produce-no-error-message) for the full explanation. The short version:

1. **Features fail silently.** A feature renders only when its gem is loaded _and_ its flag is on _and_ the page opts in. Otherwise the Liquid tag emits an empty string — no warning, no error.
2. **`Gemfile` and `_config.yml` are two lists that must agree.** A plugin in only one of them is inert. Adding or removing a plugin means editing both. Repo dirs use hyphens (`al-folio-core`); gem/plugin ids use underscores (`al_folio_core`).
3. **This repo's baseurl is blank, and must stay blank.** `clapkong.github.io` is a GitHub _user site_: it is served from the domain root, so `_config.yml` keeps the `baseurl:` key with **no value**. Deleting the key or giving it a value are both wrong — a value prefixes every asset URL and renders the site unstyled with broken links. The blog lives at `/blog/` because `_pages/blog.md` sets `permalink: /blog/`, not because of baseurl. A plain `bundle exec jekyll build` is correct; never pass `--baseurl`. Dev server is at `http://localhost:4000/`.

   > Upstream's version of this file said the baseurl here is `/al-folio`, which is true of the `alshedivat/al-folio` demo and was true of this repo until 2026-09-21. It is what made `https://clapkong.github.io/` serve an unstyled page.

4. **A gem's `id` and `data-*` attributes are contracts with its JS.** Rewriting a gem file from scratch drops them and nothing complains. Copy the gem file and edit the copy. A header rewritten without `id="navbar"` left `progress-bar.js` measuring zero and the scroll bar rendered behind the header, with a clean build and an empty console.
5. **Nothing above the fixed navbar.** Same hook: `progress-bar.js` positions the scroll bar from `#navbar`. The work-in-progress notice therefore sits after `</header>` in normal flow, not as a strip above it.
6. **The contact address must not go back into `_data/socials.yml`.** `{% social_links %}` and the al_search command palette both read that file and write a plain `mailto:` into every built page. The palette is rendered from a Liquid template inside the gem, so no include override can undo it. The address lives in `_data/contact.yml`, which is gitignored and written by CI from the `SITE_EMAIL` secret; `_data/contact.example.yml` is the tracked stand-in.

## Local conventions

- **Per-page CSS is scoped with `:has()`.** The default layout sets no per-page body class, so a page's styles hang off something the page alone renders, e.g. `.post:has(.about-hero)`.
- **`_sass/` partial names must not collide with the gem's.** A local `_sass/_publications.scss` replaces the gem's partial wholesale rather than adding to it. Suffix site-owned files (`_publications-site.scss`).

## Validated local command set

Run from the repo root, in this order:

```bash
bundle install
npm ci
npm run lint:prettier
bundle exec jekyll build
bash test/integration_comments.sh
bash test/integration_plugin_toggles.sh
bash test/integration_distill.sh
bash test/integration_bootstrap_compat.sh
bash test/integration_upgrade_cli.sh
bash test/integration_css_minify.sh
bash test/integration_new_plugins.sh
npx playwright install chromium webkit
npm run test:visual
bundle exec al-folio upgrade audit
bundle exec al-folio upgrade overrides audit
bundle exec al-folio upgrade report
docker compose up -d
curl -fsS http://127.0.0.1:8080/ >/dev/null
docker compose logs --tail=80
docker compose down
```

All seven `test/integration_*.sh` scripts are gated by `unit-tests.yml`; run the ones your change touches. Docker note: v1 uses `/srv/jekyll/bin/entry_point.sh` and serves from container-local `/tmp/_site` to avoid host bind-mount write deadlocks.

## Before you open a PR

- Keep starter work here; route runtime behavior to the owning plugin repo.
- Run `npm run lint:prettier` (Prettier with `@shopify/prettier-plugin-liquid`, `printWidth: 150`). `npx prettier . --write` fixes formatting.
- Keep docs aligned with v1 ownership, and keep each fact in one place — link rather than restate.
- If you create or keep local overrides of plugin-owned files, run `bundle exec al-folio upgrade overrides audit` and commit `.al-folio-overrides.yml` after review.

## Further reading

- [`docs/ARCHITECTURE.md`](docs/ARCHITECTURE.md) — how the starter and gems fit together, silent failure modes, the v1 config contract, local overrides.
- [`docs/BOUNDARIES.md`](docs/BOUNDARIES.md) — authoritative area-to-gem ownership table and PR triage playbook.
- [`docs/CONTRIBUTING.md`](docs/CONTRIBUTING.md) — contributor workflow and agent tooling.
- [`docs/README.md`](docs/README.md) — index of all user and maintainer guides.
- `.agents/skills/al-folio-bootstrap/SKILL.md` — new-site setup workflow.
- `.agents/skills/al-folio-v1-migration/SKILL.md` — customized-fork migration and override drift auditing.
- `.codex/skills` and `.claude/skills` are symlinks to `.agents/skills` for agent-specific discovery.
