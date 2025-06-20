# Phase 1 Feature Specification

## 1. 사용자 인증 및 로그인

- **카카오 소셜 로그인**
  - 카카오 OAuth 기반 소셜 로그인 기능 제공

## 2. 여행 장소 검색

- **Daum 검색 API 연동**  
  - 대화형 에이전트가 Daum 검색 API Tool 활용하여 여행 장소 및 정보 검색
  - 카카오맵 로컬 REST API 연동하여 키워드, 카테고리 기반 장소 검색

## 3. 여행 계획서 자동 작성

- **LangChain, LangGraph 기반 대화형 플로우**
  - 사용자의 취향, 일정, 동행자 등 대화 정보 수집
  - 맞춤형 여행 계획서 생성 및 제공

## 4. 캘린더 연동

- **카카오 톡캘린더 REST API 연동**
  - 사용자 캘린더: 목록 조회, 서브 캘린더 생성/수정/삭제
  - 일반 일정: 생성, 목록 조회, 상세 조회, 수정, 삭제
  - ~~공개 일정: 생성, 목록 조회, 상세 조회, 수정, 삭제, 사용자 캘린더에 추가~~
    - 카카오톡 채널에서 제공하는 기능은 불필요하다고 생각되어 삭제 
  - 할 일: 생성, 조회, 도전 기록 보기, 수정, 삭제
  - 연동한 API는 Agent의 Tool로 연동

## 5. UI/UX

- **Streamlit 기반 웹 인터페이스**
  - 스트리밍 방식의 대화형 UI 제공
  - OpenAI LLM 연동
  - ~~생성/수정/삭제 기능은 사용자에게 확인 후 수행~~
    - 여러 할일과 일정을 한 번에 삭제할때 매우 불편하여 삭제

이 문서는 AI 도구(ChatGPT, Claude)로 작성되었습니다. 