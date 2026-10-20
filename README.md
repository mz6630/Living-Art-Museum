# Living Art Museum · 살아있는 미술관

Web Design II (김건우 교수) 기획 프로젝트 — 현대미술 작품 열두 점을 직접 만지고 바꿔 보는 인터랙티브 웹사이트.

**사이트:** https://mz6630.github.io/Living-Art-Museum/

## 무엇이 들어 있나

| 경로 | 내용 |
| --- | --- |
| `index.html` | 사이트 전체(3D · 카드 · 전시 보기). 열두 개의 체험이 이 파일 안에 들어 있어 사이트 안에서 바로 열립니다. |
| `experiences/` | 체험 하나하나를 따로 연 파일 (호박, 마릴린, 코미디언, 몬드리안, 두들, 뱅크시, 쿤스, 상어, 수프, 바스키아, 풍선을 든 소녀, 신의 사랑을 위하여) |
| `src/` | 사이트 원본 (`main.html` + `tail.html`) |
| `scripts/build-site.py` | `src/` + `experiences/` → `index.html` 빌드 |
| `scripts/make-config.mjs` | `.env`(또는 GitHub Secrets) → `firebase-config.js` 생성 |
| `firestore.rules` | 공유 저장소(Firestore) 보안 규칙 |
| `.github/workflows/pages.yml` | main에 push하면 GitHub Pages로 자동 배포 |

체험을 고친 뒤에는 `python3 scripts/build-site.py`로 `index.html`을 다시 만들어 함께 커밋하세요.

## 모두가 함께 저장하기 (호박 · 바스키아 · 상어)

호박 밭, 바스키아 노트, 상어 앞에 머문 시간은 방문자가 남긴 것을 **모든 사람이 각자 기기에서** 보도록 Firebase Firestore에 저장합니다.
Firebase 설정이 없으면 사이트는 그대로 작동하고, 각자의 브라우저에만 저장됩니다.

### 1. Firebase 프로젝트 만들기 (한 번만)

1. <https://console.firebase.google.com> → **프로젝트 추가** (Google 애널리틱스는 꺼도 됩니다)
2. **빌드 → Firestore Database → 데이터베이스 만들기** → 위치 `asia-northeast3 (서울)` → **프로덕션 모드**
3. Firestore의 **규칙** 탭에 이 저장소의 `firestore.rules` 내용을 붙여 넣고 **게시**
4. **프로젝트 설정(톱니바퀴) → 내 앱 → 웹(`</>`)** 으로 앱 등록 → `firebaseConfig` 값 6개 확인

### 2. 키 넣기 — 저장소에는 절대 올라가지 않습니다

**내 컴퓨터에서 (`.env`)**

```bash
cp .env.example .env          # 값 6개를 채워 넣기
node scripts/make-config.mjs  # firebase-config.js 생성
python3 -m http.server 8000   # http://localhost:8000 에서 확인
```

`.env`와 `firebase-config.js`는 `.gitignore`에 들어 있어 커밋되지 않습니다.

**배포 사이트에서 (GitHub Secrets)**

저장소 **Settings → Secrets and variables → Actions → New repository secret** 으로 아래 6개를 추가합니다.

| Secret 이름 | firebaseConfig 값 |
| --- | --- |
| `FIREBASE_API_KEY` | `apiKey` |
| `FIREBASE_AUTH_DOMAIN` | `authDomain` |
| `FIREBASE_PROJECT_ID` | `projectId` |
| `FIREBASE_STORAGE_BUCKET` | `storageBucket` |
| `FIREBASE_MESSAGING_SENDER_ID` | `messagingSenderId` |
| `FIREBASE_APP_ID` | `appId` |

배포할 때 GitHub Actions가 이 값으로 `firebase-config.js`를 만들어 사이트에만 넣습니다.

### 3. GitHub Pages 켜기 (한 번만)

**Settings → Pages → Build and deployment → Source: `GitHub Actions`** 로 바꾼 뒤,
**Actions → Deploy to GitHub Pages → Run workflow** 를 누르면 배포됩니다. 이후에는 main에 push할 때마다 자동으로 배포됩니다.

### 알아 둘 점

- Firebase 웹 설정값(`apiKey` 등)은 비밀번호가 아니라 "어느 프로젝트인지"를 알려 주는 값이라, 배포된 사이트를 열면 누구나 볼 수 있습니다. 데이터를 지키는 것은 `firestore.rules`입니다. 키를 저장소에서 빼 두면 코드를 퍼 가는 사람이 내 프로젝트를 그대로 쓰는 일은 막을 수 있습니다.
- 더 안전하게 하려면 Google Cloud 콘솔 → **API 및 서비스 → 사용자 인증 정보**에서 이 API 키의 **HTTP 리퍼러**를 `mz6630.github.io/*`, `localhost:*`로 제한하세요.
- 바스키아 노트는 누구나 붙이고, 떼고, 지울 수 있게 열어 두었습니다. 상어는 방문마다 "머문 초" 숫자 하나만 저장하며(카메라 영상은 저장·전송하지 않음), 늘어나기만 합니다. 호박은 추가만 되고 지워지지 않습니다.
- 정리가 필요하면 Firebase 콘솔의 Firestore 화면에서 문서를 직접 지울 수 있습니다.

## 저작권

모든 작품 이미지·스티커·라벨·잡지는 이 프로젝트를 위해 새로 그린 것이며, 원작 이미지나 상표를 복제하지 않았습니다 (퍼블릭 도메인인 몬드리안 제외).
