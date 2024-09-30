from sqlalchemy import select

def download_table(user_class, engine):
    """
    Функция для скачки всей таблицы из БД

    :param user_class: класс таблицы из которой нужно скачать данные
    :param engine: SQLAlchemy engine
    :return: rows
    """

    stmt = select(user_class)
    try:
        with engine.connect() as conn:
            query = conn.execute(stmt)
    except Exception as e:
        print(e)
    return query
