# Streamlit 설정 가이드

## secrets.toml

Streamlit에서 사용하는 보안 설정 파일입니다. 민감한 정보(API 키, 데이터베이스 비밀번호 등)를 저장합니다.

### 파일 위치
```
.streamlit/secrets.toml
```

### 설정 형식
```toml
# Supabase Configuration
supabase_url = "YOUR_SUPABASE_URL"
supabase_key = "YOUR_SUPABASE_API_KEY"
```

### 사용 방법

**Python 코드에서:**
```python
import streamlit as st

# Streamlit secrets에서 값 읽기
url = st.secrets["supabase_url"]
key = st.secrets["supabase_key"]
```

### 보안 주의사항

⚠️ **이 파일은 Git에 커밋하면 안 됩니다!**
- `.gitignore`에 `.streamlit/secrets.toml`이 포함되어 있습니다
- 배포 시에는 호스팅 플랫폼의 환경변수 설정에서 관리합니다

### 배포 시 설정

**Streamlit Cloud (cloud.streamlit.app):**
1. 앱 설정 → Secrets 메뉴
2. 다음 내용을 입력:
```toml
supabase_url = "YOUR_SUPABASE_URL"
supabase_key = "YOUR_SUPABASE_API_KEY"
```

**Heroku, Docker 등 다른 플랫폼:**
환경변수로 설정:
```bash
export SUPABASE_URL="YOUR_SUPABASE_URL"
export SUPABASE_KEY="YOUR_SUPABASE_API_KEY"
```

## 로컬 개발

로컬에서 개발할 때는 프로젝트 루트의 `.env` 파일을 사용합니다.

```bash
# .env 파일 생성
SUPABASE_URL=https://...
SUPABASE_KEY=eyJ...
```

앱을 실행할 때:
```bash
streamlit run sales_dashboard.py
```

## 참고

- Streamlit은 자동으로 `.streamlit/secrets.toml`을 읽습니다
- 값이 없으면 환경변수 (`.env`) 또는 os.getenv()에서 읽습니다
- 배포 환경에서는 호스팅 플랫폼의 환경변수 관리 기능을 사용하세요
