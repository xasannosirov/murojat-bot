import psycopg2
from psycopg2.extras import RealDictCursor
import os
from dotenv import load_dotenv

load_dotenv()
DB_URL = os.getenv('DB_URL')

def get_connection():
    return psycopg2.connect(DB_URL, cursor_factory=RealDictCursor)

def save_user(user_id, first_name, last_name, username, phone_number, language):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO users (id, first_name, last_name, username, phone_number, language)
        VALUES (%s, %s, %s, %s, %s, %s)
        ON CONFLICT (id) DO NOTHING;
    """, (user_id, first_name, last_name, username, phone_number, language))
    conn.commit()
    cur.close()
    conn.close()

def save_appeal(user_id, appeal_text, file_url=None):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO appeals (user_id, appeal_text, file_url)
        VALUES (%s, %s, %s);
    """, (user_id, appeal_text, file_url))
    conn.commit()
    cur.close()
    conn.close()

def get_appeals(user_id):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT id, appeal_text, file_url
        FROM appeals
        WHERE user_id = %s
        ORDER BY created_at DESC;
    """, (user_id,))
    appeals = cur.fetchall()
    cur.close()
    conn.close()
    return appeals

def get_user(user_id):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT id, first_name, last_name, username, phone_number, language
        FROM users
        WHERE id = %s;
    """, (user_id,))
    user = cur.fetchone()
    cur.close()
    conn.close()

    return user
