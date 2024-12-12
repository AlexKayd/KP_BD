import streamlit as st
from datetime import datetime
from datetime import time
from db import connect_db

def show_delivery_page():
    order = st.session_state.order_data
    st.write(f"Вы заказали: ")
    st.write(f"-- Размер этикеток: {order['size']}")
    st.write(f"-- Материал этикеток: {order['material']}")
    st.write(f"-- Количество этикеток: {order['quantity']}")
    st.write(f"-- Размер втулки: {order['diameter']}")
    st.write(f"Стоимость заказа: {order['total_cost']} рублей")

    delivery_cost = 1000 if order['total_cost'] < 10000 else 0
    
    if delivery_cost == 0:
        st.write(f"Бесплатная доставка")
    else:
        st.write(f"Стоимость доставки: {delivery_cost} рублей. (Бесплатная доставка при заказе от 10000 рублей)")
    st.write(f"Общая стоимость заказа: {order['total_cost'] + delivery_cost} рублей")
    address = st.text_input("Адрес доставки")
    delivery1 = st.date_input("Дата доставки", min_value=datetime.today())
    min_time = time(10, 0)
    max_time = time(22, 0)
    delivery2 = st.time_input("Время доставки", value=time(10, 0))

    if delivery2 < min_time or delivery2 > max_time:
        st.error(f"Выберите время в пределах от {min_time} до {max_time}")
    delivery_time = datetime.combine(delivery1, delivery2)
    phone_number = st.text_input("Контактный номер телефона")
    st.write("**Оплата при получении")

    st.session_state.order_placed = False

    if not st.session_state.order_placed:
        if st.button("Заказать"):
            if address and phone_number:
                if len(phone_number) == 11 and phone_number.isdigit():
                    try:
                        conn = connect_db()
                        cur = conn.cursor()

                        cur.execute(
                            """
                            INSERT INTO orders (size_id, material_id, quantity, diameter_id, total_cost)
                            VALUES (%s, %s, %s, %s, %s) RETURNING order_id
                            """,
                            (
                                order['size_id'],
                                order['material_id'],
                                order['quantity'],
                                order['diameter_id'],
                                order['total_cost']
                            )
                        )
                        order_id = cur.fetchone()[0]

                        cur.execute(
                            """
                            INSERT INTO deliveries (order_id, address, delivery_time, delivery_cost, telephone)
                            VALUES (%s, %s, %s, %s, %s)
                            """,
                            (
                                order_id,
                                address,
                                delivery_time,
                                delivery_cost,
                                phone_number
                            )
                        )

                        cur.execute(
                            """
                            INSERT INTO user_actions (order_id, user_id, action)
                            VALUES (%s, %s, %s)
                            """,
                            (
                                order_id,
                                st.session_state.user_id,
                                "активный"
                            )
                        )

                        conn.commit()
                        st.success(f"Заказ {order_id} оформлен. Спасибо за покупку!")
                        st.session_state.page = "buy"
                        st.session_state.order_placed = True 
                        if st.button("Вернуться к покупкам"):
                            st.success()
                    except Exception as e:
                        st.error(f"Ошибка при сохранении данных: {e}")
                    finally:
                        cur.close()
                        conn.close()
                else:
                    st.error("Некорректный номер телефона.")
            else:
                st.error("Заполните все поля!")

    if not st.session_state.order_placed:
        if st.button("Отменить заказ"):
            st.success("Вы отменили заказ")
            st.session_state.page = "buy"
            st.session_state.order_placed = True
            if st.button("Вернуться к покупкам"):
                st.success()