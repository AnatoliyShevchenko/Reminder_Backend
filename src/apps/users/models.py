# SQLAlchemy
import sqlalchemy as sa

# Local
from src.apps.abstract.models import Base


class Users(Base):
    """Model for companies."""
    
    __tablename__ = "users"

    id = sa.Column(sa.Integer, primary_key=True, unique=True)
    telegram_id = sa.Column(sa.BigInteger, unique=True, nullable=False)
    timezone = sa.Column(sa.String)
    username = sa.Column(sa.String, nullable=True)
    password = sa.Column(sa.String, nullable=True)

