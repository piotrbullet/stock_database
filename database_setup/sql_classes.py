from sqlalchemy import Column, ForeignKey, Boolean, String, \
                       Integer, BigInteger, Float, DateTime, \
                       VARCHAR, Date, DECIMAL
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import Enum, UniqueConstraint
from sqlalchemy.sql import func
import enum

Base = declarative_base()


class Exchange(Base):
    __tablename__ = 'exchange'
    id = Column('id', Integer, primary_key=True, autoincrement=True)
    name = Column('name', VARCHAR(10), unique=True, nullable=False)
    currency = Column('currency', String(3))
    created_date = Column('created_date', DateTime, server_default=func.now())
    last_updated = Column('last_updated', DateTime, onupdate=func.now())


class Security(Base):
    __tablename__ = 'security'
    id = Column('id', Integer, primary_key=True, autoincrement=True)
    exchange_id = Column('exchange_id', Integer, ForeignKey('exchange.id',
                                    onupdate="CASCADE",
                                    ondelete="SET NULL"))
    ticker = Column('ticker', VARCHAR(10), nullable=False)
    name = Column('name', VARCHAR(100), nullable=False)
    sector = Column('sector', VARCHAR(100))
    industry = Column('industry', VARCHAR(100))
    created_date = Column('created_date', DateTime, server_default=func.now())
    last_updated = Column('last_updated', DateTime, onupdate=func.now())
    exchange = relationship('Exchange')

class Price(Base):
    __tablename__ = 'price'
    id = Column('id', Integer, primary_key=True, autoincrement=True)
    ticker_id = Column('ticker_id', Integer, ForeignKey('security.id',
                                           onupdate='CASCADE',
                                           ondelete='SET NULL'))
    created_date = Column('created_date', DateTime, server_default=func.now())
    last_updated = Column('last_updated', DateTime, onupdate=func.now())
    date = Column('date', Date, nullable=False)
    open = Column('open', DECIMAL(11,6))
    high = Column('high', DECIMAL(11,6))
    low = Column('low', DECIMAL(11,6))
    close = Column('close', DECIMAL(11,6))
    adj_close = Column('adj_close', DECIMAL(11,6))
    volume = Column('volume', BigInteger)
    security = relationship('Security')
