"""Скрипт для заполнения данными таблиц в БД Postgres."""
import csv
import psycopg2


def file_reader(path):
    with open(path, 'r') as csvfile:
        csvreader = csv.reader(csvfile)
        count = 0
        result = []
        for row in csvreader:
            if count == 0:
                count += 1
            else:
                result.append(row)
    return result


customers_data = file_reader('north_data/customers_data.csv')
employees_data = file_reader('north_data/employees_data.csv')
orders_data = file_reader('north_data/orders_data.csv')

try:
    with psycopg2.connect(host='localhost', database='north', user='postgres', password='12321') as conn:
        with conn.cursor() as cur:
            for customer in customers_data:
                cur.execute("INSERT INTO customers VALUES (%s, %s, %s)",
                            (customer[0], customer[1], customer[2]))
            for employee in employees_data:
                cur.execute("INSERT INTO employees VALUES (%s, %s, %s, %s, %s, %s)",
                            (employee[0], employee[1], employee[2], employee[3], employee[4], employee[5]))
            for order in orders_data:
                cur.execute("INSERT INTO orders VALUES (%s, %s, %s, %s, %s)",
                            (order[0], order[1], order[2], order[3], order[4]))
finally:
    conn.close()
