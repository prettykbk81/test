# Streamlit 설정 가이드

## 📁 파일 구조

```
.streamlit/
├── secrets.toml           # 민감한 정보 (Git에서 제외)
├── secrets.toml.example   # 설정 예제
├── config.toml            # Streamlit 설정
└── README.md              # 이 문서
```

---

## 🔐 secrets.toml - Supabase 연결 설정

### 파일 위치
```
.streamlit/secrets.toml
```

### 설정 형식

```toml
# Supabase Configuration
supabase_url = "https://xxxxxxxxxxxxx.supabase.co"
supabase_key = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3M..."
```

### 값 얻는 방법

1. **Supabase 대시보드** 접속: https://app.supabase.com
2. **프로젝트 선택**
3. **설정 (Settings)** → **API** 탭
4. 다음 정보 복사:
   - **Project URL** → `supabase_url`
   - **anon/public key** → `supabase_key`

### 파일 예제

```toml
supabase_url = "https://ishipuyszpeeayvnhehb.supabase.co"
supabase_key = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImlzaGlwdXlzenBlZWF5dm5oZWhiIiwicm9sZSI6ImFub24iLCJpYXQiOjE3ODA1NTQ4NzksImV4cCI6MjA5NjEzMDg3OX0.vWyyFrlRVzjKCPBzUVxG7qXz7r-M0B2wEVQ905FR9s8"
```

### Python 코드에서 사용

```python
import streamlit as st

# Streamlit secrets에서 값 읽기
supabase_url = st.secrets["supabase_url"]
supabase_key = st.secrets["supabase_key"]
```

---

## ⚙️ config.toml - Streamlit 전체 설정

### 주요 설정값

#### 테마 설정
```toml
[theme]
primaryColor = "#0052CC"        # 주요 색상 (홈앤쇼핑 브랜드 컬러)
backgroundColor = "#FFFFFF"     # 배경색
secondaryBackgroundColor = "#F0F2F6"  # 보조 배경색
textColor = "#262730"           # 텍스트 색상
font = "sans serif"             # 글꼴
```

#### 클라이언트 설정
```toml
[client]
showErrorDetails = true         # 오류 상세 메시지 표시
showSidebarNavigation = true    # 사이드바 네비게이션 표시
```

#### 서버 설정
```toml
[server]
port = 8501                     # 포트 번호
headless = true                 # GUI 없이 실행
runOnSave = true                # 파일 저장 시 자동 재실행
maxUploadSize = 200             # 최대 업로드 크기 (MB)
```

---

## 🖥️ 로컬 개발 환경 설정

### 1단계: secrets.toml 생성

`.streamlit/secrets.toml.example`을 참고하여 `.streamlit/secrets.toml` 파일 생성:

```bash
cp .streamlit/secrets.toml.example .streamlit/secrets.toml
```

### 2단계: 값 입력

```toml
supabase_url = "YOUR_SUPABASE_URL"
supabase_key = "YOUR_SUPABASE_ANON_KEY"
```

### 3단계: 앱 실행

```bash
streamlit run sales_dashboard.py
```

Streamlit이 자동으로 `.streamlit/secrets.toml`을 읽습니다.

---

## ☁️ 배포 환경 설정

### Streamlit Cloud (cloud.streamlit.app)

1. **앱 배포**: GitHub에서 배포
2. **App settings** 클릭 (우측 하단)
3. **Secrets** 탭
4. 다음 내용 입력:
```toml
supabase_url = "YOUR_SUPABASE_URL"
supabase_key = "YOUR_SUPABASE_ANON_KEY"
```
5. **Save** 클릭

### Docker

```dockerfile
FROM python:3.10

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
COPY .streamlit/config.toml .streamlit/config.toml

ENV SUPABASE_URL="YOUR_SUPABASE_URL"
ENV SUPABASE_KEY="YOUR_SUPABASE_ANON_KEY"

CMD ["streamlit", "run", "sales_dashboard.py"]
```

### Heroku

```bash
heroku config:set SUPABASE_URL="YOUR_SUPABASE_URL"
heroku config:set SUPABASE_KEY="YOUR_SUPABASE_ANON_KEY"

git push heroku main
```

---

## 🔒 보안 주의사항

### ✅ 해야 할 것
- ✓ `.streamlit/secrets.toml`을 `.gitignore`에 추가 (이미 됨)
- ✓ secrets.toml을 절대 Git에 커밋하지 않기
- ✓ 배포 환경에서는 플랫폼의 secrets 관리 기능 사용
- ✓ 정기적으로 API 키 로테이션

### ❌ 하면 안 되는 것
- ✗ 코드에 API 키 직접 작성
- ✗ secrets.toml을 Git에 커밋
- ✗ 공개 저장소에 API 키 노출

---

## 🔄 Streamlit 인식 순서

1. `.streamlit/secrets.toml` (로컬 개발)
2. 환경변수 (`SUPABASE_URL`, `SUPABASE_KEY`)
3. 배포 플랫폼의 secrets

---

## 📝 샘플 코드

```python
import streamlit as st
import os

try:
    supabase_url = st.secrets["supabase_url"]
    supabase_key = st.secrets["supabase_key"]
except (KeyError, FileNotFoundError):
    supabase_url = os.getenv("SUPABASE_URL")
    supabase_key = os.getenv("SUPABASE_KEY")
    
    if not supabase_url or not supabase_key:
        st.error("Supabase 설정이 필요합니다!")
        st.stop()
```

---

## 🚀 빠른 시작

```bash
# 1. secrets 파일 생성
cp .streamlit/secrets.toml.example .streamlit/secrets.toml

# 2. Supabase 값 입력
nano .streamlit/secrets.toml

# 3. 의존성 설치
pip install -r requirements.txt

# 4. 앱 실행
streamlit run sales_dashboard.py
```
