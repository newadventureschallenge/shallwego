"""
관광지 벡터 저장소 및 검색 기능을 제공하는 모듈입니다.
"""

import os
import pickle
from typing import List

import pandas as pd
from langchain_core.documents import Document
from langchain_core.embeddings import Embeddings
from langchain_core.vectorstores import InMemoryVectorStore, VectorStore
from langchain_openai import OpenAIEmbeddings


class TouristVectorStore:
    """
    관광지 벡터 저장소를 관리하는 클래스입니다.
    """
    def __init__(self, csv_path: str = "data/100TouristAttractions.csv", store_path: str = "data/vector_store_data.pkl"):
        self.csv_path = csv_path
        self.store_path = store_path
        self.embeddings = None
        self.vectorstore = None

    def get_embedding_model(self) -> Embeddings:
        """임베딩 모델을 가져옵니다."""
        return OpenAIEmbeddings(model="text-embedding-3-small")

    def load_data(self) -> List[Document]:
        """CSV에서 관광지 데이터 로드"""
        df = pd.read_csv(self.csv_path)
        documents = []
        for _, row in df.iterrows():
            content = f"{row['관광지']}: {row['설명']}"
            documents.append(Document(page_content=content, metadata={"name": row['관광지']}))
        return documents

    def create(self) -> VectorStore:
        """벡터 저장소 생성"""
        self.embeddings = self.get_embedding_model()
        documents = self.load_data()

        # 문서 임베딩 생성
        texts = [doc.page_content for doc in documents]
        metadatas = [doc.metadata for doc in documents]

        # 임베딩 생성
        embeddings_list = self.embeddings.embed_documents(texts)

        # 문서와 임베딩만 저장 (객체 전체가 아님)
        store_data = {
            "texts": texts,
            "metadatas": metadatas,
            "embeddings": embeddings_list
        }

        # 디렉토리 생성
        os.makedirs(os.path.dirname(self.store_path), exist_ok=True)

        # 데이터만 저장
        with open(self.store_path, 'wb') as f:
            pickle.dump(store_data, f)

        # 벡터스토어 생성
        self.vectorstore = InMemoryVectorStore(self.embeddings)
        self.vectorstore.add_documents(documents)

        return self.vectorstore

    def load(self) -> VectorStore:
        """저장된 벡터 저장소 데이터 로드"""
        if os.path.exists(self.store_path):
            with open(self.store_path, 'rb') as f:
                store_data = pickle.load(f)

            self.embeddings = self.get_embedding_model()
            self.vectorstore = InMemoryVectorStore(self.embeddings)

            # 문서 생성 후 추가
            documents = []
            for text, metadata in zip(store_data["texts"], store_data["metadatas"]):
                documents.append(Document(page_content=text, metadata=metadata))

            self.vectorstore.add_documents(documents)
            return self.vectorstore

        return self.create()

    def search(self, query: str, top_k: int = 3, threshold: float = 0.5) -> List[str]:
        """쿼리와 유사한 관광지 검색 (임계값 적용)"""
        if not self.vectorstore:
            self.load()

        # 점수와 함께 결과 가져오기
        results_with_scores = self.vectorstore.similarity_search_with_score(query, k=top_k)

        # 임계값으로 필터링 (코사인 유사도는 높을수록 유사함)
        filtered_results = [doc for doc, score in results_with_scores if score >= threshold]

        return [doc.page_content for doc in filtered_results]


vector_store = TouristVectorStore()
vector_store.create()
