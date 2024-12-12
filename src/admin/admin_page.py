import streamlit as st
import pandas as pd
from db import connect_db

# Функция для получения данных из базы
def get_data_from_db(query):
    conn = connect_db()
    df = pd.read_sql(query, conn)
    conn.close()
    return df

# Функция для скачивания таблицы
def download_table(df, filename="data.csv"):
    csv = df.to_csv(index=False)
    st.download_button(
        label="Скачать таблицу",
        data=csv,
        file_name=filename,
        mime="text/csv",
    )

# Функция для выделения найденных значений красным
def highlight_search_results(val, search_term):
    if search_term.lower() in str(val).lower():
        return f'background-color: red; color: white;'
    return ''

# Страница "Пользователи"
def show_users_page():
    st.title("Пользователи")
    
    query = """
    SELECT user_id, login, name, surname, sex, phone_number
    FROM public.users
    """
    users_data = get_data_from_db(query)
    search_term = st.text_input("Поиск по пользователям", "")

    if search_term:
        styled_df = users_data.style.applymap(lambda val: highlight_search_results(val, search_term))
    else:
        styled_df = users_data
    
    st.dataframe(styled_df)
    download_table(users_data)

# Страница "Действия пользователей"
def show_user_actions_page():
    st.title("Действия пользователей")
    
    query = """
    SELECT action_id, order_id, user_id, action, time
    FROM public.user_actions
    """
    user_actions_data = get_data_from_db(query)
    search_term = st.text_input("Поиск по действиям пользователей", "")

    if search_term:
        styled_df = user_actions_data.style.applymap(lambda val: highlight_search_results(val, search_term))
    else:
        styled_df = user_actions_data
    
    st.dataframe(styled_df)
    download_table(user_actions_data)

# Страница "Размеры"
def show_sizes_page():
    st.title("Размеры")
    
    query = """
    SELECT size_id, size, price
    FROM public.sizes
    """
    sizes_data = get_data_from_db(query)
    search_term = st.text_input("Поиск по размерам", "")

    if search_term:
        styled_df = sizes_data.style.applymap(lambda val: highlight_search_results(val, search_term))
    else:
        styled_df = sizes_data
    
    st.dataframe(styled_df)
    download_table(sizes_data)

# Страница "Материалы"
def show_materials_page():
    st.title("Материалы")
    
    query = """
    SELECT material_id, material, price
    FROM public.materials
    """
    materials_data = get_data_from_db(query)
    search_term = st.text_input("Поиск по материалам", "")

    if search_term:
        styled_df = materials_data.style.applymap(lambda val: highlight_search_results(val, search_term))
    else:
        styled_df = materials_data
    
    st.dataframe(styled_df)
    download_table(materials_data)

# Страница "Диаметры"
def show_diameters_page():
    st.title("Диаметры")
    
    query = """
    SELECT diameter_id, diameter
    FROM public.diameters
    """
    diameters_data = get_data_from_db(query)
    search_term = st.text_input("Поиск по диаметрам", "")

    if search_term:
        styled_df = diameters_data.style.applymap(lambda val: highlight_search_results(val, search_term))
    else:
        styled_df = diameters_data
    
    st.dataframe(styled_df)
    download_table(diameters_data)

# Страница "Заказы"
def show_orders_page():
    st.title("Заказы")
    
    query = """
    SELECT order_id, size_id, material_id, quantity, diameter_id, total_cost
    FROM public.orders
    """
    orders_data = get_data_from_db(query)
    search_term = st.text_input("Поиск по заказам", "")

    if search_term:
        styled_df = orders_data.style.applymap(lambda val: highlight_search_results(val, search_term))
    else:
        styled_df = orders_data
    
    st.dataframe(styled_df)
    download_table(orders_data)

# Страница "Доставки"
def show_deliveries_page():
    st.title("Доставки")
    
    query = """
    SELECT delivery_id, order_id, address, delivery_time, delivery_cost, telephone
    FROM public.deliveries
    """
    deliveries_data = get_data_from_db(query)
    search_term = st.text_input("Поиск по доставкам", "")

    if search_term:
        styled_df = deliveries_data.style.applymap(lambda val: highlight_search_results(val, search_term))
    else:
        styled_df = deliveries_data
    
    st.dataframe(styled_df)
    download_table(deliveries_data)

def show_admin_page():
    st.sidebar.title("Меню")
    page = st.sidebar.radio("Выберите страницу", ("Пользователи", "Действия пользователей", "Заказы",  "Доставки", "Материалы", "Размеры", "Диаметры"))

    if page == "Диаметры":
        show_diameters_page()
    elif page == "Материалы":
        show_materials_page()
    elif page == "Размеры":
        show_sizes_page()
    elif page == "Пользователи":
        show_users_page()
    elif page == "Заказы":
        show_orders_page()
    elif page == "Действия пользователей":
        show_user_actions_page()
    elif page == "Доставки":
        show_deliveries_page()