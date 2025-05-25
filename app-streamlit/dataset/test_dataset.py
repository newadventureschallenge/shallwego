"""
Tools Dataset 테스트 자동화
"""
import time
import csv
import os
from datetime import datetime

import orjson
import streamlit as st
import pandas as pd
from websocket import create_connection, WebSocketConnectionClosedException

from schemas.chat_schemas import ChatRequest
from pages.social_login import ensure_valid_token
from utils import api_endpoints
from utils.encryption import encrypt_message


def load_tools_dataset():
    """tools_dataset.csv 파일을 로드합니다."""
    current_dir = os.getcwd()
    st.info(f"현재 작업 디렉토리: {current_dir}")

    dataset_path = "dataset/tools_dataset.csv"
    try:
        df = pd.read_csv(dataset_path)
        return df
    except FileNotFoundError:
        st.error(f"데이터셋 파일을 찾을 수 없습니다: {dataset_path}")
        return None


def save_result_to_csv(tool_name, category, example_sentence, response, test_time):
    """테스트 결과를 result_dataset.csv에 저장합니다."""
    result_path = "dataset/result_dataset.csv"
    
    # 파일이 없으면 헤더와 함께 생성
    file_exists = os.path.exists(result_path)
    
    with open(result_path, 'a', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['tool_name', 'category', 'example_sentence', 'response', 'test_time', 'timestamp']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        
        if not file_exists:
            writer.writeheader()
        
        writer.writerow({
            'tool_name': tool_name,
            'category': category,
            'example_sentence': example_sentence,
            'response': response,
            'test_time': test_time,
            'timestamp': datetime.now().isoformat()
        })


def send_message_and_get_response(message, user_id, access_token, model_id):
    """메시지를 보내고 응답을 받습니다."""
    ws = None
    full_response = ""
    start_time = time.time()
    
    try:
        ws = create_connection(api_endpoints.CHAT_API_URL)
        req = ChatRequest(
            message=message,
            user_id=user_id,
            access_token=encrypt_message(access_token),
            model_id=model_id
        ).model_dump()
        
        ws.send(orjson.dumps(req))
        
        while True:
            try:
                raw = ws.recv()
                if not raw:
                    continue
                
                try:
                    message_data = orjson.loads(raw)
                except orjson.JSONDecodeError:
                    continue
                
                parts = message_data.get("messages", [])
                
                if isinstance(parts, list):
                    for chunk in parts:
                        full_response += chunk.get("text", "")
                else:
                    full_response += str(parts)
                    
            except WebSocketConnectionClosedException:
                break
                
    except Exception as e:
        full_response = f"Error: {str(e)}"
    finally:
        if ws:
            ws.close()
    
    end_time = time.time()
    test_time = end_time - start_time
    
    return full_response, test_time


def run_dataset_test():
    """데이터셋 테스트를 실행합니다."""
    # 로그인 확인
    if not st.session_state.get("token"):
        st.error("로그인 후 사용 가능합니다.")
        return False
    
    # 토큰 만료 확인
    ensure_valid_token()
    
    access_token = str(st.session_state.token.get("access_token"))
    user_id = str(st.session_state.get("user_id"))
    model_id = st.session_state.get("llm", "gpt-4")
    
    # 데이터셋 로드
    df = load_tools_dataset()
    if df is None:
        return False
    
    st.info(f"총 {len(df)}개의 테스트 케이스를 실행합니다.")
    
    # 진행률 표시
    progress_bar = st.progress(0)
    status_text = st.empty()
    result_container = st.container()
    
    total_tests = len(df)
    successful_tests = 0
    failed_tests = 0
    
    for index, row in df.iterrows():
        tool_name = row['tool_name']
        category = row['category']
        example_sentence = row['example_sentence']
        
        # 현재 진행 상황 표시
        progress = (index + 1) / total_tests
        progress_bar.progress(progress)
        status_text.text(f"테스트 중... ({index + 1}/{total_tests}) - {tool_name}")
        
        # 실시간 결과 표시
        with result_container:
            st.write(f"**{index + 1}. {tool_name}** ({category})")
            st.write(f"입력: {example_sentence}")
        
        try:
            # 메시지 전송 및 응답 받기
            response, test_time = send_message_and_get_response(
                example_sentence, user_id, access_token, model_id
            )
            
            # 결과 저장
            save_result_to_csv(tool_name, category, example_sentence, response, test_time)
            
            # 실시간 결과 표시
            with result_container:
                st.write(f"응답: {response[:200]}{'...' if len(response) > 200 else ''}")
                st.write(f"응답 시간: {test_time:.2f}초")
                st.success("✅ 성공")
                st.write("---")
            
            successful_tests += 1
            
        except Exception as e:
            # 에러 발생 시
            error_message = f"Error: {str(e)}"
            save_result_to_csv(tool_name, category, example_sentence, error_message, 0)
            
            with result_container:
                st.error(f"❌ 실패: {error_message}")
                st.write("---")
            
            failed_tests += 1
        
        # 0.5초 대기 (마지막 테스트가 아닌 경우)
        if index < total_tests - 1:
            time.sleep(0.5)
    
    # 테스트 완료
    progress_bar.progress(1.0)
    status_text.text("테스트 완료!")
    
    # 최종 결과 요약
    st.success(f"""
    🎉 **테스트 완료!**
    
    - 총 테스트: {total_tests}개
    - 성공: {successful_tests}개
    - 실패: {failed_tests}개
    - 성공률: {(successful_tests/total_tests*100):.1f}%
    
    결과는 `result_dataset.csv` 파일에 저장되었습니다.
    """)
    
    return True


def show_test_results():
    """저장된 테스트 결과를 표시합니다."""
    result_path = "app-streamlit/dataset/result_dataset.csv"
    
    if not os.path.exists(result_path):
        st.warning("아직 테스트 결과가 없습니다.")
        return
    
    try:
        df = pd.read_csv(result_path)
        
        st.subheader("📊 테스트 결과 요약")
        
        # 기본 통계
        total_tests = len(df)
        successful_tests = len(df[~df['response'].str.startswith('Error')])
        failed_tests = total_tests - successful_tests
        
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("총 테스트", total_tests)
        with col2:
            st.metric("성공", successful_tests)
        with col3:
            st.metric("실패", failed_tests)
        with col4:
            st.metric("성공률", f"{(successful_tests/total_tests*100):.1f}%")
        
        # 카테고리별 성공률
        st.subheader("📈 카테고리별 성공률")
        category_stats = df.groupby('category').agg({
            'tool_name': 'count',
            'response': lambda x: sum(~x.str.startswith('Error'))
        }).rename(columns={'tool_name': 'total', 'response': 'success'})
        category_stats['success_rate'] = (category_stats['success'] / category_stats['total'] * 100).round(1)
        st.dataframe(category_stats)
        
        # 평균 응답 시간
        avg_response_time = df[df['test_time'] > 0]['test_time'].mean()
        st.metric("평균 응답 시간", f"{avg_response_time:.2f}초")
        
        # 상세 결과 테이블
        st.subheader("📋 상세 결과")
        st.dataframe(df[['tool_name', 'category', 'example_sentence', 'test_time', 'timestamp']])
        
    except Exception as e:
        st.error(f"결과 파일을 읽는 중 오류가 발생했습니다: {str(e)}")


# 테스트 실행 함수 (버튼에서 호출할 함수)
def execute_full_dataset_test():
    """전체 데이터셋 테스트를 실행하는 메인 함수"""
    st.title("🧪 Tools Dataset 자동 테스트")
    
    # 탭으로 구분
    tab1, tab2 = st.tabs(["테스트 실행", "결과 보기"])
    
    with tab1:
        st.write("tools_dataset.csv의 모든 example_sentence를 순차적으로 테스트합니다.")
        
        # 데이터셋 미리보기
        df = load_tools_dataset()
        if df is not None:
            st.write(f"**로드된 데이터셋**: {len(df)}개 테스트 케이스")
            with st.expander("데이터셋 미리보기"):
                st.dataframe(df.head(10))
        
        # 여기에 버튼을 추가하면 됩니다
        # if st.button("테스트 시작"):
        #     run_dataset_test()
    
    with tab2:
        show_test_results()
