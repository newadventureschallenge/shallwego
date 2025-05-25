from dotenv import load_dotenv
from langchain_anthropic import ChatAnthropic
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_openai import ChatOpenAI

from agent.agent_tools import tools

load_dotenv()

llm_dicts = {}

def get_llm(model_id: str):
    """
    주어진 모델 이름에 해당하는 LLM 인스턴스를 반환합니다.
    모델이 존재하지 않으면 새로 생성하여 저장합니다.
    """
    # 첫번째 하이픈 이후의 문자열을 모델 이름으로 사용 (이후에 하이픈이 들어갈 수 있음)
    try:
        provider_name, model_name = model_id.split("-", 1)

        if model_name not in llm_dicts:
            if provider_name == "openai":
                llm = ChatOpenAI(model=model_name)
            elif provider_name == "google":
                llm = ChatGoogleGenerativeAI(model=model_name)
            elif provider_name == "anthropic":
                llm = ChatAnthropic(model_name=model_name)
            else:
                raise ValueError(f"지원하지 않는 모델 이름: {model_name}")

            llm_dicts[model_name] = llm.bind_tools(tools)

    except ValueError:
        raise ValueError(f"모델 이름 형식이 잘못되었습니다: {model_id}. 올바른 형식은 'provider-model'입니다.")

    return llm_dicts[model_name]
