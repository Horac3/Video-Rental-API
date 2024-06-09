
from datetime import datetime
from sqlalchemy import TIMESTAMP, func
from sqlalchemy.orm import Mapped, mapped_column

class TimeStampMixin:
    created_at : Mapped[datetime] = mapped_column(
        TIMESTAMP, nullable=False, server_default=func.now()
    )

    updated_at: Mapped[datetime] = mapped_column(
        TIMESTAMP, nullable=False, server_default=func.now(), onupdate=func.now()
    )