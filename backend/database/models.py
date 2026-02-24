from sqlalchemy import Column, Integer, String, DateTime, JSON
from sqlalchemy.ext.declarative import declarative_base
import datetime

Base = declarative_base()


class Twin(Base):
    __tablename__ = "twins"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False)
    metadata = Column(JSON, nullable=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)


class DisasterEvent(Base):
    __tablename__ = "disasters"
    id = Column(Integer, primary_key=True, index=True)
    type = Column(String, nullable=False)
    intensity = Column(String)
    generated_at = Column(DateTime, default=datetime.datetime.utcnow)
    payload = Column(JSON)


class SimulationRun(Base):
    __tablename__ = "simulations"
    id = Column(Integer, primary_key=True, index=True)
    scenario = Column(String)
    parameters = Column(JSON)
    started_at = Column(DateTime, default=datetime.datetime.utcnow)
    finished_at = Column(DateTime)


class Analytics(Base):
    __tablename__ = "analytics"
    id = Column(Integer, primary_key=True, index=True)
    run_id = Column(Integer)
    metrics = Column(JSON)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
