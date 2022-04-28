from psycopg2 import connect, errors 

from config import DATABASE_URL

class SQL:
    def __init__(self):
        self.conn = connect(DATABASE_URL, keepalives=1, keepalives_idle=30, keepalives_interval=10, keepalives_count=5) 
        self.conn.autocommit = True

    def create_table(self):
        cursor=self.conn.cursor()  
        cursor.execute('''CREATE TABLE IF NOT EXISTS users (
        user_id BIGSERIAL, 
        user_firstname TEXT, 
        user_lastname TEXT, 
        user_username TEXT, 
        chat_id BIGSERIAL,
        time TIMESTAMP,
        language TEXT,
        chat_and_user_INFO TEXT PRIMARY KEY,
        Author TEXT
        )''')
        cursor.close()

    def insert(self, user_id, user_firstname, user_lastname, user_username, chat_id, datatime, Lang):
        chat_and_user_INFO= str(f'user={user_id} | chat={chat_id}')
        cursor=self.conn.cursor()
        try:
            cursor.execute('''DELETE FROM users WHERE chat_and_user_INFO = %s''',(chat_and_user_INFO,))
        finally:
            cursor.execute('''INSERT INTO users VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s)''', (user_id, user_firstname, user_lastname, user_username, chat_id, datatime, Lang, chat_and_user_INFO ,'IPOleksenko'))
        cursor.close()

    def examination(self, user_id, chat_id):
        cursor=self.conn.cursor()
        chat_and_user_INFO= str(f'user={user_id} | chat={chat_id}')
        cursor.execute('''SELECT user_id FROM users WHERE chat_and_user_INFO = %s''', (chat_and_user_INFO,))
        result = cursor.fetchone()
        cursor.close()
        return result or 'None'

    def select_lang(self, user_id):
        cursor=self.conn.cursor()
        cursor.execute('''SELECT language FROM users WHERE user_id = %s''', (user_id,))
        result = cursor.fetchone()
        cursor.close()
        return result or 'en'
Database_SQL = SQL()
#Author: IPOleksenko