from app.database import engine

SQL = """
ALTER TABLE posts
ADD COLUMN author TEXT NOT NULL DEFAULT '名無しさん';
"""

def run():
    with engine.connect() as conn:
        conn.exec_driver_sql(SQL)
        print("✔ author カラムを追加しました（DEFAULT: '名無しさん'）")

if __name__ == "__main__":
    run()