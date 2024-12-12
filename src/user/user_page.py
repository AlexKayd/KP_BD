import streamlit as st
from user.buy_page import show_buy_page
from user.orders_page import show_orders_page
from user.delivery_page import show_delivery_page

def show_user_page():
    if 'page' not in st.session_state:
        st.session_state.page = 'buy'
    st.sidebar.title("Меню")
    menu = st.sidebar.radio("Выберите страницу", ["Купить", "Мои заказы"])

    if menu == "Купить":
        if st.session_state.page == "buy":
            show_buy_page()
        elif st.session_state.page == "delivery":
            show_delivery_page()
        
    elif menu == "Мои заказы":
        show_orders_page()
