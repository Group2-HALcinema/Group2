from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.schema import ForeignKey
from datetime import datetime
from flask_login import UserMixin
from pytz import timezone

japan_tz = timezone('Asia/Tokyo')

db = SQLAlchemy()

class Account(db.Model, UserMixin):
    __tablename__ = 'account'
    AccountID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    AccountNumber = db.Column(db.String(8))
    Name = db.Column(db.String(50))
    KanaName = db.Column(db.String(50))
    SexID = db.Column(db.Integer, ForeignKey('sex.SexID'))
    Password = db.Column(db.String(12))
    MailAddress = db.Column(db.String(255))
    PhoneNumber = db.Column(db.String(13))
    Birthday = db.Column(db.Date)
    MemberFlg = db.Column(db.Boolean(1), server_default="0")
    RegistDate = db.Column(db.DateTime, default=datetime.now(japan_tz))
    
    sex = db.relationship('Sex', backref='account')
    
    def get_id(self):
        return str(self.AccountID)
    
class Address(db.Model):
    __tablename__ = 'address'
    AddressID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    PostNumber = db.Column(db.String(8))
    Todohuken = db.Column(db.String(8))
    Shiku = db.Column(db.String(20))
    ChosonNumber = db.Column(db.String(255))
    AccountID = db.Column(db.Integer, ForeignKey('account.AccountID'))
    
    account = db.relationship('Account', backref='address')

class Sex(db.Model):
    __tablename__ = 'sex'
    SexID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    Sex = db.Column(db.String(4))
    
class Movie(db.Model):
    __tablename__ = 'movie'
    MovieID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    MovieTitle = db.Column(db.String(50))  # 混乱を招くためカラム名を変更
    MovieThum = db.Column(db.String(255))
    AgeLimitID = db.Column(db.Integer, ForeignKey('agelimit.AgeLimitID'))
    MD = db.Column(db.String(50))
    MS = db.Column(db.String(50))
    Overview = db.Column(db.String(2000))
    StartDate = db.Column(db.Date)
    FinishDate = db.Column(db.Date)
    
    agelimit = db.relationship('AgeLimit', backref='movie')
    
class AgeLimit(db.Model):
    __tablename__ = 'agelimit'
    AgeLimitID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    AgeLimit = db.Column(db.String(5))
    
class Screen(db.Model):
    __tablename__ = 'screen'
    ScreenID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    Capacity = db.Column(db.Integer)
    
class Showing(db.Model):
    __tablename__ = 'showing'
    ShowingID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    ShowDatetime = db.Column(db.DateTime)
    MovieID = db.Column(db.Integer, ForeignKey('movie.MovieID'))
    ScreenID = db.Column(db.Integer, ForeignKey('screen.ScreenID'))
    
    movie = db.relationship('Movie', backref='showing')
    screen = db.relationship('Screen', backref='showing')
    
class Price(db.Model):
    __tablename__ = 'price'
    PriceID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    PricePlans = db.Column(db.String(20))
    Price = db.Column(db.Integer)
    
class Discount(db.Model):
    __tablename__ = 'discount'
    DiscountID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    DiscountName = db.Column(db.String(30))
    Discount = db.Column(db.Float)
    
class Reservation(db.Model):
    __tablename__ = 'reservation'
    ReservationID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    AccountID = db.Column(db.Integer, ForeignKey('account.AccountID')) #
    ShowingID = db.Column(db.Integer, ForeignKey('showing.ShowingID')) #
    SeatNumber = db.Column(db.String(3)) #

    PriceID = db.Column(db.Integer, ForeignKey('price.PriceID'))
    DiscountID = db.Column(db.Integer, ForeignKey('discount.DiscountID'))
    
    account = db.relationship('Account', backref='reservation')
    showing = db.relationship('Showing', backref='reservation')
    price = db.relationship('Price', backref='reservation')
    discount = db.relationship('Discount', backref='reservation')

class Seat(db.Model):
    SeatID = db.Column(db.Integer,primary_key=True)
    # 行に対応(アルファベット表記を数字に変更)
    Row = db.Column(db.String(1), nullable=False)
    # 列に対応
    Number = db.Column(db.Integer, nullable=False)
    ScreenID = db.Column(db.Integer, ForeignKey('screen.ScreenID'))
    
    screen = db.relationship('Screen', backref='seat')



