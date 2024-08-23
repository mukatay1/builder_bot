from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from database.main import Base


class Apartment(Base):
    __tablename__ = 'apartments'

    id = Column(Integer, primary_key=True)
    number = Column(String, unique=True, nullable=False)
    status = Column(String, nullable=True)
    stages = relationship('ApartmentStage', back_populates='apartment')
