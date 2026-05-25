from sqlmodel import Field, SQLModel

from typing import Optional

class Item(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str = Field(index=True)
    description: Optional[str] = Field(default=None)
    quantity: int | None = Field()
    price: float | None = Field()


