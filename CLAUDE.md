# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

@AGENTS.md

`AGENTS.md` (imported above) is the **authoritative** agent entry point: change routing, the stop sign for gem-owned paths, the silent failure modes, the local conventions, and the validated command set. Keep it short and ecosystem-neutral. Cross-repo architecture — the wrapper/tag/gem delegation table, feature gating, the v1 config contract, local overrides — lives in [`docs/ARCHITECTURE.md`](docs/ARCHITECTURE.md); area-to-gem ownership lives in [`docs/BOUNDARIES.md`](docs/BOUNDARIES.md).

**Read those three before editing anything.** Everything below is Claude-specific or longer-form operational detail that does not belong in the short entry point. Do not restate facts from those files here — link to them.

## Daily dev loop

```bash
bundle install                                # ruby gems
bundle exec jekyll serve                      # dev server → http://localhost:4000/  (baseurl is blank; user site)
bundle exec jekyll build                      # production-style build to _site/ — never pass --baseurl
bash test/integration_distill.sh              # run ONE integration test (any of the seven in test/)
npm run test:visual:update                    # refresh playwright snapshots after intentional UI change
bundle exec al-folio upgrade apply --safe     # deterministic codemods (font-weight-* → font-*, remote→local URLs)
bundle exec al-folio upgrade overrides diff <path>    # then `overrides accept <path>` to acknowledge an override
```

## Optional toolchains

- **Jupyter posts.** `bin/setup-python-deps` installs _only_ `jupyter` and `nbconvert` (via `pip --user --break-system-packages`) for `jekyll-jupyter-notebook`. It does **not** read `requirements.txt`. Missing `jupyter-nbconvert` is warn-and-continue; notebook rendering is skipped.
- **Everything else Python.** [`requirements.txt`](requirements.txt) is the fuller list and must be installed separately (`python3 -m pip install -r requirements.txt`): `rendercv[full]` for CV rendering, `scholarly` for `bin/update_scholar_citations.py`, plus `nbconvert` and `pyyaml`.
- **Responsive images.** `imagemagick.enabled: true` needs ImageMagick `convert` on `PATH`.
- **Manual deploy.** `bin/deploy` is the manual `gh-pages` build + purgecss + force-push path; CI normally deploys. `purgecss` is not a devDependency — install it with `npm install -g purgecss`.

## Docker serving model (v1-specific)

`docker compose up -d` bind-mounts the repo to `/srv/jekyll` and runs `bin/entry_point.sh`, which serves with `--force_polling --destination /tmp/_site`. The build output deliberately goes to **container-local `/tmp/_site`, not the bind-mounted `_site`** — writing `_site` back across the host bind mount caused write deadlocks. The container also `inotifywait`s `_config.yml` and restarts Jekyll on change (config edits aren't hot-reloaded by `--watch`). Verify at the domain root (baseurl is blank): `curl -fsS http://127.0.0.1:8080/`. `docker-compose-slim.yml` pulls a prebuilt `:slim` image instead of building locally.

## CI gates

The style contract is gone — `test/style_contract.js`, its npm script and its `unit-tests.yml` step were deleted on 2026-09-21. `AGENTS.md` § Stop sign says what that check used to cover and what is now unverified.

Remaining gates:

- `unit-tests.yml` — all seven `test/integration_*.sh` scripts (`comments`, `plugin_toggles`, `distill`, `bootstrap_compat`, `upgrade_cli`, `css_minify`, `new_plugins`).
- `upgrade-check.yml` — `bundle exec al-folio upgrade audit`.
- `prettier.yml` — Prettier with `@shopify/prettier-plugin-liquid` and `printWidth: 150`. Run `npm run lint:prettier` before pushing; `npx prettier . --write` fixes.
- `update-tocs.yml` — regenerates `<!--ts-->…<!--te-->` blocks in changed root and `docs/` Markdown files. If you add or rename a heading, expect a follow-up auto-commit on `main`.

## Gem version pins

`Gemfile` pins every `al-*` gem to an exact released version in `group :al_folio_plugins`, and `_config.yml` lists the same gems under `plugins:`. Read the current pins from the `Gemfile` rather than trusting any version quoted in prose — including here. To test a gem fix against this site, repoint the `Gemfile` at a sibling checkout (`path:`, `git:`, or `branch:`) and `bundle install`; see [`docs/ARCHITECTURE.md`](docs/ARCHITECTURE.md#working-on-a-gem-alongside-the-starter). Revert the pin before committing.

## Punctuation ban: em dash and middle dot

**Never write an em dash (`—`) or a middle dot (`·`) in anything this repo ships or records**: site copy, page content, UI strings, SCSS/Liquid comments, commit messages, `.claude/*.md`, docs. Use a colon, a comma, parentheses, or two separate sentences instead of `—`; use a slash, a pipe, or a line break instead of `·`.

User rule, stated 2026-09-21. It applies to new work; existing occurrences are cleaned up when the file is next touched for another reason, not in a sweep of their own.

## Run `impeccable` when a page is confirmed done

**When the user confirms a page is finished, invoke the `impeccable` skill once on that page before closing the stage.** Not on a draft, not mid-iteration: on the version the user has just signed off. Treat its findings as review notes, report them, and let the user decide what to act on.

User rule, stated 2026-09-21. The point is a second pass by something that was not steering the design, at the one moment the page is stable enough for the pass to mean anything.

## Commit messages

Subject line: `type(scope): 무엇을 했는지 (스테이지 id)`. Keep it under ~70 characters.
`feat` / `fix` / `docs` / `chore` / `refactor`, scope is the page or area
(`publications`, `header`, `404`, `claude`).

The body is a `-` list. **Noun phrases, not sentences.** One line per change,
wrapped at ~80 characters. A line says what changed, and adds why in parentheses
only when the why is not guessable from the change:

```
feat(publications): DESIGN.md §8.6 레이아웃 (M2-S2.5)

- 연도 점프 사이드바, 논문 카드
- 제목 -> PDF 링크, 중복 PDF 버튼 제거
- 연도 점프에 URL 해시 미사용 (gem `bibsearch.js` 가 검색어로 읽음)
- 520px 이하 배지/본문 1열
```

What does **not** go in a commit message: what was tried and rejected, how a
value was arrived at, measurements, what surprised us. That is what
`.claude/BUILD_LOG.md` is for, and repeating it here is the same fact in two
places. If a line needs a paragraph to justify it, the paragraph belongs in the
log and the commit gets the one-line version.

Draft into `.claude/commit.txt` first when the user asked for a message rather
than a commit. Punctuation ban applies (see above).

## Session log — `.claude/BUILD_LOG.md`

Ported from the `previous` repo. It exists to answer "what did the last session actually do, and why" without re-reading a diff. **It is committed** — `.gitignore` excludes `.claude/*` but un-ignores this one file, so it travels with the repo and reads the same from a fresh clone. `PLAN.md` and `PROGRESS.md` stay local. Being committed makes it public: keep it to reasoning about the work, not to anything you would not put in a commit message.

Three files, three jobs — keep each fact in one of them:

| file                   | answers                                                                                 |
| ---------------------- | --------------------------------------------------------------------------------------- |
| `.claude/PLAN.md`      | why the plan is what it is; §0.5 is the current-state summary a new session reads first |
| `.claude/PROGRESS.md`  | what is left — the stage tracker (`[ ]` `[x]` `[-]` `[?]`)                              |
| `.claude/BUILD_LOG.md` | what happened and why, append-only                                                      |

**The log holds the reasoning, so code comments and commit messages should not repeat it.** Once a decision is written up here, a comment or a commit body that re-argues it is the same fact in three places — and the two copies outside `.claude/` are the ones that go stale. Keep in the code only what a reader needs _at that line_ and cannot infer from it: a non-obvious constraint, a hook that fails silently, a value whose source is elsewhere. Keep in the commit message what `git log` alone must answer: what changed and why, in a few lines. Everything else — what was tried, what was rejected, what surprised us — belongs in the log and nowhere else.

**Write an entry when a stage in `PROGRESS.md` reaches a real end state** — done, or abandoned with a reason. Not for clarifying questions, reads, or a half-finished edit that the next message will change. Tick the box in `PROGRESS.md` in the same breath.

**Append to the end of the file. Never insert.** New entries go after the file's last `---`, so the file always reads oldest at top, newest at bottom. Inserting at the `<!-- ENTRIES_START -->` marker reverses that order, which is how the log in `previous` got scrambled.

Entry format:

```markdown
## [YYYY-MM-DD HH:MM KST] M0-S0.5 — 배포 복구

**Status**: ✅ completed <!-- or ⚠️ partial / ❌ abandoned -->
**Files**:

- modified: .github/workflows/deploy.yml
- deleted: .github/workflows/lighthouse-badger.yml
  **Summary**: 한두 문장. 무엇을 왜 했는지. 파일명 나열보다 동작·판단 근거를 적는다.
```

Rules for the fields:

- **Stage id** matches `PLAN.md` (`M0-S0.5`, `M2-S2.3`). No stage → omit the id and keep the title.
- **Status** is honest. A stage blocked on a decision is `⚠️ partial` with the blocker named in the summary; do not mark it completed.
- **Files** lists `created:` / `modified:` / `deleted:`. Skip generated output (`_site/`, `Gemfile.lock` from a plain `bundle install`).
- **Summary** records what a diff cannot: why this approach, what was rejected, what is now unverified, what surprised us. Verification results (build time, test outcome) belong here.

Separate each entry from the previous one with `---`.
