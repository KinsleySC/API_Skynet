from enum import Enum
from typing import List, Optional
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field, field_validator, model_validator

app = FastAPI(title="RecipeShare API")


class CategoryBase(BaseModel):
    name: str = Field(min_length=2, max_length=50)


class CategoryCreate(CategoryBase):
    pass


class CategoryUpdate(BaseModel):
    name: Optional[str] = Field(default=None, min_length=2, max_length=50)


class Category(CategoryBase):
    id: int


categories: List[Category] = []
category_id_counter = 1


def get_category_or_404(category_id: int) -> Category:
    for c in categories:
        if c.id == category_id:
            return c
    raise HTTPException(status_code=404, detail=f"category {category_id} not found")


@app.post("/categories", response_model=Category, status_code=201)
def create_category(payload: CategoryCreate):
    global category_id_counter
    category = Category(id=category_id_counter, **payload.model_dump())
    category_id_counter += 1
    categories.append(category)
    return category


@app.get("/categories", response_model=List[Category])
def list_categories():
    return categories


@app.get("/categories/{category_id}", response_model=Category)
def get_category(category_id: int):
    return get_category_or_404(category_id)


@app.patch("/categories/{category_id}", response_model=Category)
def update_category(category_id: int, payload: CategoryUpdate):
    category = get_category_or_404(category_id)
    update_data = payload.model_dump(exclude_unset=True)
    updated = category.model_copy(update=update_data)
    categories[categories.index(category)] = updated
    return updated


@app.delete("/categories/{category_id}", status_code=204)
def delete_category(category_id: int):
    category = get_category_or_404(category_id)
    categories.remove(category)
    return None

