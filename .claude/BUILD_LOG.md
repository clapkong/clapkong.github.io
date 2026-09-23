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

**이메일 보호**: `protect_email: true`. 푸터는 `.al-email-protect` + `data-eu`/`data-ed`로 주소를 쪼갠다 — `{% al_email_protect_link %}` 태그는 주소를 **텍스트**로 렌더해 아이콘을 밀어내므로 손으로 짰다. 플러그인 JS가 위임 방식이고 자식 노드를 안 건드리는 걸 소스에서 확인했다. `grep -rl <내 주소> _site/` = 0건이 목표인데 **현재 1건 남았다**: about 페이지의 `{% social_links %}`가 서드파티 `jekyll-socials`라 `protect_email`을 모르고 평문 `mailto:`를 찍는다. **빌드 시점 누출이라 JS로는 못 막는다.** 사용자 결정으로 M2-S2.4(about 재스킨)에서 함께 처리하고, `PROGRESS.md` S2.4에 재현·검증 명령까지 메모했다.

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

---

## [2026-09-21 13:34 KST] M2-S2.4: about 페이지 + 이메일 보호

**Status**: ✅ completed
**Files**:

- created: `_layouts/about.liquid` (override), `_includes/section-label.liquid`, `_data/contact.yml`
- moved: `.section-label` 규칙 `_sass/_about.scss` → `_sass/_section-label.scss`
- modified: `_pages/about.md`, `_sass/_about.scss`, `_sass/_socials.scss`, `_includes/footer.liquid`, `_data/socials.yml`, `_config.yml`, `.al-folio-overrides.yml`

**Summary**: 데모 about(아인슈타인 사진, "Write your biography here...")을 DESIGN.md §8.3 의 hero + bio + skills 로 교체했다. 그 아래 latest posts / selected publications / 소셜은 al-folio 구성 그대로 두고, news 섹션만 껐다: `_news/` 에 데모 공지(2015~2016) 세 건뿐이라 없는 소식이 붙어 있었다. `_news/` 파일 정리는 S0.4 소관이라 front matter 플래그만 내렸다.

**레이아웃은 gem 파일을 복사해 세 군데만 고쳤다** (S2.1 의 교훈). ① 헤더 + float 프로필을 hero 블록으로, ② 섹션 h2 에 `class="section-label"` 추가(텍스트와 링크는 그대로), ③ `{% social_links %}` 를 명시적 목록으로. `news.liquid` / `latest_posts.liquid` / `selected_papers.liquid` include 는 손대지 않아 gem CSS/JS 계약이 그대로 남는다.

**세 가지 판단.**

① **아바타는 사진 없이 이니셜 원.** 사진이 아직 없는데 DESIGN.md §8.3 이 애초에 아바타를 "110px 원, 배경 `--color-soft`" 로 규정해서 빈 원 자체가 규격이다. 그 안에 Georgia 소문자 `s` 를 넣었으니 자리표시자로 보이지 않는다. 사진이 생기면 front matter `hero.image` 한 줄로 바뀌고 CSS 는 그대로다.

② **크기를 한 단계씩 올렸다** (사용자 요청 "조금 더 큼직큼직하게"). 아바타 110 → 124px, intro 14 → 15px, bio 13 → 14px, skills 12 → 13px. 타입 스케일은 안 건드렸다: 이름은 §8.3 의 30px 대신 사이트 h1(35px)을 쓴다. 페이지마다 제목 크기가 달라지지 않게 하려는 것이고, 35px 자체가 S2.1 에서 정한 중간값이다.

③ **아래쪽 gem 섹션 제목도 이탤릭 라벨 + 구분선으로 통일**(사용자 선택). 한 페이지에서 bio/skills 는 이탤릭 라벨, latest posts 는 27px Georgia h2 로 두 문법이 섞이는 게 문제였다. 마크업은 그대로 두고 클래스만 붙여 CSS 로 해결했으므로 되돌리기 쉽다.

`.section-label` 은 about 전용이 아니라 사이트 컴포넌트다(DESIGN.md §3 이 "이탤릭 라벨은 사이트의 서명" 이라 하고 §8.5 / §8.7 이 같은 걸 쓴다). 처음에는 `_about.scss` 에 뒀는데, 그 사이 projects 세션이 같은 걸 쓰려고 빈 `_sass/_section-label.scss` 와 `@use` 줄을 만들고 "옮기는 사람이 소유한다" 고 적어둬서 이번에 옮겼다. main.scss 가 페이지 파셜보다 먼저 로드하므로 페이지가 자기 몫을 덮는 데 문제가 없다. `_includes/section-label.liquid` 는 그대로 공유한다.

**페이지 좌우 패딩은 `:has(.about-hero)` 로 스코프했다.** DESIGN.md §4 는 단단 페이지에 80px 을 주지만 사용자가 화면에서 보고 40px 로 줄였다(본문 띠 1010px 대비 1090px). 컨테이너 1200px 은 S1.4 결정대로 안 건드렸다. default 레이아웃이 페이지별 body 클래스를 안 붙여서 CSS 만으로 이 페이지를 집을 방법이 `:has()` 뿐이었다. 모르는 브라우저는 컨테이너 패딩만 받는데 그게 무난한 폴백이다. `_layouts/default.liquid` override 가 정공법이지만 파일 하나를 통째로 떠안게 되므로 택하지 않았다. bio 문단은 640px, hero 소개는 520px 에서 끊는다(규격은 600/480).

**이메일: 만들고, 끄고, 다시 만들었다.** 처음에는 PROGRESS 메모대로 서드파티 `jekyll-socials` 의 `{% social_links %}` 를 걷어내고 플러그인의 `.al-email-protect` 분할 패턴을 써서 `grep -rl <내 주소> _site/` 를 1건에서 0건으로 만들었다. 그런데 동작을 본 사용자가 **메일 앱이 바로 열리는 편을 택했다.** 플러그인은 복사만 하므로 `protect_email` 을 `false` 로 내리고 보호는 직접 구현했다.

`.site-email` 링크가 주소를 `data-eu`/`data-ed` 두 속성으로 나눠 들고, 푸터의 스크립트가 클릭 시점에 합쳐 `location.href` 로 연다. `window.open` 이 아닌 이유는 `mailto:` 를 새 탭으로 열면 대부분의 브라우저가 빈 탭을 남기기 때문이다. 리스너는 document 에 위임해서 about 과 푸터 두 아이콘을 하나가 담당한다. JS 가 없으면 `<noscript>` 가 `clapkong [at] gmail [dot] com` 을 보여준다. 사용자는 "그냥 복사되도록" 을 제안했으나 **복사도 JS 가 필요해서** 폴백이 될 수 없다는 점을 알리고 이 형태로 정했다.

**주소를 `_data/socials.yml` 에서 `_data/contact.yml` 로 옮긴 것이 이 작업의 핵심이다.** 마크업만 고쳐서는 부족했다: ① `{% social_links %}`, ② `⌘K` 검색 팔레트가 각각 socials.yml 의 `email` 키를 읽어 `mailto:` 를 전 페이지에 박는다. 특히 팔레트는 al_search 가 **gem 안의 Liquid 템플릿**(`lib/templates/search-data.liquid.js`)을 Ruby 태그로 렌더하는 구조라 `_includes/` override 가 통하지 않는다. 데이터를 그 파일 밖으로 빼는 것이 유일한 차단 방법이었다. `metadata.liquid` 의 schema.org 이메일은 gem 이 이미 `{% comment %}` 로 막아뒀다.

**CLAUDE.md 구두점 금지 규칙이 작업 도중에 추가됐다.** 새로 쓴 파일에 em dash 와 가운뎃점이 23군데 있어서 전부 고쳤다. 특히 skills 목록은 `previous` 에서 그대로 가져와 가운뎃점이 12개 딸려 왔다. 슬래시로 바꿨다.

**검증**: 빌드 5.9초, `grep -rl <내 주소> _site/` 0건(테스트 스크립트 본문 제외), 팔레트 `social-email` 항목 0건, Playwright 로 클릭 시 조립 결과가 `mailto:<내 주소>` 이고 URL 에 `#` 이 안 붙는 것(preventDefault) 확인, 콘솔 에러 0건. 통합 테스트 4종(new_plugins / plugin_toggles / css_minify / comments) PASS, prettier PASS, `upgrade audit` blocking 0, override 6건 중 우리 것 5건 acknowledged(`_includes/scripts.liquid` 은 다른 세션 것). 데스크톱 1440px, 모바일 390px 스크린샷 확인.

**한 번 헛다리**: `integration_new_plugins.sh` 가 `RTL demo post was not built` 로 실패했는데 원인은 다른 세션이 레포 루트에 만든 `check-tmp.cjs` 가 빌드 도중 사라진 것이었다(`Errno::ENOENT` in `static_file.rb`). 재실행하니 PASS. **레포 루트에 임시 파일을 만들면 동시에 도는 빌드를 죽인다.** 이 세션도 Playwright 스크립트를 루트에 두고 돌렸다: node 가 `node_modules` 를 찾아야 해서였는데 같은 사고를 낼 수 있는 방식이었다.

**남긴 것**: ① `_pages/about_einstein.md` 도 `layout: about` 이라 이제 hero 를 타는데 front matter 에 `hero:` 가 없어서 빈 원 + 사이트 이름으로 렌더된다. 데모 페이지라 S0.4 / M4-S4.4 에서 같이 정리한다. ② 연락처 줄의 CV 아이콘은 아직 al-folio 샘플 PDF 를 가리킨다(M2-S2.7). ③ publications 는 아직 좌우 패딩이 없어 about 보다 80px 넓다. S2.5 에서 40px 으로 맞춰야 두 페이지가 같아진다.

---

## [2026-09-21 13:36 KST] M2-S2.8 (404) — 404 페이지

**Status**: ⚠️ partial: 404는 끝. 같은 스테이지의 archive(year/tag/category)는 미착수. YouTube 영상 id 하나가 비어 있다
**Files**:

- modified: `_pages/404.md`, `_sass/_404.scss`, `CLAUDE.md`

**Summary**: DESIGN.md §8.9을 구현했다. `assets/css/main.scss`는 다른 세션이 쓰고 있어 건드리지 않았고, `_base.scss`도 손대지 않았다.

**`layout: page` 대신 `layout: default`.** gem `page.liquid`가 `.post-header` 안에 `.post-title`(h1)과 `.post-description`을 찍는데, 이 페이지에서는 120px "404" 숫자가 곧 제목이라 그 둘이 그대로 중복이 된다. `.post-title`은 전역이고 지금 publications 세션이 크기를 다루는 중이라 CSS로 숨기는 것도 그쪽과 물린다. `default`로 내리면 `{{ content }}`가 `.container.mt-5` 바로 안에 들어와 마크업을 전부 우리가 쥔다. front matter의 `title`/`description`은 `<head>`와 크롤러용으로 남겼다.

**`redirect: true` 제거.** `default.liquid:22-31`이 이 키를 보고 `<meta http-equiv="refresh" content="3; url=/">`를 찍는다. 3초 뒤 홈으로 튕기므로 여기서 만든 것이 사실상 안 보인다. 레이아웃 override 없이 front matter에서 키만 빼면 된다. 대신 `← home` 링크가 이동 수단이다. 검증: `grep -c 'http-equiv="refresh"' _site/404.html` = 0.

**폰트는 Georgia로 보류.** §8.9은 Playfair Display 300 / 120px을 요구하지만 이 사이트는 웹폰트를 하나도 안 불러온다. `previous`를 확인해 보니 `_includes/head.html:24-28`에 `{% if page.layout == '404' %}` 조건부 Google Fonts 링크가 이미 있었으나, `_layouts/404.html`도 `_pages/404.md`도 없고 `assets/css/main.scss:64`의 `// @import "pages/404";`도 주석 상태다. 즉 **`previous`의 404는 목업(`mockups/404.png`)까지만 갔고 구현된 적이 없다.** 사용자가 직접 woff2를 받아 넣겠다고 해서, `_sass/_404.scss` 맨 위에 `@font-face` 블록을 주석으로 두고 `$display-font` 한 줄만 바꾸면 전환되게 했다. Georgia에는 300이 없어 400으로 렌더되므로 목업보다 굵다.

**음악 플레이어는 넣되 자동재생은 뺐다.** 브라우저가 소리 있는 자동재생을 막기 때문에 "auto-started"라는 표시가 대부분의 방문에서 거짓이 된다. 부제를 `press play while you're lost`로 바꾸고, 재생을 누르면 `now playing`으로 교체한다.

구현에서 YouTube IFrame API를 쓰지 않았다. **누르기 전에는 iframe 자체가 없다.** 클릭 시 `youtube-nocookie.com/embed/<id>?autoplay=1`을 주입하고, 정지하면 iframe을 제거한다. 클릭이 곧 사용자 제스처라 그 안에서는 autoplay가 허용된다. 얻는 것: 404 방문 한 건에 서드파티 스크립트 요청 0, 쿠키 0. 잃는 것: 정지 후 다시 재생하면 0초부터다. 404 페이지에서 감당할 만한 값이라고 봤다.

검증은 headless chromium으로 했다. 재생 클릭 후 `is-playing` 클래스, `aria-pressed=true`, iframe 1개(`...nocookie.com/embed/...autoplay=1&rel=0`), pause 아이콘 표시, 웨이브 애니메이션 동작을 확인했고 정지 후 iframe 0개로 돌아간다. 콘솔 에러 0, 1280/390 양쪽에서 가로 스크롤 없음.

**영상 id가 아직 비어 있다.** `data-yt-id="REPLACE_WITH_YOUTUBE_ID"`이고, 이 상태에서는 JS가 카드를 `hidden` 처리한다. 깨진 플레이어를 보이느니 없는 편이 낫다는 판단이다. id만 채우면 카드가 살아난다.

**`.container:has(> .page-404) { margin-top: 0 }`** 한 줄이 필요했다. gem이 콘텐츠를 `.container.mt-5`로 감싸서 48px이 §8.9의 70px 위에 더 얹힌다. Tailwind의 `mt-5`가 `@layer` 안에 있어 unlayered 규칙이 `!important` 없이 이긴다(M1에서 확인한 성질).

**발견: `sticky-bottom-footer`가 실제로는 동작하지 않는다.** body에 클래스는 붙는데 `min-height: 0px` / `display: block`이라 짧은 페이지에서 푸터 아래에 크림색 여백이 남는다. 1280x900에서 404는 599px, publications는 757px에서 문서가 끝난다. **이 세션이 만든 문제가 아니라 전역 현상**이고, 404가 사이트에서 가장 짧은 페이지라 제일 눈에 띌 뿐이다. `.page-404`에 `min-height`를 주는 국소 처방은 나중에 전역으로 고칠 때 충돌하므로 하지 않았다. 셸(S2.1) 소유 쪽에서 볼 문제다.

**`overrides audit`에 `_sass/_404.scss`가 안 잡힌다** = gem에 동명 파일이 없다는 확인이다. 이번엔 `_footer.scss`/`_publications.scss` 때 밟은 함정을 피했다.

**`CLAUDE.md`에 구두점 금지 규칙 추가.** 사용자가 em dash(`—`)와 중간점(`·`)을 절대 금지로 못박았다. 사이트 카피, 주석, 커밋 메시지, `.claude/*.md`까지 전부 해당한다. 기존 문서에 이미 박힌 것(`AGENTS.md`, 과거 로그 엔트리, 푸터의 `© 2026 · built with jekyll`)은 그 파일을 다른 이유로 만질 때 같이 정리하기로 하고 일괄 치환은 하지 않았다.

**검증**: 빌드 성공, prettier PASS, `integration_css_minify.sh` PASS, `overrides audit` 5건 중 404 관련 0건.

---

## [2026-09-21 13:50 KST] M2-S2.8 (404) — 영상 id 확정

**Status**: ✅ completed
**Files**:

- modified: `_pages/404.md`

**Summary**: 사용자가 준 주소로 `data-yt-id`를 `3_l-UI4prVY`로 채웠다. 이제 카드가 보인다.

**DESIGN.md의 아티스트 표기가 틀렸다.** YouTube oEmbed(`/oembed?url=...&format=json`)로 조회하니 `author_name`이 `KiiiKiii`(i가 세 개)다. §8.9과 목업은 `KiiKii`로 적고 있다. 실제 이름 쪽으로 맞췄다. 곡명 `404 (New Era)`는 그대로 맞다.

**임베드 가능 여부를 실제로 확인했다.** 뮤직비디오는 레이블이 외부 임베드를 막는 경우가 있어 그냥 넘기면 안 되는 지점이다. 두 번 쟀는데 첫 번째가 틀렸다: `youtube-nocookie.com/embed/<id>`를 브라우저에서 **직접** 열면 `오류 153`이 난다. 이건 임베드 차단이 아니라 referrer/origin이 없어서 나는 것이라 판정에 쓸 수 없다. 실제 404 페이지 안에 띄워 프레임 내부를 읽으니 정상이었다: `duration 179.601`, `currentTime 7.03`, `paused false`, `video.error` 없음. 즉 임베드 허용이고 클릭 제스처 안에서 자동재생도 통과한다.

`curl`로 embed 페이지를 받아 `playabilityStatus`를 찾는 방법은 쓸 수 없다. 147KB짜리 JS 셸만 오고 재생 정보가 인라인으로 들어 있지 않다.

id 가드를 `videoId === "REPLACE_WITH_YOUTUBE_ID"`에서 `!videoId`로 단순화했다. 자리표시자 문자열은 역할이 끝났고, id가 비면 카드를 숨긴다는 동작만 남기면 된다.

**검증**: 빌드 성공, prettier PASS, 1280/390 양쪽 콘솔 에러 0, 가로 스크롤 없음, 재생/정지 토글과 iframe 생성/제거 정상.

---

## [2026-09-21 13:56 KST] M2-S2.8 (404) — 사용자 피드백 반영

**Status**: ✅ completed
**Files**:

- modified: `_pages/404.md`, `_sass/_404.scss`

**Summary**: 실물을 보고 나온 지적 세 건을 반영했다.

**① "여백이 너무 많다" = 앞 엔트리에서 전역 문제라고 넘긴 그 푸터 건이었다.** 판단이 틀렸다. 1280x900에서 푸터가 711px에서 끝나고 아래 189px이 빈 채로 남아 페이지가 잘린 것처럼 보인다. "전역이니 셸 쪽 일"이라는 게 사용자에게는 그냥 깨진 화면이다.

404 페이지에서만 고쳤다. `<footer>`가 `<body>`의 직계 자식이라 `body:has(.page-404)`에 세로 flex를 주고 `.container`에 `flex: 1 0 auto` + `justify-content: center`를 주면 끝난다. body의 나머지 자식은 `<script>`(display:none), `#back-to-top`(position:fixed), 높이 0인 `<ninja-keys>`라 레이아웃에 끼지 않는다. 결과: 푸터 bottom 900px, 남는 공간 0.

**전역으로 안 고친 이유는 그대로다.** `_base.scss`와 `assets/css/main.scss`를 다른 세션이 쓰고 있다. 셸(S2.1) 쪽에서 전역 처리가 들어오면 이 세 줄은 지우면 된다. 주석에 적어뒀다.

설명이 두 번 안 통해서 세 번째는 **before/after 스크린샷을 만들어 띄웠다.** 고친 규칙을 `addStyleTag`로 되돌린 페이지와 현재 페이지를 같은 뷰포트로 찍어 나란히 열었다. 말로 두 번 실패한 걸 그림 한 장이 해결했다. 레이아웃 문제는 이 방식이 빠르다.

**② 음원 무단 사용처럼 보인다.** 출처를 두 군데에 넣었다. 곡 제목을 `youtu.be/3_l-UI4prVY` 링크로 바꿨고(새 탭), 카드 아래 9px 모노로 `streamed from YouTube`를 뒀다. 역할이 갈린다: 버튼은 제자리 재생, 제목은 출처. 출처 문구만 확대에서 빼고 9px로 남겼다.

**③ 카피.** 처음엔 설명을 세 문장으로 썼다가 "너무 verbose, chill한 개발자 느낌 선호"라는 지적을 받고 소문자 한 줄로 줄였는데, 사용자가 **원래 al-folio 기본 문구를 그대로 지정**했다: `Looks like there has been a mistake. Nothing exists here.` / `← please go back to the home page.` 즉 원하던 건 내 문장이 아니라 예전 문구였다. 리다이렉트 안내문에 있던 "please go back to the home page"를 home 링크 자리로 옮긴 셈이다.

**크기 조정** (사용자 요청: 플레이어와 home을 키우고 아래로). 재생 버튼 32→42px, 아이콘 14→17px, 곡 제목 12→14px, 부제 9→10px, 웨이브 바 2x14→3x18px, home 12→14px. 설명문 아래 간격 40→72px로 벌려 플레이어 블록 전체를 내렸다. 카드 상하 패딩 12→16px, 좌우 18→24px.

**검증**: 빌드 성공, prettier PASS, 1280/390 콘솔 에러 0, 가로 스크롤 없음, 재생/정지 토글 정상, 푸터 bottom = 뷰포트 높이. 390px에서 home 링크가 한 줄에 겨우 들어간다. 320px대에서는 두 줄로 접히며, 접히게 뒀다.

---

## [2026-09-21 14:05 KST] M2-S2.8 (404) — 마감 조정

**Status**: ✅ completed
**Files**:

- modified: `_pages/404.md`, `_sass/_404.scss`

**Summary**: 실물을 두 번 더 보고 나온 미세 조정. 앞 엔트리에서 키운 것을 일부 되돌렸다.

**직전 라운드에서 두 가지를 과하게 했다.** ① 플레이어를 "아래로" 내리려고 설명문 아래 간격을 40→72px로 벌렸는데, 그게 설명문과 카드를 갈라놔 빈 띠로 보였다. 28px로 줄였다. 원하던 건 간격이 아니라 카드 자체의 존재감이었다. ② 카드를 42px 버튼까지 키웠더니 이번엔 커 보였다. 원래(32)와 키운 것(42)의 중간인 36px로, 곡 제목 14→13px, 패딩 16/24→14/22px, 웨이브 16→14px 높이로 되돌렸다.

**"길이를 늘려"는 크기가 아니라 비율 문제였다.** `inline-flex`라 카드 폭이 내용에 딱 맞아 라벨처럼 보였다. `min-width: 380px` + `.page-404__meta`에 `flex: 1 1 auto`를 줘서 남는 폭을 제목 블록이 먹고 웨이브가 오른쪽 끝으로 밀리게 했다. 이제 띠로 읽힌다. 모바일에서는 380px가 390px 뷰포트를 넘으므로 `min-width: 0`으로 푼다.

**`streamed from YouTube`를 캡션으로 만들었다.** 카드 아래 간격 14→6px, 그 아래 간격은 40px 유지. 위로 붙이고 아래로 떼는 것만으로 독립된 줄이 아니라 박스에 달린 주석으로 읽힌다.

**home 링크 문구는 두 번 바뀌었다.** `← home` → `← please go back to the home page.`(옛 al-folio 문구 지정) → `← Home Page`. 앞 문장이 이미 상황을 설명하므로 링크까지 문장일 필요가 없다는 판단이다.

**마지막으로 카드와 캡션을 한 덩어리로 묶었다.** 위 28px / 아래 40px로 어긋나 있어서 둘 다 36px(모바일 30px)로 맞췄다. 브라우저로 실측해 맞춘 값이다: 여백은 margin만이 아니라 line-height 여유까지 더해져 보이므로, 눈으로 맞추면 틀린다. 두 margin이 짝이라 한쪽만 바뀌면 깨지므로 양쪽 주석에 서로를 가리키게 적었다. 카드와 캡션 사이 6px은 그대로 뒀다.

**검증**: 빌드 성공, prettier PASS, 1280/390 콘솔 에러 0, 가로 스크롤 없음. 카드 실측 380x66, 여백 36/6/36. 재생 시 iframe 1개/`now playing`, 정지 시 0개로 복귀.

---

## [2026-09-21 14:15 KST] M2-S2.8 — 스테이지 마감 + archive 이동

**Status**: ✅ completed
**Files**:

- modified: `.claude/PROGRESS.md`

**Summary**: 결정 두 건으로 S2.8을 닫았다.

**폰트는 Georgia로 확정**(사용자 결정). DESIGN.md §8.9의 Playfair Display 300은 쓰지 않는다. 이로써 **웹폰트 0개**라는 사이트 전제가 유지된다. `_sass/_404.scss`의 `@font-face` 주석과 `$display-font` 한 줄은 그대로 둔다. 나중에 마음이 바뀌면 그 두 곳만 건드리면 되고, 지워두면 다음 사람이 처음부터 다시 조사한다.

**archive는 S2.3a로 옮겨 블로그 묶음에 붙였다.** `/blog/2025/`, `/blog/tag/<t>/`, `/blog/category/<c>/`는 gem이 포스트를 훑어 자동 생성하는 페이지다. 즉 블로그 홈(S2.2)과 포스트(S2.3)에서 파생되므로 그 둘보다 먼저 손댈 이유가 없고, 지금 스타일을 잡아도 목록에 뜨는 건 전부 al-folio 데모 포스트다. S2.2/S2.3이 이미 "블로그는 마지막"으로 보류 상태라 같은 줄에 세웠다.

남은 것은 이 스테이지 밖이다: 전역 `sticky-bottom-footer`(셸 S2.1), archive(S2.3a).

---

## [2026-09-21 14:29 KST] M2-S2.8 (404) — 세로 정렬을 라벨 기준으로

**Status**: ✅ completed
**Files**:

- modified: `_pages/404.md`, `_sass/_404.scss`

**Summary**: "PAGE NOT FOUND가 화면 정중앙에, 음원과 home은 절단선 아래에" 라는 요구. 덩어리 전체를 가운데 두던 것을 **라벨 한 줄을 기준점으로** 바꿨다.

**구조**: `404`를 `.page-404__above`로, 나머지를 `.page-404__below`로 감싸고 라벨을 그 사이에 뒀다. 두 덩어리가 `flex: 1 1 0`으로 남는 공간을 똑같이 나눠 가지므로 사이에 낀 라벨의 중심이 자동으로 컨테이너 중심에 온다. 숫자를 박지 않아도 된다.

**앞 라운드의 사실 오류를 정정한다.** 이전 엔트리에 "Tailwind가 전부 `@layer` 안이라 unlayered CSS가 `!important` 없이 이긴다"고 적었는데, `.container:has(> .page-404) { margin-top: 0 }`은 **한 번도 적용된 적이 없었다.** `tailwind.css`의 bootstrap-compat 층이 `@layer components` 안에서 `.mt-5{margin-top:3rem!important}`로 선언한다. `!important`는 레이어와 무관하게 normal 선언을 이긴다. 일반론은 맞지만 `!important` 유틸리티에는 틀렸다. 규칙을 지우고 48px을 그냥 계산에 포함시켰다.

**두 덩어리가 반반이 아니었다.** `.page-404__below`에 `padding-top: 36px`을 줬는데 전역 `box-sizing: border-box` 때문에 **`flex-basis: 0`이어도 패딩만큼은 flex base size로 잡힌다.** free space가 그만큼 줄어 위 254 / 아래 290으로 갈렸고, 라벨이 18px 위로 밀렸다. 값이 정확히 절반(36/2)만큼 어긋난 것이 단서였다. 패딩을 flex 아이템에서 빼고 `.page-404__note`의 margin으로 옮겨 해결했다.

**중심선이 화면 중앙과 어긋나는 원인은 푸터였다.** 컨테이너 위 공간(104px)보다 아래 공간(154.5px)이 크다. 차이의 대부분은 푸터의 `margin-top: 64px`이다. 이 페이지는 푸터를 이미 바닥에 고정했으므로 그 여백은 죽은 공간이라 404에서만 걷어냈다. 결과: 1280x900과 1280x700에서 라벨 중심이 정중앙 **아래 6.8px**. 보정용 매직넘버를 넣는 것보다 원인을 없애는 쪽이 화면 크기가 바뀌어도 버틴다.

**모바일은 30px 위로 남는다.** 390px에서 푸터가 3줄로 접혀 151.5px이 되어 비대칭이 60px 남는다. 정확히 맞추려면 위쪽에 60px을 더 넣어야 하는데, 그러면 아래 덩어리가 푸터에 닿는다. 요구 조건(음원과 home이 절단선 아래)은 지켜지므로 여기서 멈췄다.

**여백**: 사용자 지적대로 `404 → 라벨`과 `라벨 → 설명문`을 둘 다 12px로 맞췄다(`$below-offset`). 라벨이 대칭인 한 쌍 사이에 놓인다.

**검증**: 빌드 성공, prettier PASS, 1280/390 콘솔 에러 0, 가로 스크롤 없음, 재생/정지 정상. 카드 위아래 여백 36/6/36 유지.

---

## [2026-09-21 14:32 KST] M2-S2.8 (404) — 기준선을 설명문 아래로

**Status**: ✅ completed
**Files**:

- modified: `_pages/404.md`, `_sass/_404.scss`

**Summary**: "`404` / `PAGE NOT FOUND` / `Looks like...` 이 부분만 위로, 아래는 그 자리 그대로." 앞 라운드에서 라벨을 기준점으로 삼았는데, 그러면 설명문이 아래 절반에 속해 같이 내려간다. 설명문을 위 덩어리로 옮겨 **기준선이 설명문과 음원 박스 사이**에 오게 했다.

구조는 그대로다. 두 덩어리가 `flex: 1 1 0`으로 반씩 나눠 가지므로 경계가 화면 중앙에 온다. 달라진 건 무엇이 어느 덩어리에 속하느냐뿐이다.

**"아래는 그대로"가 조건이라 오프셋을 역산했다.** 경계가 456.8px, 음원 박스가 있던 자리가 537px이므로 차이 80px을 박스의 `margin-top`으로 줬다. 이 값을 올리면 박스가 내려가는 게 아니라 **위 덩어리가 더 올라간다.** 아래 덩어리는 경계에서 고정 거리를 유지하기 때문이다. 결과: 설명문 바닥이 501 → 457로 44px 올라갔고 박스 537 / home 661은 그대로.

`padding`이 아니라 `margin`으로 준 이유는 앞 엔트리와 같다. `box-sizing: border-box`에서 flex 아이템의 패딩은 base size로 잡혀 두 덩어리를 어긋나게 만든다.

**모바일은 40px로 따로 뒀다.** 390x800에서 80px이면 아래 덩어리가 푸터를 파고든다.

라벨은 이제 기준점이 아니므로 중앙에서 37.8px 위에 있다. 사용자가 요구한 것은 라벨 위치가 아니라 세 줄 묶음이 절단선 위에 있는 것이다.

**검증**: 빌드 성공, prettier PASS, 1280/390 콘솔 에러 0, 가로 스크롤 없음, 재생/정지 정상. 간격 12/12, 설명문에서 박스까지 80, 박스에서 캡션 6, 캡션에서 home 36.

---

## [2026-09-21 14:47 KST] M2-S2.8 (404) — impeccable audit + 후속 수정

**Status**: ✅ completed
**Files**:

- modified: `_pages/404.md`, `_sass/_404.scss`, `CLAUDE.md`

**Summary**: 사용자가 **"페이지 완성을 confirm하면 무조건 impeccable을 한 번 돌린다"** 를 규칙으로 정했다. `CLAUDE.md` §"Run `impeccable` when a page is confirmed done"에 적었다. 그 첫 적용이 이번 404다.

`impeccable audit`, register는 PRODUCT.md가 명시한 `brand`. **15/20, Good.** 성능 4/4, anti-pattern 4/4(AI 티 없음), 접근성 2/4, 반응형 2/4, 테마 3/4.

**진짜 버그를 하나 잡았다.** 320x568(iPhone SE 급)에서 `← Home Page`가 **화면에서 사라진다.** 홈 링크 바닥이 푸터 상단을 52px 파고들어 뒤에 깔린다. 404에서 나가는 유일한 수단이 안 보이는 것이니 심각도가 높다. 원인은 내가 넣은 `min-height: 0`이다. 두 덩어리를 반반으로 유지하려고 내용보다 작게 줄어드는 걸 허용했는데, 짧은 화면에서는 아래 덩어리가 자기 몫을 넘겨 넘친 만큼 푸터 뒤로 간다. **1280x900만 보고 넘겼으면 못 잡았을 것이다.**

고친 방식: `@media (max-height: 620px)`에서 반반 분할을 끄고 그냥 가운데 정렬한다. 임계값을 처음에 700px로 잡았다가 1280x700처럼 **안 깨지던 레이아웃까지 대체 방식으로 바뀌는 것**을 보고 620px로 내렸다. 9개 사이즈(320x568 ~ 1920x1080)에서 충돌 0, 가로 스크롤 0을 확인했다.

**`<h1>`이 하나도 없었다.** `layout: page`를 버리면서 gem이 주던 `<h1 class="post-title">`이 사라졌는데 마크업을 새로 쓰며 전부 `<p>`로 찍었다. 변명의 여지가 없는 누락이다. `404`를 `<h1>`으로 바꿨다. `_base.scss`가 `h1`을 기사 본문용으로 스타일링하므로 `.page-404__code`가 모든 값을 다시 선언한다(클래스가 요소 선택자를 이긴다).

**재생 버튼 터치 타깃을 보이는 크기를 안 바꾸고 넓혔다.** 36px 원은 그대로 두고 `::after`로 44x44 투명 영역을 겹쳤다. 카드의 16px gap이 버튼 밖으로 4px 나가는 것을 흡수해 곡 제목 링크를 덮지 않는다. `elementFromPoint`로 중심에서 22px 위 지점이 버튼으로 잡히는 것을 확인했다.

**대비는 고치지 않기로 했다(사용자 결정).** 텍스트 8종 중 5종이 WCAG AA 미달인데 **그중 5건이 404의 문제가 아니라 팔레트의 문제다**: `--color-meta` `#8b7355`가 크림 위에서 4.23:1, `--color-accent` `#c99696`가 2.39:1. 둘 다 `_tokens.scss`에 있고 사이트 전역이 쓴다. PRODUCT.md는 "WCAG AA as baseline"이라 선언하지만 실제로는 본문(`#2d2d2d`, 12.99:1)만 지켜진다.

`← Home Page`(2.39:1)에 대해 세 안을 렌더해 보여줬다: ⓐ 그대로 ⓑ accent와 text를 55:45로 섞어 4.86:1 ⓒ 글자는 본문색에 밑줄만 핑크로 12.99:1. **사용자가 ⓐ를 선택했다.** 404는 오래 머무는 페이지가 아니고, 바로 위에 같은 안내 문장이 있다. 404만 색을 바꾸면 사이트의 다른 핑크와 어긋나기도 한다. **`_tokens.scss`를 열 수 있을 때 사이트 전체로 다시 볼 사안으로 남긴다.**

**죽은 코드 제거**: 사용자가 `$below-offset`을 80px에서 40px로 직접 낮춰서 미디어 쿼리의 모바일 전용 `margin-top: 40px`이 데스크톱 값과 같아졌다. 지웠다.

**미해결로 남긴 것**(전부 P2/P3): 재생 아이콘 흰색 on accent 2.53:1(필요 3), 포커스 링 2.39:1(SC 1.4.11, 필요 3), `aria-pressed`와 `aria-label`을 둘 다 바꿔 이중 안내, 재생 상태 문구 교체가 `aria-live` 없이 조용함, 하드코딩 3건(`opacity: 0.75`, 웨이브 `border-radius: 1px`, 카드 `min-width: 380px`). 곡 제목 링크 18px은 **필수 동작이 아니라는 사용자 판단으로 그대로 둔다.**

**검증**: 빌드 성공, prettier PASS, em dash/중간점 0건, 9개 뷰포트 충돌·가로 스크롤 0, `h1` 존재, 재생/정지 iframe 1개/0개, 간격 40/6/36 유지.

---

## [2026-09-21 14:57 KST] M2-S2.8 (404) — 잔여 감점 처리 결정

**Status**: ✅ completed
**Files**:

- modified: `.claude/PROGRESS.md`

**Summary**: audit의 남은 감점 4점을 **고치지 않기로 확정했다.** 점수를 채우는 것이 목적이 아니고, 셋 중 둘은 고치면 코드가 나빠진다.

**하드코딩 3건은 전부 유지.** 감점 사유가 "값이 틀렸다"가 아니라 "`_tokens.scss`를 안 거쳤다"는 형식 문제인데, 세 값 모두 토큰화가 부적절하다.

- `opacity: 0.75`(출처 문구): 빼면 대비가 2.76 → 4.23으로 오르지만 **사용자가 "잘 안 보여도 된다"고 판단했다.** 출처는 읽히라고 넣은 것이 아니라 밝히라고 넣은 것이고, 페이지에서 가장 조용해야 할 줄이다
- 웨이브 막대 `border-radius: 1px`: 막대 폭이 3px인데 토큰의 최소 둥글기가 4px이다. 토큰을 쓰면 막대가 콩알로 뭉개진다. 1px은 의도한 헤어라인
- 카드 `min-width: 380px`: 레이아웃 판단이지 색·간격 체계와 무관하다. 실측으로 근거를 남긴다. 데스크톱에서 이 값이 없으면 카드가 309px로 줄어 라벨처럼 보이고 웨이브가 제목에 붙는다. 380px이면 남는 71px을 제목 칸이 먹어 웨이브가 오른쪽 끝으로 밀리고 띠로 읽힌다. 폰에서는 차이가 0이다(390px에서 289px, 320px에서 250px). 미디어 쿼리가 `min-width: 0`으로 풀기 때문이고, 안 풀면 화면 밖으로 나간다

**곡 제목 링크 터치 영역(18px)도 유지.** 재생은 버튼이, 출처는 제목이 맡아 역할이 갈려 있고 제목 링크는 필수 동작이 아니다. 필요해지면 재생 버튼에 쓴 `::after` 방식을 그대로 복사하면 된다.

**최종 16/20.** 남은 감점은 접근성 2점(`_tokens.scss` 팔레트, 사이트 전역 사안), 반응형 1점(위 터치 영역), 테마 1점(위 하드코딩 3건). 셋 다 이유가 분명하고 여기에 적혀 있다.

---

## [2026-09-21 15:30 KST] M2-S2.6 준비 — repositories 를 메뉴에서 내리고 projects 로 흡수 결정

**Status**: ⚠️ partial
**Files**:

- modified: \_pages/repositories.md (`nav: true` -> `nav: false`)
- modified: .claude/PROGRESS.md (S2.6 에 흡수 계획과 gem 카드 함정 3건, 미결 5번 해소)
- created: \_sass/\_section-label.scss (빈 플레이스홀더)
- created: \_sass/\_projects-site.scss (빈 플레이스홀더)

**Summary**: repositories 페이지가 촌스럽다는 지적에서 출발했는데, 원인이 스타일이 아니라
구조였다. 페이지 전체가 `github-stats-extended.vercel.app` 이 그려 보내는 PNG 이고
(빌드 결과에서 확인, 외부 요청 20건) 카드 색·폰트가 그림 안에 구워져 있어 `_tokens.scss` 가
닿는 데가 이미지 바깥 여백뿐이었다. 다크 이미지 10장은 M1-S1.5 에서 다크모드를 지운 뒤에도
계속 받고 있었고, vercel 이 죽으면 `onerror` 가 카드를 숨겨 페이지가 조용히 빈다.

넷을 비교(현행 유지 / 자체 카드 / 삭제 / projects 흡수)한 결과 사용자가 **흡수**를 택했다.
결정의 근거는 디자인이 아니라 내용이었다: GitHub API 실측으로 공개 레포가 4개, 전부 star 0,
둘이 같은 수업 과제고 하나는 이 사이트 자체, 하나는 `test` 였다. 자체 카드를 예쁘게 만들어도
채울 게 3장이라 디자인이 내용보다 커진다.

**흡수라고 불렀지만 실제로 옮겨올 기능은 없다.** gem `_includes/projects.liquid` 가 이미
optional `github:` 를 지원한다. 그래서 이번에는 `nav: false` 만 내리고 나머지는 S2.6 으로 넘겼다.
페이지와 `_data/repositories.yml` 은 남겨 뒀다. 되돌리기가 한 줄이기 때문이다.

**중간에 드러난 사실 하나.** `assets/css/main.scss` 52/54 행의 `@use "section-label"` 과
`@use "projects-site"` 가 존재하지 않는 파티셜을 가리켜 **Sass 빌드가 이미 깨져 있었다**
(`Can't find stylesheet to import`). 마지막 성공 빌드가 14:39 인 것과 맞는다. 이 레포는
로더 충돌을 피하려고 `@use` 줄을 미리 걸어 두는 관행이 있고(커밋된 `_about.scss` 헤더가 그렇게
적고 있다), 그 짝이 되는 플레이스홀더 파일이 빠져 있었다. 규칙 없는 빈 파일 둘을 놓아
빌드를 되살렸다(5.7초). 두 파일의 실제 내용은 그 자리를 맡은 세션 몫이다.

**시도했다가 되돌린 것**: `.section-label` 을 `_about.scss` 에서 새 파티셜로 옮기고
`_includes/projects.liquid` 를 shadowing 해 source 알약까지 구현했으나, 여러 세션이 동시에
작업 중이라 사용자 요청으로 전부 철회했다. 되돌릴 때 `_sass/_about.scss` 는
`git checkout` 을 쓰지 않았다. 그 파일에는 다른 세션의 미커밋 about 작업 200줄이 들어 있어
같이 날아갈 뻔했다. 지웠던 블록만 손으로 복원했다.

---

## [2026-09-21 15:45 KST] M2-S2.1 후속 — 헤더 드롭다운, 다크모드, /secret/

**Status**: ✅ completed
**Files**:

- created: `_pages/secret.md`, `_sass/_secret.scss`
- modified: `_includes/header.liquid`, `_sass/_site-header.scss`, `_sass/_themes.scss`
- modified: `_config.yml`, `assets/css/main.scss`, `_pages/dropdown.md`, `_pages/profiles.md`, `robots.txt`

**Summary**: DESIGN.md §6의 우측 드롭다운을 되살리고, 그 안에 theme 세그먼트 컨트롤을 넣고, `/secret/`를 만들었다.

**드롭다운을 두 번 잃었다가 되찾은 것이다.** 처음엔 헤더를 백지에서 쓰며 만들었다가 진행바가 깨져 헤더째 되돌렸고, 그다음엔 `submenus`를 메뉴에서 내리며 그 캐럿까지 사라졌다. 이번엔 gem의 `.navbar-nav` **안에** 넣어서 `nav-toggle.js`가 그대로 구동한다 (`.dropdown` + `.dropdown-menu` + `data-nav-dropdown-toggle`, 바깥 클릭·ESC 포함). 검색은 메뉴 줄에서 패널 안 `command palette` 행으로 옮겼는데, `#search-toggle .nav-link`는 al_search가 macOS에서 `⌘ k`로 덮어쓰는 자리라 그대로 유지했다.

**설정 항목을 무엇으로 채울지가 이 세션에서 가장 오래 걸린 논의였다.** previous의 3줄(language / font size / theme) 중 **둘은 previous에서도 동작하지 않았다** — `preferences.js`가 `<html lang>` 속성만 바꾸고 `_data/i18n/`은 `.gitkeep`뿐이다. 후보를 아홉 개까지 냈지만(width, font, motion, code theme, depth, 북마크, 집중 모드 …) 사용자가 전부 "짜친다"고 했고, 그게 맞았다. **껍데기를 먼저 정하고 내용물을 찾는 순서가 거꾸로였다.** 결론은 theme 하나. 나머지는 블로그를 만들다 필요가 생기면 붙인다.

`font size`는 값어치가 아니라 **구조 때문에** 기각했다. 우리 타이포가 전부 px 고정이라 S/M/L을 만들려면 rem 전면 전환이 따라온다. `language`는 gem 레이아웃/인클루드 60개에 영어 문자열 30개가 박혀 있어 전부 복사해야 하고, 그 복사가 이 세션에서 반복해 밟은 함정(마크업 훅 유실)을 수십 배로 키운다. PLAN S4.5에 대안(글별 `lang: ko` + 영어 요약 + 번역 링크)을 적어뒀다.

**theme 세그먼트에 함정이 둘 있었다.** ① `theme.js`의 `initTheme`가 `getElementById("light-toggle")`을 **널 체크 없이** 잡는다. 없으면 DOMContentLoaded에서 throw하고 테마가 아예 초기화되지 않는다. 그런데 그 버튼의 동작은 3상태 **순환**이라 세그먼트와 맞지 않아, 보이지 않는 shim으로 남기고 세그먼트는 `setThemeSetting()`을 직접 부른다. ② 다크를 켰는데 **배경이 안 바뀌었다.** 우리 파셜이 `var(--color-base)`처럼 토큰을 직접 써서 gem의 `--global-*`만 덮는 방식이 닿지 않았다. **다크에서 토큰 자체를 재정의**하는 방식으로 바꿔 한 번에 해결했다. 덕분에 컴포넌트마다 다크 규칙을 쓸 일이 없다 — `data-theme` 선택자는 `_themes.scss`에만 있다.

**`/secret/`는 처음에 자체 팔레트를 하드코딩했다가, 사용자 지적으로 다크 테마 그 자체를 쓰도록 바꿨다.** 값을 `@mixin dark-tokens`로 빼고 `html[data-theme="dark"]`와 `html:has(.secret)` 둘이 include한다. `_secret.scss`의 하드코딩 색은 0개가 됐다.

여기서 CSS 커스텀 프로퍼티의 함정을 하나 배웠다. `body:has(.secret)`로 걸었더니 본문은 어두운데 **헤더가 크림으로 남았다.** `:root`가 `--global-bg-color: var(--color-base)`를 선언하는 순간 크림으로 치환이 끝나기 때문이다. **치환은 선언된 요소에서 일어나므로**, 자손에서 `--color-base`를 바꿔도 이미 굳은 `--global-*`은 따라오지 않는다. `html:has(.secret)`은 `:root`와 같은 요소라 해결된다.

`/secret/`을 숨기는 데 세 가지가 필요했고 **셋은 서로를 함의하지 않는다**: `nav: false`(메뉴 + al_search 인덱스, 검색은 `nav: true`인 페이지만 담는다), `sitemap: false`(sitemap.xml), `robots.txt`. previous 계획에 있던 `robots: noindex` front matter는 **어느 gem도 읽지 않아 무효**다.

**gem의 높은 특이도에 세 번 막혔다.** `#search-toggle { padding: 0 }`(id 선택자)과 `.navbar .dropdown-menu a:not(.active)`(클래스 2개 + 요소)가 우리 단일 클래스 규칙을 조용히 이겼다. 패널 정렬과 `/secret` 링크 색이 그래서 틀어져 있었다. 해당 규칙만 특이도를 올리고 이유를 주석에 남겼다 — 안 그러면 "왜 이렇게 길게 썼지" 하고 되돌린다.

**병렬 세션에 준 지시가 틀렸다.** "`assets/css/main.scss`는 건드리지 마라"고 했는데, about 세션이 새로 만든 `_section-label.scss`와 `_projects-site.scss`가 **등록되지 못해 CSS가 통째로 로드되지 않았다.** 빌드 에러도 없다. 사용자가 다크모드에서 `bio` 라벨의 이탤릭과 구분선이 사라진 걸 보고 발견했는데, 실은 처음부터 안 먹고 있었다. **한 줄 충돌이 스타일 유실보다 낫다** — 앞으로는 새 파셜을 만들면 `@use`를 직접 추가하도록 한다.

메뉴에서 `people`·`submenus`(안에 bookshelf)를 내렸다. 페이지는 `nav: false`로 남겼다. 메뉴 크기는 13px → 14px로 올렸다가 13px로 되돌렸다.

**검증**: 통합 테스트 7종 PASS, `upgrade audit` blocking 0, prettier PASS, override 5/5 acknowledged. 7개 페이지 전부 HTTP 200 / JS 에러 0, 다크모드도 전 페이지 확인.

**남은 것**: 다크 팔레트 값 셋(`--color-meta` `#a89178`, `--color-accent` `#e3b3b3`, `--color-surface` `#272724`)은 DESIGN.md에 다크 설계가 없어 **내가 정한 임시값**이고 주석에 provisional로 표시했다. 코드블록·콜아웃·이미지는 데모 콘텐츠뿐이라 다크에서 확인하지 못했다. `/secret/`의 위젯 카드는 플레이스홀더다 — previous PLAN S20.2/S20.3이 `{% include widget %}`로 포스트에 삽입하는 구조를 설계해뒀다.

---

## [2026-09-21 21:40 KST] M2-S2.5: publications 레이아웃

**Status**: ⚠️ partial
**Files**:

- created: `_sass/_publications-site.scss`, `assets/js/publications.js`, `_includes/scripts.liquid` (gem shadow)
- modified: `_pages/publications.md`, `_bibliography/papers.bib`, `_data/venues.yml`, `assets/css/main.scss`, `.al-folio-overrides.yml`

**Summary**: DESIGN.md §8.6 을 구현했다. 연도 점프 사이드바 + 논문 카드. `selected_papers.liquid` 가 about 에서 같은 마크업을 쓰므로 타이포와 배지, 알약은 두 페이지가 공유한다. `.pub-layout` 아래에 남긴 것은 2열 그리드와 흰 카드뿐이고, about 은 크림 배경 위에 그대로 올라간다(사용자 결정).

**카드 높이는 JS 로 맞춘다.** jekyll-scholar 가 연도마다 `<ol>` 을 따로 뱉어서 grid 로는 연도를 가로질러 높이를 못 맞춘다. 최대 높이를 재서 전부에 `min-height` 를 준다. 이미지 도착과 리사이즈 때 다시 잰다.

**스크립트를 `assets/js/publications.js` 로 뺐다.** 제목→PDF 링크가 인라인이면 `/publications/` 에서만 돌아서 about 에서는 링크가 안 걸렸다. gem 에 커스텀 JS 훅이 없어서 `_includes/scripts.liquid` 를 그림자로 두고 한 줄만 덧붙였다. `_layouts/about.liquid` 는 다른 세션 소유라 피했다.

**연도 점퍼는 URL 해시를 못 쓴다.** gem 의 `bibsearch.js` 가 이 페이지에서 해시를 검색어로 읽는다. `#year-2023` 을 걸면 검색창에 `year-2023` 이 들어가고 일치하는 항목이 없어서 목록이 통째로 사라진다. 에러도 경고도 없다. 링크는 `href` 를 유지하되 `preventDefault` 하고 `scrollTo` 로 직접 움직인다.

**CSS 에서 몇 번 막혔다.** `!important` 는 `@layer` 안쪽이 이기므로 `.w-100` 을 `width` 로는 못 눌렀다(`display: block` 으로 우회). grid item 은 `min-width: auto` 가 기본이라 텍스트 열이 트랙을 넘쳤다. `align-items: start` 를 주면 sticky 사이드바가 따라 움직인다.

**버튼과 abstract 패널.** gem 이 `Bib` 를 링크 버튼들 사이에 끼워 넣어서 `order` 로 맨 뒤로 뺐다. 색은 `Bib` 만 meta, 나머지는 accent 다. 열린 abstract 는 글씨 14px 가 바로 위 저자 줄보다 커서 12px 로 줄이고, 점선은 본문 검정에서 meta 로 낮췄다. 여백은 `.open` 에만 걸어서 닫힌 카드 높이는 안 변한다.

**커밋 전 impeccable 리뷰에서 세 건.** ① 520px 아래에서 배지 열 120px 이 폰 카드의 3분의 1 을 먹어 제목이 5줄로 쪼개졌다. 한 열로 쌓아서 카드 329px → 245px. 미디어 블록은 파일 맨 끝에 둔다. 중간에 넣었더니 뒤에 오는 같은 특정도의 기본 규칙에 져서 아무 일도 안 일어났다. ② 연도 점프가 `prefers-reduced-motion` 을 무시했다. `behavior` 를 분기한다. ③ 흰 카드 위 accent 글씨(알약, 배지, 활성 연도, 저자명)가 2.53:1 로 AA 미달이다. **사용자가 취향으로 유지하기로 했다.** 고치려면 `--color-accent` 자체를 낮춰야 해서 사이트 전역에 걸린다.

**검증** (더미 삭제 후): publications 카드 2장 전부 137px, about 1장 101px, 제목 링크 3/3, JS 에러 0. 390 / 520 / 521 / 768 / 1280px 가로 스크롤 0, 520px 경계에서 열 전환 확인. reduced motion 켜면 즉시 이동, 끄면 애니메이션. prettier PASS, `overrides accept` 완료.

**남은 것 (이래서 partial)**:

- **제목 크기와 `.post-description`** 은 전역 page chrome 이라 M2 이후로 미뤘다(사용자 결정)
- **카드 폭 1010px.** previous 는 760px 였다. 같은 전역 결정에 묶인다
- **`max_author_limit: 3`** 이라 5인 논문이 "2 more authors" 로 접힌다. 미판단

---

## [2026-09-21 22:32 KST] 작업 중 배너 + 이메일 보호 방식 교체

**Status**: ✅ completed
**Files**:

- created: `_sass/_wip-notice.scss`
- modified: `_includes/header.liquid`, `_config.yml`, `assets/css/main.scss`, `.al-folio-overrides.yml`

**Summary**: 데모 포스트와 샘플 CV가 아직 섞여 있으니 방문자에게 알리자는 요청. `_config.yml` 의 `wip_notice` 한 줄이 문구이고, 비우면 배너가 사라진다. 닫기 버튼은 두지 않기로 했다(사용자 선택).

**헤더 위가 아니라 `</header>` 다음 문서 흐름에 넣었다.** navbar 가 `fixed-top` 이고 `progress-bar.js` 가 `#navbar` 를 재서 스크롤 진행바를 배치하기 때문에, 위에 띠를 하나 끼우면 navbar 오프셋, body 패딩, 그 측정값 셋을 손으로 맞춰야 하고 어긋나면 **조용히** 깨진다. S2.1 에서 이미 한 번 당한 자리다. 흐름에 두면 스크롤과 함께 올라가는 대신 그 위험이 없다. 측정으로 확인: navbar top 0 / 높이 56, 배너 top 56 / 높이 36, `#progress` top 56 으로 **변화 없음**.

마크업은 `_includes/header.liquid`(이미 우리 override)에 넣어 `_layouts/default.liquid` 를 새로 떠안지 않았다. 색은 경고색이 아니라 blush 콜아웃 배경이다. 전 페이지에 반복되는 한 줄이고 경보가 아니라 고백이라서(PRODUCT.md "quiet, never silent").

**이메일 보호를 다시 만들었다.** 앞 항목에서 `protect_email` 을 껐던 결정의 후속이다. 플러그인은 클릭 시 복사만 하는데 사용자는 메일 앱이 열리길 원했으므로, `.site-email` 링크가 주소를 `data-eu`/`data-ed` 로 쪼개 들고 푸터 스크립트가 클릭 시점에 합쳐 여는 방식으로 바꿨다. 자세한 내용과 `_data/contact.yml` 이동 근거는 앞 항목에 적었다.

**레포가 PUBLIC 이라 소스에서도 뺐다.** 사용자가 `contact.yml` 에 평문으로 두는 게 괜찮냐고 물었고, 처음에는 "이미 git 히스토리 3개 커밋과 모든 커밋의 author 이메일에 있으니 데이터 파일을 옮겨도 소용없다" 고 설명만 하고 넘어갔다. 사용자가 다시 요구해서 반영했다: `_data/contact.yml` 을 `.gitignore` 에 넣고, `deploy.yml` 이 빌드 직전에 `SITE_EMAIL` secret 으로 그 파일을 쓴다. 로컬 체크아웃은 자기 사본을 두면 되고 `_data/contact.example.yml` 이 그 방법을 적어둔다. secret 이 없으면 경고만 남기고 이메일 아이콘이 빠진 채로 빌드된다(확인함).

설명이 틀린 건 아니었지만 **결론이 틀렸다.** 히스토리에 남아 있다는 사실이 앞으로 소스에 계속 두어도 된다는 근거가 되지는 않는다. 커밋 author 이메일 쪽은 여전히 남아 있고, GitHub noreply 로 바꾸는 것이 다음 조치다(PROGRESS 에 미완료로 적음).

---

## [2026-09-21 22:37 KST] M2-S2.5: 연도 사이드바를 젬 tocbot 으로 교체

**Status**: ⚠️ partial
**Files**:

- modified: `_pages/publications.md`, `_pages/cv.md`, `_pages/teaching.md`, `_sass/_base.scss`, `_sass/_publications-site.scss`, `assets/js/publications.js`

**Summary**: "cv 는 어떻게 목차가 제목 옆에 있느냐" 는 질문에서 시작했다. 답은 front matter `toc: sidebar` 한 줄이고, 젬 `_layouts/default.liquid` 가 그 키를 보면 컨테이너를 `col-sm-3` + `col-sm-9` 로 쪼갠다. **제목이 `{{ content }}` 안에 들어 있어서** 목차와 제목의 윗변이 같은 줄에서 시작한다. 직접 만든 `.pub-years` 는 본문 안 그리드라 구조상 제목 아래일 수밖에 없었다. 그래서 자체 구현을 버리고 젬 쪽으로 갔다. 마크업, SCSS 60줄, JS `yearJumper()` 를 지웠다.

**켜기만 해서는 사이드바가 빈 채로 뜬다.** 젬 `assets/js/common.js` 가 tocbot 을 돌리기 직전에 `.publications h2` 전부에 `data-toc-skip` 을 박는다. 일반적인 논문 목록에서는 연도 제목이 목차에 끼는 게 방해라서일 텐데, 이 페이지에서는 그게 정확히 목차의 내용이다. `common.js` 를 그림자로 뜨는 대신 우리 `publications.js` 가 (defer 순서상 뒤에 실행된다) 속성을 떼고 같은 옵션으로 tocbot 을 다시 init 한다. 젬 파일을 안 떠안는 쪽이 업그레이드에 유리하다.

**해시 함정은 S2.5 에서 한 번 당한 그대로 재현됐다.** tocbot 링크를 누르면 `#year-2026` 이 붙고 `bibsearch.js` 의 `hashchange` 핸들러가 그걸 검색어로 읽어 목록이 0건이 된다(검색창에 `year-2026` 이 들어가는 것까지 측정). 사이드바에 **캡처 단계** 클릭 리스너를 달아 tocbot 핸들러보다 먼저 `preventDefault` + `stopPropagation` 하고 직접 스크롤한다.

**왼쪽/오른쪽은 사용자가 오른쪽을 골랐다.** 나는 왼쪽을 권했다(연도가 쌓이면 레일이 구조로 읽힌다). 사용자 근거가 더 나았다: 오른쪽이면 publications 제목이 다른 페이지 제목들과 같은 세로선에 선다. cv 도 함께 오른쪽으로 옮겼다. 전환 비용은 front matter 한 단어다.

**폭을 고정한 것이 반응형을 조용히 깼다.** `col-sm-3` 은 25%(1280px 에서 300px)라 연도 목록에 과했다. `:has(#toc-sidebar)` 로 그 칼럼만 집어 `flex: 0 0 240px` 를 줬는데, 이게 좁은 화면에서 `col-sm-*` 이 100% 로 풀려 위로 쌓이는 동작을 막았다. 젬은 576px 아래에서 nav 를 `visibility: hidden; height: 0` 으로만 숨기므로 **빈 칼럼이 240px 를 계속 먹었다.** 700px 창에서 본문이 460px 로 찌그러진 게 그것이다. 처음에는 칼럼을 `display: none` 으로 덮었는데 그건 증상만 가리는 것이었고(목차가 통째로 사라진다), 768px 아래에서 젬이 의도한 대로 목차를 제목 위 가로 배치로 되돌렸다. `order: -1` 이 필요한 이유는 `sidebar: right` 라 목차 칼럼이 DOM 상 본문 뒤이기 때문이다.

목차 타이포는 `previous` 의 `_sass/pages/_publications.scss` 와 DESIGN.md §8.6 을 그대로 옮겼다. 한 군데 다르다: tocbot 은 활성 막대를 절대배치 `::before` 로 그리고 젬이 거기에 `!important` 로 색을 넣는다. `previous` 는 링크의 `border-left` 였고 그래야 막대가 글자 한 줄 높이로 떨어져서, `::before` 를 `display: none` 으로 끄고 보더로 다시 그렸다. `display` 에는 `!important` 가 없어서 통한다.

검색칸은 젬 기본이 350px 에 거의 검정 1px 테두리와 드롭 섀도라 정작 그게 거르는 카드보다 세게 보였다. 240px, `0.5px solid var(--color-border)`, 섀도 제거, placeholder 는 `years` 라벨과 같은 Georgia 이탤릭으로 맞췄다. 위아래 여백 32/36 을 20/20 으로 줄였는데 **첫 연도 제목의 `margin-top: 2rem` 이 부모와 병합되어 되살아나서** `:first-child` 일 때만 0 으로 눌러야 했다.

**검증**: 1440 / 1280 / 1024 / 900 / 800 / 700 / 600 / 480 / 375px 에서 가로 스크롤 없음, 콘솔 에러 0건, 목차 링크 클릭 후 `location.hash` 빈 문자열이고 항목 2건 유지, about 의 selected papers 영향 없음(제목 링크 포함), prettier PASS.

**남긴 것**: 전역 페이지 크롬(제목 크기, `.post-description` 노출 여부), 카드 폭 1010px 대 `previous` 의 760px, `max_author_limit: 3`. 이번 작업에서 `.post-description` 아래 여백을 음수 마진으로 상쇄했는데, 크롬을 정리할 때 그 줄은 지워져야 한다.

**BUILD_LOG 복구**: 이 항목을 쓰기 직전에 작업 트리의 로그가 **331줄 손실** 상태였다. 다른 세션이 S2.4 항목을 고쳐 쓰면서 그 아래 12개 항목(404 연작, secret, repositories, S2.5)을 통째로 날린 것이다. HEAD 사본에 그 세션의 S2.4 수정과 새 항목만 얹어 되살렸다. **append only 규칙이 이래서 있다**: 파일을 통으로 다시 쓰면 동시에 도는 세션의 기록이 조용히 사라진다.

---

## [2026-09-23 18:23 KST] M2-S2.6: Notion HTML export 변환 스크립트

**Status**: ⚠️ partial
**Files**:

- created: `bin/notion-to-project.py`
- created: `_projects/protein-inverse-folding.md`, `assets/img/projects/protein-inverse-folding/` (로컬 전용, 아래 참고)
- modified: `_projects/oxford-iiit-segmentation.md`, `.gitignore`

**Summary**: Oxford 상세 페이지가 Notion 에서 가로로 놓인 이미지를 전부 세로로 쌓고 있었다. 원인은 레이아웃이 아니라 원본이다. Notion Markdown export 는 컬럼과 이미지 폭을 버리고, HTML export 는 `column-list` / `column` (`width:%`, `data-notion-column-ratio`) 과 `<img style="width:px">` 로 둘 다 남긴다. 그래서 입력을 HTML zip 으로 정했다. 그리드는 젬 `app.css` 의 `.row` / `.col-sm` 을 쓰는데 `col-sm-5` / `col-sm-7` 이 없어서, Notion 비율(1/16 단위)을 `col-sm` + `flex-grow` 정수비로 옮긴다(68.75:31.25 -> 11:5).

**정규식으로 컬럼을 훑은 첫 시도가 틀렸다.** 컬럼의 닫는 태그를 안 봐서 컬럼 바로 뒤 블록(Oxford 의 IoU 표, Figure 13)까지 컬럼 안에 넣었다. 사용자가 PDF 와 다르다고 짚어서 알았다. 스크립트는 `html.parser` 로 작은 DOM 을 세워 중첩을 추적한다.

**테스트에서 잡은 것**: Year 속성이 없으면 `date:` 가 빈 값으로 나가 **사이트 전체 빌드가 실패**한다(주석으로 대체). kramdown 은 하위 목록을 부모 글자 열(`1. ` 이면 3칸)에 맞춰야 중첩으로 읽는다. 컬럼은 HTML 블록이라 안의 Markdown 이 파싱되지 않으므로 컬럼 내용은 HTML 로 쓴다. 컬럼 안 문단을 `.caption` 으로 내보냈더니 작은 회색 가운데 정렬이 돼서 일반 `<p>` 로 바꿨다(사용자 지적). 실제 export 에서 새로 나온 블록은 `details.toggle`(새 토글 형식)과 클래스 없는 `figure > div.source`(임베드) 두 가지였다.

**방향 전환: 본문은 스크립트 출력 그대로.** 처음에는 생성 뒤 내가 본문을 영어로 옮기고 다듬었는데, 사용자는 내용 수정을 Notion 에서 하려고 스크립트를 원한 것이었다. 손으로 고친 본문은 다음 export 때 덮어써지니 그 흐름을 깬다. 그래서 `--force` 재실행은 기존 front matter 만 보존하고 본문과 이미지(`NN.*`)를 갈아끼운다. 같은 export 로 두 번 돌려 결과가 동일한 것을 확인했다. Oxford 도 이 방식으로 재생성했고 영어판(도입부 2줄, alt 14개 포함)은 `.claude/backup/oxford-iiit-segmentation.en.md` 에 있다. 2026-09-21 의 "카피 영어 통일" 결정은 유지하되, 번역은 이제 Notion 쪽 작업이다.

**Google Slides 임베드는 비공개 슬라이드면 로그인 화면이 뜬다.** Notion 에서 보였던 건 작성자 계정으로 로그인해 있어서다. 스크립트는 Slides / Docs / Sheets / YouTube 를 iframe 으로 바꾸고(CSP `frame-src https:` 허용) 공개 여부는 원본 공유 설정에 맡긴다.

**검증**: Oxford 자동 변환 결과가 수작업 레이아웃과 1280px 스크린샷에서 일치, 이미지 14장 md5 일치. Notion 마크업을 흉내 낸 픽스처 12종(토글, 코드, 표, 수식, 체크리스트, 중첩 목록, 컬럼 안 목록 등) Jekyll 빌드 후 렌더 확인. 네 페이지(Oxford, Video, Korean, Protein) 본문이 스크립트 출력과 동일. prettier PASS.

**남긴 것**: Video / Korean 은 테스트로 생성했다가 사용자 요청으로 본문과 이미지를 지우고 `has_detail: false` 로 되돌렸다. 프로젝트 `.md` 와 이미지는 git 변경이 많아 `.gitignore` 에 임시로 막아 두었다. **상세 페이지를 커밋하기 전에 그 블록을 지워야 한다**(PROGRESS S2.6). 상세 레이아웃(DESIGN.md §8.5) 은 다음 작업이다.

---

## [2026-09-23 18:25 KST] 첫 배포 push: 이메일 / 배너 / robots 만 골라서

**Status**: ✅ completed
**Files**:

- modified: `.gitignore`, `.github/workflows/deploy.yml`, `_config.yml`, `_data/socials.yml`, `_includes/footer.liquid`, `_includes/header.liquid`, `_sass/_socials.scss`, `assets/css/main.scss`, `robots.txt`, `.claude/BUILD_LOG.md`
- created: `_data/contact.example.yml`, `_sass/_wip-notice.scss`

**Summary**: 작업 트리에 세 세션 분량의 미커밋 변경이 쌓여 있었고, 사용자가 **about 과 projects 디자인은 아직 기록에 남기고 싶지 않다** 고 해서 이메일 보호, 작업 중 배너, robots.txt 만 떼어 커밋하고 push 했다. `origin/main` `d8e6274..51d8a81`, 커밋 8개.

**한 파일은 줄 단위로 쪼개야 했다.** `assets/css/main.scss` 에 `@use` 세 줄(`wip-notice`, `section-label`, `projects-site`)이 함께 들어와 있었는데, 뒤의 둘은 아직 미추적인 파셜을 가리킨다. 같이 올리면 **Sass 가 통째로 실패**한다. `git hash-object -w` 로 배너 줄만 넣은 사본을 만들어 `git update-index --cacheinfo` 로 인덱스에만 올렸다. 작업 트리는 건드리지 않았다.

**"커밋 안 된 것 때문에 사이트가 깨지느냐" 는 질문에는 빌드로 답했다.** push 는 커밋만 보내므로 판단 기준은 HEAD 혼자 온전한지다. `git worktree` 로 HEAD 사본을 떠서 빌드했다(9.5초, 에러 없음). 산출물에서 평문 주소 0건, `.site-email` 분할 링크 존재, 배너와 `.site-wip` CSS 존재, publications 목차와 teaching 메뉴 제외 확인. `_data/contact.yml` 을 지우고 한 번 더 빌드해 **secret 이 없을 때도 경고만 내고 빌드가 성공**하는 것까지 봤다.

**이메일 보호의 실제 효력을 다시 쟀다.** 막는 것은 HTML 을 정규식으로 긁는 수집기 하나다. 못 막는 것이 셋인데, 그중 둘이 이미 공개돼 있었다. ① 커밋 author 이메일이 14개 중 13개에 주소로 들어가 있다. ② 주소를 담은 과거 커밋 5개 중 **2개는 이미 `origin/main` 에 올라가 있었다**(`7484557`, `577f39f`). 그래서 히스토리 재작성은 "이미 유출된 것을 회수" 하지 못하면서 해시만 전부 바꾼다고 설명했고, 사용자가 지금 상태로 가기로 했다. ③ `.claude/BUILD_LOG.md` 는 커밋되는 파일인데 `grep` 명령 인용문에 주소가 세 번 있었다. 이건 `<내 주소>` 로 지우고 커밋했다(이미 작업 트리에서 누군가 고쳐둔 상태였고 나는 커밋만 했다).

교훈 하나: **로그가 커밋된다는 사실은 로그를 쓸 때마다 다시 적용된다.** 검증 명령을 그대로 붙여넣으면 그 안의 값도 같이 공개된다.

**남은 미커밋**: about 재디자인(`_pages/about.md`, `_sass/_about.scss`, `_layouts/about.liquid`, section-label 2종), projects 재디자인(`_pages/projects.md`, `_projects/` 11건, `_sass/_projects-site.scss`), 그 둘에 딸린 `main.scss` 의 `@use` 두 줄과 `.al-folio-overrides.yml` 의 about 해시, 그리고 `CLAUDE.md` 커밋 메시지 가이드와 `AGENTS.md` 의 침묵 실패 항목 추가. 앞의 둘은 사용자가 디자인이 마음에 들지 않아 보류한 것이다.

---

## [2026-09-24 00:55 KST] M2-S2.6: 프로젝트 상세 레이아웃

**Status**: ⚠️ partial <!-- 레이아웃 완료. 실제 프로젝트 콘텐츠 교체와 커밋이 남음 -->
**Files**:

- created: \_layouts/project.liquid, \_plugins/project_detail_gate.rb, \_includes/projects.liquid, \_includes/project-thumb.liquid, \_includes/project-links.liquid, \_includes/project-link.liquid
- modified: \_sass/\_projects-site.scss, \_projects/[1-9]\_project.md, \_pages/projects.md (display_categories), \_config.yml (external_sources), bin/notion-to-project.py, .claude/CONTENT_GUIDE.md, .al-folio-overrides.yml, assets/css/main.scss
  **Summary**: previous 의 DESIGN.md §8.5 를 출발점으로 상세 페이지를 새 레이아웃으로 분리했다. gem `page.liquid` 는 다른 페이지와 공유라 흰 paper 를 걸 곳이 없어서다. 헤더는 세 덩어리(라벨 + 제목 + 부제 + 태그 / 정보 카드 / 소개 + 버튼)로 묶고 덩어리 사이만 띄웠다. 정보 카드 위 26px 은 아래 20px 에 소개 문단의 줄간격이 더해져 보이는 간격과 맞춘 값이다. 본문 폭은 제한 없음(1070px 글자 폭), 860px, 960px 를 비교해 사용자가 960px 로 정했다. Notion 이미지 폭이 708px 기준이라 제한이 없으면 전체 폭 이미지가 두 배로 커진다.

  사용자가 되돌린 것: accent 를 진하게 섞은 그라디언트(텁텁함), 팔레트 밖 진한 핑크 라벨, 초록/민트 그라디언트, 이미지 위 핑크 오버레이, 흰 글자 대신 어두운 글자의 github 버튼(previous 와 같게 흰 글자로 복귀, 대비 2.5:1 은 알고 둔 것), 임베드 둥근 모서리. 결론은 previous 팔레트의 핑크(`#f4c2c2 -> #fbeaf0`)와 보라(`#eeedfe -> #fbeaf0`) 두 개. 토큰 대신 hex 를 쓴 이유는 다크 모드가 `--color-soft-bg` 를 10% 틴트로 재정의해서 그라디언트 끝이 검게 변했기 때문이다.

  카드 전체를 `<a>` 로 감싼 gem 구조에 아이콘 링크를 넣으면 중첩 앵커가 된다. 파서가 바깥 링크를 끊어서 카드 뒤쪽이 클릭되지 않는다. 제목 링크의 `::after` 를 카드 전체로 늘리고 아이콘 행을 z-index 로 올렸다. 게이트 플러그인은 숨긴 문서의 `permalink` 를 `/projects/` 로 바꾼다. al_search 팔레트가 gem 템플릿에서 모든 컬렉션 문서를 `item.url` 로 링크하므로 그대로 두면 404 다.

  실제 프로젝트 `.md` 가 더미 데이터라 배포하면 거짓 정보가 된다. 그래서 al-folio 샘플 9건을 삭제하지 않고 템플릿 쇼케이스로 다시 썼다(모든 필드, 링크 종류, 표). 실제 것은 `.gitignore` 임시 블록 아래 두고 샘플만 배포한다. 로컬 빌드가 medium.com RSS 타임아웃으로 두 번 실패해서 al-folio 예제 `external_sources` 를 비웠다.

  impeccable critique 27/40. 자동 검사기는 Roboto 로드(gem head 가 Google Fonts 로 불러오지만 사이트는 시스템 sans 와 Georgia 를 쓴다)와 oxford 의 12px 반복 간격(Notion 컬럼 유틸리티라 대부분 오탐)을 잡았다. 브라우저 오버레이 주입은 CSP `script-src 'self' 'unsafe-inline' https:` 가 `http://localhost` 스크립트를 막아 실패했다. 반영 여부는 사용자 결정으로 PROGRESS 에 남겼다. 커밋은 아직: 작업 트리의 about / section-label / `_pages/projects.md` 정렬 변경은 다른 세션 것이라 스테이징에서 뺐다.

---

## [2026-09-24 01:40 KST] M2-S2.6: impeccable 후속

**Status**: ✅ completed
**Files**:

- created: assets/css/no-google-fonts.css
- modified: \_config.yml (third_party_libraries.google_fonts), \_sass/\_projects-site.scss
  **Summary**: critique 다섯 항목 중 둘만 반영했다. 본문 줄 길이는 70ch / 85ch / 90ch 비교 캡처를 보고 사용자가 90ch 로 정했다. 문단, 목록, 토글에만 걸고 이미지, 컬럼, 표는 종이 폭 그대로다. 한글이 섞이면 `ch` 가 영문 폭 기준이라 한 줄 한글 수는 더 적다. Google Fonts 는 gem `head.liquid` 가 조건 없이 `<link>` 를 넣어서 URL 을 비우면 `href=""` 로 현재 페이지를 CSS 로 다시 받는다. CSP `style-src` 가 `data:` 를 막아서 빈 로컬 CSS 를 가리키게 했다. head 를 shadow 하는 것보다 gem 업데이트에 안전하다. 끄기 전에 빌드 결과를 뒤졌다: Roboto 는 Tailwind body 기본값뿐(`_base.scss` 가 덮음), al_search 팔레트는 Material Icons 대신 SVG 아이콘, distill 은 시스템 폰트 스택 안의 이름일 뿐. 이득은 렌더를 막는 외부 CSS 요청 하나라 작다. 그라디언트, accent 대비, Slides 임베드는 사용자가 유지로 결정. 카드 아이콘 크기 지적은 상세 페이지 범위 밖이라 뺐다.
