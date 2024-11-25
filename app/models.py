from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from app.extansions import db


class Company(db.Model):
    id = Column(Integer, primary_key=True)
    name = Column(String(30))
    secret_key = Column(String(16))
    site = Column(String(50))
    orders = relationship('Orders', backref='company', lazy=True)

    def __repr__(self):
        return f'<Product {self.id}>'

class Orders(db.Model):
    id = Column(Integer, primary_key=True)
    price = Column(Integer)
    status = Column(Integer)
    company_id = Column(Integer, ForeignKey('company.id'), nullable=False)
