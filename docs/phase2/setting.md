- `app-fastapi/.env`: 백엔드 환경 변수

KAKAO_APP_REST_API_KEY, KAKAO_APP_ADMIN_KEY: 카카오 API 키
OPENAI_API_KEY: OPENAI API 키
GOOGLE_API_KEY: GOOGLE API 키
ANTHROPIC_API_KEY: ANTHROPIC API 키
LANGFUSE_SECRET_KEY, LANGFUSE_PUBLIC_KEY: LANGFUSE 키 
ENCRYPTION_ACCESS_KEY: 액세스 토큰 암호화

- `app-fastapi/utils/api_endpoints.py`: API 엔드포인트 설정

LANGFUSE_HOST: LANGFUSE 호스트 주소
그 외는 카카오 API 엔드포인트

- `app-streamlit/.env`: 프론트엔드 환경 변수

STREAMLIT_COOKIE_SECRET_KEY: 스트림릿 쿠키 저장 키
ENCRYPTION_ACCESS_KEY: 액세스 토큰 암호화화

- `app-streamlit/.streamlit/secrets.toml`: Streamlit 시크릿 설정

[auth.kakao]
redirect_uri: REDIRECT URL
client_id: 카카오 제품 클라이언트 ID
client_secret: 카카오 제품 클라이언트 시크릿
server_metadata_url: https://kauth.kakao.com/.well-known/openid-configuration
client_kwargs: OAuth 권한 설정

- `app-streamlit/utils/api_endpoints.py`: API 엔드포인트 설정
CHAT_API_URL: api-fastapi CHAT 엔드포인트
RESET_API_URL: api-fastapi RESET 엔드포인트
