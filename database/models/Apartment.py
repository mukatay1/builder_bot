from sqlalchemy import Column, Integer, String, Boolean, Date
from sqlalchemy.orm import relationship

from database.main import Base


class Apartment(Base):
    __tablename__ = 'apartments'

    id = Column(Integer, primary_key=True)
    number = Column(String, unique=True, nullable=False)
    status = Column(String, nullable=True)
    stages = relationship('ApartmentStage', back_populates='apartment')
    status_date = Column(Date, nullable=True)
    start_date = Column(Date, nullable=True)
    end_date = Column(Date, nullable=True)
    is_accepted = Column(Boolean, default=False)
    clear_level = Column(String, nullable=True)