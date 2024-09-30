from sqlalchemy.orm import Session

def upload_table(engine, data):
    """
    Выгружает даннные в таблицу, соответствующую классу объектов в списке data.

    :param engine: SQLAlchemy engine
    :param data: список объектов
    """

    try:
        with Session(bind=engine) as session:
            for obj in data:
                session.add(obj)
            session.commit()
    except Exception as e:
        print(e)
