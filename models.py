from sqlalchemy.orm import DeclarativeBase
from sqlalchemy import Column, Integer, String, ForeignKey, Date, Numeric
from sqlalchemy.orm import relationship


class Base(DeclarativeBase):
    pass


class Publisher(Base):
    __tablename__ = 'publisher'

    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False)

    publisher_book = relationship("Book", back_populates='book_publisher')


class Book(Base):
    __tablename__ = 'book'

    id = Column(Integer, primary_key=True)
    title = Column(String(150), nullable=False)
    id_publisher = Column(Integer, ForeignKey('publisher.id'))

    book_publisher = relationship("Publisher", back_populates='publisher_book')
    book_stock = relationship("Stock", back_populates='stock_book')


class Shop(Base):
    __tablename__ = 'shop'

    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False)

    shop_stock = relationship("Stock", back_populates='stock_shop')


class Stock(Base):
    __tablename__ = 'stock'

    id = Column(Integer, primary_key=True)
    id_book = Column(Integer, ForeignKey('book.id'))
    id_shop = Column(Integer, ForeignKey('shop.id'))
    count = Column(Integer, nullable=False)

    stock_book = relationship("Book", back_populates='book_stock')
    stock_shop = relationship("Shop", back_populates='shop_stock')
    stock_sale = relationship("Sale", back_populates='sale_stock')


class Sale(Base):
    __tablename__ = 'sale'

    id = Column(Integer, primary_key=True)
    price = Column(Numeric(8, 2), nullable=False)
    date_sale = Column(Date, nullable=False)
    id_stock = Column(Integer, ForeignKey('stock.id'))
    count = Column(Integer, nullable=False)

    sale_stock = relationship("Stock", back_populates='stock_sale')


def create_tables(engine):
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
