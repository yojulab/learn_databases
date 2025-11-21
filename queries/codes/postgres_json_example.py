import psycopg2
import os
import json

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
        print("PostgreSQL 데이터베이스에 성공적으로 연결되었습니다.")
        return conn
    except psycopg2.OperationalError as e:
        print(f"데이터베이스 연결에 실패했습니다: {e}")
        return None

def setup_database_json(conn):
    """JSONB를 사용하는 테이블을 생성합니다."""
    if not conn:
        return

    try:
        with conn.cursor() as cur:
            cur.execute('CREATE EXTENSION IF NOT EXISTS "uuid-ossp";')
            # jsonb_ops는 JSONB 데이터 유형에 대한 인덱싱을 지원합니다.
            cur.execute("""
                CREATE TABLE IF NOT EXISTS products (
                    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
                    name VARCHAR(255) UNIQUE NOT NULL,
                    details JSONB,
                    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
                );
            """)
            print("'products' 테이블이 생성되었거나 이미 존재합니다.")
            
            # 테이블 초기화 (예제 반복 실행 시 데이터 중복 방지)
            cur.execute("TRUNCATE TABLE products;")
            print("'products' 테이블의 모든 데이터가 삭제되었습니다.")

            conn.commit()
    except psycopg2.Error as e:
        print(f"테이블 생성 중 오류가 발생했습니다: {e}")
        conn.rollback()

def json_crud_examples(conn):
    """JSON 데이터에 대한 CRUD 작업을 수행합니다."""
    if not conn:
        return

    try:
        with conn.cursor() as cur:
            # 1. CREATE: JSON 데이터 삽입
            print("\n--- 1. CREATE: JSON 데이터 삽입 ---")
            product_data = {
                "name": "노트북",
                "details": {
                    "category": "electronics",
                    "price": 1200,
                    "specs": {"cpu": "i7", "ram": 16, "storage": "512GB SSD"},
                    "tags": ["computer", "portable"]
                }
            }
            # psycopg2는 dict를 자동으로 JSON으로 변환하지만, json.dumps를 사용하는 것이 명시적입니다.
            cur.execute(
                "INSERT INTO products (name, details) VALUES (%s, %s) RETURNING id;",
                (product_data["name"], json.dumps(product_data["details"]))
            )
            notebook_id = cur.fetchone()[0]
            print(f"노트북 제품이 추가되었습니다. ID: {notebook_id}")

            product_data_2 = {
                "name": "스마트폰",
                "details": {
                    "category": "electronics",
                    "price": 800,
                    "specs": {"cpu": "Snapdragon 8", "ram": 8, "storage": "256GB"},
                    "tags": ["mobile", "camera"]
                }
            }
            cur.execute(
                "INSERT INTO products (name, details) VALUES (%s, %s);",
                (product_data_2["name"], json.dumps(product_data_2["details"]))
            )
            print("스마트폰 제품이 추가되었습니다.")
            conn.commit()

            # 2. READ: JSON 데이터 조회
            print("\n--- 2. READ: JSON 데이터 조회 ---")
            # 전체 데이터 조회
            cur.execute("SELECT id, name, details FROM products;")
            products = cur.fetchall()
            print("전체 제품 조회:")
            for p in products:
                print(f"  ID: {p[0]}, Name: {p[1]}, Details: {json.dumps(p[2], indent=2, ensure_ascii=False)}")

            # JSON의 특정 필드로 조회 (->> 연산자는 필드 값을 텍스트로 반환)
            print("\n'electronics' 카테고리 제품 조회:")
            cur.execute("SELECT name, details FROM products WHERE details->>'category' = 'electronics';")
            electronics = cur.fetchall()
            for item in electronics:
                print(f"  - {item[0]}")

            # 중첩된 JSON 객체 내부 값으로 조회
            print("\nRAM이 16GB인 제품 조회:")
            cur.execute("SELECT name FROM products WHERE details->'specs'->>'ram' = '16';")
            powerful_laptops = cur.fetchall()
            for item in powerful_laptops:
                print(f"  - {item[0]}")
            
            # JSON 배열에 특정 요소가 포함된 경우 조회 (@> 연산자 사용)
            print("\n'portable' 태그를 가진 제품 조회:")
            cur.execute("SELECT name FROM products WHERE details->'tags' @> '[\"portable\"]';")
            portables = cur.fetchall()
            for item in portables:
                print(f"  - {item[0]}")


            # 3. UPDATE: JSON 데이터 수정
            print("\n--- 3. UPDATE: JSON 데이터 수정 ---")
            # 특정 필드 값 수정 (jsonb_set 함수 사용)
            # 노트북의 가격을 1250으로 변경
            cur.execute(
                "UPDATE products SET details = jsonb_set(details, '{price}', '1250') WHERE id = %s;",
                (notebook_id,)
            )
            print("노트북 가격이 1250으로 변경되었습니다.")

            # 새로운 필드 추가
            # 노트북에 'manufacturer' 필드 추가
            cur.execute(
                "UPDATE products SET details = details || '{\"manufacturer\": \"Gemini\"}'::jsonb WHERE id = %s;",
                (notebook_id,)
            )
            print("노트북에 제조사 정보가 추가되었습니다.")
            conn.commit()

            # 수정된 데이터 확인
            cur.execute("SELECT details FROM products WHERE id = %s;", (notebook_id,))
            updated_product = cur.fetchone()
            print("수정된 노트북 정보:", json.dumps(updated_product[0], indent=2, ensure_ascii=False))


            # 4. DELETE: JSON 데이터를 기준으로 삭제
            print("\n--- 4. DELETE: JSON 데이터를 기준으로 삭제 ---")
            # 가격이 1000 미만인 제품 삭제
            cur.execute("DELETE FROM products WHERE (details->>'price')::numeric < 1000;")
            deleted_count = cur.rowcount
            print(f"{deleted_count}개의 제품(가격 1000 미만)이 삭제되었습니다.")
            conn.commit()

            # 남은 데이터 확인
            cur.execute("SELECT name FROM products;")
            remaining_products = cur.fetchall()
            print("남아있는 제품:")
            for p in remaining_products:
                print(f"  - {p[0]}")

    except psycopg2.Error as e:
        print(f"JSON CRUD 작업 중 오류가 발생했습니다: {e}")
        conn.rollback()

def main():
    """메인 실행 함수"""
    try:
        import psycopg2
    except ImportError:
        print("psycopg2 라이브러리가 설치되지 않았습니다.")
        print("pip install psycopg2-binary 를 실행하여 설치하세요.")
        return

    conn = None
    try:
        conn = get_db_connection()
        if conn:
            setup_database_json(conn)
            json_crud_examples(conn)
    finally:
        if conn:
            conn.close()
            print("\nPostgreSQL 데이터베이스 연결이 종료되었습니다.")

if __name__ == "__main__":
    main()
