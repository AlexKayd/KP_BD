import streamlit as st
from db import connect_db

def show_orders_page():
    st.title("Мои заказы")

    # Функция для получения текстового значения материала, размера, диаметра по ID
    def get_value_by_id(table_name, column_name, id_column, id_value):
        conn = connect_db()
        cur = conn.cursor()
        cur.execute(
            f"SELECT {column_name} FROM {table_name} WHERE {id_column} = %s",
            (id_value,)
        )
        result = cur.fetchone()
        cur.close()
        conn.close()
        return result[0] if result else "Не указано"

    user_id = st.session_state.get('user_id')
    conn = connect_db()
    cur = conn.cursor()

    # Получаем все заказы текущего пользователя
    cur.execute("""
        SELECT order_id, size_id, material_id, quantity, diameter_id, total_cost 
        FROM orders 
        WHERE order_id IN (
            SELECT order_id 
            FROM user_actions 
            WHERE user_id = %s
        )
        ORDER BY order_id DESC
    """, (user_id,))
    
    orders = cur.fetchall()

    if not orders:
        st.write("У вас нет заказов.")
    else:
        for order in orders:
            order_id, size_id, material_id, quantity, diameter_id, total_cost = order
            
            size_name = get_value_by_id("sizes", "size", "size_id", size_id)
            material_name = get_value_by_id("materials", "material", "material_id", material_id)
            diameter_name = get_value_by_id("diameters", "diameter", "diameter_id", diameter_id)

            # Получаем статус последнего действия заказа
            cur.execute("""
                SELECT action FROM user_actions 
                WHERE order_id = %s 
                ORDER BY time DESC LIMIT 1
            """, (order_id,))
            action = cur.fetchone()[0]
            
            # Получаем информацию о доставке заказа
            cur.execute("""
                SELECT address, delivery_time, delivery_cost, telephone 
                FROM deliveries 
                WHERE order_id = %s
            """, (order_id,))
            delivery = cur.fetchone()
            
            if delivery:
                address, delivery_time, delivery_cost, telephone = delivery
            else:
                address, delivery_time, delivery_cost, telephone = ("Не указано", "Не указано", 0, "Не указан")
            
            # Выводим информацию о заказе
            st.write(f"## Заказ {order_id}")
            if action.lower() == "активный":
                st.markdown(f"Статус заказа: <span style='color: green;'>{action}</span>", unsafe_allow_html=True)
            else:
                st.markdown(f"Статус заказа: <span style='color: red;'>{action}</span>", unsafe_allow_html=True)
                
            st.write(f"Размер: {size_name}")
            st.write(f"Материал: {material_name}")
            st.write(f"Диаметр втулки: {diameter_name}")
            st.write(f"Количество этикеток: {quantity}")
            st.write(f"Стоимость заказа: {total_cost} рублей")
            st.write(f"### Доставка:")
            st.write(f"Адрес доставки: {address}")
            st.write(f"Время доставки: {delivery_time}")
            st.write(f"Стоимость доставки: {delivery_cost} рублей")
            st.write(f"Контактный номер: {telephone}")
            
            if action.lower() == "активный":
                if st.button(f"Отменить заказ {order_id}"):
                    cur.execute("""
                        INSERT INTO user_actions (order_id, user_id, action) VALUES (%s, %s, 'отменен')
                    """, (order_id, user_id))
                    conn.commit()
                    
                    st.success(f"Заказ {order_id} отменен.")
            st.write("---")
    
    cur.close()
    conn.close()