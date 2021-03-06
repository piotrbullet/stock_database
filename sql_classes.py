from sqlalchemy import Column, ForeignKey, Boolean, String, \
                       Integer, BigInteger, Float, Date
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import Enum, UniqueConstraint
import enum

Base = declarative_base()

class Security(Base):
    __tablename__ = 'security'
    id = Column(Integer, primary_key=True, autoincrement=True)
    id_intrinio = Column('id_intrinio', String(10), unique=True, nullable=False)
    code = Column('code', String(3), nullable=False)
    currency = Column('currency', String(3), nullable=False)
    name = Column('name', String(200), nullable=False)
    figi = Column('figi', String(12))
    composite_figi = Column('composite_figi', String(12))
    share_class_figi = Column('share_class_figi', String(12))
    exchange_id = Column(Integer, ForeignKey('exchange.id',
                                    onupdate="CASCADE",
                                    ondelete="SET NULL"))
    exchange = relationship('Exchange')
    company = relationship('Company')

class Exchange(Base):
    __tablename__ = 'exchange'
    id = Column(Integer, primary_key=True, autoincrement=True)
    mic = Column('mic', String(10), unique=True, nullable=False)
    acronym = Column('acronym', String(20))
    name = Column('name', String(200), nullable=False)
    security = relationship('Security')

class SecurityPrice(Base):
    __tablename__ = 'security_price'
    id = Column(Integer, primary_key=True)
    date = Column('date', Date, nullable=False)
    open = Column('open', Float)
    high = Column('high', Float)
    low = Column('low', Float)
    close = Column('close', Float)
    volume = Column('volume', BigInteger)
    adj_close = Column('adj_close', Float)
    security_id = Column(Integer, ForeignKey('security.id',
                                    onupdate="CASCADE",
                                    ondelete="CASCADE"),
                                    nullable=False)
    UniqueConstraint('date', 'security_id')
    security = relationship('Security')

class StockAdjustment(Base):
    __tablename__ = 'stock_adjustment'
    id = Column(Integer, primary_key=True)
    date = Column('date', Date, nullable=False)
    factor = Column('factor', Float, nullable=False)
    dividend = Column('dividend', Float)
    split_ratio = Column('split_ratio', Float)
    security_id = Column(Integer, ForeignKey('security.id',
                                    onupdate="CASCADE",
                                    ondelete="CASCADE"),
                                    nullable=False)
    security = relationship('Security')

class Company(Base):
    __tablename__ = 'company'
    id = Column(Integer, primary_key=True)
    name = Column('name', String(100), nullable=False)
    cik = Column('cik', String(10))
    description = Column('description', String(2000))
    company_url = Column('company_url', String(100))
    sic = Column('sic', String(4))
    employees = Column('employees', Integer)
    sector = Column('sector', String(200))
    industry_category = Column('industry_category', String(200))
    industry_group = Column('industry_group', String(200))
    security_id = Column(Integer, ForeignKey('security.id',
                                    onupdate="CASCADE",
                                    ondelete="CASCADE"),
                                    nullable=False)
    security = relationship('Security')