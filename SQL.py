from aiogram.types import Message, User
import psycopg2 as pg
from psycopg2.extras import RealDictCursor
from psycopg2.sql import SQL, Literal

class Database:
    def __init__(self, dsn: str = None, **kwargs):
        self.conn = pg.connect(
            dsn,
            keepalives=1,
            keepalives_idle=30,
            keepalives_interval=10,
            keepalives_count=5,
            **kwargs
        )
        self.conn.autocommit = True

        with self.conn.cursor() as cursor:
            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS users (
                    id bigint not null unique primary key,
                    is_bot boolean,
                    first_name varchar(64),
                    last_name varchar(64),
                    username varchar(64) unique,
                    language_code varchar(3),
                    created_at timestamp,
                    updated_at timestamp
                );
                CREATE TABLE IF NOT EXISTS chats (
                    id bigint not null unique primary key,
                    first_name varchar(64),
                    last_name varchar(64),
                    title varchar(64),
                    username varchar(64),
                    users bigint[] default '{}',
                    created_at timestamp,
                    updated_at timestamp
                );
                CREATE TABLE IF NOT EXISTS messages (
                    "from" bigint references users(id),
                    chat bigint references chats(id),
                    text varchar(4096),
                    audio json,
                    document json,
                    photo json,
                    sticker json,
                    video json,
                    video_note json,
                    voice json,
                    contact json,
                    location json,
                    sended_at timestamp
                );
            """
            )

    def update_user(self, message: Message) -> bool:
        if not isinstance(message, Message):
            raise TypeError("excepted Message, but got", type(message))

        with self.conn.cursor() as cursor:
            user_id = message.from_user.id
            chat_id = message.chat.id
            is_bot = message.from_user.is_bot
            first_name = message.from_user.first_name
            last_name = message.from_user.last_name
            username = message.from_user.username
            language_code = message.from_user.language_code
            title = message.chat.title

            cursor.execute(
                SQL(
                    """
                INSERT INTO users (
                    id,
                    is_bot,
                    first_name,
                    last_name,
                    username,
                    language_code,
                    created_at,
                    updated_at
                )
                VALUES (
                    {user_id},
                    {is_bot},
                    {first_name},
                    {last_name},
                    {username},
                    {language_code},
                    now(),
                    now()
                ) ON CONFLICT (id) DO UPDATE SET
                    first_name = {first_name},
                    last_name = {last_name},
                    username = {username},
                    language_code = {language_code},
                    updated_at = now();
                INSERT INTO chats as c (
                    id,
                    first_name,
                    last_name,
                    title,
                    username,
                    users,
                    created_at,
                    updated_at
                )
                VALUES (
                    {chat_id},
                    {first_name},
                    {last_name},
                    {title},
                    {username},
                    ARRAY[{user_id}],
                    now(),
                    now()
                ) ON CONFLICT (id) DO UPDATE SET
                    first_name = {first_name},
                    last_name = {last_name},
                    title = {title},
                    username = {username},
                    users = array_append(c.users, {user_id}),
                    updated_at = now();
            """
                ).format(
                    user_id=Literal(user_id),
                    chat_id=Literal(chat_id),
                    is_bot=Literal(is_bot),
                    first_name=Literal(first_name),
                    last_name=Literal(last_name),
                    title=Literal(title),
                    username=Literal(username),
                    language_code=Literal(language_code),
                )
            )

            return True

    def get_user(self, message: Message) -> User:
        if not isinstance(message, Message):
            raise TypeError("excepted Message, but got", type(message))

        with self.conn.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute(
                """SELECT * FROM users WHERE id = %s""", (message.from_user.id,)
            )
            result = cursor.fetchone()
            del result["created_at"]
            del result["updated_at"]

            return User(**result)

    def save_message(self, message: Message) -> bool:
        if not isinstance(message, Message):
            raise TypeError("excepted Message, but got", type(message))

        with self.conn.cursor() as cursor:
            from_user = message.from_user.id
            date = message.date.date()
            chat = message.chat.id
            text = message.caption if message.caption else message.text
            audio = message.audio.as_json() if message.audio else None
            document = message.document.as_json() if message.document else None
            photo = message.photo[0].as_json() if message.photo else None
            sticker = message.sticker.as_json() if message.sticker else None
            video = message.video.as_json() if message.video else None
            video_note = message.video_note.as_json() if message.video_note else None
            voice = message.voice.as_json() if message.voice else None
            contact = message.contact.as_json() if message.contact else None
            location = message.location.as_json() if message.location else None

            cursor.execute(
                """
                INSERT INTO messages (
                    "from",
                    chat,
                    text,
                    audio,
                    document,
                    photo,
                    sticker,
                    video,
                    video_note,
                    voice,
                    contact,
                    location,
                    sended_at
                )
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, TIMESTAMP %s)
                ON CONFLICT DO NOTHING;
            """,
                (
                    from_user,
                    chat,
                    text,
                    audio,
                    document,
                    photo,
                    sticker,
                    video,
                    video_note,
                    voice,
                    contact,
                    location,
                    date,
                ),
            )

            return True

#Author: IPOleksenko