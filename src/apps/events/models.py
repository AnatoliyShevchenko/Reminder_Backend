# SQLAlchemy
import sqlalchemy as sa

# Local
from src.apps.abstract.models import Base


class Events(Base):
    """Model for Events."""

    __tablename__ = "events"

    id = sa.Column(sa.Integer, primary_key=True, unique=True)
    title = sa.Column(sa.String)
    date = sa.Column(sa.DateTime(timezone=True))
    is_finished = sa.Column(sa.Boolean)
    telegram_id = sa.Column(sa.BigInteger, sa.ForeignKey(
        column="users.telegram_id", ondelete="CASCADE", onupdate="CASCADE"
    ))

