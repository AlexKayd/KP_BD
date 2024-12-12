import streamlit as st
import bcrypt
from db import connect_db

# Хеширование пароля
def hash_password(password):
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

# Проверка пароля пользователя
def authenticate_user(login, password):
    conn = connect_db()
    cur = conn.cursor()
    
    cur.execute("SELECT user_id, password_hash, name FROM users WHERE login = %s", (login,))
    user = cur.fetchone()
    
    if user is None:
        cur.close()
        conn.close()
        return "Пользователь с таким логином не найден."
    
    stored_password_hash = user[1]
    user_name = user[2]
    
    if isinstance(stored_password_hash, memoryview):
        stored_password_hash = bytes(stored_password_hash)

    if bcrypt.checkpw(password.encode('utf-8'), stored_password_hash):
        st.session_state.user_id = user[0]
        cur.close()
        conn.close()
        return f"Добро пожаловать, {user_name}!"
    else:
        cur.close()
        conn.close()
        return "Неверный пароль."

# Проверка пароля админа
def authenticate_admin(login, password):
    conn = connect_db()
    cur = conn.cursor()
    
    cur.execute("SELECT admin_id, password, name FROM admins WHERE login = %s", (login,))
    admin = cur.fetchone()
    
    if admin is None:
        cur.close()
        conn.close()
        return "Администратор с таким логином не найден."
    
    stored_password = admin[1]
    admin_name = admin[2]

    if int(password) == int(stored_password):
        st.session_state.admin_id = admin[0]
        cur.close()
        conn.close()
        return f"Добро пожаловать, {admin_name}!"
    else:
        cur.close()
        conn.close()
        return "Неверный пароль."

# Регистрация нового пользователя
def register_user(login, password, name, surname, sex, phone_number):
    if not all([login, password, name, surname, sex, phone_number]):
        return "Заполните все поля."
    
    if len(phone_number) != 11 or not phone_number.isdigit():
        return "Некорректный номер телефона."
    
    conn = connect_db()
    cur = conn.cursor()

    cur.execute("SELECT login FROM users WHERE login = %s", (login,))
    if cur.fetchone():
        cur.close()
        conn.close()
        return "Логин уже используется."

    cur.execute("SELECT phone_number FROM users WHERE phone_number = %s", (phone_number,))
    if cur.fetchone():
        cur.close()
        conn.close()
        return "Номер телефона уже используется."

    password_hash = hash_password(password)

    cur.execute(
        "INSERT INTO users (login, password_hash, name, surname, sex, phone_number) VALUES (%s, %s, %s, %s, %s, %s)",
        (login, password_hash, name, surname, sex, phone_number),
    )
    conn.commit()
    cur.close()
    conn.close()
    return "Регистрация успешна."