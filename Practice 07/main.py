import psycopg2
import csv
db_params = {
    "host": "localhost",
    "database": "postgres",
    "user": "postgres",
    "password": "mysecretpassword"
}

def create_table():
    query = """
    CREATE TABLE IF NOT EXISTS phonebook (
        id SERIAL PRIMARY KEY,
        first_name VARCHAR(50) NOT NULL,
        last_name VARCHAR(50),
        phone VARCHAR(20) UNIQUE NOT NULL
    );
    """
    with psycopg2.connect(**db_params) as conn:
        with conn.cursor() as cur:
            cur.execute(query)
            conn.commit()

def insert_from_csv(file_path):
    query = "INSERT INTO phonebook (first_name, last_name, phone) VALUES (%s, %s, %s) ON CONFLICT (phone) DO NOTHING"
    with psycopg2.connect(**db_params) as conn:
        with conn.cursor() as cur:
            with open(file_path, 'r') as f:
                reader = csv.reader(f)
                for row in reader:
                    cur.execute(query, row)
            conn.commit()
    print("Данные из CSV успешно загружены.")

def insert_from_console():
    f_name = input("Имя: ")
    l_name = input("Фамилия: ")
    phone = input("Телефон: ")
    
    query = "INSERT INTO phonebook (first_name, last_name, phone) VALUES (%s, %s, %s)"
    try:
        with psycopg2.connect(**db_params) as conn:
            with conn.cursor() as cur:
                cur.execute(query, (f_name, l_name, phone))
                conn.commit()
        print("Контакт добавлен.")
    except Exception as e:
        print(f"Ошибка: {e}")

def update_contact(phone, new_first_name):
    query = "UPDATE phonebook SET first_name = %s WHERE phone = %s"
    with psycopg2.connect(**db_params) as conn:
        with conn.cursor() as cur:
            cur.execute(query, (new_first_name, phone))
            print(f"Обновлено записей: {cur.rowcount}")

def delete_by_name_or_phone(identifier):
    query = "DELETE FROM phonebook WHERE first_name = %s OR phone = %s"
    with psycopg2.connect(**db_params) as conn:
        with conn.cursor() as cur:
            cur.execute(query, (identifier, identifier))
            print(f" Удалено записей: {cur.rowcount}")

def query_data(search_term=None):
    if search_term:
        query = "SELECT * FROM phonebook WHERE first_name ILIKE %s OR last_name ILIKE %s"
        params = (f"%{search_term}%", f"%{search_term}%")
    else:
        query = "SELECT * FROM phonebook"
        params = None

    with psycopg2.connect(**db_params) as conn:
        with conn.cursor() as cur:
            cur.execute(query, params)
            rows = cur.fetchall()
            print("\n--- Результаты поиска ---")
            for row in rows:
                print(f"ID: {row[0]} | {row[1]} {row[2]} | Тел: {row[3]}")
if __name__ == "__main__":
    create_table()

    #insert_from_csv('data.csv')
    insert_from_console()
    # update_contact('87010001122', 'Dmitry')
    query_data('Азамат')
    # delete_by_name_or_phone('Alice')
    
    query_data()
    #docker run --name postgres-db -e POSTGRES_PASSWORD=mysecretpassword -p 5432:5432 -d postgres