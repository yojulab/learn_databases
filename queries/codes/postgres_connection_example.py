
import psycopg2
import os

def get_db_connection():
    """PostgreSQL 데이터베이스에 연결합니다."""
    try:
        # 환경 변수 또는 기본값으로 데이터베이스 연결 정보 설정
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
        print("PostgreSQL 데이터베이스에 성공적으로 연결되었습니다.")
        return conn
    except psycopg2.OperationalError as e:
        print(f"데이터베이스 연결에 실패했습니다: {e}")
        print("연결 정보를 확인하거나 Docker 컨테이너가 실행 중인지 확인하세요.")
        return None

def setup_database(conn):
    """데이터베이스 테이블을 생성하고 초기 데이터를 삽입합니다."""
    if not conn:
        return

    try:
        with conn.cursor() as cur:
            cur.execute('CREATE EXTENSION IF NOT EXISTS "uuid-ossp";')
            # 벡터 확장 활성화 (pgvector가 설치된 경우)
            try:
                cur.execute("CREATE EXTENSION IF NOT EXISTS vector;")
                print("pgvector 확장이 활성화되었습니다.")
            except psycopg2.Error as e:
                print(f"pgvector 확장 활성화 중 오류 발생: {e}")
                conn.rollback() # 오류 발생 시 롤백

            # 사용자 테이블 생성 (간단한 예제)
            cur.execute("""
                CREATE TABLE IF NOT EXISTS users (
                    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
                    username VARCHAR(80) UNIQUE NOT NULL,
                    email VARCHAR(120) UNIQUE NOT NULL,
                    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
                );
            """)
            print("'users' 테이블이 생성되었거나 이미 존재합니다.")

            # 아이템과 벡터 임베딩 테이블 생성
            cur.execute("""
                CREATE TABLE IF NOT EXISTS items (
                    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
                    name VARCHAR(255) UNIQUE NOT NULL,
                    embedding vector(3) -- 예시로 3차원 벡터
                );
            """)
            print("'items' 테이블이 생성되었거나 이미 존재합니다.")
            
            conn.commit() # 변경사항 커밋
    except psycopg2.Error as e:
        print(f"테이블 생성 중 오류가 발생했습니다: {e}")
        conn.rollback()


def insert_sample_data(conn):
    """샘플 데이터를 테이블에 삽입합니다."""
    if not conn:
        return

    try:
        with conn.cursor() as cur:
            # 샘플 사용자 데이터 삽입
            sample_users = [
                ('user1', 'user1@example.com'),
                ('user2', 'user2@example.com')
            ]
            # ON CONFLICT DO NOTHING: 이미 존재하는 경우 무시
            cur.executemany("""
                INSERT INTO users (username, email) VALUES (%s, %s)
                ON CONFLICT (username) DO NOTHING;
            """, sample_users)
            print(f"{cur.rowcount}개의 새로운 사용자가 'users' 테이블에 추가되었습니다.")

            # 샘플 아이템 및 벡터 데이터 삽입
            sample_items = [
                ('item1', '[1,2,3]'),
                ('item2', '[4,5,6]'),
                ('item3', '[7,8,9]')
            ]
            cur.executemany("""
                INSERT INTO items (name, embedding) VALUES (%s, %s)
                ON CONFLICT (name) DO NOTHING;
            """, sample_items)
            print(f"{cur.rowcount}개의 새로운 아이템이 'items' 테이블에 추가되었습니다.")

            conn.commit()
    except psycopg2.Error as e:
        print(f"데이터 삽입 중 오류가 발생했습니다: {e}")
        conn.rollback()

def query_data(conn):
    """테이블에서 데이터를 조회하고 출력합니다."""
    if not conn:
        return

    try:
        with conn.cursor() as cur:
            print("\n--- 'users' 테이블 데이터 조회 ---")
            cur.execute("SELECT id, username, email, created_at FROM users;")
            users = cur.fetchall()
            if users:
                for user in users:
                    print(f"ID: {user[0]}, Username: {user[1]}, Email: {user[2]}, Created: {user[3]}")
            else:
                print("사용자 데이터가 없습니다.")

            print("\n--- 'items' 테이블 데이터 조회 ---")
            cur.execute("SELECT id, name, embedding FROM items;")
            items = cur.fetchall()
            if items:
                for item in items:
                    print(f"ID: {item[0]}, Name: {item[1]}, Embedding: {item[2]}")
            else:
                print("아이템 데이터가 없습니다.")

    except psycopg2.Error as e:
        print(f"데이터 조회 중 오류가 발생했습니다: {e}")

def vector_similarity_search(conn, query_vector):
    """벡터 유사도 검색을 수행합니다."""
    if not conn:
        return

    try:
        with conn.cursor() as cur:
            print(f"\n--- 벡터 유사도 검색 (쿼리: {query_vector}) ---")
            # 코사인 유사도(<=|>)를 사용하여 가장 유사한 아이템 찾기
            # L2 거리(<->) 또는 내적(<#>)도 사용 가능
            cur.execute("SELECT name, embedding, 1 - (embedding <=> %s) AS similarity FROM items ORDER BY similarity DESC LIMIT 5;", (query_vector,))
            results = cur.fetchall()
            
            if results:
                print("검색 결과:")
                for res in results:
                    print(f"  - Item: {res[0]}, Embedding: {res[1]}, Similarity: {res[2]:.4f}")
            else:
                print("유사한 아이템을 찾을 수 없습니다.")
                
    except psycopg2.Error as e:
        print(f"벡터 검색 중 오류가 발생했습니다: {e}")

def main():
    """메인 실행 함수"""
    # psycopg2가 설치되어 있지 않다면 설치 안내 메시지 출력
    try:
        import psycopg2
    except ImportError:
        print("psycopg2 라이브러리가 설치되지 않았습니다.")
        print("pip install psycopg2-binary 를 실행하여 설치하세요.")
        return

    conn = None
    try:
        # 1. 데이터베이스 연결
        conn = get_db_connection()

        if conn:
            # 2. 데이터베이스 테이블 설정
            setup_database(conn)

            # 3. 샘플 데이터 삽입
            insert_sample_data(conn)

            # 4. 데이터 조회
            query_data(conn)
            
            # 5. 벡터 유사도 검색 예시
            vector_similarity_search(conn, '[1,1,1]')

    finally:
        # 5. 연결 종료
        if conn:
            conn.close()
            print("\nPostgreSQL 데이터베이스 연결이 종료되었습니다.")

if __name__ == "__main__":
    main()
