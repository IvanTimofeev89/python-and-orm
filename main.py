import json

import sqlalchemy
from sqlalchemy.orm import Session

from config import DSN, echo
from models import create_tables
from models import Book, Publisher, Shop, Stock, Sale
from create_db import create_db

engine = sqlalchemy.create_engine(url=DSN, echo=echo)
create_tables(engine)


def db_filling(session, file_path: str):
    with open(f'{file_path}', 'r') as fd:
        data = json.load(fd)

        for record in data:
            model = {
                'publisher': Publisher,
                'shop': Shop,
                'book': Book,
                'stock': Stock,
                'sale': Sale,
            }[record.get('model')]
            session.add(model(id=record.get('pk'), **record.get('fields')))
        session.commit()


def get_sales_info(session, user_input):
    stmt = session.query(Book.title, Shop.name, Sale.price, Sale.date_sale).\
        select_from(Shop).\
        join(Stock).\
        join(Book).\
        join(Publisher).\
        join(Sale)
    if user_input.isdigit():
        stmt = stmt.filter(Publisher.id == user_input).all()
    else:
        stmt = stmt.filter(Publisher.name == user_input).all()
    for row in stmt:
        print(f"{row[0]: <40} | {row[1]: <10} | {row[2]: <8} | {row[3].strftime('%d-%m-%Y')}")


if __name__ == '__main__':
    with Session(engine) as session:
        create_db()
        db_filling(session=session, file_path='tests_data.json')
        print("Доступные имена и id издателей:1 - O\u2019Reilly, 2 - Pearson, 3 - Microsoft Press, 4 - No starch press")
        user_input = input('Введите имя или id автора: ')
        get_sales_info(session=session, user_input=user_input)
