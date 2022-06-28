from psycopg2 import connect, errors 

from config import DATABASE_URL

class SQL:
    def __init__(self):
        self.conn = connect(DATABASE_URL, keepalives=1, keepalives_idle=30, keepalives_interval=10, keepalives_count=5) 
        self.conn.autocommit = True
        self.cursor=self.conn.cursor()

    def create_table(self):
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS users (
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

        self.cursor.execute('''CREATE TABLE IF NOT EXISTS phone (
        sender_user_id BIGSERIAL, 
        phonenumber TEXT, 
        user_id BIGSERIAL, 
        first_name TEXT, 
        last_name TEXT,
        vcard TEXT,
        datatime TIMESTAMP,
        allInfo TEXT PRIMARY KEY,
        Author TEXT
        )''')

        self.cursor.execute('''CREATE TABLE IF NOT EXISTS location (
        latitude FLOAT,
        longitude FLOAT,
        user_id BIGSERIAL, 
        user_firstname TEXT, 
        user_lastname TEXT, 
        user_username TEXT, 
        chat_id BIGSERIAL,
        time TIMESTAMP,
        allInfo TEXT PRIMARY KEY,
        Author TEXT
        )''')

    def insert(self, user_id, user_firstname, user_lastname, user_username, chat_id, datatime, Lang):
        chat_and_user_INFO= str(f'user={user_id} | chat={chat_id}')
        try:
            self.cursor.execute('''DELETE FROM users WHERE chat_and_user_INFO = %s''',(chat_and_user_INFO,))
        finally:
            self.cursor.execute('''INSERT INTO users VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s)''', (user_id, user_firstname, user_lastname, user_username, chat_id, datatime, Lang, chat_and_user_INFO ,'IPOleksenko'))

    def phoneSeve(self, sender_user_id, phonenumber, user_id, first_name, last_name, vcard, datatime):
        allInfo = str(f"sender_user_id={sender_user_id} | phonenumber={phonenumber} | user_id={user_id} | first_name={first_name} | last_name={last_name} | vcard={vcard} | datatime={datatime}")
        try:
            self.cursor.execute('''DELETE FROM phone WHERE allInfo = %s''',(allInfo,))
        finally:
            self.cursor.execute('''INSERT INTO phone VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s)''', (sender_user_id, phonenumber, user_id, first_name, last_name, vcard, datatime, allInfo,'IPOleksenko'))

    def locationSeve(self, latitude, longitude, user_id, user_firstname, user_lastname, user_username, chat_id, time):
        allInfo = str(f"latitude={latitude} | longitude={longitude} | user_id={user_id} | user_firstname={user_firstname} | user_lastname={user_lastname} | user_username={user_username} | chat_id={chat_id} | time={time}")
        try:
            self.cursor.execute('''DELETE FROM location WHERE allInfo = %s''',(allInfo,))
        finally:
            self.cursor.execute('''INSERT INTO location VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)''', (latitude, longitude, user_id, user_firstname, user_lastname, user_username, chat_id, time, allInfo,'IPOleksenko'))

    def examination(self, user_id, chat_id):
        chat_and_user_INFO= str(f'user={user_id} | chat={chat_id}')
        self.cursor.execute('''SELECT user_id FROM users WHERE chat_and_user_INFO = %s''', (chat_and_user_INFO,))
        result = self.cursor.fetchone()
        return result or 'None'

    def select_lang(self, user_id):
        self.cursor.execute('''SELECT language FROM users WHERE user_id = %s''', (user_id,))
        result = self.cursor.fetchone()
        return result or 'en'

    def __del__(self):
        self.cursor.close()

Database_SQL = SQL()
#Author: IPOleksenko