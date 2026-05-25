from sqlmodel import Field, SQLModel


class ItemImage(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    item_id: int = Field(index=True)
    image_data: bytes
    image_content_type: str
