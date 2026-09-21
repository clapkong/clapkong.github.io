# BUILD_LOG.md

> `.claude/PLAN.md`의 스테이지가 끝날 때마다 **파일 맨 끝에 append**한다. 규칙은 `CLAUDE.md` § Session log.
> 오래된 항목이 위, 최신 항목이 아래. 로컬 전용(gitignored) — 공유 히스토리는 `git log`.

---

<!-- ENTRIES_START -->
<!-- 새 항목은 이 주석이 아니라 파일 맨 끝에 붙인다 -->

## [2026-09-21 01:18 KST] M0-S0.5 — 배포 복구

**Status**: ⚠️ partial — Pages 설정·코드 수정은 끝, push 후 스타일 확인 남음
**Files**:

- modified: .github/workflows/deploy.yml

**Summary**: `https://clapkong.github.io/`가 404였던 원인은 코드가 아니라 Pages 설정이었다. `build_type: legacy` + `source.branch: main`이라 GitHub이 자체 레거시 빌더(Jekyll 3.10 + github-pages gem)로 `main`을 직접 빌드하려 했고, al-folio v1 런타임은 화이트리스트에 없는 커스텀 gem이라 `The al_folio_core theme could not be found`로 매번 실패했다. 정작 `deploy.yml`(JamesIves)은 계속 성공해서 결과물이 `gh-pages`에 올라가 있었다. 사용자가 웹 UI에서 source를 `gh-pages`로 변경 → `status: built`, HTTP 200 확인. 추가로 `deploy.yml` purgecss 뒤에 `touch _site/.nojekyll` 스텝을 넣었다 — 없으면 GitHub이 완성된 산출물을 다시 Jekyll로 빌드해 `_pages/` 같은 밑줄 디렉터리를 누락시킨다. 현재 서빙되는 HTML은 아직 `baseurl: /al-folio` 시절 빌드라 로컬 CSS가 404다(외부 CDN만 200). push 후 재빌드되면 해소.

---

## [2026-09-21 01:20 KST] M0-S0.7 — 불필요 CI 정리

**Status**: ✅ completed
**Files**:

- modified: .github/workflows/render-cv.yml
- deleted: .github/workflows/visual-regression.yml
- deleted: .github/workflows/lighthouse-badger.yml

**Summary**: `render-cv.yml`은 `push:` 트리거만 주석 처리하고 `workflow_dispatch`/`workflow_call`은 남겼다 — 데모 `_data/cv.yml`(아인슈타인)이 현행 rendercv 스키마 검증에 걸려 실패하는데, 끝에서 `main`으로 auto-commit을 밀기까지 한다. M2-S2.7에서 실데이터 넣을 때 주석만 풀면 된다. `visual-regression.yml`은 v0.16.3 al-folio baseline과 픽셀 비교라 M1~M2 전면 재스킨 후엔 전부 실패가 예정되어 삭제했고, `test/visual/`과 `test:visual` 스크립트는 나중에 우리 baseline을 다시 찍기 위해 남겼다. `lighthouse-badger.yml`은 `page_build`마다 돌면서 `Input required and not supplied: token`으로 2초 만에 죽는다 — README 배지용 PAT 시크릿이 필요한데 만들 생각이 없으므로 삭제.

---

## [2026-09-21 01:22 KST] M0-S0.3 — style contract 제거

**Status**: ✅ completed
**Files**:

- deleted: test/style_contract.js
- modified: package.json (`lint:style-contract` 스크립트 제거)
- modified: .github/workflows/unit-tests.yml (style contract 스텝 제거, integration 7개 유지)
- modified: .github/pull_request_template.md (체크박스 제거)

**Summary**: PLAN은 "재범위 지정"이었으나 사용자가 삭제를 선택했다. 이 검사는 `_includes/` `_layouts/` `_sass/` `assets/tailwind/` `tailwind.config.js` 등이 존재하면 실패하는데, 그건 upstream 스타터 레포의 thin-starter 경계지 템플릿에서 만든 사이트의 규칙이 아니다(al-folio 문서도 이 모순을 인정한다). M1-S1.2에서 디자인 토큰 넣는 순간 CI가 깨질 예정이었다. **대가**: 이 검사가 겸하던 다른 assertion — `_config.yml`의 `theme: al_folio_core`와 필수 플러그인 목록, `third_party_libraries` SRI 핀, `al_math` 버전 핀 — 도 같이 사라졌다. AGENTS.md § Stop sign에 "이제 아무도 검사하지 않으니 Gemfile/`_config.yml` 플러그인 목록은 손으로 대조하라"고 기록해 뒀다.

---

## [2026-09-21 01:25 KST] 에이전트 지침 문서 정정

**Status**: ✅ completed
**Files**:

- modified: AGENTS.md
- modified: CLAUDE.md

**Summary**: 스테이지에 없던 작업. style contract를 지우고 나니 두 파일이 존재하지 않는 검사를 설명하고 있어 손보다가, **AGENTS.md 실패모드 3번이 사실과 정반대**인 것을 발견했다 — _"This repo's effective baseurl is `/al-folio`… blanking the baseurl out is what renders the site unstyled"_. 이건 upstream 데모 기준 서술이고, 방금 404를 낸 원인이며, PLAN.md §0.5에 기록된 "한 번 `/blog/`로 잘못 들어간 적 있음" 사고의 출처로 보인다. 두 파일은 매 세션 컨텍스트에 자동 로드되므로 방치하면 같은 실수가 반복된다. baseurl 항목을 user site 기준으로 다시 쓰고(키는 남기되 값은 비움, `--baseurl` 절대 전달 금지, dev server는 `:4000/`), stop sign은 "이 레포에서는 해제됨"으로 표시하고, CLAUDE.md의 daily dev loop·docker 확인 URL·CI gates 목록을 현재 상태에 맞췄다.

---

## [2026-09-21 01:27 KST] M0-S0.2 — 사이트 identity (부분)

**Status**: ⚠️ partial — `description`·`keywords`·`icon`·`contact_note` 남음
**Files**:

- modified: \_config.yml

**Summary**: `title`/`first_name`/`last_name`/`url`/`baseurl`/`enable_darkmode`는 이미 적용되어 있었다 — PLAN.md §0.5는 "title/first_name·last_name이 아직 데모값"이라고 적고 있으나 **사실과 다르다**(전체 diff를 확인). 이번 세션에서는 `middle_name:` 뒤 trailing space 하나만 제거했다. Prettier CI가 이것 때문에 깨질 상태였다. 남은 데모값은 `description`, `keywords`, `icon`, `contact_note` 넷.

---

## [2026-09-21 01:30 KST] 세션 로그 규칙 도입

**Status**: ✅ completed
**Files**:

- created: .claude/BUILD_LOG.md
- modified: CLAUDE.md (§ Session log 추가)

**Summary**: previous 레포의 BUILD_LOG 관례를 이식했다. append-only 규칙(맨 끝에 붙이기, `<!-- ENTRIES_START -->` 자리에 insert 금지)은 previous에서 로그 순서가 뒤집혔던 실제 사고에서 나온 것이라 그대로 가져왔다. 스테이지 id는 `PLAN.md`의 M0~M6 체계(`M0-S0.5`)를 쓴다. 파일은 `.gitignore`의 `.claude/*`에 걸려 커밋되지 않는 로컬 기록이다. 위 5개 항목은 이번 세션 작업을 소급 기록한 것.

---

## [2026-09-21 01:34 KST] M0-S0.5 — 배포 확인 (S0.5 종결)

**Status**: ✅ completed — 위 01:18 항목의 `⚠️ partial`을 닫는다
**Files**: 없음 (검증만)

**Summary**: 커밋 `9424a16` push 후 확인. `Deploy site` 64초 → `pages build and deployment` 60초로 성공, `https://clapkong.github.io/` HTTP 200. 서빙되는 `<head>` 리소스 27개가 로컬 빌드와 **diff 0**, CSS 3종 모두 200이고 `.navbar`/`.container`/`.row`/`.col-sm`/`.fixed-top` 포함 확인. purgecss가 tailwind.css를 27,355B→20,902B로 줄였으나 필요한 클래스는 남아 있다(`mx-auto`만 제거됨 — 현재 마크업에서 미사용).

사용자가 "스타일이 다 깨졌다"며 스크린샷을 보냈으나 **브라우저 캐시였다.** 판별 근거: 스크린샷에 다크모드 토글(🌙☀️)이 보이는데 현재 라이브 HTML에는 `light-toggle`/`fa-moon` 등이 0개다 — 즉 push 이전 HTML이고, 그 HTML은 CSS를 `/al-folio/assets/...`에서 찾으므로 전부 404가 나 무스타일로 렌더된 것. `Cmd+Shift+R`로 해소. **다음에 같은 증상이 나오면 `curl -sI <css> | grep last-modified`로 서버 쪽부터 확인할 것.**

CI 소요시간 실측: Deploy 64초 · pages 60초 · Prettier 14초 · Upgrade contract 12초 · Update TOCs 15초 · Docker 2종·star-history는 skip. **Integration tests와 CodeQL만 3분 이상** 걸리며 배포와 무관하다. `Update TOCs`는 `main`에 auto-commit을 밀 수 있으니 다음 작업 전 `git pull` 필요.

---

## [2026-09-21 01:40 KST] PROGRESS.md 도입 + S0.4 보류 결정

**Status**: ✅ completed
**Files**:

- created: .claude/PROGRESS.md
- modified: .claude/PLAN.md (§0.5의 M0 표 → PROGRESS 포인터, 읽는 순서, S0.4·M2 보류 반영)
- modified: CLAUDE.md (§ Session log — 세 파일의 역할 분담 표 추가)

**Summary**: previous의 PROGRESS.md 관례를 이식했다. MD_MIGRATION §C는 "짝(PLAN)이 사라졌으니 안 옮긴다"고 적었으나, 새 PLAN의 M0~M6이 짝 역할을 하므로 전제가 바뀌었다. 마커는 previous와 동일하게 `[ ]`/`[x]`/`[-]`를 쓰고 `[?]`(결정 대기)를 추가했다 — M3은 `IMPORT_CHECKLIST.md`가 전부 미체크라 스테이지 자체가 아직 없어서 이 마커가 필요했다. 현재 완료 6 / 미완료 28 / 보류 3 / 결정대기 2.

**S0.4(예제 콘텐츠 정리) 보류** — 사용자가 "블로그는 마지막에 수정하겠다"고 결정. 같은 이유로 M2의 블로그 홈(S2.2)·포스트 페이지(S2.3)도 M2 끝으로 밀었다. S0.4는 M4-S4.4(콘텐츠 이관)와 묶어서 한 번에 한다.

문서 중복을 정리했다: PLAN §0.5에 있던 M0 진행 표를 PROGRESS로 옮기고 §0.5는 포인터만 남겼다. 세 파일의 역할(PLAN=왜 / PROGRESS=뭐가 남았나 / BUILD_LOG=뭘 했나)을 CLAUDE.md에 표로 명시.

---

## [2026-09-21 01:48 KST] M1-S1.1 — Tailwind 빌드 경로 조사

**Status**: ⚠️ partial — 사실관계는 확정, **방향 결정은 사용자 대기**
**Files**:

- modified: .claude/PLAN.md (M1-S1.1에 조사 결과 표로 기록)
- modified: .claude/PROGRESS.md (S1.1 → `[?]`)

**Summary**: M1 세션 시작 프롬프트를 쓰려다 확인한 것. **스타일이 두 층이고 성질이 정반대다.** `main.css`는 gem의 `assets/css/main.scss` + `_sass/*.scss` 13개에서 **Jekyll이 매번 컴파일**한다(gem에 `main.css` 실물이 없고 `main.scss`만 있는 것이 근거) → 로컬 override로 쉽게 바꾼다. 반면 `tailwind.css`는 **gem이 미리 빌드해 넣은 완성 CSS를 그대로 복사**할 뿐이다 — gem의 `assets/css/tailwind.css`와 우리 `_site/` 산출물의 SHA256이 `8ec12492…`로 **동일**한 것이 결정적 증거다.

따라서 `@theme` 블록을 넣어 토큰을 바꾸려면 **Tailwind를 우리가 직접 돌려야 한다.** 그런데 `tailwind.css`에는 유틸리티뿐 아니라 레이아웃이 의존하는 **Bootstrap 호환 클래스(`.navbar` `.container` `.row` `.col-sm` `.collapse`)** 가 함께 들어 있어서, 교체하려면 `bootstrap-compat.input.css`까지 같이 빌드해야 한다. 게다가 gem `app.css`의 `@source`가 **gem 자기 경로**를 스캔하도록 쓰여 있어 우리 마크업용으로 재작성이 필요하다.

싼 길이 따로 있다: 색은 대부분 `--global-*` **CSS 변수 30개**(gem `_sass/_themes.scss`)로 빠져 있다. DESIGN.md 토큰을 여기에 매핑하면 Tailwind를 건드리지 않고도 재색상이 가능하다. 대신 `bg-accent` 같은 `@theme` 유틸리티는 못 만든다.

`package.json`의 `build:css` 금지는 style contract가 하던 것이라 **S0.3 삭제로 이미 사라졌다** — 기술적 장애물은 없고 순수한 트레이드오프 결정만 남았다.

---

## [2026-09-21 02:15 KST] M1-S1.1 — 스타일 작성 방식 결정: SCSS

**Status**: ✅ completed
**Files**:

- created: `_sass/_tokens.scss`
- created: `_sass/_base.scss`
- created: `_sass/_themes.scss` (override of `al_folio_core`)
- created: `assets/css/main.scss` (override of `al_folio_core`)
- modified: `_config.yml` (`max_width: 930px` → `1200px`)

**Summary**: **(A) Sass override 채택.** 전 세션의 조사는 맞았지만 "합법이니 트레이드오프만 남았다"는 결론이 틀렸다 — 업스트림 문서가 이미 답을 정해놨고, 이번에 사용자가 추가한 `docs/CUSTOMIZE.md`에서 확인했다.

근거 넷. ① CUSTOMIZE.md §"Changing theme color"가 **"create local `_sass/_themes.scss` and `_sass/_variables.scss` override files"** 라고 (A)를 문자 그대로 지정한다. ② §"Customizing fonts, spacing, and more"도 `_sass/` override를 지정하고, override 패턴으로 `--global-theme-color`를 명시한다. ③ §Technology Stack이 두 층의 역할을 규정한다 — "Tailwind generates core styles, while **SCSS variables/tokens provide stable theme configuration**", "theme tokens remain in `_sass/` and are **bridged into** Tailwind-based output". ④ 결정적으로 **FAQ.md §"Why does v1.x starter not have `npm run build:css` anymore?"** — Tailwind 빌드 소유권이 v0→v1에서 **의도적으로** gem으로 넘어갔다. 즉 (B)는 업스트림이 일부러 버린 것을 되살리는 일이다.

전 세션이 놓친 비용도 하나 더 나왔다: (B)에서 우리가 만들 `assets/css/tailwind.css`는 **생성물**이라 `.al-folio-overrides.yml`의 SHA256 추적 대상이 아니다. gem이 `app.css`를 바꿔도 audit가 못 잡고 조용히 어긋난다 — PLAN §1.2가 "override 관리가 유지보수의 핵심"이라 한 바로 그 지점에서 (A)보다 나쁘다. 더해서 `tailwind.css`의 bootstrap-compat 층은 **v2.0에서 제거 예정**이라, 우리 사본에 복제해두면 v2 이행 짐이 된다.

PLAN의 사실 오류 하나 정정: `al_folio.compat.bootstrap.enabled`(우리는 `false`)는 **`data-toggle` JS 동작**을 켜는 플래그고, `.navbar`/`.row`/`.col-*` **클래스 자체는 그것과 무관하게 `tailwind.css`에 박혀 있다.** 전 세션이 둘을 뭉뚱그렸다.

추가 발견 — `tailwind.css`는 27KB에 불과하고 유틸리티 세트가 **gem 마크업 기준으로 이미 스캔되어 고정**돼 있다. `gap-4` `text-sm` `grid-cols-3` `md:*` 전부 없다. 그러니 (A)는 "유틸리티를 쓰되 일부만"이 아니라 **처음부터 유틸리티를 안 쓰는 것**이다. 반대로 `bg-card`/`text-text`/`border-divider`는 `var(--global-*)`로 컴파일돼 있어서, `--global-*` 하나만 덮으면 Sass 층과 Tailwind 층이 **동시에** 바뀐다. 이게 문서가 말하는 "SCSS token bridge"의 실물이다.

구현. `_tokens.scss`가 DESIGN.md §2~§4의 단일 소스(al-folio를 전혀 참조하지 않는다), `_themes.scss`가 그걸 `--global-*` 29개로 매핑하는 어댑터. 이 분리 덕에 gem 계약이 바뀌어도 토큰 원본은 안 흔들린다. `_base.scss`는 gem partial이 아니라 우리 것이고 `main.scss`에서 **마지막에** 로드해 특이도 싸움 없이 이긴다 — `tailwind.css`가 전부 `@layer` 안에 있어서 **unlayered CSS가 캐스케이드에서 무조건 이기기 때문에** `!important`가 한 번도 필요 없었다.

S1.5(다크 잔재)도 여기서 같이 끝났다. `_themes.scss` override에서 `html[data-theme="dark"]`·`[data-theme-setting]`·`.fa-half-sun-moon`·`#light-toggle-*`를 들어냈다. Tailwind 층에는 `dark:` variant가 **애초에 하나도 없어서** 할 일이 없었다(PLAN은 있을 수 있다고 봤다). `.only-light`/`.only-dark`는 콘텐츠용 헬퍼라 남겼다.

S1.4 일부도 해결. **`max_width`는 Sass가 아니라 `_config.yml` 키였다**(CUSTOMIZE.md §"Customizing layout and UI"). `main.scss`가 `@use "variables" with ($max-content-width: {{ site.max_width }})`로 주입한다. 930px → 1200px(DESIGN.md §4).

검증: 빌드 6.7초 성공. `_site/assets/css/main.css`에 `--color-base:#faf8f5`, `--global-theme-color:var(--color-accent)` 들어갔고 gem 기본값 보라(`#b509ac`)·dark 블록·sun-moon 아이콘은 **0회** 잔존. `.container{max-width:1200px}`로 Tailwind의 `--max-content-width:930px`를 덮은 것도 확인.

**미확정 2건.** ① DESIGN.md에 **코드블록 배경 토큰이 없다** — 노트 콜아웃의 웜 뉴트럴(`#F1EFE8`)을 파생값으로 썼다(쿨 그레이를 새로 들이지 않으려고). ② DESIGN.md에 **본문 `h1`~`h6` 스케일이 없다**(페이지 타이틀 24~30px만 규정) — about 타이틀 30px에서 본문 14px로 닫히는 스케일을 파생해 뒀다. 기사가 제 페이지 타이틀보다 커지지 않게 하려는 의도. **둘 다 M2-S2.3에서 실제 포스트로 확인할 것.**

`overrides audit`는 아직 안 돌렸다 — M1 CHECKPOINT에서 `.al-folio-overrides.yml`과 함께 커밋한다.

---

## [2026-09-21 03:10 KST] M2-S2.1 — 공통 셸 (헤더/푸터) + S0.2 잔여

**Status**: ✅ completed
**Files**:

- created: `_includes/header.liquid`, `_includes/footer.liquid` (override)
- created: `_sass/_site-header.scss`, `_sass/_site-footer.scss`, `_sass/_socials.scss`
- created: `assets/img/favicon.svg`, `assets/img/apple-touch-icon.png`
- modified: `_config.yml`, `_data/socials.yml`, `assets/css/main.scss`, `.al-folio-overrides.yml`
- modified: `test/integration_new_plugins.sh`

**Summary**: **이 스테이지의 핵심 교훈은 "gem 파일을 새로 쓰지 말고 복사해서 최소 수정하라"이고, 그 대가를 실제로 치르고 얻었다.**

1차 시도에서 `header.liquid`를 백지에서 다시 썼다. DESIGN.md §5의 3단 그리드는 잘 나왔지만 **al-folio의 동작을 네 개 날렸고 빌드는 멀쩡히 통과했다**: ① `id="navbar"` 누락 → `progress-bar.js`가 `getElementById("navbar")`로 높이를 재서 스크롤 진행바를 배치하는데, 높이가 0으로 계산돼 **진행바가 헤더 뒤에 깔렸다**(`top: 0px`, 정상은 `58px`). 콘솔 에러 0건. ② `.navbar`의 `opacity: 0.95` ③ `.navbar-toggler .icon-bar`의 햄버거→X 모핑(0.2s) ④ 소셜 아이콘 hover 트랜지션. 사용자가 "애니메이션이 바뀌었다"고 지적해서 발견했다 — **내가 자체 검증으로는 못 잡았다.** AGENTS.md §"에러 없이 실패하는 세 가지"에 네 번째 유형을 추가할 만하다: _gem 마크업의 id/data-\* 훅은 JS의 계약이고, 끊어져도 아무 신호가 없다._

2차는 방식을 뒤집었다. **gem `header.liquid`를 그대로 복사한 뒤 브랜드 블록 한 군데만 수정**(홈에서 왼쪽이 비는 걸 점+이름으로 채움)하고, 색·타이포는 전부 `_sass/_site-header.scss`로 뺐다. 훅 7종(`id="navbar"` `navbar-toggler` `icon-bar` `search-toggle` `data-nav-toggle` `data-nav-dropdown-toggle` `id="progress"`) 잔존을 grep으로 확인. 이 방식이면 구조적으로 못 잃는다.

크기는 DESIGN.md와 al-folio의 **중간값**으로 합의했다(사용자 요청, 두 번 조정). 메뉴 13px(12↔14), 로고 16px(13↔20), 제목 35/27/23/20/18/15px(30↔40 등). 근거를 주석에 남겨 나중에 재판단이 가능하게 했다. 도중에 버그 하나 — 헤더를 되돌리며 로고 스타일을 `_site-footer.scss`로 옮겼는데 거기 `font-size: 13px`가 헤더 브랜드까지 먹었다. 헤더에서 `font-size`를 명시해 분리.

푸터는 DESIGN.md §7 레이아웃(좌 브랜드 / 우 링크)을 쓰되 **업스트림 크레딧 전문을 유지**했다. DESIGN.md는 `© 2026 · built with jekyll`만 그리지만 Jekyll/al-folio/GitHub Pages 표기를 빼는 건 크레딧을 조용히 떼는 일이다. Unsplash만 제거(사진을 안 쓴다).

우측은 텍스트 2열(contact/follow) → **아이콘 4개**(메일·GitHub·LinkedIn·RSS, gap 14px)로. 순서는 사용자가 매긴 중요도다. CV·Scholar는 뺐다 — CV는 LinkedIn과 내용이 같고(본인 진술: "아카데믹 vs 인더스트리 차이뿐"), Scholar는 1편. 둘 다 about에는 남겼고 각각 M2-S2.7·S2.5에서 자체 페이지가 생긴다. **푸터는 전 페이지에 반복되므로 약한 링크가 최대 노출을 가져간다** — 짧게 유지하는 근거를 주석에 적었다.

`{% social_links %}`를 푸터에서 걷어내고 명시적 목록으로 바꿨다. about(전체)과 푸터(연락처)가 서로 다른 집합을 원하기 때문. 주소값은 여전히 `_data/socials.yml` 단일 출처다.

**버그 2건 수정.** ① `#back-to-top`(fixed, 우하단)이 800~1200px에서 푸터 아이콘 위에 앉아 클릭을 막았다(42px 겹침). 컨테이너가 1200px 중앙정렬이라 ~1344px 이상에선 여백이 알아서 비켜주지만 그 아래는 full-bleed라 충돌한다 → 769~1343px에만 `padding-right: 56px`. 전 구간 재측정해 최소 간격 14px 확보. **처음 측정은 틀렸었다** — `padding-right`가 요소 박스에 포함돼 bounding rect가 안 줄어서, 마지막 아이콘 중심점의 `elementFromPoint`로 다시 쟀다. ② 푸터 아이콘 재배열 중 블록을 잘라 붙이다 경계를 잘못 잡아 LinkedIn·RSS가 중복 출력됐다. 블록 전체를 다시 써서 해결.

**이메일 보호**: `protect_email: true`. 푸터는 `.al-email-protect` + `data-eu`/`data-ed`로 주소를 쪼갠다 — `{% al_email_protect_link %}` 태그는 주소를 **텍스트**로 렌더해 아이콘을 밀어내므로 손으로 짰다. 플러그인 JS가 위임 방식이고 자식 노드를 안 건드리는 걸 소스에서 확인했다. `grep -rl "clapkong@gmail.com" _site/` = 0건이 목표인데 **현재 1건 남았다**: about 페이지의 `{% social_links %}`가 서드파티 `jekyll-socials`라 `protect_email`을 모르고 평문 `mailto:`를 찍는다. **빌드 시점 누출이라 JS로는 못 막는다.** 사용자 결정으로 M2-S2.4(about 재스킨)에서 함께 처리하고, `PROGRESS.md` S2.4에 재현·검증 명령까지 메모했다.

**`test/integration_new_plugins.sh` 수정.** `protect_email`을 켜자 "기본값은 off"를 전제한 단언이 깨졌다. 테스트가 검증하려던 건 게이팅이지 이 사이트의 취향이 아니므로, on/off **양쪽을 명시적 override로** 빌드하도록 바꿨다. 스타터 전제가 유저 사이트를 막은 두 번째 사례다(첫 번째는 S0.3의 `style_contract.js`).

**S0.2도 여기서 끝냈다.** `description`·`keywords`를 PRODUCT.md 기준으로 교체, `contact_note`를 "Email is the best way to reach me."로, 파비콘을 `⚛️`(al-folio 데모)에서 **크림 배경 없는 핑크 점 SVG**로. iOS 홈화면용 PNG만 크림 바탕을 남겼다 — iOS는 투명을 검정으로 채운다. `socials.yml`에 실제 값(email/github/linkedin/scholar) 반영, 아인슈타인 `custom_social`과 데모 `inspirehep_id` 제거.

**미해결로 남긴 것**: `cv_pdf`가 아직 al-folio 샘플 PDF(M2-S2.7에서 교체). `_data/citations.yml`이 4,179줄/144KB 아인슈타인 인용 데이터이고 `update-citations.yml`이 월·수·금 `main`에 auto-commit을 민다 — Scholar ID가 바뀌어 지금은 죽은 데이터다. S0.4와 함께 처리할 것.

**마감 조정 2건** (기록 직후 사용자 지적, `previous` 원본 값 대조).

① 스크롤 진행바 1px → **2px + 트랙**. al-folio는 트랙 없이 1px 선만 그어서 헤어라인 잔재처럼 보인다. `previous/_sass/components/_progress-bar.scss`가 2px에 `--color-divider-soft` 트랙 + `--color-accent` 채움이라 그대로 맞췄다. 한 막대에 선택자가 셋 필요하다 — 요소 자체(Firefox 트랙·레이아웃)와 WebKit이 쪼개는 벤더 의사요소 둘.

② **활성 메뉴 밑줄을 `border-bottom` → `::after`로.** 테두리는 패딩 박스 전체를 두르는데 al-folio가 `.nav-link`에 좌우 `0.5rem`을 줘서 밑줄이 글자(36px)보다 16px 넓은 52px로 나오고 패딩 바닥에 떨어져 있었다. 의사요소를 같은 값만큼 인셋해 글자 폭에 정확히 맞췄다. 576px 미만에선 gem이 좌우 패딩을 없애므로 인셋도 0으로 따라간다. 부수 효과로 **비활성 상태의 투명 테두리 예약이 불필요해졌다** — 의사요소는 흐름 밖이라 행을 밀지 않는다.

**검증**: 통합 테스트 7종 전부 PASS, `upgrade audit` blocking 0, prettier PASS, override 4/4 acknowledged.

---

## [2026-09-21 03:45 KST] M2-S2.5 — publications 실데이터 이관 (부분)

**Status**: ⚠️ partial — 데이터·버튼은 끝. 페이지 레이아웃은 미착수
**Files**:

- modified: `_bibliography/papers.bib`, `_data/venues.yml`, `_data/coauthors.yml`, `_config.yml`
- modified: `_projects/1_project.md`, `_projects/7_project.md`, `assets/css/main.scss`
- created: `_sass/_publications-site.scss`
- created: `../examples/al-folio-initial/` + `README.md` (레포 밖, git 비관리)

**Summary**: 아인슈타인 데모 5편을 지우고 실제 논문 2편(KDD 2026 정식 / ICLR 2026 워크숍, 같은 연구의 두 버전)을 넣었다.

**Google Scholar는 코드로 못 읽는다.** WebFetch도 curl도 전부 404 + Google 로봇 페이지를 받는다. 브라우저에서는 정상이므로 봇 차단이고, `bin/update_scholar_citations.py`가 쓰는 `scholarly`도 같은 벽에 막힐 것이다. 결론적으로 상관없었다 — **Scholar는 bibliography의 출처가 아니다.** 출처는 `papers.bib`이고 Scholar는 인용수만 공급한다. 이 구분을 처음에 놓쳤다.

사용자가 Scholar 내보내기 BibTeX를 붙여줬고, 거기서 세 가지를 고쳤다. ① **두 항목의 저자 표기가 서로 뒤집혀 있었다** — KDD는 `Tamatgar, Nilufer`, 워크숍은 `Nilufer, Tamatgar`. 그대로 두면 같은 사람이 두 이름으로 표시된다. ② 워크숍 항목에 `year`가 비어 있어 `booktitle`의 "ICLR 2026"에서 채웠다 — 없으면 jekyll-scholar가 연도별 정렬에서 위치를 못 잡는다. ③ 공동 1저자·교신저자 표기(`*` `†`)는 원본에 없어서 사용자 진술로 붙였다. KDD는 Yao가 둘 다 갖는다(`Yao*†`). **워크숍 쪽 Yao의 `*` 여부는 아직 미확인.**

버튼을 6개→5개로 줄였다. `DOI`와 `HTML`이 **같은 페이지로 갔다** — `doi.org/10.1145/...`가 `dl.acm.org/doi/...`로 리다이렉트하는 걸 curl로 확인하고 `html`을 뺐다(DOI가 영구 식별자라 그쪽을 남김). 워크숍은 `pdf`를 뺐다 — OpenReview 포럼이 PDF 링크와 리뷰를 다 담은 상위 집합이다. 워크숍 `abstract`도 뺐다(KDD 초록과 거의 같은 문장이라 Abs 버튼이 두 번 뜰 뿐).

**버튼 순서가 무작위로 보인 원인**: gem 레이아웃이 `Abs → DOI → Bib → PDF → Code` 순으로 내보내서 **제자리 펼침(Abs/Bib)과 페이지 이탈(DOI/PDF/Code)이 번갈아 나온다.** 항목마다 부분집합이 달라 더 어지럽다. 레이아웃 override 대신 CSS `order`로 두 무리를 갈랐다. 식별 클래스가 `award`/`abstract`/`bibtex`에만 있고 링크 버튼은 전부 `btn`을 공유하는데, 링크끼리는 순서를 다툴 이유가 없어 충분했다. **한 번 실패했다** — `Abs`·`Bib`도 `.btn`을 갖고 있어서 나중에 쓴 포괄 규칙이 같은 특이도로 이겼다. 포괄 규칙을 먼저 쓰는 순서로 해결.

파셜 이름을 `_publications.scss`로 지으려다 **gem에 동명 파일이 있어 통째로 가릴 뻔했다.** `_publications-site.scss`로 바꿨다. 이번 세션에서 같은 함정을 두 번째 밟았다(첫 번째는 `_footer.scss`).

아인슈타인 bib 항목을 지우자 데모 3곳의 `{% cite einstein1950meaning %}`가 **빌드 에러 없이 `(missing reference)`로 렌더된다.** 프로젝트 2개는 해당 문장을 뺐고, `_posts/2023-07-12-post-bibliography.md`는 글 전체가 인용 문법 데모라 손댈 수 없어 **사용자 결정으로 그대로 뒀다**(S0.4에서 처리, PROGRESS에 메모).

지우기 전에 `421e5a6`(Initial commit)의 전체 트리를 `../examples/al-folio-initial/`에 떴다. 선별하지 않은 것은 나중에 "그건 왜 안 가져왔지"를 없애려는 것. git 히스토리에 같은 내용이 있으므로 **엄밀히는 중복**이고, README에 복원 명령을 적어 지워도 무방함을 밝혔다.

**미착수**: DESIGN.md §8.6의 페이지 레이아웃 — 연도 점프 사이드바, 논문별 흰 카드, 제목 28px/margin-bottom 36px, **부제 없음**. 사용자가 "제목 부분 공백이 많다"고 지적한 것이 이 규격과의 차이다. 측정해 보니 제목 35px·margin-bottom 17.5px에 부제가 남아 있고, 제목~첫 항목이 259px이다. 부제 제거 직전에 중단했다.
