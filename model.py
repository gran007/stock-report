from sqlalchemy import Column, Integer, String, Date, ForeignKey, Float, BigInteger, SmallInteger
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session, declarative_base


user = 'gran007'
pwd = 'gran1234'
db_name = 'stock_db'
db_url = f'mysql+pymysql://{user}:{pwd}@localhost/{db_name}?charset=utf8'

engine = create_engine(db_url, echo=True)
db_session = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))
Base = declarative_base()
Base.query = db_session.query_property()
Base.metadata.create_all(engine)


class CompanyType(Base):
    __tablename__ = 'company_type'
    id = Column(Integer, ForeignKey('daily_data.code'), primary_key=True)
    name = Column(String, nullable=False)

    def __init__(self, row):
        self.id = row[0]
        self.name = row[1]


class MarketType(Base):
    __tablename__ = 'market_type'
    id = Column(Integer, ForeignKey('daily_data.market_type'), primary_key=True)
    name = Column(String, nullable=False)


market_type_dict = {}
for q in db_session.query(MarketType).all():
    market_type_dict[q.name] = q.id


class DailyData(Base):
    __tablename__ = 'daily_data'
    id = Column(Integer, primary_key=True, autoincrement=True, comment='아이디')
    date = Column(Date, nullable=False, comment='날짜')
    code = Column(String, nullable=False, comment='종목코드')
    market_type = Column(SmallInteger, nullable=False, comment='시장구분')
    market = relationship("MarketType", uselist=False)
    company = relationship("CompanyType", uselist=False)
    section = Column(String, comment='소속부')
    closing_price = Column(Integer, nullable=False, comment='종가')
    compare_price = Column(Integer, nullable=False, comment='대비')
    fluctuation_ratio = Column(Float, nullable=False, comment='등락률')
    opening_price = Column(Integer, nullable=False, comment='시가')
    high_price = Column(Integer, nullable=False, comment='고가')
    low_price = Column(Integer, nullable=False, comment='저가')
    trading_volume = Column(Integer, nullable=False, comment='거래량')
    transaction_amount = Column(BigInteger, nullable=False, comment='거래대금')
    market_capitalization = Column(BigInteger, nullable=False, comment='시가총액')
    stock_number = Column(BigInteger, nullable=False, comment='상장주식수')

    def __init__(self, date, row):
        self.date = date
        self.code = row[0]
        self.market_type = market_type_dict[row[2]]
        self.section = row[3]
        self.closing_price = row[4]
        self.compare_price = row[5]
        self.fluctuation_ratio = row[6]
        self.opening_price = row[7]
        self.high_price = row[8]
        self.low_price = row[9]
        self.trading_volume = row[10]
        self.transaction_amount = row[11]
        self.market_capitalization = row[12]
        self.stock_number = row[13]

