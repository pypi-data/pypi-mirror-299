import psycopg2
import pandas as pd
from sqlalchemy import create_engine


def create_table_and_insert():

    engine = create_engine(f'{config.DATABASE_URI}', echo=False)
    df = pd.read_csv('shopItems_default.csv', delimiter=';', index_col='id') #todo заменить названия csv и delimiter на параметры
    df.to_sql('shop_items', engine)
    print(df)


def add_columns_if_not_exists(input_csv_file):
    conn = psycopg2.connect(database=config.POSTGRES_DBNAME,
                            user=config.POSTGRES_USERNAME,
                            password=config.POSTGRES_PASSWORD,
                            host=config.POSTGRES_HOST,
                            port=config.POSTGRES_PORT)
    cursor = conn.cursor()

    df = pd.read_excel(input_csv_file)

    # Объединение заголовков столбцов с разделением табуляцией
    headers_combined = ','.join(df.columns)

    # Объединение данных в один столбец с разделением табуляцией
    data_combined = df.apply(lambda x: ','.join([str(i) for i in x]), axis=1)

    # Запись заголовков и объединенных данных в CSV файл
    with open('output.csv', 'w', encoding='utf-8') as f:
        f.write(headers_combined + '\n')  # Записываем заголовки
        for row in data_combined:
            f.write(row + '\n')

    df = pd.read_csv('output.csv')

    # Получение списка столбцов из CSV файла
    csv_columns = df.columns.tolist()

    # Получение списка столбцов из таблицы в базе данных
    table_name = "test_p4"
    cursor.execute(f"SELECT column_name FROM information_schema.columns WHERE table_name = '{table_name}';")
    table_columns = [row[0] for row in cursor.fetchall()]

    # Проверка наличия столбцев из CSV файла в таблице и добавление их при необходимости
    for column in csv_columns:
        if column not in table_columns:
            data_type = "bigint"  # Замените на соответствующий тип данных
            query = f'ALTER TABLE {table_name} ADD COLUMN "{column}" {data_type};'
            cursor.execute(query)
            conn.commit()
            print(f"Столбец '{column}' успешно добавлен в таблицу '{table_name}'.")

    with open('output.csv', 'r') as file:
        cursor.copy_expert(f"COPY test_p4 from STDIN WITH CSV HEADER", file)   #TODO test_p4 - название таблицы, лежит в переменной table_name
        conn.commit()

    cursor.close()
    conn.close()