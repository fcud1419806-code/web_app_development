import sqlite3
import os

# 定義資料庫路徑 (對應到 instance/database.db)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
DB_PATH = os.path.join(BASE_DIR, 'instance', 'database.db')

def get_db_connection():
    """取得資料庫連線"""
    # 確保 instance 資料夾存在
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    
    conn = sqlite3.connect(DB_PATH)
    # 讓查詢結果可以用字典的方式存取欄位名稱 (例如 row['title'])
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    """初始化資料庫，執行建表語法"""
    schema_path = os.path.join(BASE_DIR, 'database', 'schema.sql')
    if os.path.exists(schema_path):
        with get_db_connection() as conn:
            with open(schema_path, 'r', encoding='utf-8') as f:
                conn.executescript(f.read())
            conn.commit()

class TransactionModel:
    """處理交易紀錄的 CRUD 操作"""
    
    @staticmethod
    def create(title, amount, type, category, date):
        """新增一筆紀錄"""
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                '''
                INSERT INTO transactions (title, amount, type, category, date)
                VALUES (?, ?, ?, ?, ?)
                ''',
                (title, amount, type, category, date)
            )
            conn.commit()
            return cursor.lastrowid

    @staticmethod
    def get_all():
        """取得所有紀錄 (依日期遞減排序)"""
        with get_db_connection() as conn:
            cursor = conn.cursor()
            # 依據 date 以及 id 反序排列，確保最新的在最上面
            cursor.execute('SELECT * FROM transactions ORDER BY date DESC, id DESC')
            return cursor.fetchall()
            
    @staticmethod
    def get_by_id(transaction_id):
        """根據 ID 取得單筆紀錄"""
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM transactions WHERE id = ?', (transaction_id,))
            return cursor.fetchone()

    @staticmethod
    def update(transaction_id, title, amount, type, category, date):
        """更新單筆紀錄"""
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                '''
                UPDATE transactions
                SET title = ?, amount = ?, type = ?, category = ?, date = ?
                WHERE id = ?
                ''',
                (title, amount, type, category, date, transaction_id)
            )
            conn.commit()
            return cursor.rowcount > 0

    @staticmethod
    def delete(transaction_id):
        """刪除單筆紀錄"""
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT title FROM transactions WHERE id = ?', (transaction_id,))
            # Execute deletion
            cursor.execute('DELETE FROM transactions WHERE id = ?', (transaction_id,))
            conn.commit()
            return cursor.rowcount > 0
