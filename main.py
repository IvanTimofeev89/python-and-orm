import json
import sqlalchemy
from sqlalchemy.orm import Session
from sqlalchemy import Select
from config import DSN, echo
from models import create_tables
from models import Book, Publisher, Shop, Stock, Sale
from create_db import create_db

engine = sqlalchemy.create_engine(url=DSN, echo=echo)
create_tables(engine)
create_db()

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


def get_sales_info(session):
    name = input('Введите имя автора: ')
    print(f"Продажи по издателю {name}:")
    stmt = Select(Book.title, Shop.name, Sale.price, Sale.date_sale).where(
        Publisher.id == Book.id_publisher,
        Stock.id_book == Book.id,
        Stock.id == Sale.id_stock,
        Stock.id_shop == Shop.id,
        Publisher.name.icontains(f'{name}'))
    result = session.execute(stmt)
    for row in result:
        print(f"{row[0]:40} | {row[1]:10} | {row[2]} | {row[3]}")


with Session(engine) as session:
    db_filling(session=session, file_path='tests_data.json')
    print("Доступные имена издателей:O\u2019Reilly, Pearson, Microsoft Press, No starch press")
    get_sales_info(session=session)
