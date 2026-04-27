import psycopg2
import csv
from connect import get_connection

def insert_from_console():
    f_name = input("Имя: ")
    l_name = input("Фамилия: ")
    phone = input("Телефон: ")
    
    try:
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("CALL upsert_contact(%s, %s, %s)", (f_name, l_name, phone))
                conn.commit()
        print("Контакт обработан (добавлен или обновлен).")
    except Exception as e:
        print(f"Ошибка: {e}")

def delete_by_name_or_phone(identifier):
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("CALL delete_contact_proc(%s)", (identifier,))
            conn.commit()
            print(f"Запрос на удаление '{identifier}' выполнен.")

def query_data(search_term=None):
    with get_connection() as conn:
        with conn.cursor() as cur:
            if search_term:
                cur.execute("SELECT * FROM get_contacts_by_pattern(%s)", (search_term,))
            else:
                cur.execute("SELECT * FROM phonebook")
            
            rows = cur.fetchall()
            print(f"\n--- Результаты ({search_term if search_term else 'Все'}) ---")
            for row in rows:
                print(f"ID: {row[0]} | {row[1]} {row[2]} | Тел: {row[3]}")

def get_paginated(limit, offset):
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT * FROM get_contacts_paginated(%s, %s)", (limit, offset))
            return cur.fetchall()

def bulk_insert_test():
    fnames = ['Aleksey', 'Mariya', 'WrongNum']
    lnames = ['Petrov', 'Ivanova', 'Test']
    phones = ['87071234567', '87479998877', '123']
    
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("CALL bulk_insert_with_validation(%s, %s, %s, NULL)", (fnames, lnames, phones))
            errors = cur.fetchone()[0]
            if errors:
                print("Ошибки вставки:", errors)
        conn.commit()

def get_contacts_by_pattern(pattern):
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT * FROM get_contacts_by_pattern(%s)", (pattern,))
            rows = cur.fetchall()
            print(rows)
            return rows

def delete_contact_proc(identifier):
    delete_by_name_or_phone(identifier)

if __name__ == "__main__":
    #insert_from_console()
    bulk_insert_test()
    query_data('8707')
    get_contacts_by_pattern('Aleksey')
    delete_contact_proc('')
    print("\nПагинация (первые 2 записи):")
    for contact in get_paginated(2, 0):
        print(contact)