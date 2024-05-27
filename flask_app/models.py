from flask_app import db
from sqlalchemy.schema import ForeignKey

class Account(db.Model):
    __tablename__ = 'account'
    AccoountID = db.Column(db.Integer, primary_key=True)
    AccountNumber = db.Column(db.String(8))
    Name = db.Column(db.String(50))
    KanaName = db.Column(db.String(50))
    SexID = db.Column(db.Integer, ForeignKey('sex.SexID'))
    Password = db.Column(db.String(12))
    MailAddress = db.Column(db.String(255))
    PhoneNumber = db.Column(db.String(13))
    Birthday = db.Column(db.Date)
    MemberFlg = db.Column(db.Boolean(0))
    RegistDate = db.Column(db.DateTime, server_default="NOW()")

class Sex(db.Model):
    __tablename__ = 'sex'
    SexID = db.Column(db.Integer, primary_key=True)
    Sex = db.Column(db.String(4))
