import streamlit as st
from enter import authenticate_user, register_user, authenticate_admin
from user.user_page import show_user_page
from admin.admin_page import show_admin_page

st.set_page_config(page_title="Магазин этикеток", layout="wide")

def main():
    if 'logged_admin_in' in st.session_state and st.session_state.logged_admin_in:
        show_admin_page()

    elif 'logged_in' in st.session_state and st.session_state.logged_in:
        show_user_page()
    
    else:
        st.title("Магазин этикеток")
        page = st.sidebar.radio("Выберите действие:", ["Регистрация", "Вход", "Вход для администратора"])

        if page == "Вход":
            st.subheader("Введите свои данные для входа")

            login = st.text_input("Логин")
            password = st.text_input("Пароль", type="password")

            if st.button("Проверить"):
                result = authenticate_user(login, password)
                if "Добро пожаловать" in result:
                    st.session_state.logged_in = True
                    st.success(result)
                    if st.button("Нажмите для входа"):
                        st.success(result)
                else:
                    st.error(result)
        
        elif page == "Регистрация":
            st.subheader("Регистрация нового пользователя")

            login = st.text_input("Логин")
            password = st.text_input("Пароль", type="password")
            name = st.text_input("Имя")
            surname = st.text_input("Фамилия")
            sex = st.selectbox("Пол", ["Мужчина", "Женщина"])
            phone_number = st.text_input("Номер телефона")

            if st.button("Зарегистрироваться"):
                result = register_user(login, password, name, surname, sex, phone_number)
                if "успешна" in result:
                    st.success(result)
                else:
                    st.error(result)
        elif page == "Вход для администратора":
            st.subheader("Введите свои данные для входа")

            login = st.text_input("Логин")
            password = st.text_input("Пароль", type="password")

            if st.button("Проверить"):
                result = authenticate_admin(login, password)
                if "Добро пожаловать" in result:
                    st.session_state.logged_admin_in = True
                    st.success(result)
                    if st.button("Нажмите для входа"):
                        st.success(result)
                else:
                    st.error(result)

if __name__ == "__main__":
    main()