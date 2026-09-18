from typing import List

from fastapi import APIRouter, HTTPException

import storage
from models import UnitClass, UnitClassCreate, UnitClassUpdate

router = APIRouter(prefix="/unit-classes", tags=["unit-classes"])


@router.post("", response_model=UnitClass, status_code=201)
def create_unit_class(payload: UnitClassCreate):
    unit_class = UnitClass(id=storage.next_unit_class_id(), **payload.model_dump())
    storage.unit_classes.append(unit_class)
    return unit_class


@router.get("", response_model=List[UnitClass])
def list_unit_classes():
    return storage.unit_classes


@router.get("/{unit_class_id}", response_model=UnitClass)
def get_unit_class(unit_class_id: int):
    return storage.get_unit_class_or_404(unit_class_id)


@router.patch("/{unit_class_id}", response_model=UnitClass)
def update_unit_class(unit_class_id: int, payload: UnitClassUpdate):
    unit_class = storage.get_unit_class_or_404(unit_class_id)
    update_data = payload.model_dump(exclude_unset=True)
    updated = unit_class.model_copy(update=update_data)
    storage.unit_classes[storage.unit_classes.index(unit_class)] = updated
    return updated


@router.delete("/{unit_class_id}", status_code=204)
def delete_unit_class(unit_class_id: int):
    unit_class = storage.get_unit_class_or_404(unit_class_id)
    if any(unit.unit_class_id == unit_class_id for unit in storage.units):
        raise HTTPException(status_code=400, detail="unit_class is used by at least one unit")
    storage.unit_classes.remove(unit_class)
    return None
