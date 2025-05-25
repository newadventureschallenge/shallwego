from typing import List, Optional
from sqlmodel import Session, select
from models.prompt_models import SystemPrompt

def add_prompt(
    session: Session,
    key: str,
    prompt_text: str,
    model_id: str,
    version: int = 1
) -> SystemPrompt:
    """
    key, prompt, model_id, version 정보를 DB에 저장하고 저장된 Prompt 객체를 반환합니다.
    """
    prompt = SystemPrompt(key=key, prompt=prompt_text, model_id=model_id, version=version)
    session.add(prompt)
    session.commit()
    session.refresh(prompt)
    return prompt


def get_prompt(
    session: Session,
    key: str,
    model_id: str
) -> SystemPrompt:
    # 1) model_name이 같은 것 중 버전이 가장 높은 한 건 조회
    stmt = (
        select(SystemPrompt)
        .where(SystemPrompt.key == key, SystemPrompt.model_id == model_id)
        .order_by(SystemPrompt.version.desc())
        .limit(1)
    )
    result = session.exec(stmt).first()
    if result:
        return result

    # 2) model_name="all"인 것 중 버전이 가장 높은 한 건 조회
    fallback = (
        select(SystemPrompt)
        .where(SystemPrompt.key == key, SystemPrompt.model_id == "all")
        .order_by(SystemPrompt.version.desc())
        .limit(1)
    )
    result = session.exec(fallback).first()

    if result:
        return result
    else:
        return ValueError(f'프롬프트가 존재하지 않습니다. 키: {key}, 모델 이름: {model_id}')

