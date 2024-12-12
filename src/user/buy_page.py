import streamlit as st
from db import connect_db

def show_buy_page():
    st.title("Страница покупки")
    
    # Получаем доступные размеры из базы данных
    conn = connect_db()
    cur = conn.cursor()
    cur.execute("SELECT size_id, size, price FROM sizes")
    sizes = cur.fetchall()
    size_options = {size[1]: (size[0], size[2]) for size in sizes}

    # Получаем доступные материалы из базы данных
    cur.execute("SELECT material_id, material, price FROM materials")
    materials = cur.fetchall()
    material_options = {material[1]: (material[0], material[2]) for material in materials}

    # Получаем доступные диаметры из базы данных
    cur.execute("SELECT diameter_id, diameter FROM diameters")
    diameters = cur.fetchall()
    diameter_options = {diameter[1]: diameter[0] for diameter in diameters}

    size = st.selectbox("Выберите размер этикетки", list(size_options.keys()))
    material = st.selectbox("Выберите материал этикетки", list(material_options.keys()))
    quantity = st.number_input("Количество этикеток", min_value=1, step=1)
    diameter = st.selectbox("Выберите размер втулки", list(diameter_options.keys()))

    if size and material and diameter and quantity:
        size_id, size_price = size_options[size]
        material_id, material_price = material_options[material]
        diameter_id = diameter_options[diameter]
        
        order_cost =  round(size_price * material_price * quantity, 2)
        st.write(f"Стоимость заказа: {order_cost} рублей")

    if st.button("Подтвердить выбор"):
        st.session_state.order_data = {
            "size": size,
            "material": material,
            "diameter": diameter,
            "quantity": quantity,
            "size_id": size_id,
            "material_id": material_id,
            "diameter_id": diameter_id,
            "total_cost": order_cost
        }

        st.write(f"Размер этикеток: {size}")
        st.write(f"Материал этикеток: {material}")
        st.write(f"Количество этикеток: {quantity}")
        st.write(f"Размер втулки: {diameter}")
        st.write(f"Стоимость заказа: {order_cost} рублей")
        st.session_state.page = "delivery"
        if st.button("Оформить доставку"):
            st.success()