import random
from datetime import datetime, timedelta
from sqlalchemy import Column, String, Integer, Float, inspect, event

from aporacle.data.db.sql.models import Base


class Symbol(Base):
    __tablename__ = "Symbol"

    id = Column(String(50), primary_key=True, nullable=False)
    name = Column(String(50), nullable=False)
    code = Column(Integer, nullable=False, unique=True)  # Ensure `unique=True` for uniqueness
    feed = Column(String(50), nullable=False)
    status = Column(Integer, nullable=False)
    timestamp = Column(String(50), nullable=False)

    def __repr__(self):
        return str(self.to_dict())

    def to_dict(self):
        return {c.key: getattr(self, c.key) for c in inspect(self).mapper.column_attrs}


@event.listens_for(Symbol, "before_insert")
def generate_code(mapper, connection, target):
    from sqlalchemy.orm import Session

    # Create a new session to query the database
    session = Session(bind=connection)

    while True:
        new_code = random.randint(10000, 99999)
        # Check if this code already exists
        if not session.query(Symbol).filter_by(code=new_code).first():
            target.code = new_code
            break
