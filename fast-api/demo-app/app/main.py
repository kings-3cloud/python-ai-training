from app.db import create_db_and_table, engine, SessionDep

from app.schemas.Item import Item as DbItem
from app.schemas.ItemImage import ItemImage

from fastapi.responses import PlainTextResponse, Response
from fastapi import FastAPI, Path, Query, HTTPException, status, UploadFile, File
from contextlib import asynccontextmanager
from pydantic import BaseModel
from typing import Optional, Annotated

from sqlmodel import select

@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Starting up... Creating database tables")
    create_db_and_table()

    yield

    print("Shutting down...")
    engine.dispose()


fastapi_app = FastAPI(title="Item API", version="0.0.1", lifespan=lifespan)

class Item(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
    quantity: int = 0

@fastapi_app.get("/", response_class=PlainTextResponse)
async def root() -> str:
    # return {"message": "Welcome to the Item API"}
    return "That is an ordinary text"


@fastapi_app.get("/items")
async def list_items(
        session: SessionDep,
        limit: Annotated[int, Query(ge=1, le=100)] = 10,
        skip: Annotated[int, Query(ge=0)] =  0,
) -> list[DbItem]:
    query = select(DbItem).limit(limit=limit).offset(offset=skip)
    return list(session.exec(query).fetchall())
    

@fastapi_app.post("/items")
async def create_item(item: Item, session: SessionDep) -> DbItem:
    dbItem = DbItem(
        name=item.name,
        description=item.description,
        quantity=item.quantity,
        price=item.price
    )

    session.add(dbItem)
    session.commit()
    session.refresh(dbItem)

    return dbItem


@fastapi_app.put("/items/{item_id}")
async def update_item(
        item_id: Annotated[int, Path(ge=1)],
        item: Item,
        session: SessionDep,
) -> DbItem:
    db_item = session.get(DbItem, item_id)
    if not db_item:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item not found")

    db_item.name = item.name
    db_item.description = item.description
    db_item.price = item.price
    db_item.quantity = item.quantity

    session.add(db_item)
    session.commit()
    session.refresh(db_item)

    return db_item


@fastapi_app.delete("/items/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_item(
        item_id: Annotated[int, Path(ge=1)],
        session: SessionDep,
) -> None:
    db_item = session.get(DbItem, item_id)
    if not db_item:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item not found")

    session.delete(db_item)
    session.commit()


ALLOWED_IMAGE_TYPES = {"image/jpeg", "image/png", "image/gif", "image/webp"}


@fastapi_app.post("/items/{item_id}/image", status_code=status.HTTP_201_CREATED)
async def create_item_image(
        item_id: Annotated[int, Path(ge=1)],
        session: SessionDep,
        file: UploadFile = File(...),
) -> dict:
    if file.content_type not in ALLOWED_IMAGE_TYPES:
        raise HTTPException(
            status_code=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
            detail=f"Unsupported media type '{file.content_type}'. Allowed: {', '.join(ALLOWED_IMAGE_TYPES)}",
        )

    db_image = ItemImage(
        item_id=item_id,
        image_data=await file.read(),
        image_content_type=file.content_type,
    )
    session.add(db_image)
    session.commit()

    return {"message": "Image created successfully"}


@fastapi_app.put("/items/{item_id}/image", status_code=status.HTTP_200_OK)
async def update_item_image(
        item_id: Annotated[int, Path(ge=1)],
        session: SessionDep,
        file: UploadFile = File(...),
) -> dict:
    if file.content_type not in ALLOWED_IMAGE_TYPES:
        raise HTTPException(
            status_code=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
            detail=f"Unsupported media type '{file.content_type}'. Allowed: {', '.join(ALLOWED_IMAGE_TYPES)}",
        )

    db_image = session.exec(select(ItemImage).where(ItemImage.item_id == item_id)).first()
    if not db_image:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Image not found")

    db_image.image_data = await file.read()
    db_image.image_content_type = file.content_type
    session.add(db_image)
    session.commit()

    return {"message": "Image updated successfully"}


@fastapi_app.get("/items/{item_id}/image")
async def get_item_image(
        item_id: Annotated[int, Path(ge=1)],
        session: SessionDep,
) -> Response:
    db_image = session.exec(select(ItemImage).where(ItemImage.item_id == item_id)).first()
    if not db_image:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No image found for this item")

    return Response(content=db_image.image_data, media_type=db_image.image_content_type)



