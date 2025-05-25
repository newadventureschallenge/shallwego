# Phase 2 Result

## 1. 확장 가능한 아키텍처 구현
- **프론트엔드-백엔드 영역 분리**
  - 기존 Streamlit-LangGraph 코드를 프론트엔드(Streamlit)-백엔드(FastAPI+LangGraph) 로 분리
  - 컨테이너화를 위한 환경 설정 및 Dockerfile 작성
  - 서버 재실행 시 대화 내역이 남을 수 있도록 Database checkpointer 적용(Sqlite)

- **LLM, 프롬프트 확장성 구조 설계**
  - OpenAI ChatGPT 외 Claude, Gemini 등의 LLM 모델 선택 기능 제공
  - 프롬프트 데이터베이스 별도 구축, 모델 별로 별도의 시스템 프롬프트 설정 및 버저닝 가능하도록 구축

## 2. 프롬프트 엔지니어링
- **도메인 맞춤형 프롬프트 엔지니어링**  
  - 여행 계획, 일정 수립에 최적화 된 시스템 프롬프트 엔지니어링
  - 스코어링, 대화 요약 등의 프롬프트 엔지니어링
  - 벡터 스토어(임베딩) 구축 및 시멘틱 서치를 포함한 RAG 프로세스 추가 구현
    (국내 여행지 100곳에 대한 CSV 합성 데이터 생성 후 변환, RAG를 통해 프롬프트 첨부)

- **LLM 가드레일 설정**
  - 여행과 무관한 질문 시 답변하지 않도록 프롬프트 엔지니어링
  - OpenAI Moderation API 적용

## 3. 모니터링
- **LLM 엔지니어링 솔루션 추가**
  - 오픈소스 LLM 엔지니어링 플랫폼 Langfuse 연동, 전 범위 Tracing 구축
  - 셀프 스코어링시스템 추가
  - 파이썬 콘솔 로깅 시스템 추가

## 4. 프로젝트 관리
- **지속 + 협업 가능한 프로젝트 체계**
  - Cursor AI MDC 추가 및 workspace 세팅. 개별 프로젝트마다 별도 python 가상환경 잡히도록 설정
  - 테스트 코드 + 데이터셋 추가 (app-streamlit/dataset/tools_dataset.csv, result_dataset.csv)
    자동화된 API 테스트 시스템 적용
  - 아키텍처 다이어그램, LangGraph 시각화, API 문서 작성

이 문서는 AI 도구(ChatGPT, Claude, Gemini)로 작성되었습니다.