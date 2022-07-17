from aiogram.types import Message, User, Chat
import psycopg2 as pg
from psycopg2.extras import RealDictCursor
from psycopg2.sql import SQL, Literal
from config import DATABASE_URL


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
                    from_user json,
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
                    chat json,
                    created_at timestamp,
                    updated_at timestamp
                );
                CREATE TABLE IF NOT EXISTS messages (
                    "from" bigint references users(id),
                    forwarded_from json,
                    message_id bigint,
                    chat bigint references chats(id),
                    text varchar(4096),
                    dice json,
                    audio json,
                    document json,
                    photo json,
                    sticker json,
                    video json,
                    video_note json,
                    voice json,
                    contact json,
                    location json,
                    message json,
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
            chat = message.chat.as_json() if message.chat else None
            is_bot = message.from_user.is_bot
            first_name = message.from_user.first_name
            last_name = message.from_user.last_name
            username = message.from_user.username
            language_code = message.from_user.language_code
            from_user = message.from_user.as_json() if message.from_user else None
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
                    from_user,
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
                    {from_user},
                    now(),
                    now()
                ) ON CONFLICT (id) DO UPDATE
                SET
                    first_name = {first_name},
                    last_name = {last_name},
                    username = {username},
                    language_code = {language_code},
                    from_user = {from_user},
                    updated_at = now();
                INSERT INTO chats (
                    id,
                    first_name,
                    last_name,
                    title,
                    username,
                    users,
                    chat,
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
                    {chat},
                    now(),
                    now()
                ) ON CONFLICT (id) DO UPDATE
                SET
                    first_name = {first_name},
                    last_name = {last_name},
                    title = {title},
                    username = {username},
                    chat = {chat},
                    updated_at = now();
                UPDATE chats
                SET users = (SELECT array_agg(distinct e) FROM unnest(users || ARRAY[{user_id}]) e)
                WHERE NOT users @> ARRAY[CAST({user_id} AS BIGINT)] AND id = {chat_id}
            """
                ).format(
                    user_id=Literal(user_id),
                    chat_id=Literal(chat_id),
                    chat=Literal(chat),
                    is_bot=Literal(is_bot),
                    first_name=Literal(first_name),
                    last_name=Literal(last_name),
                    title=Literal(title),
                    username=Literal(username),
                    language_code=Literal(language_code),
                    from_user=Literal(from_user),
                )
            )

            return True

    def get_user(self, message: Message) -> User:
        if not isinstance(message, Message):
            raise TypeError("excepted Message, but got", type(message))

        with self.conn.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute(
                """SELECT * FROM users WHERE id = %s;""", (message.from_user.id,)
            )
            result = cursor.fetchone()
            del result["created_at"]
            del result["updated_at"]

            return User(**result)

    def get_users(self) -> set[User]:
        with self.conn.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute(
                """SELECT * FROM users;"""
            )
            result: list[dict] = cursor.fetchall()

            for i in range(len(result)):
                del result[i]["created_at"]
                del result[i]["updated_at"]

            return set(User(**user) for user in result)

    def get_chats(self) -> set[Chat]:
        with self.conn.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute(
                """SELECT * FROM chats;"""
            )
            result: list[dict] = cursor.fetchall()

            for i in range(len(result)):
                del result[i]["created_at"]
                del result[i]["updated_at"]

            return set(Chat(**chat) for chat in result)


    def save_message(self, message: Message) -> bool:
        if not isinstance(message, Message):
            raise TypeError("excepted Message, but got", type(message))

        with self.conn.cursor() as cursor:
            from_user = message.from_user.id
            forwarded_from = message.forward_from.as_json() if message.forward_from else None
            message_id = message.message_id if message.message_id else None
            date = message.date
            chat = message.chat.id
            text = message.caption if message.caption else message.text
            dice = message.dice.as_json() if message.dice else None
            audio = message.audio.as_json() if message.audio else None
            document = message.document.as_json() if message.document else None
            photo = message.photo[0].as_json() if message.photo else None
            sticker = message.sticker.as_json() if message.sticker else None
            video = message.video.as_json() if message.video else None
            video_note = message.video_note.as_json() if message.video_note else None
            voice = message.voice.as_json() if message.voice else None
            contact = message.contact.as_json() if message.contact else None
            location = message.location.as_json() if message.location else None
            message = message.as_json() if message else None

            cursor.execute(
                """
                INSERT INTO messages (
                    "from",
                    forwarded_from,
                    message_id,
                    chat,
                    text,
                    dice,
                    audio,
                    document,
                    photo,
                    sticker,
                    video,
                    video_note,
                    voice,
                    contact,
                    location,
                    message,
                    sended_at
                )
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, TIMESTAMP %s)
                ON CONFLICT DO NOTHING;
            """,
                (
                    from_user,
                    forwarded_from,
                    message_id,
                    chat,
                    text,
                    dice,
                    audio,
                    document,
                    photo,
                    sticker,
                    video,
                    video_note,
                    voice,
                    contact,
                    location,
                    message,
                    date,
                ),
            )

            return True

    #todo: add date of message
    def get_message(self, type: str) -> list[Message]:
        with self.conn.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute(
                """SELECT * FROM messages WHERE %s IS NOT NULL;""", (type,)
            )
            result: list[dict] = cursor.fetchall()
            users = { user.id: user for user in self.get_users() }

            for i in range(len(result)):
                del result[i]["sended_at"]
                result[i]["from"] = users[result[i]["from"]]

            return [Message(**message) for message in result]

db = Database(dsn=DATABASE_URL)