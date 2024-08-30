from sqlalchemy import Column, Integer, String, Enum, Boolean, ForeignKey
from sqlalchemy.orm import relationship

from enum import Enum as PyEnum

from database.main import Base

class StageEnum(PyEnum):
    FIRST = "first_stage"
    SECOND = "second_stage"


class ApartmentStage(Base):
    __tablename__ = 'apartment_stages'

    id = Column(Integer, primary_key=True)
    stage = Column(Enum(StageEnum), nullable=False)
    is_ready_for_review = Column(Boolean, default=False)
    is_finished = Column(Boolean, default=False)
    started = Column(Boolean, default=False)
    apartment_id = Column(Integer, ForeignKey('apartments.id'))
    apartment = relationship('Apartment', back_populates='stages')
    comment = Column(String, nullable=True)
