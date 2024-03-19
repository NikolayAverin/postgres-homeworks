import json

import psycopg2

from config import config


def main():
    script_file = 'fill_db.sql'
    json_file = 'suppliers.json'
    db_name = 'my_new_db'

    params = config()
    conn = None

    create_database(params, db_name)
    print(f"БД {db_name} успешно создана")

    params.update({'dbname': db_name})
    try:
        with psycopg2.connect(**params) as conn:
            with conn.cursor() as cur:
                execute_sql_script(cur, script_file)
                print(f"БД {db_name} успешно заполнена")

                create_suppliers_table(cur)
                print("Таблица suppliers успешно создана")

                suppliers = get_suppliers_data(json_file)
                insert_suppliers_data(cur, suppliers)
                print("Данные в suppliers успешно добавлены")

                add_foreign_keys(cur, suppliers)
                print(f"FOREIGN KEY успешно добавлены")

    except(Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()


def create_database(params, db_name) -> None:
    """Создает новую базу данных."""
    conn = psycopg2.connect(dbname='postgres', **params)
    conn.autocommit = True

    cur = conn.cursor()
    cur.execute(f"DROP DATABASE IF EXISTS {db_name}")
    cur.execute(f"CREATE DATABASE {db_name}")
    conn.close()


def execute_sql_script(cur, script_file) -> None:
    """Выполняет скрипт из файла для заполнения БД данными."""
    with open(script_file) as file:
        data = file.read()
        cur.execute(f"{data}")


def create_suppliers_table(cur) -> None:
    """Создает таблицу suppliers."""
    cur.execute("CREATE TABLE suppliers ("
                "supplier_id serial PRIMARY KEY,"
                "company_name varchar(100) NOT NULL,"
                "contact varchar(100) NOT NULL,"
                "address varchar(100) NOT NULL,"
                "phone varchar(24) NOT NULL,"
                "fax varchar(24),"
                "homepage text)")


def get_suppliers_data(json_file: str) -> list[dict]:
    """Извлекает данные о поставщиках из JSON-файла и возвращает список словарей с соответствующей информацией."""
    with open('suppliers.json') as file:
        suppliers_json = json.load(file)
    return suppliers_json


def insert_suppliers_data(cur, suppliers: list[dict]) -> None:
    """Добавляет данные из suppliers в таблицу suppliers."""
    for supplier in suppliers:
        cur.execute("INSERT INTO suppliers (company_name, contact, address, phone, fax, homepage) "
                    "VALUES (%s, %s, %s, %s, %s, %s)",
                    (supplier['company_name'], supplier['contact'], supplier['address'],
                     supplier['phone'], supplier['fax'], supplier['homepage']))


def add_foreign_keys(cur, suppliers) -> None:
    """Добавляет foreign key со ссылкой на supplier_id в таблицу products."""
    cur.execute("ALTER TABLE products ADD COLUMN supplier_id integer")
    for supplier in suppliers:
        formatted_company_name = ''
        for name_symbol in supplier['company_name']:
            if name_symbol == "'":
                name_symbol = "''"
                formatted_company_name += name_symbol
            else:
                formatted_company_name += name_symbol
        supplier['company_name'] = formatted_company_name
        for product in supplier['products']:
            formatted_product = ''
            for product_symbol in product:
                if product_symbol == "'":
                    product_symbol = "''"
                    formatted_product += product_symbol
                else:
                    formatted_product += product_symbol
            supplier['products'] = formatted_product
            cur.execute("UPDATE products SET supplier_id = "
                        "(SELECT supplier_id FROM suppliers "
                        f"WHERE company_name = '{supplier['company_name']}')"
                        f"WHERE product_name = '{supplier['products']}'")
    cur.execute("ALTER TABLE products ADD CONSTRAINT fk_products_suppliers "
                "FOREIGN KEY(supplier_id) REFERENCES suppliers(supplier_id)")


if __name__ == '__main__':
    main()
