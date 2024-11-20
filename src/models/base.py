import uuid
from datetime import datetime

from sqlalchemy.sql.expression import text
from sqlalchemy.types import TIMESTAMP
from sqlmodel import Field, SQLModel


class BaseModel(SQLModel):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, nullable=False, primary_key=True)

    # NOTE: Specified with `default=None` to avoid typing issues elsewhere
    #   but the correct timestamp will be set by the DB itself
    created_at: datetime = Field(
        default=None,
        sa_type=TIMESTAMP(timezone=True),  # type: ignore
        sa_column_kwargs={
            "server_default": text("CURRENT_TIMESTAMP"),
        },
        nullable=True,
    )
