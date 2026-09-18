from typing import List

from fastapi import APIRouter, HTTPException

import storage
from models import Component, ComponentCreate, ComponentUpdate

router = APIRouter(prefix="/components", tags=["components"])


@router.post("", response_model=Component, status_code=201)
def create_component(payload: ComponentCreate):
    component = Component(id=storage.next_component_id(), **payload.model_dump())
    storage.components.append(component)
    return component


@router.get("", response_model=List[Component])
def list_components():
    return storage.components


@router.get("/{component_id}", response_model=Component)
def get_component(component_id: int):
    return storage.get_component_or_404(component_id)


@router.patch("/{component_id}", response_model=Component)
def update_component(component_id: int, payload: ComponentUpdate):
    component = storage.get_component_or_404(component_id)
    update_data = payload.model_dump(exclude_unset=True)
    updated = component.model_copy(update=update_data)
    storage.components[storage.components.index(component)] = updated
    return updated


@router.delete("/{component_id}", status_code=204)
def delete_component(component_id: int):
    component = storage.get_component_or_404(component_id)
    used = any(
        any(item.component_id == component_id for item in unit.components)
        for unit in storage.units
    )
    if used:
        raise HTTPException(status_code=400, detail="component is used by at least one unit")
    storage.components.remove(component)
    return None
