from datetime import datetime, timedelta
from sqlalchemy import Column, String, Integer, Float, inspect

from aporacle.data.db.sql.models import Base


class Tick(Base):
    __tablename__ = "Tick"

    id = Column(String(50), primary_key=True, nullable=False)
    chain = Column(Integer, nullable=False)
    voting_round = Column(Integer, nullable=False)
    symbol_code = Column(Integer, nullable=False)
    position = Column(Integer, nullable=False)
    mean = Column(Float, nullable=False)
    time_weighted_mean = Column(Float, nullable=False)
    volume = Column(Float, nullable=False)
    timestamp = Column(String(50), nullable=False)

    def __repr__(self):
        return str(self.to_dict())

    def to_dict(self):
        return {c.key: getattr(self, c.key) for c in inspect(self).mapper.column_attrs}

    @staticmethod
    def clear_old_records(session):
        six_hours_ago = datetime.utcnow() - timedelta(seconds=120)  # 2 minutes
        session.query(Tick).filter(Tick.timestamp < six_hours_ago.isoformat()).delete()
        session.commit()
