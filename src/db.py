from psycopg2 import sql
import psycopg2

def connect_db():
    conn = psycopg2.connect(
        dbname="postgres", user="postgres", password="Andreevna54321", host="localhost", port="5432"
    )
    return conn