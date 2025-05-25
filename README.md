# 갈까요 (Shall We Go)

**갈까요**는 대화를 통해 여행의 계획부터 일정 공유까지 도와주는 AI 에이전트 챗봇입니다. 사용자는 에이전트와의 대화를 통해 여행 장소를 탐색하고, 맞춤형 일정을 세우며, 이를 캘린더에 저장하거나 다른 사람과 공유할 수 있습니다.

## 주요 기능

- 🗺️ **여행 장소 검색**  
  에이전트와 자연스럽게 대화하며 추천 여행지를 탐색할 수 있습니다.

- 📝 **여행 계획서 작성**  
  사용자의 취향과 대화를 바탕으로 여행 계획서를 자동으로 작성합니다.

- 📅 **캘린더 연동**  
  여행 일정을 대화만으로 등록, 조회, 수정, 삭제할 수 있습니다.

## 사용한 도구

- 코드 작성, 편집: PyCharm, Cursor.ai
- 코드 어시스턴트: Github Copilot, Cursor.ai
- 검색 및 문서 작성, 합성 데이터 생성: ChatGPT, Claude, Gemini

## 시연 화면
- 최초 접속 화면 및 카카오 OAuth 로그인 구현
![최초 화면](./images/0_shallwego.png)
![카카오 OAuth](./images/1_kakao_oauth.png)
- 로그인 화면. 우측은 채팅 UI이며 좌측은 사이드바. 로그아웃, LLM 모델 선택, 전체 대화 삭제(웹 미포함, DB 내역 삭제)
![로그인 화면](./images/2_screen.png)
- 검색 및 추천 기능. Daum 검색 API 및 카카오맵 로컬 API 를 활용하여 지역 및 카테고리 기반의 장소 추천
![장소 추천 1](./images/3_search.png)
![장소 추천 2](./images/4_search.png)
- 대화 기반 여행 계획서 작성.
![계획서 작성 1](./images/5_plan.png)
![계획서 작성 2](./images/6_plan.png)
- 카카오 톡캘린더 연동, 에이전트가 직접 캘린더와 일정, 할일 등록
![캘린더 연동 1](./images/7_calendar.png)
![캘린더 연동 2](./images/8_calendar.png)
![캘린더 연동 3](./images/9_calendar.png)
![캘린더 연동 4](./images/10_calendar.png)

## 사용 기술 및 아키텍처
- 전체 아키텍처

- LangGraph

## 일정

- 1차 기능 개발(Phase 1): 5/19-5/23 
- 2차 기능 개발(Phase 2): 5/24-5/25

##### 기타 자세한 문서(시스템 프롬프트, AI 도구 활용 등)는 docs 내 phase1, phase2 폴더 참고

이 문서는 AI 도구(ChatGPT, Claude)로 작성했습니다.