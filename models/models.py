from flask_sqlalchemy import SQLAlchemy
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from datetime import datetime

db = SQLAlchemy()

class BlackList(db.Model):
    __tablename__ = "black_list"
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String)
    appUuid = db.Column(db.String)
    blockedReason = db.Column(db.String)
    ipOrigin = db.Column(db.String)
    createdAt = db.Column(db.DateTime, default=datetime.utcnow)

class BlackListSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = BlackList
        load_instance = True