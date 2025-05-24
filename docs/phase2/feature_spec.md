# Phase 2 Feature Specification

## 1. 확장 가능한 아키텍처 구현
- **프론트엔드-백엔드 영역 분리**
  - 기존 Streamlit-LangGraph 코드를 프론트엔드(Streamlit)-백엔드(FastAPI+LangGraph) 로 분리
  - 컨테이너화를 위한 환경 설정 및 Dockerfile 작성
  - 서버 재실행 시 대화 내역이 남을 수 있도록 Database checkpointer 적용(Sqlite)
- **LLM, 프롬프트 확장성 구조 설계**
  - OpenAI ChatGPT 외 Claude, Gemini 등의 LLM 모델 선택 기능 제공
  - 프롬프트 버저닝

## 2. 프롬프트 엔지니어링
- **도메인 맞춤형 프롬프트 엔지니어링**  
  - 여행 계획, 일정 수립에 최적화 된 시스템 프롬프트 제공
- **LLM 가드레일 설정**
  - 여행과 무관한 질문 시 답변하지 않도록 설정
  - 비속어 필터링

## 3. 모니터링
- **LLM 엔지니어링 솔루션 추가**
  - 오픈소스 LLM 엔지니어링 플랫폼 Langfuse 연동
  - 파이썬 로깅 시스템 추가

## 4. 프로젝트 관리
- **지속 + 협업 가능한 프로젝트 체계**
  - 코드 유지보수 적용(AI 도구 및 Pylint)
  - 테스트 코드 + 데이터셋 추가
  - 아키텍처 다이어그램, LangGraph 시각화, API 문서 작성

이 문서는 AI 도구(ChatGPT, Claude, Gemini)로 작성되었습니다.
