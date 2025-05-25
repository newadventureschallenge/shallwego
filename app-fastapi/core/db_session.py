"""
Sqlite 데이터베이스 세션 관리 모듈
"""

from contextlib import contextmanager
from pathlib import Path

from sqlmodel import SQLModel, create_engine, Session

# core 폴더의 한 단계 상위(프로젝트 루트)로 설정
BASE_DIR = Path(__file__).resolve().parent.parent

# 프로젝트 루트에 sqlite_checkpointer.sqlite 생성
sqlite_file_name = BASE_DIR / 'sqlite_checkpointer.sqlite'
sqlite_url = f"sqlite:///{sqlite_file_name}"

# 1) 엔진 생성
engine = create_engine(sqlite_url)

# 2) 테이블 생성
def init_db():
    SQLModel.metadata.create_all(engine)


# 3) 세션 제공용 컨텍스트 매니저
@contextmanager
def get_session():
    session = Session(engine)
    try:
        yield session
    finally:
        session.close()
