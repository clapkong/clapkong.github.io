# Content Guide

이 사이트의 내용을 어디서 어떻게 고치는지. 코드(레이아웃, 스타일)가 아니라 **데이터**만 다룬다.

> **아직 디자인 작업 중이다.** 대부분의 페이지 포매팅이 끝나지 않았다(진행 상황은 `.claude/PROGRESS.md`). 아래의 "어느 파일을 고치나" 는 바뀌지 않지만, 화면에 어떻게 보이는지와 일부 front matter 필드는 페이지 작업이 끝나면서 달라질 수 있다.

## 한눈에

| 바꾸고 싶은 것                  | 고칠 곳                                                        |
| ------------------------------- | -------------------------------------------------------------- |
| **블로그 글**                   | `_posts/YYYY-MM-DD-제목.md`                                    |
| **논문**                        | `_bibliography/papers.bib` (BibTeX)                            |
| **프로젝트 카드**               | `_projects/<slug>.md` 의 front matter                          |
| **프로젝트 상세 페이지**        | **Notion** 에서 쓰고 `bin/notion-to-project.py` 로 변환        |
| **about** (이름, 소개, bio)     | `_pages/about.md`                                              |
| 소셜 링크 (GitHub, LinkedIn 등) | `_data/socials.yml`                                            |
| 이메일 주소                     | `_data/contact.yml` (로컬) + GitHub secret `SITE_EMAIL` (배포) |
| 사이트 제목, 설명, 작업 중 배너 | `_config.yml`                                                  |
| 학회 배지 색                    | `_data/venues.yml`                                             |

고친 뒤에는 [미리 보기와 배포](#미리-보기와-배포) 로.

## blog

`_posts/YYYY-MM-DD-제목.md` 파일 하나가 글 하나다. 파일 이름의 날짜가 글 날짜이고, 제목 부분이 주소가 된다.

```yaml
---
layout: post
title: 글 제목
date: 2026-09-23 12:00:00
description: 목록에 보이는 한 줄
tags: tag1 tag2
categories: category
---
본문은 Markdown.
```

- 이미지는 `assets/img/posts/<글 이름>/` 에 모아 두고 `{% include figure.liquid path="assets/img/posts/<글 이름>/01.png" class="img-fluid" zoomable=true alt="설명" %}` 로 넣는 것을 권한다(프로젝트와 같은 방식)
- 이미지를 가로로 나란히 두려면 `<div class="row">` + `<div class="col-sm">` 로 감싼다. 예시는 `_posts/2015-05-15-images.md`
- 지금 `_posts/` 의 글은 al-folio 예제다. 수식, 이미지 갤러리, 코드, 표, 탭 등 **문법이 필요할 때 참고용**으로 둔다. 블로그 목록 페이지(`/blog/`)도 아직 al-folio 기본 디자인이다

## publications

`_bibliography/papers.bib` 에 BibTeX 항목을 추가하면 끝이다. 연도별로 알아서 정렬된다.

```bibtex
@inproceedings{tamatgar2026structure,
  abbr        = {KDD},                 % 배지. _data/venues.yml 의 키와 같으면 색이 붙는다
  title       = {From Structure to Function: ...},
  author      = {Tamatgar*, Nilufer and Park*, Soobin and ...},
  booktitle   = {Proceedings of ...},
  year        = {2026},
  doi         = {10.1145/...},
  pdf         = {https://...},          % 버튼이 생긴다
  code        = {https://github.com/...},
  html        = {https://...},
  abstract    = {...},                   % "ABS" 버튼으로 펼쳐진다
  annotation  = {<sup>*</sup> Equal contribution.},
  selected    = {true},                  % about 첫 화면에 노출
  bibtex_show = {true}                   % "BIB" 버튼
}
```

- 내 이름 밑줄은 `_config.yml` 의 `scholar: last_name / first_name` 과 일치하는 저자에만 붙는다. 표기가 다르면(예: `S. Park`) 그 표기도 거기에 추가
- 새 학회면 `_data/venues.yml` 에 `abbr` 과 같은 키로 `url`, `color` 를 넣는다

## projects

프로젝트는 **카드**(목록)와 **상세 페이지** 두 부분이다. 파일은 `_projects/<slug>.md` 하나.

> **slug** = 페이지의 영문 이름. 소문자와 하이픈만. 파일 이름과 주소가 된다:
> `oxford-iiit-segmentation` → `_projects/oxford-iiit-segmentation.md`, `/projects/oxford-iiit-segmentation/`

### 카드: front matter

```yaml
---
layout: page
title: Oxford-IIIT Pet Segmentation
description: 카드에 보이는 한두 문장
img: assets/img/projects/oxford-iiit-segmentation/01.png # 카드 이미지. 비워도 된다
category: research # _pages/projects.md 의 display_categories 중 하나
date: 2025-04-01 # 정렬 기준. 빈 값으로 두면 빌드가 실패한다
github: https://github.com/... # 있으면 카드에 아이콘
---
```

`subtitle`, `period`, `role`, `status`, `tech_stack`, `thumbnail`, `has_detail` 도 적어 두지만, **지금은 화면에 나오지 않는다.** 프로젝트 상세 레이아웃 작업(PROGRESS S2.6)에서 쓰일 자리다.

### 상세 페이지: Notion 에서 쓰고 변환

상세 내용은 Notion 에서 쓰고 고친다. `.md` 본문을 직접 고치지 않는다: 다음 변환 때 덮어써진다.

**1. Notion 에서 export**

페이지 오른쪽 위 `⋯` → **Export**

- Export format: **HTML** (Markdown 은 가로 배치와 이미지 폭이 사라진다)
- Include content: **Everything**
- Include subpages: 끄기

zip 파일이 받아진다. 압축은 풀지 않아도 된다.

**2. 변환**

```bash
# 처음 만들 때
bin/notion-to-project.py ~/Downloads/<export>.zip <slug>

# Notion 에서 고친 뒤 다시 반영할 때: front matter 는 그대로 두고 본문과 이미지만 바꾼다
bin/notion-to-project.py ~/Downloads/<export>.zip <slug> --force

# 파일을 만들지 않고 결과만 보기
bin/notion-to-project.py ~/Downloads/<export>.zip <slug> --dry-run
```

처음 만들었을 때는 front matter 의 `description`, `category`, `date` 등을 손으로 채운다. 그 다음부터는 Notion 만 고치고 `--force` 로 다시 돌린다.

**3. Notion 쪽에서 신경 쓸 것**

- **이미지 캡션**을 달면 사이트의 캡션과 alt 텍스트가 된다. 없으면 alt 가 비어서 나간다
- 가로 배치(컬럼), 이미지 폭과 정렬, 토글, 코드, 표, 수식은 그대로 옮겨진다
- Google Slides / Docs / YouTube 임베드는 iframe 으로 들어간다. **보는 사람에게 권한이 없으면 로그인 화면이 뜬다**: 공유를 "링크가 있는 모든 사용자" 로
- 변환하지 못한 블록은 `.md` 에 `<!-- notion: unhandled ... -->` 주석으로 남고, 실행이 끝날 때 목록이 출력된다

이미지는 `assets/img/projects/<slug>/01.png, 02.png ...` 로 페이지 순서대로 복사된다.

## about

`_pages/about.md`

- 맨 위 `hero:` 블록: `name`, `role`, `intro`(한 줄 소개). 사진이 생기면 `image:` 에 경로를 넣는다. 비워 두면 이니셜 원이 나온다
- `---` 아래 본문: bio 문단
- `selected_papers: true`: `papers.bib` 에서 `selected = {true}` 인 논문이 여기 뜬다
- `latest_posts`: 최근 블로그 글 몇 개를 보일지

---

아래는 가끔 바꾸는 것들이다.

## 소셜 링크와 이메일

- `_data/socials.yml`: GitHub, LinkedIn, Scholar 등
- **이메일은 `socials.yml` 에 넣지 않는다.** 넣으면 모든 페이지에 주소가 평문으로 박힌다
- 이메일은 `_data/contact.yml` 에 둔다. 이 파일은 git 에 올라가지 않고(`contact.example.yml` 참고), 배포 때는 GitHub 저장소의 secret `SITE_EMAIL` 로 만들어진다

## 사이트 설정

`_config.yml`

- `title`, `first_name`, `last_name`, `description`(검색 결과와 공유 카드에 보이는 한 문장)
- `wip_notice`: 헤더 아래 "작업 중" 배너 문구. 줄을 지우면 배너가 사라진다
- 바꾼 뒤에는 개발 서버를 다시 시작해야 반영된다 (`_config.yml` 은 자동 새로고침 대상이 아니다)

## 아직 샘플인 것

- **CV**: `_pages/cv.md` 의 `cv_pdf` 와 `_data/cv.yml` 이 al-folio 샘플(Albert Einstein)이다
- **news**: `_news/` 가 예제 공지뿐이라 about 에서 꺼 두었다 (`announcements.enabled: false`)

## 미리 보기와 배포

```bash
bundle exec jekyll serve      # http://localhost:4000/ 에서 확인
npm run lint:prettier         # 형식 검사 (CI 가 같은 검사를 한다)
```

`main` 에 push 하면 GitHub Actions(`deploy.yml`)가 빌드해서 배포한다.

> **임시 설정 주의**: 작업 중인 프로젝트 파일을 가리려고 `.gitignore` 맨 아래에 `/_projects/*.md`, `/assets/img/projects/` 두 줄이 있다. 프로젝트 페이지를 올릴 때는 **이 두 줄을 먼저 지워야** 배포에 포함된다.
