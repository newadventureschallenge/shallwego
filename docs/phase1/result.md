# 갈까요 (Shall We Go) Phase 1 개발 내역 요약

## 1. 개요
1차 개발 단계(Phase 1)에서는 Streamlit, LangGraph, LangChain의 기본 연결과 카카오 API 연동을 중심으로 PoC를 진행함.

## 2. 주요 개발 내역

### 1) 사용자 인증
- 카카오 OAuth 기반 소셜 로그인 구현
- Access Token을 기반으로 카카오 API 호출
- streamlit-cookies-controller(https://github.com/NathanChen198/streamlit-cookies-controller) 적용

### 2) 스트리밍 기반의 챗봇 구현
- Streamlit 내내 스트리밍 LLM 챗봇 UI 개발
- LangChain, LangGraph 로 사용자의 요청을 처리
- MemorySaver 추가로 멀티턴 기반 대화

### 3) 카카오 API 연동
- Daum 검색 API, 카카오맵 로컬 REST API 연동으로 여행지 정보 검색 제공.
- 카카오 톡캘린더 REST API 연동. 여행 일정을 캘린더에 자동 추가/수정/삭제 가능.

## 3. Phase 2 목표
 - Frontend-Backend 분리를 통한 확장 가능한 아키텍처 구성
 - 도메인 맞춤 프롬프트 엔지니어링
 - 테스트, 모니터링, 협업업 등 지속 가능한 개발이 가능한 프로젝트 설정

 이 문서는 AI 도구(ChatGPT, Claude, Gemini)로 작성되었습니다. 
