from dotenv import load_dotenv
from korcen import korcen
from openai import AsyncOpenAI

load_dotenv()

async def is_filtered(message: str) -> bool:
    """
    주어진 메시지가 필터링되어야 하는지 여부를 확인합니다.
    """
    try:
        if korcen.check(message):
            return True

        client = AsyncOpenAI()

        # 비동기 모더레이션 호출
        response = await client.moderations.create(
            model="omni-moderation-latest",
            input=message,
        )
        return response.results[0].flagged

    except Exception:
        # 예외 발생 시 안전하게 필터링하지 않음
        return False
