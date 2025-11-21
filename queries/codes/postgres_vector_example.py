import psycopg2
import os
import json
import numpy as np
from pgvector.psycopg2 import register_vector # pgvector 라이브러리 임포트
from psycopg2.extras import Json # Jsonb 대신 Json 사용

def get_db_connection():
    """PostgreSQL 데이터베이스에 연결합니다."""
    try:
        db_host = os.getenv("DB_HOST", "db_postgresql")
        db_port = os.getenv("DB_PORT", "5432")
        db_name = os.getenv("POSTGRES_DB", "main_db")
        db_user = os.getenv("POSTGRES_USER", "admin")
        db_password = os.getenv("POSTGRES_PASSWORD", "admin123")

        conn = psycopg2.connect(
            host=db_host,
            port=db_port,
            dbname=db_name,
            user=db_user,
            password=db_password
        )
        register_vector(conn) # pgvector 어댑터 등록
        print("PostgreSQL 데이터베이스에 성공적으로 연결되었습니다.")
        return conn
    except psycopg2.OperationalError as e:
        print(f"데이터베이스 연결에 실패했습니다: {e}")
        return None

def setup_database_vector(conn):
    """pgvector를 사용하는 테이블을 생성합니다."""
    if not conn:
        return

    try:
        with conn.cursor() as cur:
            cur.execute('CREATE EXTENSION IF NOT EXISTS "uuid-ossp";')
            # 1. pgvector 확장 활성화
            cur.execute("CREATE EXTENSION IF NOT EXISTS vector;")
            print("pgvector 확장이 활성화되었습니다.")

            # 2. 테이블 생성 (일반, JSON, Vector 컬럼 포함)
            # 벡터 차원을 4로 지정
            cur.execute("""
                CREATE TABLE IF NOT EXISTS documents (
                    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
                    content TEXT,
                    metadata JSONB,
                    embedding vector(4)
                );
            """)
            print("'documents' 테이블이 생성되었거나 이미 존재합니다.")

            # 3. 테이블 초기화 (예제 반복 실행을 위해)
            cur.execute("TRUNCATE TABLE documents;")
            print("'documents' 테이블이 초기화되었습니다.")

            conn.commit()
    except psycopg2.Error as e:
        print(f"데이터베이스 설정 중 오류 발생: {e}")
        conn.rollback()

def vector_crud_examples(conn):
    """Vector 데이터에 대한 CRUD 및 검색 작업을 수행합니다."""
    if not conn:
        return

    try:
        with conn.cursor() as cur:
            # 1. CREATE: 벡터 데이터 삽입
            print("\n--- 1. CREATE: 벡터 데이터 삽입 ---")
            docs_to_insert = [
                {
                    "content": "고양이는 조용하고 독립적인 동물이다.",
                    "metadata": {"category": "animal", "lang": "ko"},
                    "embedding": np.array([0.1, 0.4, 0.3, 0.2])
                },
                {
                    "content": "파이썬은 데이터 과학에 널리 사용된다.",
                    "metadata": {"category": "tech", "lang": "ko"},
                    "embedding": np.array([0.8, 0.2, 0.1, 0.9])
                },
                {
                    "content": "바나나는 칼륨이 풍부한 과일이다.",
                    "metadata": {"category": "food", "lang": "ko"},
                    "embedding": np.array([0.3, 0.8, 0.9, 0.1])
                }
            ]
            inserted_ids = []
            for doc in docs_to_insert:
                cur.execute(
                    "INSERT INTO documents (content, metadata, embedding) VALUES (%s, %s, %s) RETURNING id;",
                    (doc["content"], Json(doc["metadata"]), doc["embedding"])
                )
                inserted_id = cur.fetchone()[0]
                inserted_ids.append(inserted_id)

            print(f"{len(docs_to_insert)}개의 문서가 삽입되었습니다.")
            conn.commit()

            # 2. READ: 데이터 조회 및 유사도 검색
            print("\n--- 2. READ: 유사도 검색 ---")
            query_embedding = np.array([0.7, 0.1, 0.1, 0.8]) # "프로그래밍 언어"에 대한 가상 임베딩
            print(f"쿼리 벡터: {query_embedding.tolist()}")

            # L2 거리 (Euclidean distance): 가장 작은 값이 가장 유사
            cur.execute("SELECT id, content, embedding <-> %s AS distance FROM documents ORDER BY distance LIMIT 5;", (query_embedding,))
            results_l2 = cur.fetchall()
            print("\nL2 거리 기반 검색 결과 (가장 가까운 순):")
            for res in results_l2:
                print(f"  ID: {res[0]}, Content: {res[1]}, Distance: {res[2]:.4f}")

            # 코사인 유사도 (Cosine similarity): 1에 가까울수록 유사
            # 코사인 거리(1-유사도)가 가장 작은 것을 찾음
            cur.execute("SELECT id, content, 1 - (embedding <=> %s) AS similarity FROM documents ORDER BY similarity DESC LIMIT 5;", (query_embedding,))
            results_cosine = cur.fetchall()
            print("\n코사인 유사도 기반 검색 결과 (가장 유사한 순):")
            for res in results_cosine:
                print(f"  ID: {res[0]}, Content: {res[1]}, Similarity: {res[2]:.4f}")

            # 메타데이터 필터링과 함께 유사도 검색
            print("\n'tech' 카테고리 내에서 유사도 검색:")
            cur.execute (
                "SELECT id, content, 1 - (embedding <=> %s) AS similarity "
                "FROM documents "
                "WHERE metadata->>'category' = 'tech' "
                "ORDER BY similarity DESC LIMIT 5;",
                (query_embedding,)
            )
            results_filtered = cur.fetchall()
            for res in results_filtered:
                print(f"  ID: {res[0]}, Content: {res[1]}, Similarity: {res[2]:.4f}")

            # 3. UPDATE: 벡터 데이터 수정
            print("\n--- 3. UPDATE: 벡터 데이터 수정 ---")
            new_embedding = np.array([0.1, 0.5, 0.2, 0.2])
            cur.execute("UPDATE documents SET embedding = %s WHERE id = %s;", (new_embedding, inserted_ids[0]))
            print(f"ID {inserted_ids[0]} 문서의 임베딩이 수정되었습니다.")

            new_metadata = {"category": "animal", "lang": "ko", "has_tail": True}
            cur.execute("UPDATE documents SET metadata = %s WHERE id = %s;", (Json(new_metadata), inserted_ids[0]))
            print(f"ID {inserted_ids[0]} 문서의 메타데이터가 수정되었습니다.")
            conn.commit()

            # 수정 확인
            cur.execute("SELECT content, metadata, embedding::text FROM documents WHERE id = %s;", (inserted_ids[0],))
            updated_doc = cur.fetchone()
            print("수정된 문서:", updated_doc)


            # 4. DELETE: 데이터 삭제
            print("\n--- 4. DELETE: 데이터 삭제 ---")
            cur.execute("DELETE FROM documents WHERE id = %s;", (inserted_ids[2],))
            print(f"ID {inserted_ids[2]} 문서('바나나')가 삭제되었습니다.")
            conn.commit()

            # 삭제 확인
            cur.execute("SELECT COUNT(*) FROM documents;")
            count = cur.fetchone()[0]
            print(f"남아있는 문서 수: {count}")

    except psycopg2.Error as e:
        print(f"Vector CRUD 작업 중 오류 발생: {e}")
        conn.rollback()

def main():
    """메인 실행 함수"""
    try:
        import psycopg2
        import numpy
        import pgvector # pgvector 임포트 시도
    except ImportError as e:
        print(f"필수 라이브러리가 설치되지 않았습니다: {e.name}")
        print("pip install psycopg2-binary numpy pgvector 를 실행하여 설치하세요.")
        return

    conn = None
    try:
        conn = get_db_connection()
        if conn:
            setup_database_vector(conn)
            vector_crud_examples(conn)
    finally:
        if conn:
            conn.close()
            print("\nPostgreSQL 데이터베이스 연결이 종료되었습니다.")

if __name__ == "__main__":
    main()
