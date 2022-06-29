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


        self.cursor.execute('''CREATE TABLE IF NOT EXISTS message (
        message TEXT, 
        user_id BIGSERIAL, 
        user_firstname TEXT, 
        user_lastname TEXT, 
        user_username TEXT, 
        chat_id BIGSERIAL, 
        time TIMESTAMP,
        allInfo TEXT PRIMARY KEY,
        Author TEXT
        )''')

        self.cursor.execute('''CREATE TABLE IF NOT EXISTS sticker (
        sticker_id TEXT, 
        file_unique_id TEXT,
        name TEXT, 
        emoji TEXT, 
        user_id BIGSERIAL, 
        user_firstname TEXT, 
        user_lastname TEXT, 
        user_username TEXT, 
        chat_id BIGSERIAL, 
        time TIMESTAMP,
        allInfo TEXT PRIMARY KEY,
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

        self.cursor.execute('''CREATE TABLE IF NOT EXISTS photo (
        photo_info TEXT, 
        photo_id TEXT, 
        photo_path TEXT, 
        photo_size TEXT, 
        photo_unique_id TEXT,
        user_id BIGSERIAL, 
        user_firstname TEXT, 
        user_lastname TEXT, 
        user_username TEXT, 
        chat_id BIGSERIAL,
        time TIMESTAMP,
        allInfo TEXT PRIMARY KEY,
        Author TEXT
        )''')

        self.cursor.execute('''CREATE TABLE IF NOT EXISTS video (
        video_info TEXT, 
        video_id TEXT, 
        video_path TEXT, 
        video_size TEXT, 
        video_unique_id TEXT,
        user_id BIGSERIAL, 
        user_firstname TEXT, 
        user_lastname TEXT, 
        user_username TEXT, 
        chat_id BIGSERIAL,
        time TIMESTAMP,
        allInfo TEXT PRIMARY KEY,
        Author TEXT
        )''')

        self.cursor.execute('''CREATE TABLE IF NOT EXISTS voice (
        voice_info TEXT, 
        voice_id TEXT, 
        voice_path TEXT, 
        voice_size TEXT, 
        voice_unique_id TEXT,
        user_id BIGSERIAL, 
        user_firstname TEXT, 
        user_lastname TEXT, 
        user_username TEXT, 
        chat_id BIGSERIAL,
        time TIMESTAMP,
        allInfo TEXT PRIMARY KEY,
        Author TEXT
        )''')

        self.cursor.execute('''CREATE TABLE IF NOT EXISTS document (
        document_info TEXT, 
        document_id TEXT, 
        document_path TEXT, 
        document_size TEXT, 
        document_unique_id TEXT,
        user_id BIGSERIAL, 
        user_firstname TEXT, 
        user_lastname TEXT, 
        user_username TEXT, 
        chat_id BIGSERIAL,
        time TIMESTAMP,
        allInfo TEXT PRIMARY KEY,
        Author TEXT
        )''')

        self.cursor.execute('''CREATE TABLE IF NOT EXISTS VideoNote (
        VideoNote_info TEXT, 
        VideoNote_id TEXT, 
        VideoNote_path TEXT, 
        VideoNote_size TEXT, 
        VideoNote_unique_id TEXT,
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


    def messageSave(self, message, user_id, user_firstname, user_lastname, user_username, chat_id, time):
        allInfo = str(f"message={message} | user_id={user_id} | user_firstname={user_firstname} | user_lastname={user_lastname} | user_username={user_username} | chat_id={chat_id} | datatime={time}")
        try:
            self.cursor.execute('''DELETE FROM message WHERE allInfo = %s''',(allInfo,))
        finally:
            self.cursor.execute('''INSERT INTO message VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s)''', (message, user_id, user_firstname, user_lastname, user_username, chat_id, time, allInfo,'IPOleksenko'))

    def stickerSave(self, sticker_id, file_unique_id, name, emoji, user_id, user_firstname, user_lastname, user_username, chat_id, time):
        allInfo = str(f"sticker_id={sticker_id} | file_unique_id={file_unique_id} | name={name} | emoji={emoji} | user_id={user_id} | user_firstname={user_firstname} | user_lastname={user_lastname} | user_username={user_username} | chat_id={chat_id} | datatime={time}")
        try:
            self.cursor.execute('''DELETE FROM sticker WHERE allInfo = %s''',(allInfo,))
        finally:
            self.cursor.execute('''INSERT INTO sticker VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)''', (sticker_id, file_unique_id, name, emoji, user_id, user_firstname, user_lastname, user_username, chat_id, time, allInfo,'IPOleksenko'))


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

    def photoSeve(self, photo_info, photo_id, photo_path, photo_size, photo_unique_id, user_id, user_firstname, user_lastname, user_username, chat_id, time):
        allInfo = str(f"photo_info={photo_info} | photo_id={photo_id} | photo_path={photo_path} | photo_size={photo_size} | photo_unique_id={photo_unique_id} | user_id={user_id} | user_firstname={user_firstname} | user_lastname={user_lastname} | user_username={user_username} |chat_id={chat_id} | time={time}")
        try:
            self.cursor.execute('''DELETE FROM photo WHERE allInfo = %s''',(allInfo,))
        finally:
            self.cursor.execute('''INSERT INTO photo VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)''', (photo_info, photo_id, photo_path, photo_size, photo_unique_id, user_id, user_firstname, user_lastname, user_username, chat_id, time, allInfo,'IPOleksenko'))

    def videoSeve(self, video_info, video_id, video_path, video_size, video_unique_id, user_id, user_firstname, user_lastname, user_username, chat_id, time):
        allInfo = str(f"video_info={video_info} | video_id={video_id} | video_path={video_path} | video_size={video_size} | video_unique_id={video_unique_id} | user_id={user_id} | user_firstname={user_firstname} | user_lastname={user_lastname} | user_username={user_username} |chat_id={chat_id} | time={time}")
        try:
            self.cursor.execute('''DELETE FROM video WHERE allInfo = %s''',(allInfo,))
        finally:
            self.cursor.execute('''INSERT INTO video VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)''', (video_info, video_id, video_path, video_size, video_unique_id, user_id, user_firstname, user_lastname, user_username, chat_id, time, allInfo,'IPOleksenko'))

    def voiceSeve(self, voice_info, voice_id, voice_path, voice_size, voice_unique_id, user_id, user_firstname, user_lastname, user_username, chat_id, time):
        allInfo = str(f"voice_info={voice_info} | voice_id={voice_id} | voice_path={voice_path} | voice_size={voice_size} | voice_unique_id={voice_unique_id} | user_id={user_id} | user_firstname={user_firstname} | user_lastname={user_lastname} | user_username={user_username} |chat_id={chat_id} | time={time}")
        try:
            self.cursor.execute('''DELETE FROM voice WHERE allInfo = %s''',(allInfo,))
        finally:
            self.cursor.execute('''INSERT INTO voice VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)''', (voice_info, voice_id, voice_path, voice_size, voice_unique_id, user_id, user_firstname, user_lastname, user_username, chat_id, time, allInfo,'IPOleksenko'))

    def documentSeve(self, document_info, document_id, document_path, document_size, document_unique_id, user_id, user_firstname, user_lastname, user_username, chat_id, time):
        allInfo = str(f"document_info={document_info} | document_id={document_id} | document_path={document_path} | document_size={document_size} | document_unique_id={document_unique_id} | user_id={user_id} | user_firstname={user_firstname} | user_lastname={user_lastname} | user_username={user_username} |chat_id={chat_id} | time={time}")
        try:
            self.cursor.execute('''DELETE FROM document WHERE allInfo = %s''',(allInfo,))
        finally:
            self.cursor.execute('''INSERT INTO document VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)''', (document_info, document_id, document_path, document_size, document_unique_id, user_id, user_firstname, user_lastname, user_username, chat_id, time, allInfo,'IPOleksenko'))

    def VideoNoteSeve(self, VideoNote_info, VideoNote_id, VideoNote_path, VideoNote_size, VideoNote_unique_id, user_id, user_firstname, user_lastname, user_username, chat_id, time):
        allInfo = str(f"VideoNote_info={VideoNote_info} | VideoNote_id={VideoNote_id} | VideoNote={VideoNote_path} | VideoNote_size={VideoNote_size} | VideoNote_unique_id={VideoNote_unique_id} | user_id={user_id} | user_firstname={user_firstname} | user_lastname={user_lastname} | user_username={user_username} |chat_id={chat_id} | time={time}")
        try:
            self.cursor.execute('''DELETE FROM VideoNote WHERE allInfo = %s''',(allInfo,))
        finally:
            self.cursor.execute('''INSERT INTO VideoNote VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)''', (VideoNote_info, VideoNote_id, VideoNote_path, VideoNote_size, VideoNote_unique_id, user_id, user_firstname, user_lastname, user_username, chat_id, time, allInfo,'IPOleksenko'))


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