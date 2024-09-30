from sqlalchemy.orm import Session
from sqlalchemy import text

def clear_table(orm_table, engine):
    """
    Очищает данные из указанной таблицы и сбрасывает автоинкремент для этой таблицы в переданной базе данных.

    :param orm_table (Base): SQLAlchemy ORM-модель таблицы
    :param engine (Engine): SQLAlchemy engine
    """


    try:
        table_name_xx = orm_table.__tablename__

        with Session(bind=engine) as session:
            session.query(orm_table).delete()
            session.commit()

        with engine.connect() as connection:
            truncate_str = f"TRUNCATE TABLE {table_name_xx} RESTART IDENTITY"
            truncate_query = text(truncate_str)
            connection.execute(truncate_query)
            connection.commit()
    except Exception:
        return
